# CDA Rewrite Finalization Plan

This is the sequential checklist for taking the current CDA draft from a verbose, provisional manuscript to a credible NeurIPS/ICML/ICLR-style submission with real results. It is intentionally task-based rather than a post-hoc standards checklist.

## Panel Round 1 Aggregate

Three reviewers inspected the current draft, local paper sources, and result ledgers.

- **Motivation reviewer:** The real paper is not “CDA discovers targets from source mixtures.” The defensible claim is that source-only post-hoc selection can be underidentified by scalar source validation, and domain-wise source-risk evidence can be used to make that deployment decision more informative.
- **Experimental reviewer:** The current empirical section is not publishable. Any result inside `\prov{}`, `\provnum{}`, or scripted figure values is fake until regenerated from raw artifacts. The first empirical task is result evidence, not writing.
- **Style reviewer:** The current paper reads like a proposal memo. It over-explains why statements matter, repeatedly says what CDA is not, embeds diagnostics in the method section, and uses theorem commentary where mature papers would use concise statements and ablations.

The plan below follows those verdicts.

## Panel Round 2 Aggregate

The second panel blocked manuscript drafting and identified the remaining gates.

- **Motivation gate:** The narrative must state the source-only scalar-selection bottleneck before CDA, then motivate domain-wise source-risk evidence through DomainBed, QRM, DRO/WDRDG, DGSAM-style domain-wise analysis, and post-hoc deployment practice.
- **Evidence gate:** Every manuscript number must map to raw artifacts through a stable claim ID; hard-coded Python arrays, `.tex` tables, poster figures, and polished notes are not evidence.
- **Style gate:** The skeleton must prevent the old explanatory voice from returning by encoding section-level acceptance criteria before prose is written.

No introduction, related work, or results prose should be drafted until these gates are closed.

## Phase 0: Workspace and Source Control

- [x] Create new rewrite directory: `claude_workspace/papers/cda_rewrite_v1/`.
- [x] Create `src/`, `literature/`, `scripts/`, and `misc/`.
- [x] Copy `neurips.sty` into `src/`.
- [x] Create modular LaTeX files in `src/`: `main.tex`, section files, appendix files, `packages.tex`, `macros.tex`, `theorems.tex`, and `references.bib`.
- [x] Record the planned paper skeleton, figure plan, and table plan in `misc/method/paper_skeleton.md`.
- [x] Create a downloader script for arXiv PDFs and source bundles: `scripts/fetch_arxiv_sources.py`.
- [x] Download a local literature corpus covering SWA, DomainBed, SWAD, DiWA, MIRO, QRM, model soups, large-scale pretraining DG, DGSAM, GroupDRO, EoA, WDRDG, FAD, and WILDS.
- [x] Create a source-style audit script: `scripts/audit_literature_style.py`.
- [x] Generate `misc/literature_notes/literature_style_audit.md`.
- [x] Organize `misc/` into searchable subfolders for method decisions, result tracking, evidence schemas, audits, literature notes, and reviewer records.
- [x] Add a rewrite-local `.gitignore` for LaTeX build artifacts.
- [x] Create a `misc/panel_reviews/` folder for review records.

## Phase 0A: Modern Literature Refresh Before Narrative Freeze

