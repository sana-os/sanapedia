#!/usr/bin/env python3

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]

IDENTITY_REGISTRY = (
    ROOT / "registry" / "v2" / "entry-registry.csv"
)

LANGUAGE_REGISTRY = (
    ROOT / "registry" / "v2" / "entry-language-registry.csv"
)

CURRENT_CATALOG = (
    ROOT / "public" / "data" / "entries.json"
)

ORIGIN = "https://sanapedia.net"

ENTRY_KEY_RE = re.compile(r"^sp_[0-9]{8}$")

LANGUAGE_RE = re.compile(
    r"^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$"
)

SLUG_RE = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)

REQUIRED_FIELDS = (
    "entry_key",
    "title",
    "language",
    "status",
    "entity_type",
    "content_type",
    "revision",
    "updated",
    "slug",
)

ROUTE_CLASS = {
    "historical_hub": None,
    "person": "people",
    "event": "events",
    "timeline": "timelines",
}


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


def repo_path_to_local(raw):
    raw = raw.strip()

    if not raw:
        raise RuntimeError(
            "empty repository path"
        )

    p = PurePosixPath(raw)

    if p.is_absolute() or ".." in p.parts:
        raise RuntimeError(
            f"unsafe repository path: {raw!r}"
        )

    path = ROOT.joinpath(*p.parts)

    try:
        path.resolve(
            strict=False
        ).relative_to(
            ROOT.resolve()
        )
    except ValueError:
        raise RuntimeError(
            f"path escapes repository: {raw!r}"
        )

    return path


