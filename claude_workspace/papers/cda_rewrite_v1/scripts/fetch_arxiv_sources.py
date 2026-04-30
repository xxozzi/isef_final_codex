#!/usr/bin/env python3
"""Download arXiv PDFs and source bundles for the CDA rewrite literature corpus."""

from __future__ import annotations

import gzip
import os
import shutil
import tarfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LITERATURE_DIR = ROOT / "literature"
MISC_DIR = ROOT / "misc"

PAPERS = [
    ("swa", "1803.05407", "Averaging weights leads to wider optima and better generalization"),
    ("domainbed", "2007.01434", "In Search of Lost Domain Generalization"),
    ("swad", "2102.08604", "SWAD: Domain Generalization by Seeking Flat Minima"),
    ("diwa", "2205.09739", "Diverse Weight Averaging for Out-of-Distribution Generalization"),
    ("miro", "2203.10789", "Model-Based Domain Generalization"),
    ("qrm", "2207.09944", "Probable Domain Generalization via Quantile Risk Minimization"),
    ("model_soups", "2203.05482", "Model Soups: Averaging Weights of Multiple Fine-Tuned Models"),
    ("large_pretraining_dg", "2412.02856", "Is Large-Scale Pretraining the Secret to Good Domain Generalization?"),
    ("dgsam", "2503.23430", "DGSAM: Domain Generalization via Individual Sharpness-Aware Minimization"),
    ("groupdro", "1911.08731", "Distributionally Robust Neural Networks for Group Shifts"),
    ("eoa", "2110.10832", "Ensemble of Averages for Domain Generalization"),
    ("wdrdg", "2207.04913", "Wasserstein Distributionally Robust Domain Generalization"),
    ("fad", "2307.11108", "Flatness-Aware Minimization for Domain Generalization"),
    ("wilds", "2012.07421", "WILDS: A Benchmark of in-the-Wild Distribution Shifts"),
]


def download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "cda-rewrite-literature/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        target.write_bytes(response.read())


def unpack_source(archive: Path, target_dir: Path) -> str:
    target_dir.mkdir(parents=True, exist_ok=True)
    try:
        if zipfile.is_zipfile(archive):
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(target_dir)
            return "zip"
        if tarfile.is_tarfile(archive):
            with tarfile.open(archive) as tf:
                tf.extractall(target_dir)
            return "tar"
        with gzip.open(archive, "rb") as source, (target_dir / "source.tex").open("wb") as dest:
            shutil.copyfileobj(source, dest)
        return "gzip-tex"
    except Exception as exc:  # Keep the raw bundle for manual inspection.
        (target_dir / "UNPACK_ERROR.txt").write_text(str(exc), encoding="utf-8")
        return "raw-only"


def normalize_permissions(path: Path) -> None:
    for current, dirs, files in os.walk(path):
        for name in dirs:
            try:
                os.chmod(Path(current) / name, 0o755)
            except OSError:
                pass
        for name in files:
            try:
                os.chmod(Path(current) / name, 0o644)
            except OSError:
                pass


def main() -> None:
    LITERATURE_DIR.mkdir(parents=True, exist_ok=True)
    MISC_DIR.mkdir(parents=True, exist_ok=True)
    manifest_lines = [
        "# Downloaded Literature Corpus",
        "",
        "This file records PDFs and source bundles downloaded for the CDA rewrite.",
        "",
    ]

    for slug, arxiv_id, title in PAPERS:
        paper_dir = LITERATURE_DIR / slug
        source_dir = paper_dir / "source"
        pdf_path = paper_dir / f"{slug}.pdf"
        source_path = paper_dir / f"{slug}_source"

        manifest_lines.append(f"## {slug}")
        manifest_lines.append(f"- Title: {title}")
        manifest_lines.append(f"- arXiv: `{arxiv_id}`")

        try:
            download(f"https://arxiv.org/pdf/{arxiv_id}", pdf_path)
            manifest_lines.append(f"- PDF: `{pdf_path.relative_to(ROOT)}`")
        except urllib.error.URLError as exc:
            manifest_lines.append(f"- PDF download failed: `{exc}`")

        try:
            download(f"https://arxiv.org/e-print/{arxiv_id}", source_path)
            unpacked_as = unpack_source(source_path, source_dir)
            normalize_permissions(source_dir)
            manifest_lines.append(f"- Source bundle: `{source_path.relative_to(ROOT)}`")
            manifest_lines.append(f"- Source extraction: `{unpacked_as}` into `{source_dir.relative_to(ROOT)}`")
        except urllib.error.URLError as exc:
            manifest_lines.append(f"- Source download failed: `{exc}`")

        manifest_lines.append("")

    (LITERATURE_DIR / "download_manifest.md").write_text(
        "\n".join(manifest_lines) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