- [x] Create `misc/literature_notes/modern_literature_refresh.md`.
- [x] Build a literature matrix with columns: paper, year/status, problem setting, mechanism or assumption, relation to source mixtures, relation to checkpoint deployment, and implication for CDA novelty.
- [x] Include classical multi-source adaptation work that explicitly studies target mixtures of source distributions.
- [x] Include QRM/EQRM and current 2024--2026 critiques or boundary cases.
- [x] Include DRO, GroupDRO, WDRDG, MODE, and domain-uncertainty-set work.
- [x] Include flatness-aware DG through SWAD, FAD, DGSAM, and individual/domain-wise sharpness papers.
- [x] Include post-hoc averaging through SWA, model soups, EoA, DiWA, and linear-mode-connectivity-adjacent work.
- [x] Include pretraining-era DG through MIRO, CLIP/foundation-model DG, and ICLR 2025/2026 papers that question benchmark validity.
- [x] Include test-time or target-oriented DG only to define boundaries: if target samples, target descriptions, or test-time adaptation are used, the setting is not CDA's source-only deployment setting.
- [x] Mark invalid or partial style sources explicitly; `FAD` and `WILDS` cannot be used as writing-style evidence until usable paper prose is extracted.
- [x] Write a novelty constraint from the matrix: what CDA may claim, what it must cite as prior art, and what it must not imply.
- [x] Complete the matrix before freezing the narrative.
- [x] Keep `02_introduction.tex` and `03_related_work.tex` blocked until the matrix is complete.

## Phase 1: Freeze the Paper Narrative Before Writing

- [x] Create `narrative.md`.
- [x] Define the core claim:
  \[
  \text{source-only post-hoc selection under scalar underidentification}+\text{domain-wise source evidence}+\text{mergeable soups}.
  \]
- [x] Explicitly reject the false claim that CDA estimates the target domain.
- [x] Explicitly reject the false gap that prior work ignores source mixtures.
- [x] Explicitly reject the false implication that SWAD, DiWA, EoA, or model soups are inferior because they did not optimize source-domain composition robustness.
- [x] State the upstream problem before CDA: scalar source validation can underidentify source-only checkpoint selection.
- [x] State the general solution path before CDA: preserve and use domain-wise source-risk evidence.
- [x] Anchor the source-mixture assumption as a local candidate-family approximation:
  \[
  L_T(\theta)\le \alpha_T^\top L(\theta)+\epsilon_{\mathrm{app}},
  \qquad
  \alpha_T=\bar u+\delta,\quad
  \mathbf{1}^\top\delta=0,\quad
  \|\delta\|_2\le\rho.
  \]
- [x] Anchor the certificate target:
  \[
  \sup_{\alpha}\alpha^\top L(\theta)=\bar L(\theta)+\rho\|P_\perp L(\theta)\|_2.
  \]
- [x] Anchor the mergeability residual:
  \[
  M(w)=\|L(\bar\theta(w))-z(w)\|_2.
  \]
- [x] Run a second hostile motivation review after `narrative.md`, `finalization.md`, and `fixes.md` exist.
- [x] Revise `narrative.md` until reviewers agree the motivation is real and not HARKed from CDA.

## Phase 2: Artifact Audit Before Any Result Claim

