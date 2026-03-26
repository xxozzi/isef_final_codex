#!/usr/bin/env python3
"""
Scans all .md files for standardized headers and reports:
- Which files were edited most recently
- File descriptions, status, and key contents
- Which files lack standardized headers
"""
import re
from pathlib import Path
from datetime import datetime
import sys


def parse_header(filepath):
    """Parse the standardized YAML-like header from an .md file."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    end = content.find("---", 3)
    if end == -1:
        return None

    header_text = content[3:end].strip()
    header = {}
    current_key = None

    for line in header_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            header[key] = value
            current_key = key
        elif stripped.startswith("- ") and current_key:
            existing = header.get(current_key, "")
            if existing:
                header[current_key] = existing + " | " + stripped[2:]
            else:
                header[current_key] = stripped[2:]

    return header


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()

    md_files = sorted(root.rglob("*.md"))
    parsed = []
    unparsed = []

    for f in md_files:
        header = parse_header(f)
        if header and "last_modified" in header:
            parsed.append((f, header))
        else:
            unparsed.append(f)

    # Sort by last_modified descending
    def sort_key(item):
        lm = item[1].get("last_modified", "0000-00-00 00:00")
        return lm

    parsed.sort(key=sort_key, reverse=True)

    print("=" * 80)
    print("MARKDOWN FILE STATUS REPORT")
    print("=" * 80)
    print()

    if parsed:
        print("FILES WITH STANDARDIZED HEADERS (most recently modified first):")
        print("-" * 80)
        for filepath, header in parsed:
            rel = filepath.relative_to(root)
            print(f"  File:           {rel}")
            print(f"    Title:          {header.get('title', 'N/A')}")
            print(f"    Description:    {header.get('description', 'N/A')}")
            print(f"    Last Modified:  {header.get('last_modified', 'N/A')}")
            print(f"    Modified By:    {header.get('last_modified_by', 'N/A')}")
            print(f"    Status:         {header.get('status', 'N/A')}")
            print(f"    Key Functions:  {header.get('key_functions', 'N/A')}")
            change = header.get("latest_change", header.get("change_log", "N/A"))
            print(f"    Latest Change:  {change}")
            print()

    if unparsed:
        print()
        print("FILES WITHOUT STANDARDIZED HEADERS:")
        print("-" * 80)
        for filepath in sorted(unparsed):
            rel = filepath.relative_to(root)
            print(f"  {rel}")

    print()
    print(f"Total .md files found: {len(md_files)}")
    print(f"  With standardized headers: {len(parsed)}")
    print(f"  Without standardized headers: {len(unparsed)}")


if __name__ == "__main__":
    main()
