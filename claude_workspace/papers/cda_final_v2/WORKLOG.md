# CDA Final V2 Worklog

This file is the persistent checkpoint for the rewrite. When context gets tight, resume from here first.

## Master Checklist

- [x] Create `cda_final_v2` workspace and copy the NeurIPS style file.
- [x] Create persistent notes for sources, critiques, and approved results.
- [x] Extract the salvageable scientific core from `CDA_final`.
- [x] Build the citation map and expand the bibliography from primary sources.
- [x] Design the manuscript macro layer for canonical versus provisional red content.
- [x] Write the front matter, preamble, and infrastructure in `main.tex`.
- [x] Rewrite the abstract last.
- [x] Rewrite the introduction.
- [x] Rewrite related work.
- [x] Rewrite the theory / theoretical motivation section.
- [x] Rewrite the unified method + setup section.
- [x] Add the empirical-analysis subsection inside the method section.
- [x] Write the experiments section with evaluation protocol, main results, and ablations.
- [x] Write discussion, limitations, conclusion, and acknowledgements.
- [x] Rebuild or regenerate figures that survive the rewrite.
- [x] Integrate all citations and verify unsupported claims are removed or sourced.
- [x] Compile in draft mode and fix LaTeX issues.
- [x] Compile in submission mode and verify that provisional red content hard-fails the build.
- [x] Run adversarial critique loops and revise.
- [x] Run final consistency and banned-artifact checks.
- [x] Add local `.gitignore` rules for LaTeX build artifacts.
- [x] Visually sanity-check regenerated figure PNG exports.
- [x] Normalize table font scaling so main and appendix tables no longer upscale to fill width.
- [x] Expand comparison figures and tables to include ERM, SAM, SWA, SWAD, DiWA, EoA, and CDA-family methods where relevant.
- [x] Apply one fixed color palette across all regenerated figures.
- [x] Add method schematics for version-space compression and CDA weighting mechanics.
- [x] Export every generated paper figure as SVG in addition to PDF/PNG for Figma import.
- [x] Generate Figma-native FigJam diagrams for the CDA overview, VSC selector, and CDA weighting mechanics using the shared palette.

## Non-Negotiable Constraints

- Use `claude_workspace/papers/CDA_final/main.tex` as the only scientific predecessor.
- Treat the user-provided Dr. Asari result tables as the canonical real-results package.
- Allow provisional red values and red provisional interpretation throughout the draft in final-paper voice.
- Keep the distinction between canonical and provisional content mechanical through macros and submission-mode failure.
- Use `we`, not `this paper`.
- Remove roadmap language, reviewer-facing prose, raw internal identifiers, and obsolete internal names.
- Keep proofs and long derivations in the appendix by default.

## Current Focus

- The latest SWAD-style expansion pass is complete: the paper now follows the SWAD section sequence, has a longer abstract, expanded theory/method analysis, flatness diagnostics, loss-surface visualization, checkpoint-fluctuation analysis, combination studies, ablations, and appendix proof/protocol material.
- The latest comparison/visual pass is complete: the main result table uses `\scriptsize`, all `adjustbox` table wrappers use `max width=\linewidth` rather than forced width, and the main comparison table has tighter `\tabcolsep` / `\arraystretch` settings.
- The figure system now has eight generated assets: `cda_sampling_overview`, `vsc_mechanism`, `weighting_mechanism`, `benchmark_comparison`, `flatness_comparison`, `loss_surface`, `accuracy_fluctuation`, and `certificate_proxy_comparison`.
- The fixed palette in `scripts/generate_figures.py` is now: paper `#F7F5F0`, ink `#182033`, ERM `#9199A8`, SAM `#B85C2E`, SWA `#BF911F`, SWAD `#3658C7`, DiWA `#6E53E9`, EoA `#56657C`, CDA-Piv `#2E7D66`, and CDA-BD `#0D776A`. Do not introduce new method colors without updating that palette centrally.
- Every local figure export now has `.pdf`, `.png`, and `.svg` versions. The SVG files are the editable Figma handoff format.
- Figma-native FigJam diagrams created in this session are recorded in `notes/figma_assets.md`: CDA Overview, CDA VSC Mechanism, CDA Weighting Mechanics, CDA Certificate View, and the compact overview test.
- Draft mode compiles successfully with `latexmk -pdf main.tex` and produces a 21-page `main.pdf`.
- Submission mode intentionally fails when red provisional content is present using:
  `pdflatex -interaction=nonstopmode -jobname=submission "\def\submissionmodeflag{1}\input{main.tex}"`
- The Figma skill is installed, and the FigJam diagram generator is exposed. The lower-level `use_figma` canvas-editing tool is not exposed, so exact quantitative chart frames cannot be programmatically recreated directly in a live Figma canvas from this session.
- The downloaded FigJam outputs arrive as SVG plus thumbnail imagery. They are useful as real Figma artifacts and handoff references, but the current export path still preserves too much empty board canvas for direct paper insertion.
- Neue Montreal is not installed in the local Matplotlib environment, so local figure generation uses DejaVu Sans as a clean sans fallback.

## Open Items

- If the Figma connector exposes `use_figma` in a future session, recreate the eight current figures in a Figma canvas and export them over the current filenames. Until then, use the SVG files and `notes/figma_assets.md` as the Figma handoff record.
- If another revision pass happens, inspect the generated PDFs visually after regeneration rather than relying only on the Python source.
- If the red analysis layer is later replaced by real finalized values, remove all `\prov`, `\provnum`, and `\provcaption` uses before submission-mode compilation.
- If the benchmark provenance changes, update Appendix A and the captions before changing any headline result prose.