- [x] Make a complete inventory of every empirical claim group in `cda_final_v2/main.tex`, `appendix_tables.tex`, the old notes, and the old figure script.
- [x] For each old claim group, record whether raw run directory, config, method, dataset, target domain, seed, checkpoint bank, commit hash, replay command, BN refresh mode, selected family, soup weights, diagnostics JSON, and metric source were found.
- [x] Mark each old claim group as `verified`, `literature-only`, `provisional`, or `delete`.
- [x] Save the audit in `misc/audits/old_results_audit.md`.
- [x] Save the machine-readable inventory in `misc/audits/old_result_inventory.csv`.
- [x] Create `misc/results/cda_results_tracking.md` from the current `results/results_ledger.md` CDA-relevant rows.
- [x] Create `misc/results/cda_results_tracking.csv` with current ledger-backed CDA-BD rows, benchmark templates, and ablation templates.
- [x] Record the PACS SWAD versus `VSC+CDA-BD` comparison as an accepted same-seed real result based on the ledger values and user confirmation.
- [x] Add `result_location` and `slurm_log_directory` fields to the CDA result tracker so future HPC paths can be filled in directly.
- [x] Remove SWAD and late-window uniform from the forward-looking fill-in benchmark table, and remove late-window uniform from the ablation templates.
<!-- Skipped 2026-04-30: do not delete historical unsupported claims because they live outside the rewrite folder and may remain as archive material. They still cannot be imported into `src/`, generated tables, generated figures, or final prose unless they receive validated evidence records. Original step: `Delete all claims that cannot be traced to raw artifacts.` -->
- [x] Create `misc/evidence/result_evidence_template.csv` with required columns.
- [x] Create the populated working result tracker for existing usable artifacts in `misc/results/cda_results_tracking.csv`; use this as the current human-readable evidence staging file.
<!-- Skipped 2026-04-30: do not block the rewrite on formal evidence-infrastructure scripts. Use `misc/results/cda_results_tracking.csv`, raw run directories, and result ledger entries as the practical result tracker until final result generation. Original step: `Write or adapt a parser that converts results.jsonl, replay manifests, diagnostics JSON, and misc/results/cda_results_tracking.csv into canonical misc/evidence/result_evidence.csv.` -->
<!-- Skipped 2026-04-30: postpone manuscript-token scanning until a real manuscript draft exists. Original step: `Add a hard scan for forbidden manuscript tokens: \prov, \provnum, \provcaption, expected, placeholder, approved, fake, TBD.` -->
<!-- Skipped 2026-04-30: replaced by the simpler practical rule that final results prose must use only real tracked results. Original step: `Do not write the final results section until this audit is complete.` -->

## Phase 2A: Build the Reproducibility Spine

- [x] Create `misc/results/result_registry.yml` as the registry location for planned tables, figures, metrics, and manuscript claims.
- [x] Create `misc/evidence/result_evidence_schema.md` defining required columns, primary keys, allowed values, and failure conditions.
- [x] Required evidence columns must include stable `run_id`, `artifact_id`, artifact hashes, source domains, split IDs, selector code path, selection inputs, selection artifact IDs, target-use flags, and artifact immutability.
- [x] Define an immutable artifact root with raw-versus-derived separation: `artifacts/raw_runs`, `artifacts/replays`, `artifacts/diagnostics`, `artifacts/tables`, and `artifacts/figures`.
- [x] Add a no-overwrite policy: every rerun creates a new `run_id`; every generated artifact creates a new `artifact_id`; final validators fail on duplicate primary keys or `immutable=false`.
- [x] Add source-only audit fields: `source_domains`, `target_domain`, `selection_inputs`, `selection_artifact_id`, `selector_code_path`, `target_labels_used`, `target_samples_used`, and `target_metadata_used`.
<!-- Skipped 2026-04-30: formal evidence-builder script is overkill before final runs. Keep raw artifacts and `misc/results/cda_results_tracking.csv` organized instead. Original step: `Write scripts/build_result_evidence.py to populate misc/evidence/result_evidence.csv from raw results.jsonl, replay_manifest.json, diagnostics JSON, and generated CSV files.` -->
<!-- Skipped 2026-04-30: formal validator is deferred. Final claims still need raw locations, commands, seeds, target domains, and source-only selection notes in the tracker. Original step: `Write scripts/validate_result_evidence.py and make it fail if any final claim lacks raw artifacts, commit hash, command, seed, target domain, or source-only selection proof.` -->
<!-- Skipped 2026-04-30: manuscript-number scanning only matters after a manuscript draft exists. Original step: `Write scripts/scan_manuscript_numbers.py to scan src/**/*.tex and fail if any reported number lacks a matching claim_id.` -->
<!-- Skipped 2026-04-30: aggregation can be done when final result CSVs exist. Original step: `Write scripts/aggregate_results.py to compute mean, standard deviation, paired deltas, win/loss counts, and uncertainty convention from validated evidence only.` -->
<!-- Skipped 2026-04-30: table and figure scripts should be written after final experiment outputs exist, not before. Original step: `Write scripts/generate_tables.py and scripts/generate_figures.py so every manuscript table and figure is generated from validated CSV/JSON artifacts.` -->
<!-- Skipped 2026-04-30: replaced by the simpler rule that tables, figures, and prose must cite real tracked results. Original step: `Forbid manual evidence sources: .tex tables, hard-coded Python arrays, poster figures, and prose notes may guide rewriting but cannot validate a result.` -->
<!-- Skipped 2026-04-30: dry-run evidence chain is not the current blocker. Original step: `Add a dry-run PACS env0 chain proving raw replay file -> evidence record -> table/figure -> manuscript claim.` -->

