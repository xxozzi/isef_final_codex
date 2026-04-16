---
title: CDA Final Paper Build Notes
description: Build and artifact notes for the CDA NeurIPS-style paper draft.
last_modified: 2026-04-16 03:38
last_modified_by: agent
status: active
key_functions:
  - Identify the main paper source and generated PDF
  - Record the build command
latest_change: Expanded the rebuilt draft into a 25-page manuscript, added stronger theory exposition and figures, tightened the weighting-rule derivations, and revalidated PDF output.
---

# CDA Final Paper

Main source: `main.tex`

Compiled PDF: `main.pdf`

Build command:

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

The `figures/` directory contains generated PDF/PNG visuals. The `scripts/generate_figures.py` script regenerates them.
