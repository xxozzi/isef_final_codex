# CDA Rewrite Finalization Plan

This is the sequential checklist for taking the current CDA draft from a verbose, provisional manuscript to a credible NeurIPS/ICML/ICLR-style submission with real results. It is intentionally task-based rather than a post-hoc standards checklist.

## Panel Round 1 Aggregate

Three reviewers inspected the current draft, local paper sources, and result ledgers.

- **Motivation reviewer:** The real paper is not “CDA discovers targets from source mixtures.” The defensible claim is that source-only post-hoc selection can be underidentified by scalar source validation, and domain-wise source-risk evidence can be used to make that deployment decision more informative.
- **Experimental reviewer:** The current empirical section is not publishable. Any result inside `\prov{}`, `\provnum{}`, or scripted figure values is fake until regenerated from raw artifacts. The first empirical task is artifact lineage, not writing.
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
- [x] Create a downloader script for arXiv PDFs and source bundles: `scripts/fetch_arxiv_sources.py`.
- [x] Download a local literature corpus covering SWA, DomainBed, SWAD, DiWA, MIRO, QRM, model soups, large-scale pretraining DG, DGSAM, GroupDRO, EoA, WDRDG, FAD, and WILDS.
- [x] Create a source-style audit script: `scripts/audit_literature_style.py`.
- [x] Generate `misc/literature_style_audit.md`.
- [x] Add a rewrite-local `.gitignore` for LaTeX build artifacts.
- [x] Create a `misc/panel_reviews/` folder for review records.

## Phase 0A: Modern Literature Refresh Before Narrative Freeze

- [x] Create `misc/modern_literature_refresh.md`.
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

- [ ] Make a complete inventory of every claimed number in `cda_final_v2/main.tex`.
- [ ] For each claimed number, record raw run directory, config, method, dataset, target domain, seed, checkpoint bank, commit hash, replay command, BN refresh mode, selected family, soup weights, diagnostics JSON, and metric source.
- [ ] Mark each number as `verified`, `literature-only`, `provisional`, or `delete`.
- [ ] Delete all claims that cannot be traced to raw artifacts.
- [ ] Create `misc/result_lineage_template.csv` with required columns.
- [ ] Create `misc/result_lineage.csv` populated for all existing usable artifacts.
- [ ] Write or adapt a parser that converts `results.jsonl`, replay manifests, and diagnostics JSON into a canonical results table.
- [ ] Add a hard scan for forbidden manuscript tokens: `\prov`, `\provnum`, `\provcaption`, `expected`, `placeholder`, `approved`, `fake`, `TBD`.
- [ ] Do not write the final results section until this audit is complete.

## Phase 2A: Build the Reproducibility Spine

- [x] Create `misc/result_registry.yml` as the registry location for planned tables, figures, metrics, and manuscript claims.
- [x] Create `misc/result_lineage_schema.md` defining required columns, primary keys, allowed values, and failure conditions.
- [x] Required lineage columns must include stable `run_id`, `artifact_id`, artifact hashes, source domains, split IDs, selector code path, selection inputs, selection artifact IDs, target-use flags, and artifact immutability.
- [x] Define an immutable artifact root with raw-versus-derived separation: `artifacts/raw_runs`, `artifacts/replays`, `artifacts/diagnostics`, `artifacts/tables`, and `artifacts/figures`.
- [x] Add a no-overwrite policy: every rerun creates a new `run_id`; every generated artifact creates a new `artifact_id`; final validators fail on duplicate primary keys or `immutable=false`.
- [x] Add source-only audit fields: `source_domains`, `target_domain`, `selection_inputs`, `selection_artifact_id`, `selector_code_path`, `target_labels_used`, `target_samples_used`, and `target_metadata_used`.
- [ ] Write `scripts/build_result_lineage.py` to populate `misc/result_lineage.csv` from raw `results.jsonl`, `replay_manifest.json`, diagnostics JSON, and generated CSV files.
- [ ] Write `scripts/validate_result_lineage.py` and make it fail if any final claim lacks raw artifacts, commit hash, command, seed, target domain, or source-only selection proof.
- [ ] Write `scripts/scan_manuscript_numbers.py` to scan `src/**/*.tex` and fail if any reported number lacks a matching `claim_id`.
- [ ] Write `scripts/aggregate_results.py` to compute mean, standard deviation, paired deltas, win/loss counts, and uncertainty convention from validated lineage only.
- [ ] Write `scripts/generate_tables.py` and `scripts/generate_figures.py` so every manuscript table and figure is generated from validated CSV/JSON artifacts.
- [ ] Forbid manual evidence sources: `.tex` tables, hard-coded Python arrays, poster figures, and prose notes may guide rewriting but cannot validate a result.
- [ ] Add a dry-run PACS env0 chain proving raw replay artifact \(\rightarrow\) lineage row \(\rightarrow\) table/figure \(\rightarrow\) manuscript claim.