## Phase 3: Decide the Real Experimental Scope

- [x] Freeze the paper-facing CDA method identity:
  \[
  \text{CDA}=\text{VSC}+\text{CDA-BD}.
  \]
- [x] Record the final method in `misc/method/final_method.md`.
- [x] Map the paper method to implementation labels: `version_space_compression_selector__margin_eps_0p5_0p05` plus `blackwell_dual_target_weights__entropy_lambda_0p02`.
- [x] Set the publication target as the full DomainBed-style evaluation package, not a PACS-only fallback:
  \[
  \text{PACS}+\text{VLCS}+\text{OfficeHome}+\text{TerraIncognita}+\text{DomainNet}
  \]
  with CDA defined as \(\text{VSC}+\text{CDA-BD}\), plus the ablations and diagnostic figures planned below.
- [x] Treat five-benchmark DomainBed results as required for the paper, whether recovered from existing artifacts or produced by reruns.
<!-- Skipped 2026-04-30: PACS-only is no longer the paper scope. Original step: `If five-benchmark artifacts do not exist, make PACS the main mechanistic testbed and present broader benchmarks only after reruns finish.` -->
- [x] Use the best recorded CDA settings from `claude_workspace/results/results_ledger.md` for final runs, rather than reopening protocol selection:
  \[
  \text{selector}=\texttt{version\_space\_compression\_selector\_\_margin\_eps\_0p5\_0p05},
  \]
  \[
  \text{weigher}=\texttt{blackwell\_dual\_target\_weights\_\_entropy\_lambda\_0p02}.
  \]
  Use the same replay-bank construction and BN/evaluation settings that produced the accepted ledger results unless a benchmark requires a documented mechanical adaptation.
- [x] Use this final comparison set for the full DomainBed run package: ERM/ERM++, CORAL, SAM/DGSAM if available, SWAD, best source-validation singleton, `VSC+uniform`, `VSC+CDA-Piv`, `VSC+CDA-BD`, and CDA-on-base-method variants such as `CDA+ERM++`, `CDA+CORAL`, and `CDA+SAM` if those checkpoint banks are produced. Treat EoA-SMA/MA, DNA, and ERM++-MPA as optional same-budget additions only if they can be reproduced cleanly without delaying the core package.
- [x] Treat DiWA as related work/literature-only unless a later explicit decision adds a same-budget reproduction.
- [x] Treat full EoA and model soups as related work/literature-only because their standard setting uses multiple runs or multiple models.
- [x] Cut ImageNet robustness from the required paper package.

## Phase 3A: Benchmark Scope Gate

- [x] Create fill-in tracking rows for PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet target domains.
- [x] Define the minimum publishable package before final runs: PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet, at least \(3\) seeds where feasible, fixed protocol, and all methods run from the same checkpoint-bank construction.
- [x] Require the five-benchmark headline to cover PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet for every reproduced method under matched seeds and matched source-only selection.
- [x] If any required benchmark is incomplete, the paper is not publication-ready; do not downscope to a PACS-only main claim without an explicit later decision.
- [x] Use this uncertainty convention in every table: report per-target mean \(\pm\) standard deviation over seeds when seeds are available; report each dataset mean as the average of its target-domain means; report the final DomainBed average as the average of dataset means, not a pooled seed-domain-cell average.
- [x] Include paired deltas against the strongest matched reproduced baseline, with per-split deltas and win/loss counts in the main or appendix tables.
- [x] Label each comparison as reproduced, reanalyzed from public artifacts, or literature-only.

