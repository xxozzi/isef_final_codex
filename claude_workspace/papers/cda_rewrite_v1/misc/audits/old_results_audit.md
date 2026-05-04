# Old Results Audit

Date: 2026-04-30

This audit answers one question: which empirical claims from `claude_workspace/papers/cda_final_v2/` can be reused in the rewritten CDA paper?

Short answer: none of the old CDA headline results are publication-ready. The five-benchmark CDA numbers, the PACS generalization number, the ablation numbers, and the diagnostic figures should be deleted from the rewritten paper until regenerated from raw experiment files. The only real local evidence I found is partial PACS evidence in `claude_workspace/results/`; it is useful for planning and sanity checks, but it does not support the old five-benchmark claims.

## What I Checked

- `claude_workspace/papers/cda_final_v2/main.tex`
- `claude_workspace/papers/cda_final_v2/appendix_tables.tex`
- `claude_workspace/papers/cda_final_v2/notes/APPROVED_RESULTS_SOURCE.tex`
- `claude_workspace/papers/cda_final_v2/scripts/generate_figures.py`
- `claude_workspace/results/summary_detailed.csv`
- `claude_workspace/results/results_ledger.md`
- `claude_workspace/results/ablation_results_dcola.json`
- `claude_workspace/results/dcola_diagnostics.json`

This is a complete inventory of old empirical claim groups. I grouped repeated numbers together when the same claim appears in prose, a table, a note file, and a plotting script.

## Plain Verdicts

- `verified`: a local result file exists, but the result can only be used with its exact scope.
- `literature-only`: the number is copied from another paper or table and may only be used as a cited comparison.
- `provisional`: the number may have been intended as a future result, but the current files do not prove it.
- `delete`: do not use the claim in the rewritten paper.

## Main Findings

1. The old headline claim, CDA \(68.3\) average OOD accuracy over PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet, is not supported by raw local evidence. It appears in `main.tex`, `appendix_tables.tex`, `APPROVED_RESULTS_SOURCE.tex`, and `generate_figures.py`, but those are typed manuscript or plotting sources, not experiment evidence.

2. The old PACS CDA claim, including \(89.1\) OOD and \(97.9\) in-domain accuracy, is also not supported as a final result. I found partial PACS local evidence, but not the exact complete source package needed to justify the old PACS table.

3. The old diagnostic figures are not evidence. `generate_figures.py` contains hard-coded arrays for the benchmark plot, flatness curves, loss-surface locations, checkpoint fluctuation, and certificate proxy bars.

4. Literature baseline rows such as ERM, SWAD, DiWA, and DomainBed-style baselines can be used only as cited literature comparisons. They are not reproduced CDA evidence.

5. The real local results are mostly PACS replay/search artifacts. Some old files use historical method labels from earlier project iterations; those labels should not become method names in the rewritten paper. The evidence is incomplete, sometimes unstable, and not matched to the old five-benchmark manuscript claim.

## Inventory

