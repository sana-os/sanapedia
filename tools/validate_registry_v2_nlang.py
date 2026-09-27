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

CATALOG = (
    ROOT / "public" / "data" / "entries.json"
)

ORIGIN = "https://pastfold.org"

ENTRY_KEY_RE = re.compile(r"^sp_[0-9]{8}$")

LANGUAGE_RE = re.compile(
    r"^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$"
)

SLUG_RE = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)

ROUTE_CLASS = {
    "historical_hub": None,
    "person": "people",
    "event": "events",
    "timeline": "timelines",
}

CATALOG_TOP_FIELDS = {
    "schema_version",
    "catalog_type",
    "entry_count",
    "entries",
}

CATALOG_ENTRY_FIELDS = {
    "entry_key",
    "registry_status",
    "language_alternates",
    "languages",
}

CATALOG_LANGUAGE_FIELDS = {
    "title",
    "status",
    "entity_type",
    "content_type",
    "revision",
    "updated",
    "html_url",
    "canonical_html_url",
    "canonical_markdown_url",
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

    return data


def source_location(path, language):
    parts = path.relative_to(ROOT).parts

    # General N-language repository convention:
    # {LANG}/worlds/{world}/{region}/...
    if len(parts) < 5:
        raise RuntimeError(
            f"path too shallow: {path}"
        )

    if parts[0].lower() != language.lower():
        raise RuntimeError(
            f"language directory mismatch: "
            f"{path} vs {language}"
        )

    if parts[1] != "worlds":
        raise RuntimeError(
            f"expected worlds hierarchy: {path}"
        )

    return {
        "world": parts[2],
        "region": parts[3],
    }


def expected_urls(
    language,
    world,
    region,
    entity_type,
    slug,
):
    if entity_type not in ROUTE_CLASS:
        raise RuntimeError(
            f"no URL rule for entity_type "
            f"{entity_type!r}"
        )

    route = ROUTE_CLASS[
        entity_type
    ]

    base = (
        f"/{language}/worlds/"
        f"{world}/{region}"
    )

    if route is None:
        html_path = (
            f"{base}/{slug}/"
        )
        md_path = (
            f"{base}/{slug}.md"
        )
    else:
        html_path = (
            f"{base}/{route}/{slug}/"
        )
        md_path = (
            f"{base}/{route}/{slug}.md"
        )

    html_url = (
        ORIGIN + html_path
    )

    return {
        "html_url": html_url,
        "canonical_html_url": html_url,
        "canonical_markdown_url": (
            ORIGIN + md_path
        ),
    }


def main():
    errors = []
    info = []

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

    for row in identity_rows:
        key = row["entry_key"].strip()

        if not ENTRY_KEY_RE.fullmatch(key):
            errors.append(
                f"invalid identity entry_key: "
                f"{key!r}"
            )
            continue

        if key in identities:
            errors.append(
                f"duplicate identity: {key}"
            )
            continue

        identities[key] = {
            "status": row["status"].strip(),
            "notes": row["notes"],
        }

    manifestations = defaultdict(dict)
    seen_files = set()

    for row in language_rows:
        key = row["entry_key"].strip()
        language = row["language"].strip()
        file_value = row["file"].strip()

        if key not in identities:
            errors.append(
                f"orphan manifestation: "
                f"{key}/{language}"
            )
            continue

        if not LANGUAGE_RE.fullmatch(
            language
        ):
            errors.append(
                f"invalid language tag: "
                f"{language!r}"
            )
            continue

        if language in manifestations[key]:
            errors.append(
                f"duplicate manifestation: "
                f"{key}/{language}"
            )
            continue

        if file_value in seen_files:
            errors.append(
                f"repository file reused by "
                f"multiple manifestations: "
                f"{file_value}"
            )
        else:
            seen_files.add(file_value)

        manifestations[key][language] = (
            file_value
        )

    # Deterministic ordering.
    identity_order = [
        row["entry_key"].strip()
        for row in identity_rows
    ]

    if identity_order != sorted(
        identity_order
    ):
        errors.append(
            "identity registry is not "
            "sorted by entry_key"
        )

    manifestation_order = [
        (
            row["entry_key"].strip(),
            row["language"].strip(),
        )
        for row in language_rows
    ]

    if manifestation_order != sorted(
        manifestation_order
    ):
        errors.append(
            "language registry is not "
            "sorted by entry_key + language"
        )

    if not CATALOG.is_file():
        errors.append(
            f"catalog not found: {CATALOG}"
        )
        catalog = {}
    else:
        try:
            raw = CATALOG.read_text(
                encoding="utf-8"
            )
            catalog = json.loads(raw)
        except Exception as exc:
            errors.append(
                f"invalid catalog JSON: {exc}"
            )
            catalog = {}

    if catalog:
        if set(catalog) != CATALOG_TOP_FIELDS:
            errors.append(
                "unexpected catalog "
                "top-level fields"
            )

        if (
            catalog.get("schema_version")
            != "1.1"
        ):
            errors.append(
                "unexpected catalog "
                "schema_version"
            )

        if (
            catalog.get("catalog_type")
            != "sanapedia_entry_catalog"
        ):
            errors.append(
                "unexpected catalog_type"
            )

    catalog_entries = (
        catalog.get("entries", [])
        if isinstance(catalog, dict)
        else []
    )

    if not isinstance(
        catalog_entries,
        list,
    ):
        errors.append(
            "catalog entries is not a list"
        )
        catalog_entries = []

    if (
        catalog.get("entry_count")
        != len(catalog_entries)
    ):
        errors.append(
            "catalog entry_count mismatch"
        )

    catalog_by_key = {}

    for entry in catalog_entries:
        if not isinstance(entry, dict):
            errors.append(
                "catalog entry is not "
                "an object"
            )
            continue

        key = entry.get("entry_key")

        if key in catalog_by_key:
            errors.append(
                f"duplicate catalog "
                f"entry_key: {key}"
            )
            continue

        catalog_by_key[key] = entry

    # Historical catalog projection:
    # Registry v2 may contain identities that are not part of
    # the historical /worlds/ publication projection.
    #
    # Zero-manifestation identities are valid at the Registry
    # identity layer and are therefore outside this catalog.
    #
    # An identity with manifestations is a historical catalog
    # candidate only when all current manifestations are under
    # {LANG}/worlds/...
    historical_keys = set()
    mixed_projection_keys = set()

    for key in identities:
        rows = manifestations[key]

        if not rows:
            continue

        classes = set()

        for language, file_value in rows.items():
            parts = PurePosixPath(
                file_value
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

    for key in sorted(mixed_projection_keys):
        errors.append(
            f"{key}: mixed historical and "
            "non-historical manifestation paths"
        )

    if (
        set(catalog_by_key)
        != historical_keys
    ):
        errors.append(
            "catalog identity set differs "
            "from historical projection "
            "of Registry v2"
        )

    seen_html = set()
    seen_md = set()

    for key in sorted(historical_keys):
        entry = catalog_by_key.get(key)

        if entry is None:
            continue

        if set(entry) != (
            CATALOG_ENTRY_FIELDS
        ):
            errors.append(
                f"{key}: unexpected "
                "catalog entry fields"
            )

        if (
            entry.get("registry_status")
            != identities[key]["status"]
        ):
            errors.append(
                f"{key}: registry_status "
                "mismatch"
            )

        catalog_languages = (
            entry.get("languages")
        )

        if not isinstance(
            catalog_languages,
            dict,
        ):
            errors.append(
                f"{key}: languages is "
                "not an object"
            )
            continue

        expected_languages = set(
            manifestations[key]
        )

        if set(catalog_languages) != (
            expected_languages
        ):
            errors.append(
                f"{key}: catalog language "
                "set differs from registry"
            )

        expected_alternates = {}

        identity_entity_types = set()
        identity_content_types = set()

        for language in sorted(
            manifestations[key]
        ):
            file_value = (
                manifestations[key][language]
            )

            path = repo_path_to_local(
                file_value
            )

            fm = parse_frontmatter(path)

            if (
                fm.get("entry_key")
                != key
            ):
                errors.append(
                    f"{key}/{language}: "
                    "frontmatter entry_key "
                    "mismatch"
                )

            if (
                fm.get("language")
                != language
            ):
                errors.append(
                    f"{key}/{language}: "
                    "frontmatter language "
                    "mismatch"
                )

            if "translation_of" in fm:
                errors.append(
                    f"{key}/{language}: "
                    "registered source still "
                    "contains translation_of"
                )

            slug = fm.get(
                "slug",
                "",
            )

            if not SLUG_RE.fullmatch(
                slug
            ):
                errors.append(
                    f"{key}/{language}: "
                    f"invalid slug {slug!r}"
                )

            if slug != path.stem:
                errors.append(
                    f"{key}/{language}: "
                    "slug/file drift"
                )

            try:
                loc = source_location(
                    path,
                    language,
                )
            except RuntimeError as exc:
                errors.append(str(exc))
                continue

            entity_type = fm.get(
                "entity_type"
            )

            content_type = fm.get(
                "content_type"
            )

            identity_entity_types.add(
                entity_type
            )

            identity_content_types.add(
                content_type
            )

            try:
                urls = expected_urls(
                    language,
                    loc["world"],
                    loc["region"],
                    entity_type,
                    slug,
                )
            except RuntimeError as exc:
                errors.append(
                    f"{key}/{language}: "
                    f"{exc}"
                )
                continue

            record = catalog_languages.get(
                language
            )

            if not isinstance(
                record,
                dict,
            ):
                errors.append(
                    f"{key}/{language}: "
                    "catalog language record "
                    "missing"
                )
                continue

            if set(record) != (
                CATALOG_LANGUAGE_FIELDS
            ):
                errors.append(
                    f"{key}/{language}: "
                    "unexpected catalog "
                    "language fields"
                )

            for field in (
                "title",
                "status",
                "entity_type",
                "content_type",
                "revision",
                "updated",
            ):
                if (
                    record.get(field)
                    != fm.get(field)
                ):
                    errors.append(
                        f"{key}/{language}: "
                        f"{field} mismatch"
                    )

            for field, expected in (
                urls.items()
            ):
                if (
                    record.get(field)
                    != expected
                ):
                    errors.append(
                        f"{key}/{language}: "
                        f"{field} mismatch"
                    )

            html = urls["html_url"]
            md = urls[
                "canonical_markdown_url"
            ]

            if html in seen_html:
                errors.append(
                    f"duplicate HTML URL: "
                    f"{html}"
                )
            else:
                seen_html.add(html)

            if md in seen_md:
                errors.append(
                    f"duplicate Markdown URL: "
                    f"{md}"
                )
            else:
                seen_md.add(md)

            expected_alternates[
                language
            ] = urls[
                "canonical_html_url"
            ]

        if len(identity_entity_types) != 1:
            errors.append(
                f"{key}: entity_type differs "
                "across manifestations"
            )

        if len(identity_content_types) != 1:
            errors.append(
                f"{key}: content_type differs "
                "across manifestations"
            )

        if (
            entry.get(
                "language_alternates"
            )
            != expected_alternates
        ):
            errors.append(
                f"{key}: "
                "language_alternates mismatch"
            )

    language_counts = Counter(
        row["language"].strip()
        for row in language_rows
    )

    info.append(
        "Language enumeration comes entirely "
        "from entry-language-registry.csv."
    )

    info.append(
        "No fixed EN/JA manifestation set is "
        "required by this validator."
    )

    info.append(
        "Public URLs are independently derived "
        "from manifestation path + frontmatter "
        "+ Pastfold URL rules."
    )

    print(
        "Validator: Registry v2 / "
        "N-language Catalog v1.0"
    )
    print(
        f"Identities:       "
        f"{len(identity_rows)}"
    )
    print(
        f"Manifestations:   "
        f"{len(language_rows)}"
    )
    print(
        "Languages:        "
        + ", ".join(
            f"{lang}={count}"
            for lang, count
            in sorted(
                language_counts.items()
            )
        )
    )
    print(
        f"Catalog entries:  "
        f"{len(catalog_entries)}"
    )
    print(
        f"HTML URLs:        "
        f"{len(seen_html)}"
    )
    print(
        f"Markdown URLs:    "
        f"{len(seen_md)}"
    )
    print(
        f"Errors:           "
        f"{len(errors)}"
    )
    print("Warnings:         0")
    print(
        f"Info:             "
        f"{len(info)}"
    )
    print()

    for message in errors:
        print(
            f"[ERROR] {message}"
        )

    for message in info:
        print(
            f"[INFO] {message}"
        )

    print()

    if errors:
        print("RESULT: FAIL")
        raise SystemExit(1)

    print("RESULT: PASS")
    print("READ ONLY")


if __name__ == "__main__":
    main()