## Phase 4: Generate Real Result Packages

- [ ] Run the artifact-audited replay package on all existing checkpoint banks.
- [ ] Run high-resolution tests on all target domains for PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet.
- [ ] Use at least \(3\) seeds where feasible; use \(5\) seeds for PACS if compute permits.
- [ ] Run the canonical DomainBed package across PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet for the final method, matched baselines, and ablations.
- [ ] For each final method, record:
  \[
  \bar z(w),\quad
  \|P_\perp z(w)\|_2,\quad
  M(w),\quad
  H(w),\quad
  |\mathcal{S}|,\quad
  \epsilon_{\mathrm{app}},\quad
  \text{OOD accuracy}.
  \]
- [ ] Run BN refresh comparison: deterministic `eval_noaug` versus `train_aug`.
- [ ] Generate source-mixture residual diagnostics for each target split.
- [ ] Generate mergeability diagnostics for each deployed soup.
- [ ] Store every final run under a path that includes method, dataset, target domain, seed, and timestamp.
- [ ] Preserve replay commands in a machine-readable manifest.
- [ ] Summarize final results from raw artifacts only.

## Phase 4A: Replay Tooling Audit

- [ ] Audit `domaingen/replay_methods.py` and confirm final method names exactly match manuscript methods: `VSC+uniform`, `CDA-Piv`, and `CDA-BD`.
- [ ] Use old replay outputs only if they exactly match the final CDA method definition; otherwise exclude them from final result evidence.
- [ ] Add replay manifests that record environment, dependency versions, GPU/CPU device, data root, checkpoint list, BN refresh mode, and exact command.
- [ ] Add one dry-run replay on a PACS split that produces `results.jsonl`, diagnostics JSON, evidence CSV rows, a generated table, and a generated figure from the same artifacts.
- [ ] Fail the run package if any method uses target labels or target-domain validation during selection.

## Phase 5: Ablations and Diagnostics

- [x] Create blank tracking rows for main stack ablations, VSC tolerance ablations, entropy ablation, and BN-refresh ablations.
- [ ] Run Priority A ablations:
  - [ ] best singleton versus `VSC+uniform` versus `VSC+CDA-BD`;
  - [ ] `VSC+uniform` versus `VSC+CDA-Piv` versus `VSC+CDA-BD`;
  - [ ] fixed selector with varied weights;
  - [ ] fixed weighting with varied selectors;
  - [ ] BN refresh mode.
- [ ] Run Priority B ablations:
  - [ ] selector tolerance \(\gamma\in\{0.4,0.5,0.6\}\);
  - [ ] VSC tolerance \(\varepsilon_{\mathrm{vsc}}\in\{0.02,0.05,0.10\}\);
  - [ ] entropy \(\lambda_{\mathrm{ent}}\in\{0,0.005,0.02,0.05\}\);
  - [ ] singleton-family safety tests.
- [ ] Run Priority C diagnostics only after accuracy stabilizes:
  - [ ] loss-surface visualization;
  - [ ] local flatness;
  - [ ] certificate proxy decomposition;
  - [ ] checkpoint-selection sensitivity.
- [ ] Add a source-average underidentification diagnostic: find checkpoint/soup candidates with similar aggregate source validation but different domain-wise source-risk vectors and different OOD outcomes.
- [ ] Add at least one failure case where the source-mixture residual is large and CDA does not help.
- [ ] Pair every diagnostic figure with one quantitative table or CSV source.

## Phase 6: Figure and Table Generation