## Phase 3: Decide the Real Experimental Scope

- [ ] Pick the minimum publishable claim after the artifact audit.
- [ ] If five-benchmark artifacts already exist and are reproducible, pursue the full DomainBed-style claim.
- [ ] If five-benchmark artifacts do not exist, make PACS the main mechanistic testbed and present broader benchmarks only after reruns finish.
- [ ] Freeze the method before final runs: selector, weighting rule, hyperparameters, BN refresh, checkpoint frequency, and seed protocol.
- [ ] Freeze baselines before final runs: `ERM`, `SWAD`, late-window uniform, best source-validation singleton, `VSC+uniform`, `CDA-Piv`, `CDA-BD`.
- [ ] Decide whether DiWA is reproduced under the same protocol or cited as literature-only. If literature-only, phrase comparisons accordingly.
- [ ] Decide whether EoA/model soups are reproduced or discussed only in related work.
- [ ] Cut ImageNet robustness unless core DG results are already complete.

## Phase 3A: Benchmark Scope Gate

- [ ] Define the minimum publishable package before final runs: PACS all four target domains, at least \(3\) seeds, fixed protocol, and all methods run from the same checkpoint-bank construction.
- [ ] Permit a five-benchmark headline only if PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet all have complete lineage for every reproduced method under matched seeds and matched source-only selection.
- [ ] If any benchmark is incomplete, remove the grand average and report the incomplete package only as future work or an appendix-in-progress item.
- [ ] Decide whether uncertainty is computed over seeds, domains, or seed-domain cells, and use the same convention in every table.
- [ ] Add paired comparisons against the strongest matched baseline, including per-split deltas and win/loss counts.
- [ ] State whether each comparison is reproduced, reanalyzed from public artifacts, or literature-only.

## Phase 4: Generate Real Result Packages

- [ ] Run the artifact-audited replay package on all existing checkpoint banks.
- [ ] Run PACS high-resolution tests on all four target domains.
- [ ] Use at least \(3\) seeds; use \(5\) seeds for PACS if compute permits.
- [ ] Run the canonical DomainBed package across PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet only after the PACS package is stable.
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

- [ ] Audit `domaingen/replay_methods.py` and confirm final method names exactly match manuscript methods: `late-window uniform`, `VSC+uniform`, `CDA-Piv`, and `CDA-BD`.
- [ ] Rename or wrap old `D-COLA` replay outputs so final artifacts use CDA terminology consistently without changing historical raw files.
- [ ] Add replay manifests that record environment, dependency versions, GPU/CPU device, data root, checkpoint list, BN refresh mode, and exact command.
- [ ] Add one dry-run replay on a PACS split that produces `results.jsonl`, diagnostics JSON, lineage CSV rows, a generated table, and a generated figure from the same artifacts.
- [ ] Fail the run package if any method uses target labels or target-domain validation during selection.

## Phase 5: Ablations and Diagnostics

- [ ] Run Priority A ablations:
  - [ ] best singleton versus late-window uniform versus `VSC+uniform` versus `VSC+CDA-BD`;
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
- [ ] Generate component ablation table.
- [ ] Generate source-average underidentification figure.
- [ ] Generate selector-weight heatmap.
- [ ] Generate certificate decomposition bar plot.
- [ ] Generate certificate-vs-OOD scatter.
- [ ] Generate mergeability plot comparing \(z(w)\) and \(L(\bar\theta(w))\).
- [ ] Generate source-mixture residual plot for \(\epsilon_{\mathrm{app}}\).
- [ ] Generate family-size/entropy scatter against OOD accuracy.
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
- [ ] Write `03_related_work.tex` from the downloaded corpus, web-checked current literature, and `misc/modern_literature_refresh.md`.
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
  - [ ] Every table is generated from validated lineage.
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
- [ ] Confirm every result has provenance.
- [ ] Confirm all results use target-domain-safe selection.
- [ ] Confirm all reported comparisons specify whether they are reproduced or literature-only.
- [ ] Confirm source files contain no provisional macros.
- [ ] Confirm the author block is professional and venue-appropriate.
- [ ] Run one final hostile review pass focused only on reviewer-2 objections.
- [ ] Produce the final PDF, source archive, and reproducibility bundle.
