# CDA Figure Design System Handoff

This directory contains the publication figure exports used by `main.tex`.
Each figure is exported as PDF, PNG, and SVG. The SVG files are the editable
handoff format for Figma import when a writable Figma session is available.

## Palette

| Role | Hex |
| --- | --- |
| Paper background | `#FAF7F0` |
| Ink text | `#161B26` |
| Muted text | `#687083` |
| Grid lines | `#D9E0EA` |
| Cool panel | `#EEF2F7` |
| Warm panel | `#F7E5D4` |
| Mint panel | `#DFF0E8` |
| Lilac panel | `#ECE8F7` |
| ERM | `#8C95A6` |
| SAM | `#D55E00` |
| SWA | `#E69F00` |
| SWAD | `#0072B2` |
| DiWA | `#CC79A7` |
| EoA | `#394150` |
| VSC-uniform | `#5E8C31` |
| CDA-Piv | `#009E73` |
| CDA-BD | `#006D5B` |

## Figure Files

| Figure | Purpose |
| --- | --- |
| `cda_sampling_overview.svg` | Full method overview comparing late-window averaging with CDA deployment. |
| `vsc_mechanism.svg` | Version-space compression selector schematic. |
| `weighting_mechanism.svg` | CDA-Piv and CDA-BD weighting mechanics. |
| `benchmark_comparison.svg` | Benchmark comparison against ERM, SWA, SWAD, DiWA, EoA, and CDA-BD. |
| `flatness_comparison.svg` | Source-loss and source-mixture flatness comparison. |
| `loss_surface.svg` | Two-surface geometric visualization using the same palette ramp. |
| `accuracy_fluctuation.svg` | Checkpoint trajectory and OOD fluctuation comparison. |
| `certificate_proxy_comparison.svg` | Certificate-term comparison across related post-hoc methods. |

## Figma-Native FigJam Diagrams Created In This Session

These are editable FigJam diagrams generated through the Figma plugin with the
same palette as the local figure exports.

| Diagram | Figma URL |
| --- | --- |
| CDA Method Overview Figure | https://www.figma.com/online-whiteboard/create-diagram/ffdb8ac9-1590-4aaf-8993-019ed8c6e477?utm_source=chatgpt&utm_content=edit_in_figjam&oai_id=&request_id=e36b06be-1c85-4ac1-a535-0a4f660f9726 |
| CDA Version-Space Compression Figure | https://www.figma.com/online-whiteboard/create-diagram/c576060a-4602-4e2b-849c-662f3d341aa6?utm_source=chatgpt&utm_content=edit_in_figjam&oai_id=&request_id=4df7fa9f-fc02-4e32-9f88-763c3cf9dcbf |
| CDA Weighting Mechanics Figure | https://www.figma.com/online-whiteboard/create-diagram/87cca7f1-e33a-43f4-b659-673b9854131a?utm_source=chatgpt&utm_content=edit_in_figjam&oai_id=&request_id=009612be-f196-4ba7-9fbc-218f94f834be |

## Figma Import Instructions

1. Open the target Figma file.
2. Import each `.svg` file from this directory.
3. Convert imported groups to frames only if the figure needs manual editing.
4. Preserve the palette above exactly across all figures.
5. Export the final Figma figures back over the same PDF filenames used by LaTeX.

## Current Tooling Limitation

The current Codex session exposes the Figma skill documentation but does not expose
the lower-level writable Figma MCP tools required to create exact chart frames
from arbitrary coordinates and table data. It does expose the FigJam diagram
generator, which was used for the three method schematics above. The exact
quantitative charts are still generated deterministically from
`scripts/generate_figures.py` and exported as SVGs for Figma import.
