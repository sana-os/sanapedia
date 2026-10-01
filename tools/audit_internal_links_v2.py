#!/usr/bin/env python3

import argparse
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]

IDENTITY_REGISTRY = (
    ROOT / "registry" / "v2" / "entry-registry.csv"
)

LANGUAGE_REGISTRY = (
    ROOT / "registry" / "v2" / "entry-language-registry.csv"
)

CANONICAL_HOST = "sanapedia.net"

ROUTE_CLASS = {
    "historical_hub": None,
    "person": "people",
    "event": "events",
    "timeline": "timelines",
}

MARKDOWN_LINK_RE = re.compile(
    r'!?\[[^\]]*\]\('
    r'(?P<target><[^>]+>|[^\s)]+)'
)

QUOTED_INTERNAL_RE = re.compile(
    r'''["'](
        /(?:[A-Za-z0-9._~!$&*+,;=:@%#/-]+)
        |
        \.\.?/(?:[^"' \t]+)
        |
        \#[A-Za-z0-9._:-]+
    )["']''',
    re.VERBOSE,
)


def load_csv(path, expected_header):
    if not path.is_file():
        raise RuntimeError(
            f"registry not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as f:
        reader = csv.DictReader(f)

        if reader.fieldnames != expected_header:
            raise RuntimeError(
                f"{path}: unexpected header: "
                f"{reader.fieldnames}"
            )

        return list(reader)


def repo_path(raw):
    p = PurePosixPath(raw.strip())

    if p.is_absolute() or ".." in p.parts:
        raise RuntimeError(
            f"unsafe registry path: {raw!r}"
        )

    path = ROOT.joinpath(*p.parts)

    path.resolve(strict=False).relative_to(
        ROOT.resolve()
    )

    return path


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "---":
        return {}, 0

    try:
        end = lines.index("---", 1)
    except ValueError:
        raise RuntimeError(
            f"frontmatter closing fence missing: {path}"
        )

    data = {}

    for line in lines[1:end]:
        if not line or line[0].isspace():
            continue

        m = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*):"
            r"(?:\s*(.*))?$",
            line,
        )

        if not m:
            continue

        key = m.group(1)
        value = (m.group(2) or "").strip()

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in ('"', "'")
        ):
            value = value[1:-1]

        data[key] = value

    return data, end


def build_registry_maps():
    identities = load_csv(
        IDENTITY_REGISTRY,
        ["entry_key", "status", "notes"],
    )

    manifestations = load_csv(
        LANGUAGE_REGISTRY,
        ["entry_key", "language", "file"],
    )

    identity_keys = {
        row["entry_key"].strip()
        for row in identities
    }

    registered_files = set()
    route_map = {}
    language_dirs = {}

    for row in manifestations:
        key = row["entry_key"].strip()
        language = row["language"].strip()

        if key not in identity_keys:
            raise RuntimeError(
                f"orphan manifestation: {key}/{language}"
            )

        path = repo_path(row["file"])

        if not path.is_file():
            raise RuntimeError(
                f"registered file missing: {path}"
            )

        resolved = path.resolve()
        registered_files.add(resolved)

        parts = path.relative_to(ROOT).parts

        if not parts:
            raise RuntimeError(
                f"invalid manifestation path: {path}"
            )

        language_dir = parts[0]

        existing_dir = language_dirs.get(language)

        if (
            existing_dir is not None
            and existing_dir != language_dir
        ):
            raise RuntimeError(
                f"{language}: multiple repository "
                f"language roots"
            )

        language_dirs[language] = language_dir

        fm, _ = parse_frontmatter(path)

        if fm.get("entry_key") != key:
            raise RuntimeError(
                f"{key}/{language}: entry_key mismatch"
            )

        if fm.get("language") != language:
            raise RuntimeError(
                f"{key}/{language}: language mismatch"
            )

        entity_type = fm.get("entity_type")
        slug = fm.get("slug")

        if entity_type not in ROUTE_CLASS:
            continue

        if not slug:
            raise RuntimeError(
                f"{key}/{language}: slug missing"
            )

        if (
            len(parts) < 5
            or parts[1] != "worlds"
        ):
            raise RuntimeError(
                f"unexpected registered path: {path}"
            )

        world = parts[2]
        region = parts[3]
        route = ROUTE_CLASS[entity_type]

        base = (
            f"/{language}/worlds/"
            f"{world}/{region}"
        )

        if route is None:
            public_paths = {
                f"{base}/{slug}.md",
                f"{base}/{slug}/",
            }
        else:
            public_paths = {
                f"{base}/{route}/{slug}.md",
                f"{base}/{route}/{slug}/",
            }

        for public_path in public_paths:
            previous = route_map.get(public_path)

            if (
                previous is not None
                and previous != resolved
            ):
                raise RuntimeError(
                    f"duplicate public route: "
                    f"{public_path}"
                )

            route_map[public_path] = resolved

    return (
        registered_files,
        route_map,
        language_dirs,
    )


