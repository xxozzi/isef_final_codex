#!/usr/bin/env python3
"""Summarize section structure, tone, and figure/table patterns in local TeX sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LITERATURE_DIR = ROOT / "literature"
MISC_DIR = ROOT / "misc"
CURRENT_DRAFT = ROOT.parent / "cda_final_v2" / "main.tex"

PAPER_TEX = {
    "current_cda": [CURRENT_DRAFT],
    "swad": sorted((LITERATURE_DIR / "swad" / "source").glob("*.tex")),
    "diwa": sorted((LITERATURE_DIR / "diwa" / "source").glob("**/*.tex")),
    "miro": sorted((LITERATURE_DIR / "miro" / "source").glob("*.tex")),
    "qrm": sorted((LITERATURE_DIR / "qrm" / "source").glob("*.tex")),
    "domainbed": sorted((LITERATURE_DIR / "domainbed" / "source").glob("*.tex")),
    "model_soups": sorted((LITERATURE_DIR / "model_soups" / "source").glob("**/*.tex")),
    "large_pretraining_dg": sorted((LITERATURE_DIR / "large_pretraining_dg" / "source").glob("*.tex")),
    "dgsam": sorted((LITERATURE_DIR / "dgsam" / "source").glob("*.tex")),
    "groupdro": sorted((LITERATURE_DIR / "groupdro" / "source").glob("*.tex")),
    "eoa": sorted((LITERATURE_DIR / "eoa" / "source").glob("**/*.tex")),
    "wdrdg": sorted((LITERATURE_DIR / "wdrdg" / "source").glob("*.tex")),
    "fad": sorted((LITERATURE_DIR / "fad" / "source").glob("**/*.tex")),
    "wilds": sorted((LITERATURE_DIR / "wilds" / "source").glob("*.tex")),
}

TONE_PATTERNS = [
    "matters because",
    "this is why",
    "why ",
    "not merely",
    "not just",
    "does not compete",
    "the claim is",
    "coherent reason",
    "defensible",
    "should be read",
    "primitive object",
]


def read_files(paths: list[Path]) -> str:
    parts = []
    for path in paths:
        if path.exists() and path.is_file():
            parts.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def strip_comments(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("%"))


def collect_sections(text: str) -> list[str]:
    pattern = re.compile(r"\\(?:section|subsection|subsubsection|paragraph)\*?\{([^{}]+)\}")
    return pattern.findall(text)


def first_paragraphs(text: str, n: int = 6) -> list[str]:
    text = strip_comments(text)
    text = re.sub(r"\\input\{[^{}]+\}", "", text)
    text = re.sub(r"\\(?:section|subsection|subsubsection|paragraph)\*?\{[^{}]+\}", "\n\n", text)
    chunks = [re.sub(r"\s+", " ", chunk).strip() for chunk in re.split(r"\n\s*\n", text)]
    chunks = [chunk for chunk in chunks if len(chunk.split()) >= 25 and not chunk.startswith("\\")]
    return chunks[:n]


def count_env(text: str, env: str) -> int:
    return len(re.findall(r"\\begin\{" + re.escape(env) + r"\}", text))


def tone_hits(text: str) -> dict[str, int]:
    lowered = text.lower()
    return {pattern: lowered.count(pattern) for pattern in TONE_PATTERNS if lowered.count(pattern)}


def main() -> None:
    MISC_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Literature Style Audit",
        "",
        "This audit is generated from downloaded/local TeX sources and is meant to guide the CDA rewrite.",
        "",
    ]

    for name, paths in PAPER_TEX.items():
        text = read_files(paths)
        if not text.strip():
            continue
        sections = collect_sections(text)
        paragraphs = first_paragraphs(text)
        hits = tone_hits(text)
        words = len(re.findall(r"\b\w+\b", text))
        lines.extend(
            [
                f"## {name}",
                f"- TeX files scanned: `{len(paths)}`",
                f"- Approximate TeX word count: `{words}`",
                f"- Figures: `{count_env(text, 'figure')}`; tables: `{count_env(text, 'table') + count_env(text, 'table*')}`; algorithms: `{count_env(text, 'algorithm')}`",
                f"- Section sequence: {', '.join(sections[:18]) if sections else 'N/A'}",
                f"- Over-explanatory tone hits: {hits if hits else '{}'}",
                "",
                "Representative opening paragraphs:",
            ]
        )
        for paragraph in paragraphs[:3]:
            clipped = paragraph[:650] + ("..." if len(paragraph) > 650 else "")
            lines.append(f"- {clipped}")
        lines.append("")

    (MISC_DIR / "literature_style_audit.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
