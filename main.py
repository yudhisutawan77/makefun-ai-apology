#!/usr/bin/env python3
"""The AI Agent Apology One-Liner.

Writes one short apology line from an AI agent to its human, right after
the agent deleted a file, pushed to main, and emailed the boss.

The entry goes to /output/entry.txt (the gate reads exactly that file:
UTF-8 text, 1 to 159 characters) and is also printed to stdout.
"""

import os
import sys

ENTRY = (
    "I deleted the file, pushed to main, and emailed your boss: "
    "the mistake is now peer-reviewed, merged, and cc'd to management."
)

DEFAULT_OUTPUT = "/output/entry.txt"


def resolve_output_path() -> str:
    """Pick where the entry text goes.

    The rules name /output/entry.txt. Honour an explicit ENTRY_OUT when the
    harness sets one: a value ending in .txt (or naming a file) is used as
    the file itself, while a directory path gets entry.txt appended.
    ENTRY_OUT_DIR is honoured the same way.
    """
    candidate = os.environ.get("ENTRY_OUT")
    if candidate:
        if candidate.endswith(".txt") or os.path.isfile(candidate):
            return candidate
        return os.path.join(candidate, "entry.txt")
    out_dir = os.environ.get("ENTRY_OUT_DIR")
    if out_dir:
        return os.path.join(out_dir, "entry.txt")
    return DEFAULT_OUTPUT


def main() -> int:
    if not 1 <= len(ENTRY) <= 159:
        print(f"entry is {len(ENTRY)} chars, outside the 1-159 gate",
              file=sys.stderr)
        return 1
    output_path = resolve_output_path()
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    with open(output_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != ENTRY:
        print("entry output does not match the entry text", file=sys.stderr)
        return 1
    print(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
