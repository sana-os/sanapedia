#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

SCANNED_EXTENSIONS = {".md", ".txt"}

CODE_FENCE_ID = re.compile(
    r'^`{3,}[A-Za-z0-9_-]+[ \t]+id="[^"]+"[ \t]*$'
)

FOUR_OR_MORE_BACKTICKS = re.compile(
    r'^`{4,}[ \t]*$'
)

id_fences = []
long_fences = []
files_scanned = 0

for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue

    if ".git" in path.parts:
        continue

    if path.suffix.lower() not in SCANNED_EXTENSIONS:
        continue

    files_scanned += 1

    try:
        lines = path.read_text(
            encoding="utf-8"
        ).splitlines()
    except UnicodeDecodeError:
        print(f"[ERROR] UTF-8 decode failed: {path.relative_to(ROOT)}")
        sys.exit(1)

    for lineno, line in enumerate(lines, 1):
        rel = path.relative_to(ROOT)

        if CODE_FENCE_ID.fullmatch(line):
            id_fences.append((rel, lineno))

        if FOUR_OR_MORE_BACKTICKS.fullmatch(line):
            long_fences.append((rel, lineno))

print("Checker: Repository Markdown Hygiene v1.0")
print(f"Files scanned:                    {files_scanned}")
print(f"Code-fence id attributes:         {len(id_fences)}")
print(f"Four-or-more backtick fences:     {len(long_fences)}")

errors = len(id_fences) + len(long_fences)

if id_fences:
    print()
    print("=== CODE-FENCE id ATTRIBUTES ===")
    for path, lineno in id_fences:
        print(f"{path}:{lineno}")

if long_fences:
    print()
    print("=== FOUR-OR-MORE BACKTICK FENCES ===")
    for path, lineno in long_fences:
        print(f"{path}:{lineno}")

print()
print(f"Errors: {errors}")

if errors:
    print("RESULT: FAIL")
    sys.exit(1)

print("RESULT: PASS")