def files_in_scope(language_dirs):
    paths = []

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue

        paths.append(path)

    for name in ("llms.txt",):
        root_file = ROOT / name

        if root_file.is_file():
            paths.append(root_file)

        for language_dir in sorted(
            set(language_dirs.values())
        ):
            candidate = (
                ROOT / language_dir / name
            )

            if candidate.is_file():
                paths.append(candidate)

    seen = set()
    result = []

    for path in sorted(paths):
        resolved = path.resolve()

        if resolved in seen:
            continue

        seen.add(resolved)
        result.append(path)

    return result


def extract_references(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    refs = []

    # Frontmatter path-like references.
    body_start = 0

    if lines and lines[0] == "---":
        try:
            end = lines.index("---", 1)
        except ValueError:
            raise RuntimeError(
                f"frontmatter closing fence missing: {path}"
            )

        for lineno, line in enumerate(
            lines[1:end],
            start=2,
        ):
            for match in QUOTED_INTERNAL_RE.finditer(
                line
            ):
                refs.append({
                    "target": match.group(1),
                    "line": lineno,
                    "kind": "frontmatter",
                })

        body_start = end + 1

    # Markdown body links.
    in_fence = False
    fence_char = None

    for lineno, line in enumerate(
        lines[body_start:],
        start=body_start + 1,
    ):
        stripped = line.lstrip()

        if stripped.startswith("```"):
            marker = "```"

            if not in_fence:
                in_fence = True
                fence_char = marker
            elif fence_char == marker:
                in_fence = False
                fence_char = None

            continue

        if stripped.startswith("~~~"):
            marker = "~~~"

            if not in_fence:
                in_fence = True
                fence_char = marker
            elif fence_char == marker:
                in_fence = False
                fence_char = None

            continue

        if in_fence:
            continue

        for match in MARKDOWN_LINK_RE.finditer(
            line
        ):
            target = match.group("target")

            if (
                target.startswith("<")
                and target.endswith(">")
            ):
                target = target[1:-1]

            refs.append({
                "target": target,
                "line": lineno,
                "kind": "markdown",
            })

    return refs


def safe_relative_candidate(source, path_text):
    candidate = (
        source.parent
        / PurePosixPath(path_text)
    )

    resolved = candidate.resolve(
        strict=False
    )

    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        return None

    return resolved


def root_candidate(
    public_path,
    language_dirs,
):
    clean = public_path

    parts = [
        p
        for p in clean.split("/")
        if p
    ]

    if not parts:
        index = ROOT / "index.md"
        return (
            index.resolve()
            if index.is_file()
            else None
        )

    language = parts[0].lower()

    if language in language_dirs:
        language_root = (
            ROOT
            / language_dirs[language]
        )

        tail = parts[1:]

        if not tail:
            candidate = (
                language_root / "index.md"
            )

            return (
                candidate.resolve()
                if candidate.is_file()
                else None
            )

        if public_path.endswith("/"):
            candidate = (
                language_root
                .joinpath(*tail)
                / "index.md"
            )
        else:
            candidate = (
                language_root
                .joinpath(*tail)
            )

        if candidate.is_file():
            return candidate.resolve()

        return None

    if clean == "/llms.txt":
        candidate = ROOT / "llms.txt"

        return (
            candidate.resolve()
            if candidate.is_file()
            else None
        )

    if clean.startswith("/data/"):
        candidate = (
            ROOT
            / "public"
            / clean.lstrip("/")
        )

        return (
            candidate.resolve()
            if candidate.is_file()
            else None
        )

    candidate = ROOT / clean.lstrip("/")

    return (
        candidate.resolve()
        if candidate.is_file()
        else None
    )


def classify_existing(
    resolved,
    original_path,
    registered_files,
    language_dirs,
):
    if resolved in registered_files:
        return "REGISTERED_FILE_PATH"

    language_root_routes = {
        f"/{language}"
        for language in language_dirs
    }

    if (
        resolved.name == "index.md"
        and (
            original_path.endswith("/")
            or original_path
            in language_root_routes
        )
    ):
        return "NAVIGATION_EXISTING"

    try:
        repository_path = (
            resolved
            .relative_to(ROOT)
            .as_posix()
        )
    except ValueError:
        return "EXISTING_UNREGISTERED"

    publication_artifacts = {
        "llms.txt",
        "EN/llms.txt",
        "JA/llms.txt",
        "public/data/entries.json",
    }

    repository_governance = {
        "README.md",
        "AI-USE.md",
        "CITATION.md",
        "LICENSE.md",
    }

    if repository_path in publication_artifacts:
        return "PUBLICATION_ARTIFACT"

    if repository_path in repository_governance:
        return "REPOSITORY_GOVERNANCE"

    return "EXISTING_UNREGISTERED"


def is_virtual_navigation(
    source,
    path_text,
    language_dirs,
):
    sections = {
        "people",
        "events",
        "phenomena",
        "timelines",
        "columns",
    }

    if not path_text.endswith("/"):
        return False

    # Public route: /{language}/{section}/
    if path_text.startswith("/"):
        parts = [
            part
            for part in path_text.split("/")
            if part
        ]

        if len(parts) != 2:
            return False

        language = parts[0].lower()
        section = parts[1]

        return (
            language in language_dirs
            and section in sections
        )

    # Repository-relative route from a language root:
    # ./people/, ./events/, ...
    parts = [
        part
        for part in path_text.split("/")
        if part not in ("", ".")
    ]

    if (
        len(parts) != 1
        or parts[0] not in sections
    ):
        return False

    source_parent = source.parent.resolve()

    return any(
        source_parent
        == (ROOT / language_dir).resolve()
        for language_dir in language_dirs.values()
    )


def resolve_reference(
    source,
    raw_target,
    registered_files,
    route_map,
    language_dirs,
):
    target = raw_target.strip()

    if not target:
        return (
            "EMPTY_TARGET",
            "",
            None,
        )

    if target.startswith("//"):
        return (
            "EXTERNAL",
            target,
            None,
        )

    split = urlsplit(target)

    if split.scheme:
        if split.scheme in ("http", "https"):
            host = split.netloc.lower()

            if host != CANONICAL_HOST:
                return (
                    "EXTERNAL",
                    target,
                    None,
                )

            path_text = split.path or "/"
            fragment = split.fragment

        else:
            return (
                "OTHER_SCHEME",
                target,
                None,
            )

    else:
        path_text = split.path
        fragment = split.fragment

    if not path_text and fragment:
        return (
            "ANCHOR_ONLY",
            f"#{fragment}",
            None,
        )

    if not path_text:
        return (
            "EMPTY_TARGET",
            target,
            None,
        )

    # Public root-relative route.
    if path_text.startswith("/"):
        generated_publication_routes = {
            "/sitemap.xml",
        }

        if path_text in generated_publication_routes:
            return (
                "GENERATED_PUBLICATION_ARTIFACT",
                path_text,
                None,
            )

        registered = route_map.get(
            path_text
        )

        if registered is not None:
            return (
                "REGISTERED_CANONICAL",
                path_text,
                registered,
            )

        existing = root_candidate(
            path_text,
            language_dirs,
        )

        if existing is not None:
            category = classify_existing(
                existing,
                path_text,
                registered_files,
                language_dirs,
            )

            return (
                category,
                path_text,
                existing,
            )

        if (
            fragment
            and re.search(
                r"/(?:people|phenomena|events|"
                r"timelines|columns)/?$",
                path_text,
            )
        ):
            return (
                "TAG_OR_ANCHOR_ROUTE",
                path_text + "#" + fragment,
                None,
            )

        if (
            path_text.endswith("/")
            and is_virtual_navigation(
                source,
                path_text,
                language_dirs,
            )
        ):
            return (
                "VIRTUAL_NAVIGATION",
                path_text,
                None,
            )

        if path_text.endswith("/"):
            return (
                "MISSING_NAVIGATION",
                path_text,
                None,
            )

        if path_text.endswith(".md"):
            return (
                "MISSING_CONTENT",
                path_text,
                None,
            )

        return (
            "MISSING_INTERNAL",
            path_text,
            None,
        )

    # Repository-relative Markdown route.
    candidate = safe_relative_candidate(
        source,
        path_text,
    )

    if candidate is None:
        return (
            "OUTSIDE_REPOSITORY",
            path_text,
            None,
        )

    if path_text.endswith("/"):
        candidate = (
            candidate / "index.md"
        ).resolve(strict=False)

    if candidate.is_file():
        category = classify_existing(
            candidate,
            path_text,
            registered_files,
            language_dirs,
        )

        return (
            category,
            path_text,
            candidate,
        )

    if (
        fragment
        and re.search(
            r"/(?:people|phenomena|events|"
            r"timelines|columns)/?$",
            path_text,
        )
    ):
        return (
            "TAG_OR_ANCHOR_ROUTE",
            path_text + "#" + fragment,
            None,
        )

    if (
        path_text.endswith("/")
        and is_virtual_navigation(
            source,
            path_text,
            language_dirs,
        )
    ):
        return (
            "VIRTUAL_NAVIGATION",
            path_text,
            None,
        )

    if path_text.endswith("/"):
        return (
            "MISSING_NAVIGATION",
            path_text,
            None,
        )

    if path_text.endswith(".md"):
        return (
            "MISSING_CONTENT",
            path_text,
            None,
        )

    return (
        "MISSING_INTERNAL",
        path_text,
        None,
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Read-only repository-wide internal "
            "Markdown link audit using Registry v2."
        )
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help=(
            "show all categories, not only "
            "review/action categories"
        ),
    )

    args = parser.parse_args()

    (
        registered_files,
        route_map,
        language_dirs,
    ) = build_registry_maps()

    source_files = files_in_scope(
        language_dirs
    )

    occurrences = defaultdict(list)
    category_counts = Counter()
    kind_counts = Counter()

    errors = []

    for source in source_files:
        try:
            refs = extract_references(
                source
            )
        except Exception as exc:
            errors.append(
                f"{source.relative_to(ROOT)}: "
                f"{exc}"
            )
            continue

        for item in refs:
            raw = item["target"]

            try:
                (
                    category,
                    normalized,
                    resolved,
                ) = resolve_reference(
                    source,
                    raw,
                    registered_files,
                    route_map,
                    language_dirs,
                )

            except Exception as exc:
                errors.append(
                    f"{source.relative_to(ROOT)}:"
                    f"{item['line']}: "
                    f"{raw!r}: {exc}"
                )
                continue

            category_counts[category] += 1
            kind_counts[item["kind"]] += 1

            key = (
                category,
                normalized,
            )

            occurrences[key].append({
                "source": (
                    source
                    .relative_to(ROOT)
                    .as_posix()
                ),
                "line": item["line"],
                "kind": item["kind"],
                "raw": raw,
                "resolved": (
                    resolved
                    .relative_to(ROOT)
                    .as_posix()
                    if resolved is not None
                    else None
                ),
            })

    total_refs = sum(
        category_counts.values()
    )

    internal_categories = {
        "REGISTERED_CANONICAL",
        "REGISTERED_FILE_PATH",
        "NAVIGATION_EXISTING",
        "PUBLICATION_ARTIFACT",
        "GENERATED_PUBLICATION_ARTIFACT",
        "REPOSITORY_GOVERNANCE",
        "EXISTING_UNREGISTERED",
        "TAG_OR_ANCHOR_ROUTE",
        "VIRTUAL_NAVIGATION",
        "MISSING_NAVIGATION",
        "MISSING_CONTENT",
        "MISSING_INTERNAL",
        "ANCHOR_ONLY",
        "OUTSIDE_REPOSITORY",
        "EMPTY_TARGET",
    }

    internal_count = sum(
        count
        for category, count
        in category_counts.items()
        if category in internal_categories
    )

    print(
        "Audit: Internal Links v2.0 "
        "(Registry v2)"
    )
    print(
        f"Files scanned:          "
        f"{len(source_files)}"
    )
    print(
        f"References parsed:      "
        f"{total_refs}"
    )
    print(
        f"Internal references:    "
        f"{internal_count}"
    )
    print(
        f"Unique classified refs: "
        f"{len(occurrences)}"
    )
    print(
        f"Errors:                 "
        f"{len(errors)}"
    )
    print()

    print("Reference syntax:")
    for kind in sorted(kind_counts):
        print(
            f"  {kind:<14} "
            f"{kind_counts[kind]}"
        )

    print()
    print("=== CATEGORY SUMMARY ===")

    for category in sorted(
        category_counts
    ):
        unique_count = sum(
            1
            for key in occurrences
            if key[0] == category
        )

        print(
            f"{category:<28} "
            f"occurrences="
            f"{category_counts[category]:>4} "
            f"unique={unique_count:>3}"
        )

    if errors:
        print()
        print("=== ERRORS ===")

        for error in errors:
            print(f"  {error}")

    review_categories = {
        "MISSING_CONTENT",
        "MISSING_NAVIGATION",
        "MISSING_INTERNAL",
        "TAG_OR_ANCHOR_ROUTE",
        "OUTSIDE_REPOSITORY",
        "EMPTY_TARGET",
    }

    if args.all:
        detail_categories = set(
            category_counts
        )
    else:
        detail_categories = (
            review_categories
        )

    print()
    print(
        "=== DETAILED REFERENCES "
        "REQUIRING REVIEW ==="
        if not args.all
        else "=== ALL CLASSIFIED REFERENCES ==="
    )

    found_detail = False

    for category in sorted(
        detail_categories
    ):
        keys = sorted(
            key
            for key in occurrences
            if key[0] == category
        )

        if not keys:
            continue

        found_detail = True

        print()
        print(f"[{category}]")

        for key in keys:
            _, normalized = key
            rows = occurrences[key]

            print(
                f"  {normalized}"
            )
            print(
                f"    occurrences: "
                f"{len(rows)}"
            )

            unique_sources = sorted({
                row["source"]
                for row in rows
            })

            print(
                f"    source files: "
                f"{len(unique_sources)}"
            )

            for row in rows:
                print(
                    f"      - "
                    f"{row['source']}:"
                    f"{row['line']} "
                    f"[{row['kind']}]"
                )

    if not found_detail:
        print("  none")

    print()
    print("=== NOTES ===")
    print(
        "REGISTERED_CANONICAL = "
        "current Registry v2 public route"
    )
    print(
        "REGISTERED_FILE_PATH = "
        "existing registered source reached "
        "through a repository-style path"
    )
    print(
        "PUBLICATION_ARTIFACT = "
        "existing rebuildable publication or "
        "machine-readable output"
    )
    print(
        "GENERATED_PUBLICATION_ARTIFACT = "
        "public output expected to be generated "
        "at build or deployment time"
    )
    print(
        "REPOSITORY_GOVERNANCE = "
        "repository-level governance or "
        "project documentation"
    )
    print(
        "EXISTING_UNREGISTERED = "
        "target file exists but is not "
        "a current Registry v2 manifestation "
        "or known non-Registry artifact"
    )
    print(
        "NAVIGATION_EXISTING = "
        "existing index/navigation target"
    )
    print(
        "VIRTUAL_NAVIGATION = "
        "build-time language-root category route "
        "with no source index"
    )
    print(
        "MISSING_* = no current target found; "
        "not automatically a broken-link judgment"
    )
    print(
        "TAG_OR_ANCHOR_ROUTE = "
        "fragment-based category/tag route"
    )
    print(
        "ANCHOR_ONLY = local anchor; "
        "anchor existence is not yet validated"
    )
    print(
        "Sanapedia absolute URLs are treated "
        "as internal references."
    )
    print()
    print("READ ONLY")
    print("No files modified.")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