- [ ] Remove all current scripted illustrative figures from evidence status.
- [ ] Rebuild figure scripts so every plotted value comes from raw result artifacts.
- [ ] Generate main benchmark table with mean \(\pm\) standard deviation.
- [ ] Generate PACS per-domain table.
- [ ] Generate CDA-on-base-method table for ERM++, CORAL, SAM/DGSAM if available, and any other stable checkpoint-bank producer.
- [ ] Generate component ablation table.
- [ ] Generate Figure 1: source-evidence underidentification, including \(\bar L\) versus \(\|P_\perp L\|_2\) and certificate contours.
- [ ] Generate Figure 2: CDA selection geometry, including VSC-retained family, CDA-BD weights, final soup, and checkpoint-step inset.
- [ ] Generate Figure 3: domain-risk cancellation diagram for nontrivially weighted CDA-BD checkpoints.
- [ ] Generate Figure 4: local deployment geometry, including source-loss contour plot and flatness-versus-radius curves for representative single-run models by role, not only SWAD.
- [ ] Generate Figure 5: assumption audit comparing \(z(w)\), \(L(\bar\theta(w))\), \(M(w)\), and \(\epsilon_{\mathrm{app}}\) for CDA variants and CDA-on-base-method variants.
- [ ] Generate optional appendix figures only if nonredundant: source-risk heatmap, prediction-diversity map, BN refresh sensitivity, and per-seed uncertainty.
- [ ] Export every final figure as `.pdf`, `.png`, and `.svg`.
- [ ] Visually inspect every PDF figure in the compiled manuscript.

## Phase 6A: Evidence-Generated Tables and Figures

- [ ] Replace all hard-coded plotting arrays with loaders from validated CSV/JSON artifacts.
- [ ] Make every generated table include a footer or sidecar metadata file listing source artifact IDs.
- [ ] Fail figure generation if any plotted value is typed directly into the plotting script.
- [ ] Archive generated tables as `.csv`, `.tex`, and `.md`.
- [ ] The manuscript may only `\input{}` generated `.tex` tables; it may not contain manually typed result tables.

## Phase 7: Rewrite the Paper From Scratch

- [ ] Do not edit the old `cda_final_v2/main.tex` into shape. Use it only as source material.
- [ ] Write `02_introduction.tex` only after the modern literature matrix and narrative review are approved.
- [ ] Introduction acceptance criteria:
  - [ ] \(5\)--\(7\) paragraphs maximum.
  - [ ] Paragraph 1 states the modern DG evaluation problem without generic examples.
  - [ ] Paragraph 2 introduces post-hoc checkpoint deployment from a fixed bank.
  - [ ] Paragraph 3 states the non-CDA problem: scalar source validation can underidentify the choice among checkpoint candidates.
  - [ ] Paragraph 4 motivates domain-wise source-risk vectors from DomainBed, QRM, DRO/WDRDG, DGSAM-style domain-wise analysis, and post-hoc deployment practice before CDA is named.
  - [ ] Paragraph 5 states source-domain composition robustness as one conditional scalarization of that vector, then introduces the local source-mixture certificate and mergeability issue.
  - [ ] Paragraph 6 gives CDA and contributions.
  - [ ] No paragraph says what CDA is "not" unless defining scope in one sentence.
- [ ] Write `03_related_work.tex` from the downloaded corpus, web-checked current literature, and `misc/literature_notes/modern_literature_refresh.md`.
- [ ] Related work acceptance criteria:
  - [ ] Organize by mechanism, not chronology.
  - [ ] Explicitly cite multi-source adaptation, QRM/EQRM, DRO/WDRDG, DomainBed, SWAD, DiWA, EoA, model soups, MIRO, DGSAM, and pretraining-era DG.
  - [ ] End each paragraph with the exact boundary CDA occupies.
  - [ ] Do not claim prior work ignores mixtures, robustness, flatness, or averaging.