| ID | Old claim group | Main old locations | Available evidence | Status | Plain action |
|---|---|---|---|---|---|
| OLD-001 | CDA reaches \(68.3\) average OOD over five DomainBed benchmarks, with PACS \(89.1\), VLCS \(79.5\), OfficeHome \(72.9\), TerraIncognita \(52.3\), DomainNet \(47.8\). | `main.tex:113`, `main.tex:143-160`, `main.tex:845`, `appendix_tables.tex:66`, `APPROVED_RESULTS_SOURCE.tex:53`, `generate_figures.py:230-252` | Typed tables and hard-coded plot values. No matching raw runs found for all five datasets. | delete | Remove from rewritten paper until rerun under a documented protocol. |
| OLD-002 | Published/literature baseline rows in the five-benchmark table. | `main.tex:145-153`, `APPROVED_RESULTS_SOURCE.tex:21-53`, `appendix_tables.tex` | The note says all values except the final CDA row are copied from the SWAD table source. | literature-only | Keep only with exact citations and wording that says these are literature comparisons. |
| OLD-003 | CDA PACS per-domain row: A \(89.4\), C \(84.2\), P \(98.1\), S \(84.6\), average \(89.1\). | `appendix_tables.tex:41`, `APPROVED_RESULTS_SOURCE.tex:121` | Typed table row. Local PACS artifacts exist, but not a complete verified match to this row. | delete | Regenerate from all four PACS target domains and matched seeds. |
| OLD-004 | CDA PACS generalization table: OOD \(89.1\), in-domain \(97.9\). | `main.tex:688-710`, `APPROVED_RESULTS_SOURCE.tex:60-79` | Typed table row. No exact raw support for \(97.9\) found. | delete | Delete until exact OOD and in-domain metrics are regenerated. |
| OLD-005 | PACS env0 local replay summary using historical method labels, including a row labeled D-COLA with full \(0.8726\), in \(0.8737\), out \(0.8680\). | `claude_workspace/results/summary_detailed.csv` | Real CSV exists, but all rows are one PACS test environment, one seed, and `complete=False`. | verified | Use only as a pilot sanity check, not as a manuscript result or method name. |
| OLD-006 | Historical PACS art_painting tuning/search results, including peaks such as \(0.8887\), \(0.8843\), and related variants. | `claude_workspace/results/results_ledger.md:134-216`, `results_ledger.md:379-391`, `results_ledger.md:1493-1568` | Real ledger entries exist, but many are search/tuning results and not final matched-method evaluations. | verified | Use to design the final PACS package; do not quote as final headline evidence or introduce old method names. |
| OLD-007 | Version-space-only PACS coverage for art_painting, cartoon, sketch, and photo, including mean full around \(0.8843\). | `results_ledger.md:1626-1699` | Real ledger summary exists for all four PACS splits, but it is not yet converted into immutable result records with raw files, commands, hashes, and source-only proof. | provisional | Recover raw artifacts and rebuild as final evidence if the method is still the chosen method. |
| OLD-008 | Exact retained-family CDA objective runs underperforming graph-diffusion family. | `results_ledger.md:44-46` and related sections | Real ledger statement exists. It is a negative result and not part of the old headline table. | verified | Keep as an internal warning; include only if raw artifacts are recovered and the failure case matters. |
| OLD-009 | Selector bridge diagnostics: family size \(19.8\), disagreement mismatch \(4.7\%\), residual \(0.21\), proxy reduction \(0.19\). | `main.tex:351-366`, `generate_figures.py:171-173` | Marked with provisional macros and hard-coded in a figure. | delete | Regenerate from final selector outputs or cut. |
| OLD-010 | Method diagnostics: retained family size, entropy, proxy reduction, mergeability residual. | `main.tex:563-580` | Marked with provisional macros. No raw diagnostic source found. | delete | Regenerate from final diagnostics JSON. |
| OLD-011 | Post-hoc family comparison diagnostics against SWAD, DiWA, EoA, and CDA-BD. | `main.tex:662-684` | Mostly provisional values; baseline average accuracies are mixed with unverified diagnostics. | delete | Rebuild only after matched evidence exists. |
| OLD-012 | Component ablation table, including \(68.3\) for VSC+CDA-BD and multiple intermediate stacks. | `main.tex:747-767`, `appendix_tables.tex:52-66` | All old ablation values are provisional typed values. | delete | Rerun ablations from the final method and final checkpoint banks. |
| OLD-013 | Flatness, checkpoint fluctuation, and mechanism summary, including CDA-BD \(\mathcal{F}^{src}=1.09\), \(\mathcal{F}^{mix}=0.44\), OOD std. \(0.33\). | `main.tex:522-545`, `main.tex:774-791`, `appendix_tables.tex:75-89`, `generate_figures.py:255-289` | Provisional table values and hard-coded curves. | delete | Regenerate only after the accuracy package is fixed. |
| OLD-014 | Loss-surface visualization. | `main.tex:529-545`, `generate_figures.py:292-325` | Plot locations and surfaces are generated from synthetic formulas, not real loss grids. | delete | Replace with a real loss-surface script or cut. |
| OLD-015 | Checkpoint-selection fluctuation figure. | `main.tex:547-555`, `generate_figures.py:328-357` | Uses hard-coded sinusoidal series plus random noise. | delete | Replace with actual nearby-checkpoint replay measurements. |
| OLD-016 | Certificate proxy comparison figure. | `generate_figures.py:360-377` | Uses hard-coded arrays. | delete | Replace with artifact-derived certificate decomposition. |
| OLD-017 | ImageNet robustness table. | `main.tex:793-813` | Entire table is provisional and outside the core DG claim. | delete | Cut unless the core DG results are already complete and verified. |
| OLD-018 | Conceptual figures: CDA sampling overview, VSC mechanism, weighting mechanism. | `main.tex:286-288`, `main.tex:343-345`, `main.tex:436-438`, `generate_figures.py` | These are diagrams, not empirical evidence. | provisional | May be redrawn as conceptual diagrams, but captions must not imply measured results. |

## What Can Be Salvaged

- The old literature baseline rows can become cited comparison rows if every copied value is tied to the correct paper and table.
- The PACS local results can guide the first real experiment package.
- The existing result ledger is useful as a map of what was tried, including failures.
- The conceptual diagrams may be useful after rewriting, but they must be visually cleaner and clearly separated from measured evidence.

## What Must Not Be Reused

- No old CDA five-benchmark number should appear in the rewritten paper.
- No old CDA average, ablation, flatness, fluctuation, certificate, or ImageNet number should appear unless regenerated.
- No figure from `cda_final_v2/scripts/generate_figures.py` should be treated as evidence.
- The file name `APPROVED_RESULTS_SOURCE.tex` should not be trusted as proof. It is a polished table source, not raw experiment evidence.

## Next Practical Step

Build a small evidence table from the real PACS files first. The first useful target is:

1. PACS all four target domains.
2. One fixed checkpoint-bank protocol.
3. At least \(3\) seeds.
4. Exact source-only selection proof for each method.
5. Generated tables and figures only from raw result files.
