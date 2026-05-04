# CDA Paper Plan

This file is the working plan. It supersedes `finalization.md` for day-to-day execution.

Final paper method:

\[
\mathrm{CDA}=\mathrm{VSC}+\mathrm{CDA\text{-}BD}.
\]

Implementation labels:

- selector: `version_space_compression_selector__margin_eps_0p5_0p05`
- weights: `blackwell_dual_target_weights__entropy_lambda_0p02`

## Current Execution Status (2026-05-03)

- [x] Non-DomainNet checkpoint banks appear complete from the latest collapsed Slurm/job-status output: `PACS`, `VLCS`, `OfficeHome`, and `TerraIncognita` across `ERM`, `ERMPlusPlus`, `CORAL`, `SAM`, and `DGSAM`, with \(3\) seeds per split.
- [ ] Export and archive the latest collapsed bank-status table as the evidence artifact before treating the non-DomainNet bank layer as paper-frozen.
- [ ] DomainNet bank generation is now being relaunched intentionally, despite the compute cost. Relaunch policy: all \(90\) DomainNet bank configs run with `DOMAINGEN_RESUME=1`, so timed-out or in-flight-cancelled runs continue from the latest dense checkpoint and queued-cancelled runs start from step \(0\).
- [ ] Implement the final-only `VSC+CDA-BD` runner before launching CDA over the completed banks. The current broad selector/weight sweep machinery is too expensive for the frozen final method.

## 1. Generate Checkpoint Banks

- [x] Port the DomainBed dataset downloader and DomainNet duplicate list into `domaingen`.
- [x] Install the remaining DomainBed datasets on the HPC: `VLCS`, `OfficeHome`, `TerraIncognita`, and `DomainNet`.
- [x] Verify the full data root with `python -m domaingen.download_data --dataset all --verify_only`.
- [ ] Generate checkpoint banks for every leave-one-domain-out split in DomainBed:
  - [x] PACS: `A`, `C`, `P`, `S`
  - [x] VLCS: `C`, `L`, `S`, `V`
  - [x] OfficeHome: `A`, `C`, `P`, `R`
  - [x] TerraIncognita: `L100`, `L38`, `L43`, `L46`
  - [ ] DomainNet: `clip`, `info`, `paint`, `quick`, `real`, `sketch`
- [x] For each non-DomainNet target split, generate ERM checkpoint banks with \(3\) seeds.
- [x] For each non-DomainNet target split, generate ERM++ checkpoint banks with \(3\) seeds.
- [x] For each non-DomainNet target split, generate CORAL checkpoint banks with \(3\) seeds.
- [x] For each non-DomainNet target split, generate SAM checkpoint banks with \(3\) seeds.
- [x] For each non-DomainNet target split, generate DGSAM checkpoint banks with \(3\) seeds.
- [ ] Relaunch/resume DomainNet checkpoint banks with \(3\) seeds for all five bank producers using `DOMAINGEN_RESUME=1` and a small active-job cap.
- [x] Implement train-time `SAM` and `DGSAM` in `domaingen`.
- [x] Implement `ERMPlusPlus` in `domaingen` with linear-head warmup and simple model-parameter averaging.
- [ ] Decide whether the paper needs exact published ERM++ reproduction with the official AugMix/timm initialization, or whether `ERMPlusPlus` is only a same-backbone checkpoint-bank producer for CDA analysis.
- [x] Generate the full DomainBed bank config grid for `ERM`, `ERMPlusPlus`, `CORAL`, `SAM`, and `DGSAM`.
- [x] Validate all `330` generated bank configs with `python domaingen/scripts/validate_cda_domainbed_configs.py`.
- [x] Replace the old PACS dense-replay settings with paper-backed bank settings: per-domain batch size \(32\), \(5000\)-step non-DomainNet runs, \(15000\)-step DomainNet runs, checkpoint/evaluation frequency \(25\) for non-DomainNet and \(50\) for DomainNet, ERM++ loop overrides, and DGSAM dataset-specific table overrides.
- [x] Submit the PACS bank smoke batch: `60` Slurm jobs, IDs `149170`--`149229`.
- [x] Record the PACS bank submission batch in `domaingen/configs/generated/cda_domainbed_v1/bank_run_tracking.md`.
- [x] Monitor PACS bank jobs to completion and mark finished rows as `complete` after checking Slurm state and output `done` markers.
- [x] Resume and complete failed/timed-out non-DomainNet bank jobs from latest available checkpoints after the initial Slurm failures, timeouts, and cancellations.
- [ ] Export the latest collapsed non-DomainNet bank status table and archive it as completion evidence.
- [ ] Use the existing best replay-bank settings from `claude_workspace/results/results_ledger.md` unless a run fails mechanically.
- [ ] Use saved checkpoints for CDA replay. Current train-bank configs save/evaluate every `25` steps for non-DomainNet datasets and every `50` steps for `DomainNet`.
- [ ] Track every completed bank in `misc/results/cda_results_tracking.csv`.

