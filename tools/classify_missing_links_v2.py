#!/usr/bin/env python3

import argparse
import importlib.util
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
AUDITOR_PATH = Path(__file__).resolve().with_name("audit_internal_links_v2.py")

HISTORICAL_CLASSES = {
    "people",
    "events",
    "phenomena",
    "timelines",
    "timeline",
    "columns",
}

def load_auditor():
    spec = importlib.util.spec_from_file_location(
        "audit_internal_links_v2",
        AUDITOR_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"cannot load auditor: {AUDITOR_PATH}"
        )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def source_language(
    source,
    language_dirs,
):
    rel = source.relative_to(ROOT)
    parts = rel.parts

    if not parts:
        return None

    language_root = parts[0]

    matches = [
        language
        for language, directory
        in language_dirs.items()
        if directory == language_root
    ]

    if len(matches) == 1:
        return matches[0]

    if len(matches) > 1:
        raise RuntimeError(
            f"multiple languages mapped to "
            f"repository root {language_root}"
        )

    return None


def target_language(
    normalized,
    source,
    language_dirs,
):
    path = urlsplit(normalized).path

    parts = [
        part
        for part in path.split("/")
        if part
    ]

    if normalized.startswith("/") and parts:
        language = parts[0].lower()

        if language in language_dirs:
            return language

    return source_language(
        source,
        language_dirs,
    )


def has_legacy_content_prefix(
    value,
    language_dirs,
):
    clean = value.lstrip("/")

    return any(
        clean.startswith(
            f"content/{language_dir}/"
        )
        for language_dir
        in set(language_dirs.values())
    )


def target_basename(normalized):
    path = urlsplit(normalized).path.rstrip("/")

    if not path:
        return None

    return path.split("/")[-1]


def path_components(normalized):
    path = urlsplit(normalized).path

    return {
        part
        for part in path.split("/")
        if part
    }


def build_registered_basename_map(
    registered_files,
    language_dirs,
):
    result = defaultdict(list)

    for path in registered_files:
        language = source_language(
            path,
            language_dirs,
        )

        if language is None:
            continue

        result[
            (language, path.name)
        ].append(path)

    return result