def parse_frontmatter(path):
    if not path.is_file():
        raise RuntimeError(
            f"registered file not found: {path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    if not lines or lines[0] != "---":
        raise RuntimeError(
            f"frontmatter is not first: {path}"
        )

    try:
        end = lines.index("---", 1)
    except ValueError:
        raise RuntimeError(
            f"frontmatter closing fence "
            f"missing: {path}"
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
        value = (
            m.group(2) or ""
        ).strip()

        if key in data:
            raise RuntimeError(
                f"duplicate top-level key "
                f"{key!r}: {path}"
            )

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in ('"', "'")
        ):
            value = value[1:-1]

        data[key] = value

    missing = [
        field
        for field in REQUIRED_FIELDS
        if not data.get(field)
    ]

    if missing:
        raise RuntimeError(
            f"missing required fields "
            f"{missing}: {path}"
        )

    return data


def source_location(path):
    parts = path.relative_to(ROOT).parts

    # Repository convention:
    # {language-dir}/worlds/{world}/{region}/...
    if len(parts) < 5:
        raise RuntimeError(
            f"path too shallow: {path}"
        )

    if parts[1] != "worlds":
        raise RuntimeError(
            f"expected worlds hierarchy: {path}"
        )

    return {
        "language_dir": parts[0],
        "world": parts[2],
        "region": parts[3],
    }


def build_urls(
    language,
    world,
    region,
    entity_type,
    slug,
):
    if entity_type not in ROUTE_CLASS:
        raise RuntimeError(
            f"no public URL rule for "
            f"entity_type {entity_type!r}"
        )

    route = ROUTE_CLASS[entity_type]

    base = (
        f"/{language}/worlds/"
        f"{world}/{region}"
    )

    if route is None:
        html_path = (
            f"{base}/{slug}/"
        )
        markdown_path = (
            f"{base}/{slug}.md"
        )
    else:
        html_path = (
            f"{base}/{route}/{slug}/"
        )
        markdown_path = (
            f"{base}/{route}/{slug}.md"
        )

    html_url = (
        ORIGIN + html_path
    )

    return {
        "html_url": html_url,
        "canonical_html_url": html_url,
        "canonical_markdown_url": (
            ORIGIN + markdown_path
        ),
    }


def build_catalog():
    identity_rows = load_csv(
        IDENTITY_REGISTRY,
        [
            "entry_key",
            "status",
            "notes",
        ],
    )

    language_rows = load_csv(
        LANGUAGE_REGISTRY,
        [
            "entry_key",
            "language",
            "file",
        ],
    )

    identities = {}
    manifestations = defaultdict(list)

    for row in identity_rows:
        key = row["entry_key"].strip()

        if not ENTRY_KEY_RE.fullmatch(key):
            raise RuntimeError(
                f"invalid entry_key: {key!r}"
            )

        if key in identities:
            raise RuntimeError(
                f"duplicate identity: {key}"
            )

        identities[key] = {
            "status": row["status"].strip(),
            "notes": row["notes"],
        }

    seen_pairs = set()

    for row in language_rows:
        key = row["entry_key"].strip()
        language = row["language"].strip()
        file_value = row["file"].strip()

        if key not in identities:
            raise RuntimeError(
                f"orphan manifestation: "
                f"{key}/{language}"
            )

        if not LANGUAGE_RE.fullmatch(
            language
        ):
            raise RuntimeError(
                f"invalid language tag: "
                f"{language!r}"
            )

        pair = (key, language)

        if pair in seen_pairs:
            raise RuntimeError(
                f"duplicate manifestation: "
                f"{key}/{language}"
            )

        seen_pairs.add(pair)

        manifestations[key].append({
            "language": language,
            "file": file_value,
        })

    # Historical catalog projection:
    # Registry v2 may contain identities outside the
    # historical /worlds/ publication catalog.
    #
    # Zero-manifestation identities are valid at the
    # Registry identity layer and are omitted here.
    #
    # An identity is included only when all current
    # manifestations are under {LANG}/worlds/...
    historical_keys = set()
    mixed_projection_keys = set()

    for key in identities:
        rows = manifestations[key]

        if not rows:
            continue

        classes = set()

        for row in rows:
            parts = PurePosixPath(
                row["file"]
            ).parts

            is_worlds = (
                len(parts) >= 2
                and parts[1] == "worlds"
            )

            classes.add(
                "historical"
                if is_worlds
                else "non_historical"
            )

        if classes == {"historical"}:
            historical_keys.add(key)
        elif len(classes) > 1:
            mixed_projection_keys.add(key)

    if mixed_projection_keys:
        joined = ", ".join(
            sorted(mixed_projection_keys)
        )
        raise RuntimeError(
            "mixed historical and "
            "non-historical manifestation "
            f"paths: {joined}"
        )

    entries = []

    seen_html = set()
    seen_markdown = set()

    for key in sorted(historical_keys):
        language_records = {}

        rows = sorted(
            manifestations[key],
            key=lambda row: row["language"],
        )

        for row in rows:
            language = row["language"]
            path = repo_path_to_local(
                row["file"]
            )

            fm = parse_frontmatter(path)
            loc = source_location(path)

            if fm["entry_key"] != key:
                raise RuntimeError(
                    f"{key}/{language}: "
                    "frontmatter entry_key mismatch"
                )

            if fm["language"] != language:
                raise RuntimeError(
                    f"{key}/{language}: "
                    "frontmatter language mismatch"
                )

            slug = fm["slug"]

            if not SLUG_RE.fullmatch(slug):
                raise RuntimeError(
                    f"{key}/{language}: "
                    f"invalid slug {slug!r}"
                )

            if slug != path.stem:
                raise RuntimeError(
                    f"{key}/{language}: "
                    f"slug/file drift: "
                    f"{slug!r} != "
                    f"{path.stem!r}"
                )

            urls = build_urls(
                language=language,
                world=loc["world"],
                region=loc["region"],
                entity_type=(
                    fm["entity_type"]
                ),
                slug=slug,
            )

            if (
                urls["html_url"]
                in seen_html
            ):
                raise RuntimeError(
                    f"duplicate HTML URL: "
                    f"{urls['html_url']}"
                )

            if (
                urls[
                    "canonical_markdown_url"
                ]
                in seen_markdown
            ):
                raise RuntimeError(
                    "duplicate Markdown URL: "
                    + urls[
                        "canonical_markdown_url"
                    ]
                )

            seen_html.add(
                urls["html_url"]
            )

            seen_markdown.add(
                urls[
                    "canonical_markdown_url"
                ]
            )

            language_records[
                language
            ] = {
                "title": fm["title"],
                "status": fm["status"],
                "entity_type": (
                    fm["entity_type"]
                ),
                "content_type": (
                    fm["content_type"]
                ),
                "revision": fm["revision"],
                "updated": fm["updated"],
                "html_url": (
                    urls["html_url"]
                ),
                "canonical_html_url": (
                    urls[
                        "canonical_html_url"
                    ]
                ),
                "canonical_markdown_url": (
                    urls[
                        "canonical_markdown_url"
                    ]
                ),
            }

        # Identity-level fields that must agree
        # across all language manifestations.
        entity_types = {
            record["entity_type"]
            for record
            in language_records.values()
        }

        content_types = {
            record["content_type"]
            for record
            in language_records.values()
        }

        if len(entity_types) != 1:
            raise RuntimeError(
                f"{key}: entity_type differs "
                "across languages"
            )

        if len(content_types) != 1:
            raise RuntimeError(
                f"{key}: content_type differs "
                "across languages"
            )

        alternates = {
            language: (
                language_records[
                    language
                ]["canonical_html_url"]
            )
            for language
            in sorted(language_records)
        }

        entries.append({
            "entry_key": key,
            "registry_status": (
                identities[key]["status"]
            ),
            "language_alternates": (
                alternates
            ),
            "languages": (
                language_records
            ),
        })

    catalog = {
        "schema_version": "1.1",
        "catalog_type": (
            "sanapedia_entry_catalog"
        ),
        "entry_count": len(entries),
        "entries": entries,
    }

    return (
        catalog,
        identity_rows,
        language_rows,
        seen_html,
        seen_markdown,
    )


def main():
    (
        catalog,
        identity_rows,
        language_rows,
        seen_html,
        seen_markdown,
    ) = build_catalog()

    rendered = (
        json.dumps(
            catalog,
            ensure_ascii=False,
            indent=2,
        )
        + "\n"
    ).encode("utf-8")

    if not CURRENT_CATALOG.is_file():
        raise RuntimeError(
            f"current catalog not found: "
            f"{CURRENT_CATALOG}"
        )

    current = (
        CURRENT_CATALOG.read_bytes()
    )

    language_counts = Counter(
        row["language"].strip()
        for row in language_rows
    )

    print(
        "Generator: Entries JSON "
        "from Registry v2 (N-language)"
    )
    print(
        f"Identity rows:     "
        f"{len(identity_rows)}"
    )
    print(
        f"Manifestations:    "
        f"{len(language_rows)}"
    )
    print(
        "Languages:         "
        + ", ".join(
            f"{lang}={count}"
            for lang, count
            in sorted(
                language_counts.items()
            )
        )
    )
    print(
        f"Catalog entries:   "
        f"{catalog['entry_count']}"
    )
    print(
        f"HTML URLs:         "
        f"{len(seen_html)}"
    )
    print(
        f"Markdown URLs:     "
        f"{len(seen_markdown)}"
    )
    print(
        f"Generated bytes:   "
        f"{len(rendered)}"
    )
    print(
        f"Current bytes:     "
        f"{len(current)}"
    )
    print()

    if rendered == current:
        print(
            "Comparison:       "
            "BYTE-FOR-BYTE MATCH"
        )
    else:
        print(
            "Comparison:       "
            "DIFFERENT"
        )
        print("RESULT: FAIL")
        raise SystemExit(1)

    print()
    print(
        "Registry v2 successfully reproduces "
        "the current public catalog."
    )
    print(
        "No EN/JA assumptions are used in "
        "catalog language enumeration."
    )
    print("RESULT: PASS")
    print("READ ONLY")
    print("No files modified.")


if __name__ == "__main__":
    main()
