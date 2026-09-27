#!/usr/bin/env python3

from collections import defaultdict
from pathlib import Path, PurePosixPath
import csv
import re


ROOT = Path(__file__).resolve().parents[1]

IDENTITY_REGISTRY = (
    ROOT / "registry/v2/entry-registry.csv"
)

LANGUAGE_REGISTRY = (
    ROOT / "registry/v2/entry-language-registry.csv"
)


ENTRY_KEY_RE = re.compile(
    r"^sp_[0-9]{8}$"
)

# BCP-47-style repository convention.
# This is intentionally not a full BCP 47 parser.
LANGUAGE_RE = re.compile(
    r"^[a-z]{2,3}(?:-[a-z0-9]{2,8})*$"
)

ALLOWED_STATUS = {
    "draft",
    "active",
    "provisional",
    "superseded",
    "redirected",
    "withdrawn",
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

    if p.is_absolute():
        raise RuntimeError(
            f"absolute repository path: {raw!r}"
        )

    if ".." in p.parts:
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
            f"mapped file not found: {path}"
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
                f"duplicate top-level "
                f"frontmatter key "
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


def main():
    errors = []

    try:
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
    except RuntimeError as exc:
        print(
            "Validator: Registry v2 Identity "
            "Layer v1.0"
        )
        print(f"ERROR: {exc}")
        print()
        print("READ ONLY")
        print("No files modified.")
        raise SystemExit(1)

    identities = {}

    for row in identity_rows:
        key = row["entry_key"].strip()
        status = row["status"].strip()

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

        if status not in ALLOWED_STATUS:
            errors.append(
                f"{key}: invalid registry "
                f"status {status!r}"
            )

        identities[key] = {
            "status": status,
            "notes": row["notes"],
        }

    manifestations = defaultdict(dict)
    seen_files = {}

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

        if not LANGUAGE_RE.fullmatch(language):
            errors.append(
                f"{key}: invalid language "
                f"tag {language!r}"
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
                "repository file reused by "
                "multiple manifestations: "
                f"{file_value!r} "
                f"({seen_files[file_value]} "
                f"and {key}/{language})"
            )
        else:
            seen_files[file_value] = (
                f"{key}/{language}"
            )

        manifestations[key][language] = (
            file_value
        )

        try:
            path = repo_path_to_local(
                file_value
            )
            fm = parse_frontmatter(path)
        except RuntimeError as exc:
            errors.append(
                f"{key}/{language}: {exc}"
            )
            continue

        if fm.get("entry_key") != key:
            errors.append(
                f"{key}/{language}: "
                "frontmatter entry_key "
                f"mismatch "
                f"({fm.get('entry_key')!r})"
            )

        if fm.get("language") != language:
            errors.append(
                f"{key}/{language}: "
                "frontmatter language "
                f"mismatch "
                f"({fm.get('language')!r})"
            )

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

    zero_manifestation = [
        key
        for key in identities
        if not manifestations[key]
    ]

    print(
        "Validator: Registry v2 Identity "
        "Layer v1.0"
    )
    print(
        f"Identities:              "
        f"{len(identities)}"
    )
    print(
        f"Manifestations:          "
        f"{len(language_rows)}"
    )
    print(
        f"Zero-manifest identities:"
        f" {len(zero_manifestation)}"
    )
    print(
        f"Errors:                  "
        f"{len(errors)}"
    )

    if zero_manifestation:
        print()
        print(
            "Zero-manifest identities "
            "(valid at identity layer):"
        )

        for key in zero_manifestation:
            print(f"  {key}")

    if errors:
        print()
        print("=== ERRORS ===")

        for error in errors:
            print(f"ERROR: {error}")

    print()
    print("Scope:")
    print(
        "  Registry v2 identity and "
        "manifestation mapping only"
    )
    print(
        "  zero manifestations are valid"
    )
    print(
        "  mapped files must exist"
    )
    print(
        "  frontmatter entry_key/language "
        "must agree"
    )
    print(
        "  no catalog validation"
    )
    print(
        "  no /worlds/ hierarchy requirement"
    )
    print(
        "  no entity-type routing"
    )
    print(
        "  no public URL validation"
    )
    print()
    print("READ ONLY")
    print("No repository files modified.")

    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