def classify_missing(
    source,
    raw,
    category,
    normalized,
    registered_by_basename,
    language_dirs,
):
    basename = target_basename(normalized)
    components = path_components(normalized)

    if category == "TAG_OR_ANCHOR_ROUTE":
        return (
            "TAG_OR_ANCHOR",
            "fragment-based navigation route",
        )

    if (
        category == "MISSING_INTERNAL"
        and normalized == "/sitemap.xml"
    ):
        return (
            "DEFERRED_SITEMAP",
            "sitemap phase is intentionally deferred",
        )

    if category == "MISSING_NAVIGATION":
        return (
            "NAVIGATION_NO_INDEX",
            "navigation route has no current index target",
        )

    if (
        has_legacy_content_prefix(
            raw,
            language_dirs,
        )
        or has_legacy_content_prefix(
            normalized,
            language_dirs,
        )
    ):
        return (
            "README_STALE_REPO_PATH",
            "old repository path form",
        )

    if (
        normalized.startswith("/principles/")
        or normalized.startswith("/frameworks/")
    ):
        return (
            "LANGUAGELESS_METHOD_ROUTE",
            "methodology route lacks language namespace",
        )

    language = target_language(
        normalized,
        source,
        language_dirs,
    )

    if language and basename:
        matches = registered_by_basename.get(
            (language, basename),
            [],
        )

        if len(matches) == 1:
            rel = matches[0].relative_to(
                ROOT
            ).as_posix()

            return (
                "REGISTERED_ENTRY_RELOCATED",
                f"registered source exists at {rel}",
            )

        if len(matches) > 1:
            rels = ", ".join(
                p.relative_to(ROOT).as_posix()
                for p in matches
            )

            return (
                "OTHER_REVIEW",
                f"multiple registered basename matches: {rels}",
            )

    if components & HISTORICAL_CLASSES:
        return (
            "FUTURE_HISTORICAL_CONTENT",
            "historical content-like target has "
            "no current source file",
        )

    return (
        "OTHER_REVIEW",
        "no current automatic policy classification",
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Read-only semantic classification of "
            "missing references from Internal Link Audit v2."
        )
    )

    parser.add_argument(
        "--detail",
        action="store_true",
        help="show individual classified references",
    )

    args = parser.parse_args()

    audit = load_auditor()

    (
        registered_files,
        route_map,
        language_dirs,
    ) = audit.build_registry_maps()

    registered_by_basename = (
        build_registered_basename_map(
            registered_files,
            language_dirs,
        )
    )

    source_files = audit.files_in_scope(
        language_dirs
    )

    missing_categories = {
        "MISSING_CONTENT",
        "MISSING_NAVIGATION",
        "MISSING_INTERNAL",
        "TAG_OR_ANCHOR_ROUTE",
    }

    occurrences = defaultdict(list)
    semantic_counts = Counter()
    raw_category_counts = Counter()

    errors = []

    for source in source_files:
        try:
            refs = audit.extract_references(
                source
            )
        except Exception as exc:
            errors.append(
                f"{source.relative_to(ROOT)}: {exc}"
            )
            continue

        for item in refs:
            raw = item["target"]

            try:
                (
                    category,
                    normalized,
                    resolved,
                ) = audit.resolve_reference(
                    source,
                    raw,
                    registered_files,
                    route_map,
                    language_dirs,
                )
            except Exception as exc:
                errors.append(
                    f"{source.relative_to(ROOT)}:"
                    f"{item['line']}: {raw!r}: {exc}"
                )
                continue

            if category not in missing_categories:
                continue

            semantic, reason = classify_missing(
                source,
                raw,
                category,
                normalized,
                registered_by_basename,
                language_dirs,
            )

            raw_category_counts[category] += 1
            semantic_counts[semantic] += 1

            key = (
                semantic,
                normalized,
                reason,
            )

            occurrences[key].append({
                "source": (
                    source.relative_to(ROOT).as_posix()
                ),
                "line": item["line"],
                "kind": item["kind"],
                "raw": raw,
                "audit_category": category,
            })

    total = sum(semantic_counts.values())

    print(
        "Classifier: Missing References v2.0 "
        "(Registry v2)"
    )
    print(
        f"Files scanned:        {len(source_files)}"
    )
    print(
        f"Missing occurrences:  {total}"
    )
    print(
        f"Unique missing refs:  {len(occurrences)}"
    )
    print(
        f"Errors:               {len(errors)}"
    )
    print()

    print("=== AUDIT CATEGORY INPUT ===")

    for category in sorted(
        raw_category_counts
    ):
        print(
            f"{category:<24} "
            f"{raw_category_counts[category]:>4}"
        )

    print()
    print("=== SEMANTIC SUMMARY ===")

    for semantic in sorted(
        semantic_counts
    ):
        unique = sum(
            1
            for key in occurrences
            if key[0] == semantic
        )

        print(
            f"{semantic:<30} "
            f"occurrences={semantic_counts[semantic]:>4} "
            f"unique={unique:>3}"
        )

    if errors:
        print()
        print("=== ERRORS ===")

        for error in errors:
            print(f"  {error}")

    if args.detail:
        print()
        print("=== DETAILS ===")

        semantics = sorted({
            key[0]
            for key in occurrences
        })

        for semantic in semantics:
            print()
            print(f"[{semantic}]")

            keys = sorted(
                key
                for key in occurrences
                if key[0] == semantic
            )

            for key in keys:
                _, normalized, reason = key
                rows = occurrences[key]

                print(f"  {normalized}")
                print(
                    f"    occurrences: {len(rows)}"
                )
                print(
                    f"    signal: {reason}"
                )

                for row in rows:
                    print(
                        f"      - "
                        f"{row['source']}:"
                        f"{row['line']} "
                        f"[{row['kind']}]"
                    )

    print()
    print("=== POLICY NOTE ===")
    print(
        "FUTURE_HISTORICAL_CONTENT means "
        "'no current source file found'; "
        "it is not automatically a broken-link judgment."
    )
    print(
        "REGISTERED_ENTRY_RELOCATED means "
        "the knowledge entry exists, but the reference "
        "uses a non-current repository/public path."
    )
    print()
    print("READ ONLY")
    print("No files modified.")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
