#!/usr/bin/env python3
"""Prints a visual tree of all directories and files from a given root."""
from pathlib import Path
import sys


def tree(path: Path, prefix: str = "") -> None:
    try:
        entries = sorted(
            path.iterdir(),
            key=lambda p: (p.is_file(), p.name.lower())
        )
    except PermissionError:
        print(prefix + "[Permission Denied]")
        return

    count = len(entries)
    for index, entry in enumerate(entries):
        connector = "└── " if index == count - 1 else "├── "
        print(prefix + connector + entry.name)

        if entry.is_dir():
            extension = "    " if index == count - 1 else "│   "
            tree(entry, prefix + extension)


def main():
    if len(sys.argv) > 1:
        root = Path(sys.argv[1]).resolve()
    else:
        root = Path.cwd()

    if not root.exists():
        print(f"Error: '{root}' does not exist.")
        sys.exit(1)

    print(root)
    if root.is_dir():
        tree(root)
    else:
        print("The given path is a file, not a directory.")


if __name__ == "__main__":
    main()