Initial PACS launch grid used as the smoke batch:

\[
4\ \text{target splits}\times 3\ \text{seeds}\times 5\ \text{bank producers}
=60\ \text{checkpoint banks}.
\]

Current completed non-DomainNet bank scope:

\[
16\ \text{target splits}\times 3\ \text{seeds}\times 5\ \text{bank producers}
=240\ \text{checkpoint banks}.
\]

Full generated DomainBed target grid:

\[
22\ \text{target splits}\times 3\ \text{seeds}\times 5\ \text{bank producers}
=330\ \text{checkpoint banks}.
\]

## 2. Run CDA and Baselines

### 2.0 Required Implementation Correction: Final-Only CDA Runner

The current codebase can produce the final method, but the available sweep-oriented runner is the wrong execution path for paper-scale runs. `selector_weight_cross_sweep.py` and the related selector/weight sweep scripts were built to compare many selector families, many weighting rules, support augmentations, mergeability barriers, and evaluation variants. That is useful for method discovery, but it is badly mismatched to the frozen paper method:

\[
\mathrm{CDA}=\mathrm{VSC}+\mathrm{CDA\text{-}BD}.
\]

For the final method, the required work is much smaller and more specific:

1. Evaluate all \(N\) checkpoints on the support set \(S\) for VSC selection.
2. Select \(K\) checkpoints.
3. Evaluate only those \(K\) selected checkpoints on source-heldout domains \(H\) for CDA-BD weighting.
4. Average the selected checkpoints using `blackwell_dual_target_weights__entropy_lambda_0p02`.
5. Evaluate the final averaged model.

So the intended final-only image-evaluation count is approximately:

\[
F_{\mathrm{final\text{-}only}} = NS + KH + 2G,
\]

where \(N\) is the dense checkpoint count, \(K\) is the selected family size, \(S\) is the support subset, \(H\) is the total source-heldout image count, and \(G\) is the target-domain image count. The current sweep path behaves closer to:

\[
F_{\mathrm{sweep}} \approx N(6S + 2V) + H(1.5K^2 + 7.5K - 5) + 4G,
\]

where \(V\) is the remaining validation pool. That extra cost comes from running broad selector diagnostics, multiple support augmentation variants, anchor/neighbor checks, pairwise mergeability-style barriers, a whole library of weight rules, and final/all-target evaluation variants. With \(N=200\), \(K=20\), and the current `freeze_bn: true` configs, the final-only path is roughly an order of magnitude cheaper on PACS/VLCS/OfficeHome/TerraIncognita and far more important for DomainNet.

| Dataset | Final-only evals per target | Current sweep-style evals per target | Approx. reduction |
|---|---:|---:|---:|
| PACS | \(244{,}769\) | \(2{,}565{,}145\) | \(10.5\times\) |
| VLCS | \(262{,}952\) | \(2{,}755{,}035\) | \(10.5\times\) |
| OfficeHome | \(381{,}958\) | \(4{,}002{,}427\) | \(10.5\times\) |
| TerraIncognita | \(607{,}358\) | \(6{,}364{,}527\) | \(10.5\times\) |
| DomainNet | \(3{,}379{,}575\) | \(117{,}244{,}313\) | \(34.7\times\) |