- [ ] Write `04_problem_certificate.tex` with only notation, assumptions, theorem statements, and compact interpretation.
- [ ] Problem/certificate acceptance criteria:
  - [ ] State \(L_T(\theta)\le \alpha_T^\top L(\theta)+\epsilon_{\mathrm{app}}\) as a candidate-family approximation.
  - [ ] State \(\sup_\alpha \alpha^\top L(\theta)=\bar L(\theta)+\rho\|P_\perp L(\theta)\|_2\).
  - [ ] Define \(M(w)=\|L(\bar\theta(w))-z(w)\|_2\).
  - [ ] Put all proofs and derivation commentary in the appendix.
- [ ] Move all proofs to `appendix_proofs.tex`.
- [ ] Write `05_method.tex` as an algorithm definition section, not an evidence section.
- [ ] Method acceptance criteria:
  - [ ] Inputs, retained-family rule, weighting objective, constraints, and deployment object are specified.
  - [ ] Hyperparameters are listed but not justified with prose speculation.
  - [ ] Complexity and implementation details are concise.
- [ ] Write `06_experiments.tex` only after real generated tables exist.
- [ ] Experiments acceptance criteria:
  - [ ] Every table is generated from validated evidence.
  - [ ] Every comparison states reproduced versus literature-only.
  - [ ] Every uncertainty statistic defines its aggregation unit.
- [ ] Write `07_analysis_ablations.tex` only after real diagnostics exist.
- [ ] Analysis acceptance criteria:
  - [ ] Include selector/weight ablations, source-average underidentification, source-mixture residuals, mergeability, and at least one failure case.
  - [ ] Do not use conceptual diagrams as evidence.
- [ ] Write `08_limitations.tex` plainly and briefly.
- [ ] Write `09_conclusion.tex` as one paragraph.
- [ ] Write the abstract last.
- [ ] Keep main text concise enough for conference-page constraints.

## Phase 8: Professionalize the Writing

- [ ] Remove all negative framing of the form “CDA does not...”.
- [ ] Remove all phrases like “matters because,” “this is why,” “the claim is,” “not merely,” “primitive object,” and “should be read as.”
- [ ] Replace self-explaining theorem prose with direct mathematical statements.
- [ ] Limit each paragraph to one claim.
- [ ] Move every derivation that does not affect the method into the appendix.
- [ ] Keep captions descriptive rather than argumentative.
- [ ] Ensure related work positions CDA by mechanism and evidence, not by saying what other methods fail to do.
- [ ] Keep limitations concrete and non-defensive.
- [ ] Ensure no fake/provisional result mechanism exists in `src/`.

## Phase 9: Review Panels and Revision Gates

- [x] Complete first panel: motivation, experiments, style.
- [x] Complete second panel after initial plan files are written:
  - [x] motivation reviewer checks `narrative.md`;
  - [x] experimental reviewer checks `finalization.md`;
  - [x] editor reviewer checks `fixes.md` and `src/` organization.
- [x] Revise all planning files from second-panel feedback.
- [x] Complete third/narrow re-review after motivation and reproducibility revisions.
- [x] Complete motivation-update council after replacing the circular source-reweighting motivation with scalar source-validation underidentification.
- [ ] Complete third panel after real result tables exist.
- [ ] Complete fourth panel after full paper draft exists.
- [ ] Require unanimous approval before treating the narrative as frozen.
- [ ] Preserve reviewer objections in `misc/panel_reviews/`.

## Phase 10: Submission Readiness

- [ ] Compile draft with `pdflatex` or `latexmk`.
- [ ] Fix all warnings that affect references, citations, floats, fonts, or overfull boxes.
- [ ] Confirm all citations resolve.
- [ ] Confirm all figures are readable in grayscale and color.
- [ ] Confirm every result has source files and evidence records.
- [ ] Confirm all results use target-domain-safe selection.
- [ ] Confirm all reported comparisons specify whether they are reproduced or literature-only.
- [ ] Confirm source files contain no provisional macros.
- [ ] Confirm the author block is professional and venue-appropriate.
- [ ] Run one final hostile review pass focused only on reviewer-2 objections.
- [ ] Produce the final PDF, source archive, and reproducibility bundle.