- [ ] Block broad CDA benchmark launches through `selector_weight_cross_sweep.py` unless the goal is explicitly exploratory ablation, not final paper evaluation.
- [x] Implement a final-only runner, `domaingen/experimentation/final_vsc_cda_bd.py`, that performs the intended \(NS + KH + 2G\)-style work for one bank and one target split.
- [x] Add a one-bank Slurm submission wrapper for the final-only runner: `domaingen/scripts/submit_final_vsc_cda_bd.sh`.
- [ ] Validate the final-only runner on one PACS bank.
- [ ] Validate the final-only runner on one larger non-DomainNet bank, preferably OfficeHome or TerraIncognita, before broad launch.
- [ ] Recompute the final CDA tables from the final-only runner outputs, not from exploratory sweep outputs.

#### Final-only CDA execution memo (2026-05-03)

Use `final_vsc_cda_bd.py` for the frozen paper method. Do not use `selector_weight_cross_sweep.py` for main CDA numbers unless the run is explicitly an exploratory ablation.

The runner freezes:

- selector: `version_space_compression_selector__margin_eps_0p5_0p05`
- weights: `blackwell_dual_target_weights__entropy_lambda_0p02`

It writes `final_result.json`, `leaderboard.csv`, `selected_family.json`, `weights.json`, `scheme_results.jsonl`, and `final_vsc_cda_bd.pkl` under the chosen output directory.

Single-bank interactive smoke command:

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
eval "$(conda shell.bash hook)"
conda activate research

export DOMAINGEN_WORK_ROOT=/project/jje239_dgxpublicai25/jwje228/work
export DOMAINGEN_REPO_ROOT="$DOMAINGEN_WORK_ROOT/domaingen"
export DOMAINGEN_RESULTS_ROOT="$DOMAINGEN_WORK_ROOT/results"
export DOMAINGEN_SLURM_LOG_ROOT="$DOMAINGEN_WORK_ROOT/slurm_output"

python -u -m domaingen.experimentation.final_vsc_cda_bd \
  --run_dir "$DOMAINGEN_RESULTS_ROOT/cda_domainbed_v1/banks/ERM/PACS/A/seed_0" \
  --output_dir "$DOMAINGEN_RESULTS_ROOT/cda_domainbed_v1/final_cda/ERM/PACS/A/seed_0" \
  --set dcola_deterministic_bn_refresh=true \
  --set dcola_bn_refresh_view=eval_noaug \
  --set dcola_bn_refresh_seed=0 \
  --set dcola_bn_refresh_num_workers=0 \
  --resume
```

Single-bank Slurm smoke command:

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
export DOMAINGEN_WORK_ROOT=/project/jje239_dgxpublicai25/jwje228/work
export DOMAINGEN_REPO_ROOT="$DOMAINGEN_WORK_ROOT/domaingen"
export DOMAINGEN_RESULTS_ROOT="$DOMAINGEN_WORK_ROOT/results"
export DOMAINGEN_SLURM_LOG_ROOT="$DOMAINGEN_WORK_ROOT/slurm_output"

bash domaingen/scripts/submit_final_vsc_cda_bd.sh \
  "$DOMAINGEN_RESULTS_ROOT/cda_domainbed_v1/banks/ERM/PACS/A/seed_0"
```

After the PACS smoke and one larger smoke pass, submit completed non-DomainNet banks with an active-job cap:

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
export DOMAINGEN_WORK_ROOT=/project/jje239_dgxpublicai25/jwje228/work
export DOMAINGEN_REPO_ROOT="$DOMAINGEN_WORK_ROOT/domaingen"
export DOMAINGEN_RESULTS_ROOT="$DOMAINGEN_WORK_ROOT/results"
export DOMAINGEN_SLURM_LOG_ROOT="$DOMAINGEN_WORK_ROOT/slurm_output"
export MAX_ACTIVE_CDA_FINAL=8

python - <<'PY' > /tmp/cda_final_non_domainnet.tsv
import csv
import os

work_root = os.environ["DOMAINGEN_WORK_ROOT"]
results_root = os.environ["DOMAINGEN_RESULTS_ROOT"]
manifest = os.path.join(work_root, "domaingen/configs/generated/cda_domainbed_v1/bank_manifest.csv")

with open(manifest, newline="") as handle:
    for row in csv.DictReader(handle):
        if row["dataset"] == "DomainNet":
            continue
        run_dir = row["output_dir"]
        if not os.path.exists(os.path.join(run_dir, "done")):
            continue
        output_dir = os.path.join(
            results_root,
            "cda_domainbed_v1/final_cda",
            row["algorithm"],
            row["dataset"],
            row["target_env"],
            f"seed_{row['seed']}",
        )
        if os.path.exists(os.path.join(output_dir, "final_result.json")):
            continue
        print(f"{run_dir}\t{output_dir}")
PY

while IFS=$'\t' read -r run_dir output_dir; do
  while [ "$(squeue -h -u "$USER" -n final_cda | wc -l)" -ge "$MAX_ACTIVE_CDA_FINAL" ]; do
    sleep 60
  done
  bash domaingen/scripts/submit_final_vsc_cda_bd.sh "$run_dir" "$output_dir"
done < /tmp/cda_final_non_domainnet.tsv
```

For all \(330\) banks after DomainNet finishes, use the same command but remove the `if row["dataset"] == "DomainNet": continue` filter.

- [ ] On every completed non-DomainNet ERM bank, run:
  - [ ] final checkpoint
  - [ ] best source-validation singleton
  - [ ] SWAD
  - [ ] `VSC+uniform`
  - [ ] `VSC+CDA-Piv`
  - [ ] `VSC+CDA-BD`
- [ ] On every completed non-DomainNet ERM++ bank, run:
  - [ ] final checkpoint
  - [ ] best source-validation singleton
  - [ ] `VSC+uniform`
  - [ ] `VSC+CDA-BD`
- [ ] On every completed non-DomainNet CORAL bank, run:
  - [ ] final checkpoint
  - [ ] best source-validation singleton
  - [ ] `VSC+uniform`
  - [ ] `VSC+CDA-BD`
- [ ] On every completed non-DomainNet SAM/DGSAM bank, run:
  - [ ] final checkpoint
  - [ ] best source-validation singleton
  - [ ] `VSC+uniform`
  - [ ] `VSC+CDA-BD`
- [ ] If reporting official SWAD, run it with its actual online dense averaging behavior. If using saved checkpoints only, label it as SWAD replay.
- [ ] Record per-target accuracy, per-dataset mean, DomainBed mean, and paired deltas against the strongest matched reproduced baseline.

## 3. Run Ablations

- [ ] Component ablation:
  - [ ] best singleton
  - [ ] `VSC+uniform`
  - [ ] `VSC+CDA-Piv`
  - [ ] `VSC+CDA-BD`
- [ ] Selector ablation:
  - [ ] fixed `CDA-BD` weights with alternate retained families
  - [ ] full-bank uniform versus VSC-retained uniform
  - [ ] singleton-family safety checks
- [ ] Weight ablation:
  - [ ] fixed VSC family with uniform weights
  - [ ] fixed VSC family with `CDA-Piv`
  - [ ] fixed VSC family with `CDA-BD`
  - [ ] entropy setting sweep for \(\lambda_{\mathrm{ent}}\)
- [ ] Sensitivity checks:
  - [ ] VSC tolerance sweep
  - [ ] BN refresh mode: deterministic `eval_noaug` versus `train_aug`
  - [ ] checkpoint-bank density if the result is suspicious
- [ ] Failure analysis:
  - [ ] find at least one split where CDA does not help
  - [ ] show whether the failure matches a large mergeability or source-mixture residual

## 4. Generate Tables

- [ ] Main DomainBed table: reproduced single-run baselines first, CDA rows last.
- [ ] Per-dataset target-domain table for PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet.
- [ ] CDA-on-base-method table: ERM, ERM++, CORAL, SAM, and DGSAM banks before and after CDA.
- [ ] Ablation table for selector, weighting, BN refresh, and sensitivity checks.
- [ ] Appendix raw-result table with target split, seed, bank producer, method, and accuracy.
- [ ] Do not use benchmark bar charts. Benchmark numbers belong in tables.

## 5. Generate Figures

Goal: make the figures show what is unusual about CDA, not just that it adds another row to DomainBed. The main-paper visual story is:

\[
\text{source-average underidentification}
\rightarrow
\text{domain-wise source evidence}
\rightarrow
\text{mergeable weighted deployment}
\rightarrow
\text{audited limitations}.
\]

### 5.1 Main-Paper Figure Set

- [ ] Figure 1: source-average underidentification.
  - Purpose: show why source validation alone is not enough.
  - Plot: a compact two-panel motivation figure. Panel A shows two candidates with similar average source risk \(\bar L\) but different source-risk vectors \(L(\theta)\). Panel B plots candidates by \(\bar L(\theta)\) and \(\|P_\perp L(\theta)\|_2\), with contours of
    \[
    \bar L(\theta)+\rho\|P_\perp L(\theta)\|_2.
    \]
  - Highlight: final checkpoint, best source-validation singleton, `VSC+uniform`, and `VSC+CDA-BD`.
  - Message: two checkpoints can look nearly identical under \(\bar L\) while encoding meaningfully different domain-risk profiles.

- [ ] Figure 2: CDA selection geometry.
  - Purpose: show how CDA moves from a checkpoint bank to a deployed weighted family.
  - Plot: centered source-risk vectors \(P_\perp L(\theta)\), projected into \(2\) dimensions with PCA or a fixed simplex view.
  - Highlight: all \(N\) checkpoints in gray, the selected \(K\)-checkpoint VSC family in color, point size proportional to `CDA-BD` weight, and the final averaged model.
  - Inset: checkpoint step versus `CDA-BD` weight mass, plus effective family size
    \[
    K_{\mathrm{eff}}=\frac{1}{\sum_i w_i^2}.
    \]
  - Message: CDA is not averaging arbitrary checkpoints; it compresses the bank to a source-compatible family and then assigns nonuniform weights inside that family.

- [ ] Figure 3: domain-risk cancellation.
  - Purpose: show the unique weighting mechanism of `CDA-BD`.
  - Plot: per-source-domain centered risk residuals before and after weighting.
  - Possible formats: residual heatmap, signed bar chart, or vector-sum diagram.
  - Message: `CDA-BD` does not only prefer low-risk checkpoints; it combines checkpoints whose domain-wise deviations cancel.

- [ ] Figure 4: local deployment and mergeability geometry.
  - Purpose: test whether CDA lands in a stable, mergeable region rather than merely finding a lucky high-accuracy endpoint.
  - Plot: source-loss contour plot around representative deployed models, paired with flatness-versus-radius curves
    \[
    \Delta_r(\theta)=\mathbb{E}_{\|\delta\|=r}\left[L(\theta+\delta)-L(\theta)\right].
    \]
  - Compare: final checkpoint or ERM++, SWAD or another single-run averaging reference, `VSC+uniform`, `VSC+CDA-Piv`, and `VSC+CDA-BD`.
  - Message: CDA should be credible as a weight-space soup only when the selected family is locally stable enough for source-loss-vector arithmetic to remain meaningful.

- [ ] Figure 5: assumption audit and failure anatomy.
  - Purpose: test the core approximation behind post-hoc weight optimization.
  - Plot: predicted mixture risk
    \[
    z(w)=\sum_i w_iL(\theta_i)
    \]
    against measured soup risk
    \[
    L(\bar\theta(w)).
    \]
  - Report:
    \[
    M(w)=\|L(\bar\theta(w))-z(w)\|_2,
    \qquad
    \epsilon_{\mathrm{app}}.
    \]
  - Include: one split where CDA helps and one split where CDA does not help.
  - Message: CDA is strongest when the linearized source-risk prediction is faithful enough after averaging; when \(M(w)\) or \(\epsilon_{\mathrm{app}}\) is large, the failure is expected rather than mysterious.

### 5.2 Appendix / Diagnostic Figure Candidates

- [ ] Appendix figure: accuracy-versus-compute frontier.
  - Plot: target accuracy or mean delta versus image-evaluation count for best singleton, `VSC+uniform`, final-only `VSC+CDA-BD`, and the old sweep-style execution path.
  - Use to justify the final-only runner and explain why DomainNet is paused, not to support the main scientific claim.

- [ ] Appendix figure: \(K\)-sensitivity curve.
  - Plot: target accuracy, source-heldout risk, and \(K_{\mathrm{eff}}\) as selected family size \(K\) changes.
  - Use to show whether the method is robust or tuned to a single lucky \(K\).

- [ ] Appendix figure: support-size sensitivity.
  - Plot: final accuracy and selected-family stability as support size \(S\) changes.
  - Use to show how much target-support information CDA needs.

- [ ] Appendix figure: base-method consistency.
  - Plot: paired deltas for `ERM`, `ERMPlusPlus`, `CORAL`, `SAM`, and `DGSAM`.
  - Use a paired dot/slope plot rather than a benchmark bar chart.
  - Use to show CDA is a post-hoc layer over multiple bank producers, not a one-off ERM trick.

- [ ] Appendix figure: extended failure-case gallery.
  - Plot: additional splits where CDA does not help, including selected family, weights, mergeability residual, and target result.
  - Include only if Figure 5 needs more evidence to make the limitation concrete.

- [ ] Appendix figure: selected-family overlap across seeds.
  - Plot: overlap or Jaccard similarity of selected checkpoint steps across seeds for the same target split.
  - Use to show whether CDA is selecting a stable region of training or chasing seed-specific noise.

- [ ] Appendix figure: prediction-diversity map.
  - Plot: pairwise disagreement or prediction diversity among selected checkpoints versus the full bank.
  - Include only if it adds information beyond Figure 2 and Figure 3.

- [ ] Appendix figure: checkpoint timeline and selected-family behavior.
  - Plot: training step versus source validation accuracy, selected-family membership, and `CDA-BD` weight mass.
  - Include only if the Figure 2 inset is too compressed to explain where the selected family comes from.

- [ ] Appendix figure: raw weight distribution and entropy.
  - Plot: sorted weights \(w_i\), effective family size \(K_{\mathrm{eff}}\), and entropy
    \[
    H(w)=-\sum_i w_i\log w_i.
    \]
  - Include only if reviewers need evidence that `CDA-BD` is not secretly selecting one checkpoint.

### 5.3 Figure Selection Rule

- [ ] Keep exactly these \(5\) main-paper figure roles unless a result genuinely breaks the narrative.
- [ ] Every main-paper figure must answer one specific question about CDA that a table cannot answer.
- [ ] Prefer paired plots, residual plots, trajectories, and geometry plots over benchmark bars.
- [ ] Use benchmark numbers mainly in tables; use figures to explain mechanism, failure modes, and compute tradeoffs.

## 6. Write the Paper

- [ ] Write the introduction after the main DomainBed result shape is known.
- [ ] Write related work around the real comparison setting: DomainBed, SWAD, single-run post-hoc DG, DRO/QRM, model averaging, and modern DG evaluation.
- [ ] Write the problem and certificate section compactly.
- [ ] Write the method section as an algorithm definition for `VSC+CDA-BD`.
- [ ] Write experiments from the final tables.
- [ ] Write analysis from the ablations and figures.
- [ ] Write limitations honestly: source-only, checkpoint-bank dependence, mergeability failures, and compute cost.
- [ ] Write abstract and conclusion last.

## 7. Finalize

- [ ] Remove verbose narrative explanations and defensive phrasing.
- [ ] Move proofs and long derivations to the appendix.
- [ ] Compile the paper.
- [ ] Fix citations, tables, figures, overfull boxes, and author formatting.
- [ ] Run one harsh reviewer pass.
- [ ] Produce final PDF, source archive, and result bundle.
