---
title: Results Ledger
description: Comprehensive ledger and method catalog for completed baselines, soups, probe batteries, strict post-hoc projection pilots, and replay-visible methods in the repo.
created: 2026-03-30 22:05
last_modified: 2026-04-16 01:36
last_modified_by: agent
status: active
related_files: claude_workspace/results/swing_lessons_learned.md, domaingen/posthoc/swing.py, domaingen/posthoc/tsf.py, domaingen/posthoc/shotgun.py, domaingen/posthoc/moonshot_2.py, domaingen/posthoc/subset_soups.py
key_functions:
  - Preserve completed PRISM, SWING, TSF, probe-battery, subset-soup, and strict post-hoc projection empirical results in one place
  - Describe what each tested method actually does mechanically, not just what score it reached
  - Track which replay-visible methods in the repo have and have not been empirically exercised
  - Remove placeholder-only entries such as TBD, running, queued, and submitted rows
  - Make the current empirical conclusions easy to recover later
latest_change: Added the completed version-space-only selector+weight sweeps on the PACS sketch and photo splits and marked broad method development/search as paused.
change_log:
  - 2026-03-30 22:05: Initial PRISM-only ledger created
  - 2026-04-01 09:40: Initial SWING-only ledger created
  - 2026-04-01 12:20: Merged PRISM and SWING ledgers into one completed-results-only ledger
  - 2026-04-04 00:35: Added SpectralSubsetSoup, GraphDiffusionSubsetSoup, and GibbsTopKSubsetSoup replay results on PACS art_painting
  - 2026-04-05 18:05: Added TSF, SHOTGUN, MOONSHOT-2, the full-lean Gibbs rerun, and the 16-cell graph-diffusion ablation on PACS art_painting
  - 2026-04-05 19:10: Added the focused 12-cell local graph-diffusion sweep and updated the subset-soup conclusions
  - 2026-04-05 20:05: Added TrajectoryNuisanceProjection, FisherRashomonProjection, and LogitCovarianceDebias pilot runs on PACS art_painting
  - 2026-04-05 14:52: Added replay-visible method inventory, detailed SHOTGUN/MOONSHOT suite descriptions, and the GraphDiffusionWeightedSubsetSoup failure study
  - 2026-04-05 18:53: Added JacobianCanalizationRepair as a completed strict post-hoc repair pilot on PACS art_painting
  - 2026-04-08 18:40: Added the ERM/SWAD/DCA/D-COLA/GCS replay refresh on `erm_replay_bank_painting` and recorded DCA/GCS as exercised replay-visible methods
  - 2026-04-08 21:55: Added the D-COLA extension sweep on `erm_replay_bank_painting` and recorded which theory-aligned additions helped or hurt legacy D-COLA
  - 2026-04-09 00:42: Added the completed 10-run D-COLA tuning sweep on `erm_replay_bank_painting` and recorded `dcola_lambda_cov=0.08` as the current best full-accuracy setting
  - 2026-04-09 00:55: Added the local covariance refinement (`0.06`, `0.07`, `0.09`) and confirmed that `dcola_lambda_cov=0.08` remains the best setting
  - 2026-04-09 01:10: Added the 7-run micro-tuning block around the tuned winner, including the `cov008` rerun and local continuation/temperature probes
  - 2026-04-09 01:32: Added deterministic D-COLA reruns and revised the current empirical recommendation toward the best deterministic branch
  - 2026-04-09 15:52: Added the deterministic BN-refresh view comparison (`train_aug` vs `eval_noaug`) for baseline and tuned D-COLA variants
  - 2026-04-09 16:02: Added deterministic single-addition tests on top of the no-augmentation BN-refresh baseline
  - 2026-04-09 17:18: Added BN-aware, mergeability-graph, and class-conditional D-COLA structural tests on the stable no-augmentation path
  - 2026-04-09 18:30: Added multi-anchor and alternate-pool D-COLA tests on the stable no-augmentation path
  - 2026-04-09 19:39: Added graph-diffusion-pool continuation follow-ups on the stable no-augmentation path
  - 2026-04-09 20:57: Added the plain graph-diffusion D-COLA sweep and recorded that the default graph-diffusion pool remains the best stable current-bank branch
  - 2026-04-09 22:08: Added graph-diffusion D-COLA weighting-fix tests (prior and deploy-aware path search) and recorded that the plain graph-diffusion pool still wins
  - 2026-04-10 00:40: Added graph-diffusion D-COLA source-risk variants and recorded that none beat the plain graph-diffusion pool
  - 2026-04-10 02:00: Added graph-diffusion D-COLA covariance/complementarity variants and recorded that none beat the plain graph-diffusion pool
  - 2026-04-10 03:00: Added graph-diffusion D-COLA support-only pruning variants and recorded that none beat the plain graph-diffusion pool
  - 2026-04-10 15:45: Added graph-diffusion union-of-pools D-COLA variants and recorded that none beat the plain graph-diffusion pool
  - 2026-04-11 05:54: Added graph-diffusion support-search D-COLA variants and recorded that support-level swap search also failed to beat the plain graph-diffusion pool
  - 2026-04-11 17:17: Added exact retained-family CDA objective runs on the graph-diffusion pool and recorded that untuned observable/surrogate settings underperform the plain graph-diffusion family
  - 2026-04-11 18:46: Added exact CDA coefficient-calibration runs on the graph-diffusion pool and recorded that reduced mergeability scales still do not recover the plain graph-diffusion baseline
  - 2026-04-12 01:32: Added normalized support-level exact CDA runs on the graph-diffusion pool and recorded that they still do not beat the plain graph-diffusion family
  - 2026-04-13 14:40: Added the completed selector-family sweep on PACS art_painting, including all 53 selector/control runs with descriptions, per-run hyperparameters, and final family sizes
  - 2026-04-14 19:47: Added the corrected 12x6 selector-family sweep summary on PACS art_painting, including the top overall schemes, the full family leaderboard, and updated conclusions about adaptive family selection
  - 2026-04-15 01:10: Added the completed focused family-local nonuniform weighting sweeps on the original Blackwell and version-space families, including method winners, control comparisons, and updated weighting conclusions
  - 2026-04-15 04:42: Added a partial live snapshot from the resumed expanded selector-family sweep on PACS art_painting, including the current top schemes and in-progress family leaderboard after removing the barycenter-merge variant
  - 2026-04-15 05:18: Added the completed crossed selector+weight sweep on PACS art_painting, including the 4x8 selector/weight combinations and the updated headline recommendation
  - 2026-04-15 06:02: Added the PACS cartoon selector+weight cross-sweep leaderboard, including the top combinations and the singleton-family weighting bug caveat
  - 2026-04-15 06:14: Replaced the PACS cartoon selector+weight entry with the completed 32-combination leaderboard and updated the split-specific conclusions
  - 2026-04-16 01:36: Added completed version-space-only selector+weight results on the PACS sketch and photo splits and recorded that method development/search is paused for reporting.
---

# Scope

This file is the current source of truth for completed baselines, PRISM-family methods, SWING/TSF, probe batteries, subset-soups, strict post-hoc projection pilots, and replay-visible method status in this project.

Conventions:

- Only completed, real entries are included here.
- Planning-only rows such as `TBD`, `running`, `queued`, and `submitted` have been intentionally removed.
- `SWING-uniform` means the plain uniform average of the accepted safe candidate set from the same run.
- PACS `art_painting` corresponds to replay bank:
  - `/project/jje239_dgxpublicai25/jwje228/work/results/erm_replay_bank_painting`

# 0. Method Catalog and Repo Inventory

## 0.1 How to read the catalog

- A `top-level replay method` is a direct `--methods` choice in [replay_methods.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/replay_methods.py).
- A `probe suite` is a battery of cheap or semi-cheap hypotheses that may contain many internal method families.
- A `probe family` is a family inside `SHOTGUN`, `MOONSHOT`, `MOONSHOT-2`, or `MOONSHOT-3`; these are often not standalone replay IDs unless later promoted.
- This ledger now records both scores and mechanism-level status, because several branches failed specifically because the mechanism did not survive translation from probe space to a deployable object.

## 0.2 Replay-visible methods already exercised in this project

| Replay ID | Name | Implementation sketch | Current empirical status |
|---|---|---|---|
| `erm` | ERM replay baseline | Evaluate the saved training trajectory endpoint / selector without post-hoc editing. | tested baseline |
| `swad` | SWAD | LossValley picks a contiguous late flat region and densely averages it. | tested baseline; strong but not current lead on art |
| `stawa` | STAWA | Find a stationary predictive plateau and average the connected admissible window. | tested historically |
| `stawa_new` | STAWA-new | Revised STAWA variant with newer defaults and divergence handling. | tested historically |
| `stawa_old` | STAWA-old | Older STAWA variant retained for backward comparison. | tested historically and weaker |
| `dca` | DCA | D-COLA-style candidate family with the later CDA/DCA theorem-aligned projected-subgradient optimizer. | tested on painting bank; below SWAD and slightly below legacy D-COLA in current replay |
| `dcola` | D-COLA | Optimize simplex weights over a candidate pool using covariance, locality, and worst-domain structure. | tested; strong when source-domain structure is allowed |
| `dcola_ablate` | D-COLA ablations | Run controlled D-COLA variants with pieces removed or altered. | tested diagnostic only |
| `cross_pool_ablate` | Cross-pool ablation | Swap D-COLA and PRISM candidate pools to separate objective quality from pool quality. | tested diagnostic only |
| `cora` | CORA | Consensus/Rashomon simplex optimization over barrier-filtered candidates. | tested historically |
| `roar` | ROAR | Robust simplex optimization against hard source losses over an averageable Rashomon set. | tested historically |
| `scout` | SCOUT | Robust capped coverage over PRISM-style safe actions. | tested historically |
| `prism` | PRISM | Enumerate small safe subsets from a barrier-filtered pool and minimize implicit subgroup regret. | tested; strongest clean DG average branch |
| `swing` | SWING | Fit a local quadratic source-shift model in the safe-pool eigenspace and shrink the final point accordingly. | tested; directional correction too weak vs `SWING-uniform` |
| `tsf` | TSF | Filter checkpoint-to-checkpoint updates with a DCT spectral response and reconstruct one endpoint. | tested; collapsed to the final checkpoint |
| `shotgun` | SHOTGUN | Cheap cached-prediction probe battery over many weighting and subset hypotheses. | tested probe suite |
| `moonshot` | MOONSHOT | First expanded cached-prediction probe suite with geometry, graph, and spectral families. | tested probe suite |
| `moonshot_2` | MOONSHOT-2 | Second expanded cached-prediction probe suite adding Gibbs, view-TTA, and support-conditioned families. | tested probe suite |
| `moonshot_3` | MOONSHOT-3 | Direct state-update and state-search probe suite using actual weight-space edits or tiny post-hoc surgeries. | tested probe suite |
| `spectral_subset` | SpectralSubsetSoup | Build a similarity graph on support predictions, take a spectral embedding, choose a sparse subset, then uniformly soup it. | tested; translation weaker than graph/Gibbs |
| `graph_diffusion_subset` | GraphDiffusionSubsetSoup | Anchor on a good checkpoint, diffuse over the similarity graph, keep top-`k`, then uniformly soup them. | tested; current best subset-soup full result |
| `graph_diffusion_weighted_subset` | GraphDiffusionWeightedSubsetSoup | Same graph-selected subset, but use diffusion mass as final soup weights. | tested and failed |
| `gibbs_topk_subset` | GibbsTopKSubsetSoup | Score checkpoints with a Gibbs posterior over source-held losses, keep top-`k`, then uniformly soup them. | tested; alive branch |
| `gcs` | GCS | Global Canalized Souping; full-bank convex soup over canalization and mergeability terms. | tested on painting bank; under current defaults trails SWAD/DCA/D-COLA |
| `trajectory_nuisance_projection` | TrajectoryNuisanceProjection | Estimate unstable low-rank late-trajectory directions and shrink them in a single final state. | tested; small local gain only |
| `fisher_rashomon_projection` | FisherRashomonProjection | Move from an anchor toward a witness barycenter under a Fisher-style trust metric. | tested; projection lost to barycenter baseline |
| `logit_covariance_debias` | LogitCovarianceDebias | Apply a closed-form affine correction to the final classifier using support logit covariance. | tested; null result |
| `jacobian_canalization_repair` | JacobianCanalizationRepair | Freeze features, repair the linear head against validation loss while penalizing sensitivity to source-mixture reweighting. | tested; both repair variants lost to the anchor |

## 0.3 Replay-visible methods present in the repo but not yet validated here as standalone completed branches

| Replay ID | Name | Where visible | Notes |
|---|---|---|---|
| `choir` | CHOIR | [choir.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/choir.py) | top-level replay path exists, but there is no completed standalone `CHOIR` result recorded in this ledger yet |
| `base` | infrastructure selector | [replay_methods.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/replay_methods.py) | utility/infrastructure choice, not a research method |

## 0.4 Probe suites: what they were actually testing

| Suite | Object being manipulated | Cost model | Main purpose |
|---|---|---|---|
| `SHOTGUN` | cached checkpoint predictions only | cheapest | broad sweep over simple weighting/subset/routing hypotheses |
| `MOONSHOT` | cached checkpoint predictions only | cheap | first expansion into graph, spectral, and geometry-heavy probe families |
| `MOONSHOT-2` | cached checkpoint predictions plus cached augmented views | cheap-to-moderate | second expansion with Gibbs, support-conditioned, and augmentation-view families |
| `MOONSHOT-3` | actual model weights / tiny state updates / state search | expensive | first nontrivial weight-space probe suite beyond cached-prediction reweighting |

Important caution:

- `SHOTGUN`, `MOONSHOT`, and `MOONSHOT-2` are probe-space suites. Their wins are ranking signals over cached predictions, not automatically valid deployable models.
- `MOONSHOT-3` mixes mechanisms that are now outside the stricter current definition of acceptable post-hoc methods, because many families perform post-hoc optimization. It is still recorded here because it is part of the actual project history.

# 1. Global Baselines

## 1.1 ERM replay baseline on PACS art_painting

| Run | Status | Art full | In | Out | Notes |
|---|---|---:|---:|---:|---|
| `ERM-base` | successful | `0.8208` | `0.8188` | `0.8289` | Base replay metrics printed at the start of SWING replays |

## 1.2 2026-04-08 replay refresh on `erm_replay_bank_painting`

| Method | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| ERM | 0.8208 | 0.8188 | 0.8289 | `erm_painting_v1` |
| SWAD | 0.8755 | 0.8713 | 0.8924 | `swad_painting_v1` |
| DCA | 0.8730 | 0.8719 | 0.8778 | `dca_painting_v1` |
| D-COLA | 0.8740 | 0.8676 | 0.8998 | `dcola_painting_v1` |
| GCS | 0.8579 | 0.8542 | 0.8729 | `gcs_painting_v1` |

Interpretation:

- On this specific five-method replay refresh, `SWAD` is best on `art_painting_full_acc` at `0.8755`.
- `D-COLA` is slightly below `SWAD` on full (`0.8740`) but is best on out (`0.8998`).
- `DCA` under the new theorem-aligned optimizer is close to legacy `D-COLA` on full but currently worse on out.
- `GCS` is not competitive yet on this bank under the current default settings.

## 1.3 2026-04-08 D-COLA extension sweep on `erm_replay_bank_painting`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA | 0.8740 | 0.8676 | 0.8998 | `dcola_painting_v1` |
| D-COLA+pair | 0.8706 | 0.8688 | 0.8778 | `dcola_pairwise_painting_v1` |
| D-COLA+smoothmax | 0.8765 | 0.8737 | 0.8875 | `dcola_smoothmax_painting_v1` |
| D-COLA+covshrink | 0.8623 | 0.8578 | 0.8802 | `dcola_covshrink_painting_v1` |
| D-COLA+covweighted | 0.8784 | 0.8755 | 0.8900 | `dcola_covweighted_painting_v1` |
| D-COLA+refine | 0.8291 | 0.8237 | 0.8509 | `dcola_refine_painting_v1` |
| D-COLA+continuation | 0.8750 | 0.8719 | 0.8875 | `dcola_continuation_painting_v1` |

Interpretation:

- The strongest single addition on `art_painting_full_acc` is `D-COLA+covweighted` at `0.8784`, which is above legacy `D-COLA` (`0.8740`) and above `SWAD` on this bank refresh (`0.8755`).
- `D-COLA+smoothmax` is also a real positive signal at `0.8765`, and `D-COLA+continuation` is mildly positive at `0.8750`.
- Legacy `D-COLA` remains the best of this group on out (`0.8998`), so the current extensions improve full more than they improve OOD-tail performance.
- `D-COLA+pair` is not helpful under the current pairwise-locality proxy, `D-COLA+covshrink` is clearly harmful, and `D-COLA+refine` is a strong negative result.
- The current empirical shortlist for combination testing is therefore:
  - covariance weighting
  - smooth-max source risk
  - continuation

## 1.4 2026-04-09 tuned D-COLA sweep on `erm_replay_bank_painting`

Fixed scaffold for this sweep:

- `dcola_cov_weighting=domain_loss`
- `dcola_source_risk=smooth_max`
- `dcola_source_smooth_temp=20.0` unless otherwise noted
- `dcola_continuation_mode=regularizers`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+covweighted+smoothmax+cont | 0.8838 | 0.8822 | 0.8900 | `dcola_covweighted_smoothmax_continuation_painting_v1` |
| D-COLA+tune-cont2 | 0.8853 | 0.8841 | 0.8900 | `dcola_tune_cont2_painting_v1` |
| D-COLA+tune-cont3 | 0.8823 | 0.8829 | 0.8802 | `dcola_tune_cont3_painting_v1` |
| D-COLA+tune-cont6 | 0.8750 | 0.8743 | 0.8778 | `dcola_tune_cont6_painting_v1` |
| D-COLA+tune-cont8 | 0.8823 | 0.8816 | 0.8851 | `dcola_tune_cont8_painting_v1` |
| D-COLA+tune-temp8 | 0.8823 | 0.8841 | 0.8753 | `dcola_tune_temp8_painting_v1` |
| D-COLA+tune-temp12 | 0.8760 | 0.8731 | 0.8875 | `dcola_tune_temp12_painting_v1` |
| D-COLA+tune-temp30 | 0.8760 | 0.8731 | 0.8875 | `dcola_tune_temp30_painting_v1` |
| D-COLA+tune-temp40 | 0.8789 | 0.8755 | 0.8924 | `dcola_tune_temp40_painting_v1` |
| D-COLA+tune-cov008 | 0.8887 | 0.8877 | 0.8924 | `dcola_tune_cov008_painting_v1` |
| D-COLA+tune-cov015 | 0.8862 | 0.8853 | 0.8900 | `dcola_tune_cov015_painting_v1` |

Interpretation:

- The best current `art_painting_full_acc` on this bank is now `D-COLA+tune-cov008` at `0.8887`.
- The strongest settings so far are:
  - `dcola_cov_weighting=domain_loss`
  - `dcola_source_risk=smooth_max`
  - `dcola_source_smooth_temp=20.0`
  - `dcola_continuation_mode=regularizers`
  - `dcola_continuation_start_mult=2.0`
  - `dcola_lambda_cov=0.08`
- The continuation sweep shows that weaker continuation (`start_mult=2.0`) is better than stronger continuation on this bank.
- The temperature sweep shows that the original `smooth_temp=20.0` remains best on full; lowering or raising it hurts the headline metric.
- The covariance sweep shows that the best setting is below the original `0.10`, and that `0.15` is already too strong.
- This tuned D-COLA variant now exceeds the prior `0.8843` art-painting leader recorded elsewhere in the project history.

## 1.5 2026-04-09 local covariance refinement around the tuned D-COLA winner

Fixed scaffold for this local refinement:

- `dcola_cov_weighting=domain_loss`
- `dcola_source_risk=smooth_max`
- `dcola_source_smooth_temp=20.0`
- `dcola_continuation_mode=regularizers`
- `dcola_continuation_start_mult=2.0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+tune-cov006 | 0.8809 | 0.8792 | 0.8875 | `dcola_tune_cov006_painting_v1` |
| D-COLA+tune-cov007 | 0.8569 | 0.8591 | 0.8484 | `dcola_tune_cov007_painting_v1` |
| D-COLA+tune-cov008 | 0.8887 | 0.8877 | 0.8924 | `dcola_tune_cov008_painting_v1` |
| D-COLA+tune-cov009 | 0.8726 | 0.8707 | 0.8802 | `dcola_tune_cov009_painting_v1` |

Interpretation:

- `dcola_lambda_cov=0.08` remains the clear local winner on `art_painting_full_acc`.
- The neighborhood is highly non-smooth: `0.07` collapses badly and `0.09` is also clearly worse.
- This makes further broad covariance sweeps low-value; the next sensible move is a narrow rerun/micro-tune on gentler knobs rather than continuing to search this axis.

## 1.6 2026-04-09 micro-tuning around the tuned D-COLA winner

Fixed scaffold for this micro-tuning block:

- `dcola_cov_weighting=domain_loss`
- `dcola_source_risk=smooth_max`
- `dcola_lambda_cov=0.08`
- `dcola_continuation_mode=regularizers`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+tune-cov008 | 0.8887 | 0.8877 | 0.8924 | `dcola_tune_cov008_painting_v1` |
| D-COLA+cov008-rerun | 0.8745 | 0.8719 | 0.8851 | `dcola_tune_cov008_rerun_painting_v1` |
| D-COLA+cont1.5 | 0.8853 | 0.8841 | 0.8900 | `dcola_tune_cont15_cov008_painting_v1` |
| D-COLA+cont1.75 | 0.8770 | 0.8780 | 0.8729 | `dcola_tune_cont175_cov008_painting_v1` |
| D-COLA+cont2.25 | 0.8750 | 0.8737 | 0.8802 | `dcola_tune_cont225_cov008_painting_v1` |
| D-COLA+temp18 | 0.8691 | 0.8664 | 0.8802 | `dcola_tune_temp18_cov008_painting_v1` |
| D-COLA+temp22 | 0.8721 | 0.8700 | 0.8802 | `dcola_tune_temp22_cov008_painting_v1` |
| D-COLA+temp24 | 0.8833 | 0.8780 | 0.9046 | `dcola_tune_temp24_cov008_painting_v1` |

Interpretation:

- No run in this block crossed `0.8900` full.
- The `cov008` rerun fell from `0.8887` to `0.8745`, which means the current tuned branch is not stable enough to treat a single lucky run as the final answer.
- `cont1.5` is the strongest full-oriented result in this block at `0.8853`.
- `temp24` is the strongest out-oriented result in this block at `0.9046`, but its full score remains below the `cov008` peak.
- The right next move is therefore not another blind local sweep on the same scaffold. It is either:
  - a repeatability audit / deterministic replay check, or
  - one small cross test combining the best full-friendly continuation (`1.5`) with the best out-friendly temperature (`24`).

## 1.7 2026-04-09 deterministic BN-refresh reruns for tuned D-COLA

Deterministic replay change:

- BN refresh uses deterministic sequential source-train loaders
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

x

Interpretation:

- The previous tuned peaks above `0.888` full do not survive deterministic BN refresh.
- The best deterministic variant in this block is `D-COLA+det-cont1.5` at `0.8799` full with `0.8949` out.
- This strongly suggests that replay-time nondeterminism in the old BN-refresh path was materially inflating the apparent tuned peaks.
- The correct current recommendation is:
  - use deterministic BN refresh for any future tuning or reporting
  - treat pre-deterministic tuned peaks as optimistic / not yet reproducible

## 1.8 2026-04-09 deterministic BN-refresh view comparison (`train_aug` vs `eval_noaug`)

BN-refresh view change:

- `dcola_bn_refresh_view=train_aug` keeps the stochastic source-train transform during BN refresh
- `dcola_bn_refresh_view=eval_noaug` swaps BN refresh onto a deterministic no-augmentation source-train view

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+det-baseline-trainaug | 0.8657 | 0.8621 | 0.8802 | `dcola_det_baseline_trainaug_painting_v1` |
| D-COLA+det-baseline-noaug | 0.8765 | 0.8713 | 0.8973 | `dcola_det_baseline_noaugbn_painting_v1` |
| D-COLA+det-cov008 | 0.8711 | 0.8713 | 0.8704 | `dcola_det_cov008_rerun_painting_v1` |
| D-COLA+det-cov008-noaug | 0.8706 | 0.8676 | 0.8826 | `dcola_det_cov008_noaugbn_painting_v1` |
| D-COLA+det-cont1.5 | 0.8799 | 0.8761 | 0.8949 | `dcola_det_cont15_rerun_painting_v1` |
| D-COLA+det-cont1.5-noaug | 0.8408 | 0.8359 | 0.8606 | `dcola_det_cont15_noaugbn_painting_v1` |

Interpretation:

- `eval_noaug` is not a universal fix. It helps baseline deterministic D-COLA substantially (`0.8657 -> 0.8765` full), but it does not improve the tuned `cov008` branch on full and it severely damages the tuned `cont1.5` branch.
- The best deterministic full score across the view comparison remains `D-COLA+det-cont1.5` at `0.8799`, using `train_aug`.
- The best deterministic baseline-style out score in this block is `D-COLA+det-baseline-noaug` at `0.8973`.
- This means the remaining instability story is not “always use no-augmentation BN refresh.” The BN-refresh view interacts with the selected soup family, so it must remain an explicit experimental knob rather than a global replacement.
- The main empirical conclusion remains unchanged:
  - we still do not have a reproducible `>0.8900` full result on `art_painting`
  - the tuned peaks above `0.888` are not currently stable enough to treat as final

## 1.9 2026-04-09 deterministic single-addition tests on the no-augmentation BN-refresh base

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+det-baseline-noaug | 0.8765 | 0.8713 | 0.8973 | `dcola_det_baseline_noaugbn_painting_v1` |
| D-COLA+det-noaug+covweighted | 0.8774 | 0.8774 | 0.8778 | `dcola_det_noaugbn_covweighted_painting_v1` |
| D-COLA+det-noaug+smoothmax | 0.8340 | 0.8273 | 0.8606 | `dcola_det_noaugbn_smoothmax_painting_v1` |
| D-COLA+det-noaug+continuation | 0.8799 | 0.8768 | 0.8924 | `dcola_det_noaugbn_continuation_painting_v1` |

Interpretation:

- On the stable no-augmentation BN-refresh base, only `continuation` remains a meaningful positive direction.
- `covweighted` is almost neutral on full (`0.8765 -> 0.8774`) and materially hurts out (`0.8973 -> 0.8778`).
- `smoothmax` is clearly not viable on this stable base.
- `continuation` improves full from `0.8765` to `0.8799`, but it still does not produce a reproducible `>0.8900` full result.
- The current stable recommendation for this replay bank is therefore:
  - use deterministic BN refresh for reporting
  - treat `D-COLA+det-noaug+continuation` as the strongest stable full-oriented variant observed so far on the no-augmentation BN path
  - do not continue broad tuning unless there is a new structural idea to test

## 1.10 2026-04-09 structural D-COLA extensions on the stable no-augmentation path

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+det-baseline-noaug | 0.8765 | 0.8713 | 0.8973 | `dcola_det_baseline_noaugbn_painting_v1` |
| D-COLA+bnaware | 0.8594 | 0.8566 | 0.8704 | `dcola_bnaware_consistency_painting_v1` |
| D-COLA+mergegraph | 0.8623 | 0.8585 | 0.8778 | `dcola_mergegraph_painting_v1` |
| D-COLA+classcond | 0.8701 | 0.8713 | 0.8655 | `dcola_classconditional_painting_v1` |

Interpretation:

- None of the three structural, theory-motivated extensions improved on the stable no-augmentation D-COLA baseline.
- `bnaware` is the clearest negative result in this block; the current BN-aware selection criterion is over-penalizing and loses badly on both full and out.
- `mergegraph` also hurts materially, which suggests the current connected-component family construction is too restrictive on this replay bank.
- `classcond` is the least bad of the three, but it still loses to the stable baseline on full and substantially on out.
- The current evidence therefore does not support continuing this exact branch of structural modifications as the route to a reproducible `>0.8900` full result.

## 1.11 2026-04-09 multi-anchor and alternate-pool D-COLA on the stable no-augmentation path

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+det-baseline-noaug | 0.8765 | 0.8713 | 0.8973 | `dcola_det_baseline_noaugbn_painting_v1` |
| D-COLA+multi-anchor3 | 0.8765 | 0.8749 | 0.8826 | `dcola_multianchor3_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+pool-gibbs | 0.8730 | 0.8694 | 0.8875 | `dcola_pool_gibbs_noaugbn_painting_v1` |
| D-COLA+pool-swadvalley | 0.8564 | 0.8609 | 0.8386 | `dcola_pool_swadvalley_noaugbn_painting_v1` |

Interpretation:

- `multi-anchor3` does not improve stable D-COLA on full; it is effectively neutral on full and worse on out.
- `gibbs` is mildly negative and `swad_valley` is a strong negative result on this replay bank.
- `graph_diffusion_subset` is the first structural change in this branch that clearly helps:
  - full improves from `0.8765` to `0.8843`
  - out improves from `0.8973` to `0.9022`
- This is still below the `0.8900` target, but it changes the diagnosis:
  - the main remaining bottleneck is much more likely to be the candidate pool than the D-COLA weight optimizer itself
  - if D-COLA is going to break `0.8900` on this bank, the strongest current route is to run it on stronger external pools rather than continue tuning the legacy internal family builder

## 1.12 2026-04-09 graph-diffusion-pool D-COLA follow-ups on the stable no-augmentation path

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`
- `dcola_pool_source=graph_diffusion_subset`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff+cont | 0.8643 | 0.8627 | 0.8704 | `dcola_pool_graphdiff_cont_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff+cont+barrier | 0.8774 | 0.8749 | 0.8875 | `dcola_pool_graphdiff_cont_barrier_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff+k16+cont | 0.8691 | 0.8676 | 0.8753 | `dcola_pool_graphdiff_k16_cont_noaugbn_painting_v1` |

Interpretation:

- The plain graph-diffusion pool remains the strongest stable D-COLA variant on this replay bank.
- Adding continuation on top of the graph-diffusion pool is strongly harmful.
- Reintroducing an external barrier filter recovers part of the loss but still remains below the plain graph-diffusion pool.
- Shrinking the graph-diffusion pool to `k=16` with continuation also remains clearly worse than the plain graph-diffusion pool.
- The graph-diffusion result changes the picture from “D-COLA is capped” to “the legacy internal family builder is capped.” However, the immediate graph-diffusion follow-ups also show that the next gain is unlikely to come from layering the old continuation heuristic onto that better pool.

## 1.13 2026-04-09 plain graph-diffusion D-COLA sweep on the current painting bank

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`
- `dcola_pool_source=graph_diffusion_subset`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff-k32 | 0.8760 | 0.8731 | 0.8875 | `dcola_pool_graphdiff_k32_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff-a045 | 0.8765 | 0.8731 | 0.8900 | `dcola_pool_graphdiff_a045_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff-bestval | 0.8496 | 0.8456 | 0.8655 | `dcola_pool_graphdiff_bestval_noaugbn_painting_v1` |
| D-COLA+pool-graphdiff-s2 | 0.8555 | 0.8523 | 0.8680 | `dcola_pool_graphdiff_s2_noaugbn_painting_v1` |

Interpretation:

- The default graph-diffusion pool remains the strongest stable D-COLA branch on the current painting bank.
- Every single-axis perturbation in this block made the result worse, so there is no evidence that simple `k`, anchor, diffusion-step, or lower-`alpha` local tuning will push this bank over `0.8900`.
- `bestval` anchor and `steps=2` are both clearly wrong directions on this bank.
- `k=32` and `alpha=0.45` are milder negatives, but still negatives.
- The practical conclusion is now sharper: if D-COLA is going to break `0.8900`, the next serious move should be a stronger replay bank rather than more current-bank graph-diffusion tuning.

## 1.14 2026-04-09 graph-diffusion D-COLA weighting fixes on the current painting bank

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+prior005 | 0.8799 | 0.8755 | 0.8973 | `dcola_pool_graphdiff_prior005_noaugbn_painting_v1` |
| D-COLA+graphdiff+path | 0.8799 | 0.8792 | 0.8826 | `dcola_pool_graphdiff_path_noaugbn_painting_v1` |
| D-COLA+graphdiff+prior005+path | 0.8721 | 0.8694 | 0.8826 | `dcola_pool_graphdiff_prior005_path_noaugbn_painting_v1` |
| D-COLA+graphdiff+prior010+path | 0.8750 | 0.8725 | 0.8851 | `dcola_pool_graphdiff_prior010_path_noaugbn_painting_v1` |

Interpretation:

- Neither the trust-region prior nor the deploy-aware path search improved on the plain graph-diffusion pool.
- The prior alone is the least bad change, but it still loses to the unmodified graph-diffusion-pool D-COLA run.
- The deploy-aware path-search branch is a clear negative in its current form, and combining it with the prior is worse still.
- This is useful because it narrows the failure mode: once the candidate family is upgraded to the graph-diffusion subset, the remaining weakness is not bank size or obvious weight-path selection. The remaining mismatch is more likely in the source-risk surrogate itself.

## 1.15 2026-04-10 graph-diffusion D-COLA source-risk variants on the current painting bank

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+domainwcvar | 0.8711 | 0.8700 | 0.8753 | `dcola_pool_graphdiff_domainwcvar_painting_v1` |
| D-COLA+graphdiff+examplecvar | 0.8779 | 0.8774 | 0.8802 | `dcola_pool_graphdiff_examplecvar_a020_painting_v1` |
| D-COLA+graphdiff+classcvar-freq | 0.8550 | 0.8523 | 0.8655 | `dcola_pool_graphdiff_classcvar_freq_a020_painting_v1` |
| D-COLA+graphdiff+classcvar-uniform | 0.8735 | 0.8713 | 0.8826 | `dcola_pool_graphdiff_classcvar_uniform_a020_painting_v1` |

Interpretation:

- None of the new robust source-risk surrogates improved on the plain graph-diffusion pool.
- `example_cvar` is the least bad of the four, but it still loses clearly to the plain graph-diffusion-pool D-COLA run.
- `domain_weighted_cvar` and especially `class_conditional_cvar` are strong negatives on this bank in their first instantiations.
- This narrows the remaining problem further: on the current bank, D-COLA is not rescued by harder source-risk surrogates, deploy-aware path selection, or trust-region priors once the graph-diffusion pool is fixed. The next serious move must be a different structural change to the method rather than another local surrogate swap.

## 1.16 2026-04-10 graph-diffusion D-COLA covariance/complementarity variants on the current painting bank

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+covweighted | 0.8735 | 0.8713 | 0.8826 | `dcola_pool_graphdiff_covweighted_painting_v1` |
| D-COLA+graphdiff+classcov-freq | 0.8618 | 0.8578 | 0.8778 | `dcola_pool_graphdiff_classcov_freq_painting_v1` |
| D-COLA+graphdiff+classcov-uniform | 0.8721 | 0.8688 | 0.8851 | `dcola_pool_graphdiff_classcov_uniform_painting_v1` |
| D-COLA+graphdiff+covweighted+norm | 0.8667 | 0.8670 | 0.8655 | `dcola_pool_graphdiff_covweighted_norm_painting_v1` |
| D-COLA+graphdiff+covweighted+shrink025 | 0.8760 | 0.8755 | 0.8778 | `dcola_pool_graphdiff_covweighted_shrink025_painting_v1` |

Interpretation:

- None of the covariance/complementarity-side tweaks improved on the plain graph-diffusion pool.
- `covweighted` and `classcov-uniform` are milder negatives; `classcov-freq` and `covweighted+norm` are strong negatives.
- `covweighted+shrink025` partially recovers the loss but still remains below the plain graph-diffusion-pool D-COLA run.
- At this point, the evidence is consistent across pool, weighting, source-risk, and covariance branches: the graph-selected family is the useful object, while D-COLA’s continuous simplex reweighting and surrogate refinements are not adding value on top of that family.

## 1.17 2026-04-10 graph-diffusion D-COLA support-only pruning variants on the current painting bank

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_support_only_mode=backward_prune`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+support16 | 0.8770 | 0.8737 | 0.8900 | `dcola_pool_graphdiff_support16_painting_v1` |
| D-COLA+graphdiff+support12 | 0.8789 | 0.8780 | 0.8826 | `dcola_pool_graphdiff_support12_painting_v1` |
| D-COLA+graphdiff+support08 | 0.8730 | 0.8731 | 0.8729 | `dcola_pool_graphdiff_support08_painting_v1` |
| D-COLA+graphdiff+support08-dropanchor | N/A | N/A | N/A | `dcola_pool_graphdiff_support08_dropanchor_painting_v1` |

Interpretation:

- Support-only pruning is also a negative result on this bank.
- The least bad support-only variant is `support12`, but it still loses to the plain graph-diffusion-pool D-COLA run.
- More aggressive pruning hurts progressively more.
- The missing `support08-dropanchor` row should be treated as a failed or incomplete run, not evidence either way.
- The current picture is now consistent across every tested D-COLA-side modification: the graph-diffusion-selected 24-checkpoint family is the useful object, and every attempt to further optimize, reweight, robustify, or prune that family has made it worse on this bank.

## 1.18 2026-04-10 graph-diffusion union-of-pools D-COLA variants on the current painting bank

Fixed scaffold for this block:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+union-graph-gibbs-uniform | 0.8789 | 0.8755 | 0.8924 | `dcola_union_graph_gibbs_uniform_painting_v1` |
| D-COLA+union-graph-gibbs-support16 | 0.8818 | 0.8780 | 0.8973 | `dcola_union_graph_gibbs_support16_painting_v1` |
| D-COLA+union-graph-gibbs-dcola-uniform | 0.8745 | 0.8713 | 0.8875 | `dcola_union_graph_gibbs_dcola_uniform_painting_v1` |
| D-COLA+union-graph-gibbs-dcola-support16 | 0.8755 | 0.8731 | 0.8851 | `dcola_union_graph_gibbs_dcola_support16_painting_v1` |

Interpretation:

- The union-of-pools branch is also a negative result relative to the plain graph-diffusion pool.
- `union-graph-gibbs-support16` is the least bad union variant, but it still loses to `D-COLA+pool-graphdiff` on both full and out.
- Adding legacy D-COLA candidates to the union makes the result worse, both with uniform deployment and with support pruning.
- This tightens the empirical picture further:
  - the graph-diffusion-selected family is the useful object
  - enlarging that family with Gibbs or legacy D-COLA candidates does not improve it on this bank
- The best stable D-COLA-adjacent result on the current painting bank therefore remains `D-COLA+pool-graphdiff` at `0.8843 / 0.8798 / 0.9022`.

## 1.19 2026-04-11 graph-diffusion support-search D-COLA variants on the current painting bank

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+swap1 | 0.8726 | 0.8719 | 0.8753 | `dcola_pool_graphdiff_swap1_painting_v1` |
| D-COLA+graphdiff+swap3 | 0.8774 | 0.8761 | 0.8826 | `dcola_pool_graphdiff_swap3_painting_v1` |
| D-COLA+graphdiff+support16+swap3 | 0.8745 | 0.8719 | 0.8851 | `dcola_pool_graphdiff_support16_swap3_painting_v1` |

Interpretation:

- Support-level swap search is also a negative result relative to the plain graph-diffusion pool.
- Allowing one or three swaps against the full 300-checkpoint bank did not improve the graph-diffusion support; both variants are materially worse on full and out.
- Pre-pruning to `support16` before swap search also remains clearly below the plain graph-diffusion pool.
- This is the strongest evidence so far that, on the current painting bank, the graph-diffusion-selected 24-checkpoint uniform family is already the right local face and that D-COLA-side support optimization is not finding a better one.
- The best stable D-COLA-adjacent result on the current painting bank still remains `D-COLA+pool-graphdiff` at `0.8843 / 0.8798 / 0.9022`.

## 1.20 2026-04-11 exact retained-family CDA objectives on the graph-diffusion pool

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+cdaobs | 0.8530 | 0.8548 | 0.8460 | `dcola_pool_graphdiff_cdaobs_painting_v1` |
| D-COLA+graphdiff+cdasurr | 0.8384 | 0.8395 | 0.8337 | `dcola_pool_graphdiff_cdasurr_painting_v1` |

Interpretation:

- The exact retained-family CDA objectives are not empirically dead, but the first untuned coefficient settings are strong negatives.
- Both `cda_observable` and `cda_surrogate` lose badly to the plain graph-diffusion family, which means the implementation mismatch was real but the theory branch is not plug-and-play at default scales.
- This changes the recommendation:
  - do not continue heuristic D-COLA tuning on this bank
  - if CDA theory is the required branch, the next defensible work is coefficient calibration of the exact retained-family objectives
- The practical conclusion remains unchanged for the current bank:
  - the best stable D-COLA-adjacent result is still `D-COLA+pool-graphdiff` at `0.8843 / 0.8798 / 0.9022`
  - exact CDA, as currently calibrated, underperforms that family substantially
  - any further CDA-theory push should be framed as calibrating the observable/surrogate coefficients implied by Eq. `\eqref{eq:observable_upper}` and Eq. `\eqref{eq:practical_objective}`, not as another heuristic branch

## 1.21 2026-04-11 exact CDA coefficient calibration on the graph-diffusion pool

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+cdaobs-r0.25-k0.01 | 0.8545 | 0.8572 | 0.8435 | `dcola_pool_graphdiff_cdaobs_r0p25_k0p01_painting_v1` |
| D-COLA+graphdiff+cdaobs-r0.50-k0.01 | 0.8574 | 0.8603 | 0.8460 | `dcola_pool_graphdiff_cdaobs_r0p50_k0p01_painting_v1` |
| D-COLA+graphdiff+cdasurr-can0.05-mg0.01 | 0.8394 | 0.8383 | 0.8435 | `dcola_pool_graphdiff_cdasurr_can0p05_mg0p01_painting_v1` |
| D-COLA+graphdiff+cdasurr-can0.10-mg0.01 | 0.8311 | 0.8273 | 0.8460 | `dcola_pool_graphdiff_cdasurr_can0p10_mg0p01_painting_v1` |

Interpretation:

- Reducing the mergeability coefficient by two orders of magnitude helps relative to the naive exact-CDA settings, but the calibrated exact objectives are still strong negatives against the plain graph-diffusion family.
- The observable exact-CDA objective is consistently less bad than the surrogate exact-CDA objective on this bank.
- Neither calibrated exact-CDA setting approaches the `D-COLA+pool-graphdiff` baseline on full, in, or out accuracy.
- The practical conclusion therefore remains unchanged:
  - the best stable D-COLA-adjacent result on this bank is still `D-COLA+pool-graphdiff` at `0.8843 / 0.8798 / 0.9022`
  - the exact CDA branch is still theoretically valid but empirically miscalibrated on this bank
  - any further CDA-theory work must focus on better coefficient scaling or observable-bank normalization, not on more heuristic D-COLA tuning

## 1.22 2026-04-12 normalized support-level exact CDA on the graph-diffusion pool

Fixed scaffold for this block:

- `dcola_pool_source=graph_diffusion_subset`
- `graph_diffusion_subset_k=24`
- `graph_diffusion_subset_anchor=bestmean`
- `graph_diffusion_subset_walk_alpha=0.60`
- `graph_diffusion_subset_steps=1`
- `dcola_cda_normalization=family`
- `dcola_cda_geometry_scope=trainable_params`
- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`

| Variant | Art full | In | Out | Replay dir |
|---|---:|---:|---:|---|
| D-COLA+pool-graphdiff | 0.8843 | 0.8798 | 0.9022 | `dcola_pool_graphdiff_noaugbn_painting_v1` |
| D-COLA+graphdiff+cdaobs-norm-uniform | 0.8564 | 0.8530 | 0.8704 | `dcola_graphdiff_cdaobs_norm_uniform_painting_v1` |
| D-COLA+graphdiff+cdaobs-norm-swap3-postbn | 0.8755 | 0.8737 | 0.8826 | `dcola_graphdiff_cdaobs_norm_swap3_postbn_painting_v1` |
| D-COLA+graphdiff+cdaobs-norm-support16-postbn | 0.8545 | 0.8511 | 0.8680 | `dcola_graphdiff_cdaobs_norm_support16_postbn_painting_v1` |
| D-COLA+graphdiff+cdasurr-norm-uniform | 0.8706 | 0.8670 | 0.8851 | `dcola_graphdiff_cdasurr_norm_uniform_painting_v1` |

Interpretation:

- Normalizing the exact CDA terms, restricting geometry to trainable parameters, and reranking supports after BN refresh improve over the earlier raw exact-CDA branch, but they still do not beat the plain graph-diffusion family.
- The best run in this block is `cdaobs-norm-swap3-postbn` at `0.8755 / 0.8737 / 0.8826`, which remains clearly below `D-COLA+pool-graphdiff` on full and out.
- The normalized surrogate branch is less catastrophic than the raw surrogate branch, but it is still well below the graph-diffusion baseline.
- This is the strongest evidence so far that, on the current painting bank:
  - the graph-diffusion support family is the useful empirical object
  - exact CDA does not improve deployment when used as a support scorer or weight rule on top of that family
  - CDA may still be defensible as a retained-family principle, but not as a winning deployment-time optimizer on this bank

# 2. PRISM

## 2.1 Clean current PACS 4-split domain-label-free replay sweep

| Split | ERM | SWAD | PRISM |
|---|---:|---:|---:|
| art_painting | 82.08 | 87.60 | 87.26 |
| cartoon | 81.57 | 82.38 | 81.57 |
| photo | 94.55 | 97.07 | 97.54 |
| sketch | 78.32 | 81.73 | 83.53 |
| average | 84.13 | 87.19 | 87.47 |

Interpretation:

- `PRISM` is currently the best domain-label-free method in this sweep by average.
- The margin over `SWAD` is small: `+0.28`.
- `PRISM` wins on `photo` and `sketch`.
- `SWAD` wins on `art_painting` and `cartoon`.

## 2.2 Fresh canonical `erm_replay_bank` seed-1 comparison

| Method | Art full | In | Out |
|---|---:|---:|---:|
| ERM | 0.8066 | 0.8096 | 0.7946 |
| SWAD | 0.8794 | 0.8786 | 0.8826 |
| D-COLA | 0.8921 | 0.8926 | 0.8900 |
| PRISM | 0.8862 | 0.8883 | 0.8778 |

Interpretation:

- `D-COLA` is still the strongest overall method when source-domain structure is allowed.
- `PRISM` is competitive but not yet uniformly stronger than `SWAD`.
- On this bank, `PRISM` beats `SWAD` on art full and in, but loses on out.

## 2.3 Cross-pool ablation on fresh canonical bank

| Variant | Runner | Pool | Art full | In | Out |
|---|---|---|---:|---:|---:|
| baseline_dcola | D-COLA | D-COLA | 0.8901 | 0.8908 | 0.8875 |
| dcola_on_prism_pool | D-COLA | PRISM | 0.8877 | — | — |
| baseline_prism | PRISM | PRISM | 0.8833 | 0.8853 | 0.8753 |
| prism_on_dcola_pool | PRISM | D-COLA | 0.8672 | 0.8676 | 0.8655 |

Interpretation:

- PRISM’s remaining weakness is not only the candidate pool.
- The cross-pool result is consistent with an objective-level limitation in the current PRISM formulation.

## 2.4 Verified D-COLA ablations

| Variant | Art full |
|---|---:|
| baseline | 0.8750 |
| uniform | 0.8745 |
| early | 0.8687 |
| no_loc | 0.8667 |
| pooled_anchor | 0.8638 |
| contiguous | 0.8613 |
| no_cov | 0.8594 |

Interpretation:

- exact optimized weights matter little
- complementarity / nonredundancy matters a lot
- noncontiguity matters

## 2.5 Up-to-date `erm_cora` replay-bank comparisons

| Method / Variant | Art full | In | Out |
|---|---:|---:|---:|
| ERM | 0.7676 | 0.7627 | 0.7873 |
| D-COLA | 0.8770 | 0.8768 | 0.8778 |
| SCOUT | 0.8442 | 0.8456 | 0.8386 |
| PRISM baseline | 0.8706 | 0.8725 | 0.8631 |
| PRISM `epsilon=0.03, tau=0.03` | 0.8516 | 0.8493 | 0.8606 |
| PRISM `alpha=0.20, epsilon=0.03, tau=0.03` | 0.8940 | 0.8975 | 0.8802 |
| PRISM `M=4, epsilon=0.03, tau=0.03` | 0.8696 | 0.8700 | 0.8680 |

Interpretation:

- This was the first strong sign that `alpha=0.20` could materially improve PRISM.
- Loosening the pool helped less than changing `alpha`.

## 2.6 Historical local workspace leaderboard

| Method | Art full | In | Out |
|---|---:|---:|---:|
| ERM-replay | 0.7676 | 0.7627 | 0.7873 |
| SWAD-replay | 0.8584 | 0.8609 | 0.8484 |
| STAWA-new | 0.8643 | 0.8658 | 0.8582 |
| STAWA-old | 0.8022 | 0.7999 | 0.8117 |
| D-COLA | 0.8726 | 0.8737 | 0.8680 |
| CORA | 0.8413 | 0.8401 | 0.8460 |
| ROAR | 0.8633 | 0.8639 | 0.8606 |

Use with caution:

- these results are real and useful for project history
- but the cleaner banks above should be preferred for current claims

## 2.7 Completed PRISM full-cap art_painting grid cells

| Run name | alpha | epsilon | tau | M | Art full | In | Out | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| art_a015_e002_t002_m3 | 0.15 | 0.02 | 0.02 | 3 | 88.28 | 88.35 | 88.02 | best art full and best in among completed full-cap cells |
| art_a015_e002_t003_m3 | 0.15 | 0.02 | 0.03 | 3 | 87.74 | 87.74 | 87.78 | completed full-cap rerun |
| art_a015_e002_t005_m3 | 0.15 | 0.02 | 0.05 | 3 | 87.16 | 87.37 | 86.31 | completed full-cap rerun |
| art_a020_e002_t002_m3 | 0.20 | 0.02 | 0.02 | 3 | 86.43 | 86.09 | 87.78 | completed full-cap rerun |
| art_a020_e002_t003_m3 | 0.20 | 0.02 | 0.03 | 3 | 88.04 | 87.86 | 88.75 | tied best out among completed full-cap cells |
| art_a020_e002_t005_m3 | 0.20 | 0.02 | 0.05 | 3 | 87.74 | 87.55 | 88.51 | completed full-cap rerun |
| art_a025_e002_t002_m3 | 0.25 | 0.02 | 0.02 | 3 | 87.94 | 88.16 | 87.04 | completed full-cap rerun |
| art_a025_e002_t003_m3 | 0.25 | 0.02 | 0.03 | 3 | 87.01 | 86.88 | 87.53 | completed full-cap rerun |
| art_a025_e002_t005_m3 | 0.25 | 0.02 | 0.05 | 3 | 87.16 | 87.31 | 86.55 | completed full-cap rerun |
| art_a025_e003_t002_m3 | 0.25 | 0.03 | 0.02 | 3 | 87.11 | 86.70 | 88.75 | tied best out among completed full-cap cells |
| art_a025_e003_t003_m3 | 0.25 | 0.03 | 0.03 | 3 | 87.45 | 87.68 | 86.55 | completed full-cap rerun |
| art_a025_e003_t005_m3 | 0.25 | 0.03 | 0.05 | 3 | 87.79 | 87.55 | 88.75 | tied best out among completed full-cap cells |

Interpretation:

- completed feasible full-cap cells: `12`
- best art full so far: `art_a015_e002_t002_m3` at `88.28`
- best in so far: `art_a015_e002_t002_m3` at `88.35`
- best out so far is tied at `88.75`
- among the completed feasible cells, the strongest region remains the tighter `epsilon = 0.02` corner, especially with `alpha = 0.15`

# 3. SWING

## 3.1 Historical SWING-only successful runs

| Run | Rank | Art full | In | Out | Notes |
|---|---:|---:|---:|---:|---|
| `swing_art_painting_debug` | 1 | 0.8726 | 0.8713 | 0.8778 | First end-to-end successful SWING run; tiny 5-checkpoint safe basin |
| `swing_art_rank2_auto_bn512` | 2 | 0.8818 | 0.8780 | 0.8973 | Best raw SWING number observed to date; older schema, no within-run uniform baseline recorded |

## 3.2 Completed runs with explicit SWING-uniform comparison

| Run | Rank | SWING-uniform full | SWING full | Full gap | SWING-uniform out | SWING out | Out gap | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `swing_art_rank2_refresh` | 2 | 0.8765 | 0.8774 | +0.0009 | 0.8900 | 0.8949 | +0.0049 | SWING barely beat uniform; both directions almost annihilated |
| `swing_art_rank2_tau1e3` | 2 | 0.8779 | 0.8735 | -0.0044 | 0.8973 | 0.8875 | -0.0098 | `tau=1e-3` reduced over-shrink but hurt relative to uniform |
| `swing_art_rank2_loc18` | 2 | 0.8745 | 0.8779 | +0.0034 | 0.8851 | 0.8875 | +0.0024 | Best explicit within-run evidence for SWING; still a very small margin |
| `swing_art_rank3_auto_bn512_loc30` | 3 | 0.8770 | 0.8750 | -0.0020 | 0.8900 | 0.8900 | +0.0000 | Rank 3 worked numerically but underperformed uniform |
| `swing_art_rank3_tau1e3` | 3 | 0.8784 | 0.8755 | -0.0029 | 0.8924 | 0.8900 | -0.0024 | Healthier rank 3 numerically, still worse than uniform |

Interpretation:

- The safe-pool construction is strong.
- The uniform average of the accepted safe candidate set is a very strong baseline.
- The current directional SWING edit does not clearly and consistently beat that uniform baseline.

## 3.3 Important real diagnostic runs

| Run | Status | What happened | Main lesson |
|---|---|---|---|
| `swing_art_probe_e05_t04` | failed probe | Safe pool widened to 25 candidates, but local projected models produced `nan` losses | Widen the safe pool, but keep the local cloud local |
| `swing_art_probe_e08_t05` | failed probe | Safe pool widened to 91 candidates, but local projected models again produced `nan` losses | Global local-cloud regression is too aggressive |
| early `rank=3` attempts | diagnostic bottleneck | The main failure moved from pool size to source-fit conditioning | Rank 3 is not blocked by basin size anymore; it is blocked by estimator quality |

# 4. Probe Discovery and Subset-Soup Follow-ups

## 4.1 TSF diagnostic failure on PACS art_painting

| Method | Art full | In | Out | Same-run uniform full | Same-run uniform in | Same-run uniform out | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| `TSF` | 0.8203 | 0.8182 | 0.8289 | 0.8735 | 0.8694 | 0.8900 | deployed filter collapsed back to the final checkpoint; coefficient summary had `l1=1`, `max=1`, effectively a one-hot endpoint |

Interpretation:

- The current deployed `TSF` endpoint is a real negative result.
- The replay succeeded end to end, but the method itself degenerated algebraically to the last checkpoint.
- The same-run uniform baseline remained strong, so this was a method failure rather than a pipeline failure.

## 4.2 SHOTGUN nuclear probe sweep on PACS art_painting

| Run | Checkpoints | Probe count | Uniform-all full | Uniform-all in | Uniform-all out | Best full probe | Best full metrics | Best balanced probe | Best balanced metrics |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| `shotgun_painting_nuclear_v2` | 300 | 1704 | 0.8643 | 0.8597 | 0.8826 | `diverse_supporttail_k007_l10` | `0.8799 / 0.8829 / 0.8680` | `even_018_prob` | `0.8716 / 0.8664 / 0.8924` |

Interpretation:

- The strongest live signal from `SHOTGUN` was sparse noncontiguous subset selection rather than continuous full-bank reweighting.
- `49` probes beat the `uniform-all` baseline on both full and out.
- The most important deployable clue was `even_018_prob`, which suggested trajectory coverage and sparse spacing could matter more than late contiguous windows.

Implementation sketch:

- `SHOTGUN` is a pure cached-prediction probe battery implemented in [shotgun.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/shotgun.py).
- It loads the dense checkpoint bank once, caches support/validation predictions, and then scores many global mixtures or subset rules without constructing a new weight-space model for each probe.
- The suite is broad rather than principled: it tests whether any simple object already explains the gains, including dense averaging, sparse spacing, quality-ranked subsets, soft loss-based weights, class-conditional experts, per-example routing, and trajectory filters.

### 4.2.1 SHOTGUN family inventory

| Family | Probe count | Implementation sketch | Best full | Best out |
|---|---:|---|---:|---:|
| `center_weighting` | 70 | Use Gaussian weights centered on anchor checkpoints. | 0.84375 | 0.8655256723716381 |
| `class_conditional` | 72 | Assign different checkpoint mixtures to different classes. | 0.8642578125 | 0.882640586797066 |
| `dense_uniform` | 95 | Uniformly average the whole bank or contiguous windows/prefixes. | 0.87060546875 | 0.882640586797066 |
| `diversity_subset` | 234 | Greedily pick subsets balancing held-out quality and predictive diversity. | 0.8798828125 | 0.8924205378973105 |
| `dynamic_selection` | 192 | Choose checkpoint weights per example from confidence, margin, or entropy. | 0.865234375 | 0.8850855745721271 |
| `hard_example_subset` | 13 | Greedily pick checkpoints that reduce hard-example loss. | 0.8603515625 | 0.8753056234718827 |
| `loss_softmax_weighting` | 504 | Apply dense softmax weights from source losses or tail losses. | 0.8701171875 | 0.8875305623471883 |
| `quality_subset` | 78 | Take top-`k` checkpoints by source-held quality scores. | 0.87646484375 | 0.8875305623471883 |
| `recency_smoothing` | 61 | Bias weights toward later checkpoints with EMA or polynomial priors. | 0.86376953125 | 0.8875305623471883 |
| `robust_statistics` | 41 | Use trimmed means, medians, rank means, majority vote, or geometric means. | 0.86572265625 | 0.8850855745721271 |
| `routing` | 108 | Gate examples between two candidate experts using uncertainty or disagreement signals. | 0.86865234375 | 0.8850855745721271 |
| `single_checkpoint` | 23 | Evaluate individual checkpoints directly. | 0.87109375 | 0.8753056234718827 |
| `sparse_spacing` | 69 | Use evenly spaced or stride-phase checkpoint subsets. | 0.87158203125 | 0.8924205378973105 |
| `trajectory_filter` | 144 | Apply temporal DCT, smoothing, or PCA filters in prediction space. | 0.865234375 | 0.8850855745721271 |

Reading the `SHOTGUN` outcome:

- The suite mostly falsified dense full-bank weighting stories.
- The winners were sparse and structurally simple: quality subsets, diversity subsets, and sparse spacing.
- That is the historical reason the later subset-soup work happened at all.

## 4.3 Original MOONSHOT nuclear probe sweep on PACS art_painting

| Run | Best full probe | Best full / out | Best out probe | Best full / out | Uniform-all full | Uniform-all out | Notes |
|---|---|---|---|---|---:|---:|---|
| `shotgun_painting_nuclear_v2_moonshot_verbose1` | `pca_quantile_pc1_k024` | `0.8735 / 0.8851` | `pca_quantile_pc3_k015` | `0.8608 / 0.8924` | 0.8643 | 0.8826 | first broader geometry/graph/spectral probe expansion beyond `SHOTGUN` |

Implementation sketch:

- `MOONSHOT` is implemented in [moonshot.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot.py).
- Like `SHOTGUN`, it stays in probe space over cached predictions.
- The main novelty versus `SHOTGUN` is that it introduces checkpoint-graph objects, temporal spectral filters, and geometric subset rules derived from PCA and graph structure.

### 4.3.1 MOONSHOT family inventory

| Family | Probe count | Implementation sketch | Best full | Best out |
|---|---:|---|---:|---:|
| `geometry_subset` | 40 | Pick sparse checkpoint subsets using PCA geometry and quantile coverage. | 0.87353515625 | 0.8924205378973105 |
| `graph_centrality` | 24 | Weight checkpoints by degree, eigenvector, or PageRank centrality. | 0.8642578125 | 0.882640586797066 |
| `graph_diffusion` | 480 | Diffuse mass from anchor checkpoints across a similarity graph. | 0.86767578125 | 0.8850855745721271 |
| `graph_projector` | 128 | Project trajectories through low- or high-frequency graph eigenmodes. | 0.865234375 | 0.882640586797066 |
| `harmonic_weighting` | 84 | Use sinusoidal time weights with different envelopes. | 0.86669921875 | 0.8875305623471883 |
| `label_fit` | 18 | Solve ridge-style weights to fit support labels directly in prediction space. | 0.8642578125 | 0.882640586797066 |
| `loss_curve_geometry` | 35 | Exploit loss minima, turning points, and trajectory geometry. | 0.8662109375 | 0.8875305623471883 |
| `sparse_approximation` | 44 | Approximate dense targets with sparse checkpoint supports. | 0.861328125 | 0.882640586797066 |
| `spectral_bandpass` | 224 | Keep selected temporal frequency bands with DCT filters. | 0.8642578125 | 0.882640586797066 |
| `spectral_subset` | 80 | Pick sparse subsets via graph spectral embeddings and medoids. | 0.8720703125 | 0.8875305623471883 |
| `svd_reconstruction` | 80 | Reconstruct trajectory predictions with low-rank temporal SVD. | 0.86474609375 | 0.8850855745721271 |

Reading the original `MOONSHOT` outcome:

- It validated that geometry-derived sparse subsets were more promising than most dense spectral or graph weightings.
- It did not yet clearly demonstrate that graph diffusion itself was strong.
- In hindsight, this suite was an intermediate bridge: it suggested where to look, but not yet which mechanism would survive deployment.

## 4.4 MOONSHOT-2 nuclear probe sweep on PACS art_painting

| Run | Best full probe | Best full / out | Best out probe | Best full / out | Best balanced probe | Best full / out | Wins vs uniform on both full and out | Notes |
|---|---|---|---|---|---|---|---:|---|
| `moonshot_2_painting_nuclear_v1` | `gibbs_recency_supporttail_t0p01_logit` | `0.8784 / 0.8753` | `spectral_subset_cos_k024_r04` | `0.8711 / 0.8949` | `diffuse_cos_bestmean_a06_s01_logit` | `0.8745 / 0.8900` | 36 | no `MOONSHOT-2` probe beat `even_018_prob` on both full and out simultaneously |

Interpretation:

- `MOONSHOT-2` confirmed that graph/diffusion and Gibbs-style ranking were alive, while pure center weighting and several other exotic families were not.
- The earlier `MOONSHOT` pass had only `10` probes beating uniform on both full and out; `MOONSHOT-2` raised that count to `36`.
- The strongest new deployable directions coming out of probe space were graph diffusion and Gibbs top-`k`, not spectral subset alone.
- These are probe-space results over cached predictions, not final weight-space soups.

Implementation sketch:

- `MOONSHOT-2` is implemented in [moonshot_2.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot_2.py).
- It inherits the cached-probability workflow from `MOONSHOT` and expands it with Gibbs posteriors, geometry-center hypotheses, spectral notch filters, support-conditioned prototype/prior rules, and a much larger augmentation-view bank.
- This is the suite that materially changed the project direction because two of its probe families later survived translation: graph diffusion and Gibbs top-`k`.

### 4.4.1 MOONSHOT-2 family inventory

| Family | Probe count | Implementation sketch | Best full | Best out |
|---|---:|---|---:|---:|
| `geometry_center` | 10 | Use geometry-derived center weights rather than sparse subsets. | 0.80517578125 | 0.8117359413202934 |
| `geometry_subset` | 40 | Pick sparse checkpoint subsets using PCA geometry and quantile coverage. | 0.869140625 | 0.8850855745721271 |
| `gibbs_weighting` | 150 | Build Gibbs posteriors over checkpoints from source-held losses and priors. | 0.87841796875 | 0.8924205378973105 |
| `graph_centrality` | 24 | Weight checkpoints by degree, eigenvector, or PageRank centrality. | 0.8642578125 | 0.882640586797066 |
| `graph_diffusion` | 480 | Diffuse mass from anchor checkpoints across a similarity graph. | 0.8759765625 | 0.8899755501222494 |
| `graph_projector` | 128 | Project trajectories through low- or high-frequency graph eigenmodes. | 0.86572265625 | 0.882640586797066 |
| `harmonic_weighting` | 84 | Use sinusoidal time weights with different envelopes. | 0.86669921875 | 0.8875305623471883 |
| `kernel_herding` | 10 | Choose sparse subsets by herding toward the trajectory mean. | 0.86083984375 | 0.882640586797066 |
| `label_fit` | 18 | Solve ridge-style weights to fit support labels directly in prediction space. | 0.86474609375 | 0.882640586797066 |
| `loss_curve_geometry` | 35 | Exploit loss minima, turning points, and trajectory geometry. | 0.86865234375 | 0.8850855745721271 |
| `sparse_approximation` | 44 | Approximate dense targets with sparse checkpoint supports. | 0.86572265625 | 0.8850855745721271 |
| `spectral_bandpass` | 224 | Keep selected temporal frequency bands with DCT filters. | 0.8642578125 | 0.882640586797066 |
| `spectral_notch` | 24 | Delete selected temporal frequency bands rather than keeping them. | 0.8642578125 | 0.882640586797066 |
| `spectral_subset` | 80 | Pick sparse subsets via graph spectral embeddings and medoids. | 0.873046875 | 0.8948655256723717 |
| `support_prior` | 32 | Inject source-label priors into prediction mixtures. | 0.86474609375 | 0.882640586797066 |
| `support_prototype` | 64 | Replace or blend predictions with support-derived class prototypes. | 0.8642578125 | 0.882640586797066 |
| `svd_reconstruction` | 80 | Reconstruct trajectory predictions with low-rank temporal SVD. | 0.86474609375 | 0.8850855745721271 |
| `view_tta` | 156 | Aggregate cached label-preserving augmented views without target data. | 0.87744140625 | 0.8899755501222494 |

Reading the `MOONSHOT-2` outcome:

- `gibbs_weighting` was the strongest full-oriented family.
- `graph_diffusion` became strong enough to justify a real weight-space translation.
- `spectral_subset` and `view_tta` were real probe-space positives, but only `spectral_subset` later got promoted, and it did not survive deployment as cleanly as graph/Gibbs.
- `geometry_center` was a harsh negative result. That matters because it killed the vague “just move toward the center” story very early.

## 4.5 MOONSHOT-3 nuclear merged probe sweep on PACS art_painting

| Run | Probe count | Best full probe | Best full / out | Best out probe | Best full / out | Notes |
|---|---:|---|---|---|---|---|
| `moonshot_3_painting_final_nuclear_merged_v1` | 128 | `final_simplex_quality` | `0.8779 / 0.8875` | `bestval_simplex_quality` | `0.8765 / 0.8875` | first probe suite to test actual weight-space state search and post-hoc updates rather than only cached mixtures |

Implementation sketch:

- `MOONSHOT-3` is implemented in [moonshot_3.py](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot_3.py).
- This suite is qualitatively different from `SHOTGUN`, `MOONSHOT`, and `MOONSHOT-2`:
  - some families do post-hoc SGD on classifier, BN-affine, featurizer, or full-model scopes
  - some families do direct state search over checkpoint lines, planes, simplices, or local PCA subspaces
  - some families do zero-SGD interventions such as BN-stat surgery or prototype reset
- Under the stricter current definition of acceptable post-hoc methods, many `MOONSHOT-3` families are now out-of-scope because they do post-hoc training. They are still important historically because they tested whether there was any strong non-soup direction at all.

### 4.5.1 MOONSHOT-3 family inventory

| Family | Probe count | Implementation sketch | Best full | Best out |
|---|---:|---|---:|---:|
| `agreement_pseudo_update` | 4 | Classifier pseudo-label update gated by agreement with local teacher or anchor. | 0.80712890625 | 0.8141809290953546 |
| `anchor_kl_l2_update` | 4 | Classifier fine-tune with KL-to-anchor plus L2 anchoring. | 0.82666015625 | 0.823960880195599 |
| `anchor_kl_update` | 4 | Classifier fine-tune with KL regularization to anchor predictions. | 0.8125 | 0.8215158924205379 |
| `anchor_l2_update` | 4 | Classifier fine-tune with explicit L2 pull toward anchor weights. | 0.8203125 | 0.8337408312958435 |
| `bn_affine_update` | 4 | Optimize only BatchNorm affine parameters on support CE. | 0.7998046875 | 0.8117359413202934 |
| `bn_consistency_update` | 4 | Optimize only BatchNorm affine parameters for view consistency. | 0.31982421875 | 0.3251833740831296 |
| `bn_stat_surgery` | 4 | Refresh BatchNorm statistics from support data without SGD. | 0.85302734375 | 0.8557457212713936 |
| `checkpoint_line_search` | 8 | Search along line segments between anchor and peer checkpoints. | 0.87158203125 | 0.8875305623471883 |
| `checkpoint_plane_search` | 4 | Search in the affine plane spanned by anchor and two peers. | 0.87158203125 | 0.8704156479217604 |
| `checkpoint_simplex_search` | 4 | Sample simplex combinations over local checkpoint neighborhoods. | 0.86083984375 | 0.8508557457212714 |
| `consistency_update` | 8 | Optimize classifier or featurizer for view-consistency objectives. | 0.8017578125 | 0.8190709046454768 |
| `distillation_update` | 4 | Distill from a fixed teacher soup into a smaller post-hoc update. | 0.83837890625 | 0.8484107579462102 |
| `drift_orthogonal_update` | 4 | Update classifier while projecting away trajectory drift directions. | 0.81640625 | 0.8190709046454768 |
| `fisher_update` | 8 | Use Fisher-preconditioned or Fisher-trust regularized post-hoc updates. | 0.82080078125 | 0.8312958435207825 |
| `hard_example_update` | 4 | Classifier update emphasizing top-alpha hard support examples. | 0.78759765625 | 0.8019559902200489 |
| `pca_orthogonal_update` | 4 | Classifier update orthogonal to local PCA basis directions. | 0.82421875 | 0.823960880195599 |
| `pca_state_search` | 4 | Search a low-rank PCA state subspace directly in weight space. | 0.828125 | 0.8533007334963325 |
| `pca_subspace_update` | 4 | Constrain classifier updates to a local PCA basis. | 0.81884765625 | 0.8361858190709046 |
| `prototype_distill` | 4 | Prototype reset followed by distillation from a teacher. | 0.802734375 | 0.8117359413202934 |
| `prototype_finetune` | 4 | Prototype reset followed by supervised fine-tuning. | 0.80908203125 | 0.8117359413202934 |
| `prototype_reset` | 4 | Replace classifier with support feature class prototypes. | 0.83154296875 | 0.8508557457212714 |
| `pseudo_consistency_update` | 4 | Mix pseudo-label and consistency losses in a post-hoc update. | 0.8095703125 | 0.8288508557457213 |
| `pseudo_label_update` | 4 | Classifier update on confident pseudo-labels from a teacher. | 0.83740234375 | 0.8386308068459658 |
| `quality_simplex_search` | 4 | Sample simplex states around top-quality checkpoints. | 0.8779296875 | 0.8875305623471883 |
| `sam_update` | 8 | Post-hoc SAM-style update on classifier or full model. | 0.857421875 | 0.8655256723716381 |
| `supervised_update` | 4 | Direct post-hoc supervised fit on support data. | 0.79150390625 | 0.7946210268948656 |
| `trust_region_blend` | 4 | Blend anchor with nearby checkpoints under a local trust-region rule. | 0.853515625 | 0.863080684596577 |
| `two_stage_update` | 4 | Classifier update followed by a small full-model refinement stage. | 0.8271484375 | 0.8386308068459658 |

Reading the `MOONSHOT-3` outcome:

- The best families were state-search families, especially `quality_simplex_search` and `checkpoint_line_search`.
- The worst failures were the update families that tried to do too much on too little source support, especially `bn_consistency_update`.
- `MOONSHOT-3` did not beat the best soup-based branches, but it did at least show that direct state search was not completely dead.

## 4.6 First probe-to-weight-space translations on PACS art_painting

| Method | Art full | In | Out | Same-run uniform full | Same-run uniform in | Same-run uniform out | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| `SpectralSubsetSoup` | 0.8750 | 0.8731 | 0.8826 | 0.8755 | 0.8719 | 0.8900 | translation failed to beat its own uniform subset-soup baseline on full or out |
| `GraphDiffusionSubsetSoup` | 0.8809 | 0.8780 | 0.8924 | 0.8740 | 0.8700 | 0.8900 | clear positive translation from probe space to deployable weight-space soup |
| `GibbsTopKSubsetSoup` | 0.8828 | 0.8804 | 0.8924 | 0.8745 | 0.8700 | 0.8924 | best art full in this family; beats its own uniform baseline on full and in, ties on out |

Interpretation:

- `GraphDiffusionSubsetSoup` and `GibbsTopKSubsetSoup` survived the probe-to-weight-space translation.
- `SpectralSubsetSoup` did not survive that translation cleanly; its own uniform baseline remained better on full and out.
- The strongest subset-soup results so far on `art_painting` are:
  - best art full: `GibbsTopKSubsetSoup` at `0.8828`
  - best out: tie between `GraphDiffusionSubsetSoup` and `GibbsTopKSubsetSoup` at `0.8924`
- On this bank, `GibbsTopKSubsetSoup` matches the best completed PRISM full-cap art-full value (`0.8828`), and both live subset-soup methods exceed the best completed PRISM full-cap out value (`0.8875`).

## 4.7 Full-lean Gibbs rerun on PACS art_painting

| Method | Prior | Loss | Temperature | k | Art full | In | Out | Same-run uniform full | Same-run uniform in | Same-run uniform out | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `GibbsTopKSubsetSoup` | `recency` | `supporttail` | 0.01 | 24 | 0.8833 | 0.8798 | 0.8973 | 0.8726 | 0.8682 | 0.8900 | tail-heavy Gibbs improved out strongly but moved full only slightly beyond the earlier Gibbs run |

Interpretation:

- This run showed that `out` was no longer the bottleneck in the Gibbs branch.
- Pushing harder on `supporttail` mainly bought `out`, not a decisive jump in `full`.
- That result motivated the later shift toward graph-focused ablations for the next push.

## 4.8 `GraphDiffusionSubsetSoup` 16-cell art_painting ablation

| Config | Similarity | Anchor | Alpha | Steps | k | Art full | In | Out | Delta vs same-run uniform full | Delta vs same-run uniform out | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| best full | `cos` | `bestmean` | 0.4 | 1 | 16 | 0.8843 | 0.8816 | 0.8949 | +0.0112 | +0.0049 | current best art-full subset-soup result so far |
| best out | `corr` | `bestval` | 0.6 | 1 | 24 | 0.8774 | 0.8719 | 0.8998 | +0.0044 | +0.0122 | current best out among the graph-diffusion ablation cells |

Interpretation:

- Only `2 / 16` tested graph-diffusion configurations were nonnegative against their same-run uniform baselines on both full and out.
- `bestmean` was the stronger anchor for full, while `bestval` was the stronger anchor for out.
- `k=16` beat `k=24` on the best full-oriented branch.
- `GraphDiffusionSubsetSoup` is now ahead of the earlier Gibbs runs on art full, and the best full configuration also exceeded the best completed PRISM full-cap art-full result.

## 4.9 Focused 12-cell local `GraphDiffusionSubsetSoup` sweep around the winning region

| Config | Similarity | Anchor | Alpha | Steps | k | Art full | In | Out | Delta vs same-run uniform full | Delta vs same-run uniform out | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| confirmed best full | `cos` | `bestmean` | 0.40 | 1 | 16 | 0.8843 | 0.8816 | 0.8949 | +0.0112 | +0.0049 | the previous best graph cell remained the best after the local sweep |
| near-tie full | `cos` | `bestmean` | 0.55 | 1 | 12 | 0.8838 | 0.8816 | 0.8924 | +0.0107 | +0.0049 | within about `0.05` full points of the best graph cell |
| best focused out | `cos` | `bestmean` | 0.35 | 1 | 16 | 0.8774 | 0.8719 | 0.8998 | +0.0039 | +0.0122 | matched the strongest out value seen in the earlier broader graph sweep |

Interpretation:

- The focused sweep validated a real local plateau around `cos + bestmean` rather than discovering a new winner.
- For full, the strongest region is now clearly:
  - `similarity = cos`
  - `anchor = bestmean`
  - `steps = 1`
  - `k` around `12` to `16`
  - `alpha` in the rough range `0.25` to `0.55`, with `0.40` still best
- Several nearby `cos + bestmean` cells beat their same-run uniform baselines on both full and out, which makes this branch look meaningfully more robust than it did after the first 16-cell sweep.
- The focused sweep did not crack `89.0` on full, so the remaining bottleneck is probably no longer subset discovery alone.

## 4.10 `GraphDiffusionWeightedSubsetSoup` failure study on PACS art_painting

| Weight power | Weighted full | Weighted in | Weighted out | Selected-uniform full | Selected-uniform in | Selected-uniform out | Full-bank uniform full | Full-bank uniform in | Full-bank uniform out | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `0.5` | 0.8521 | 0.8469 | 0.8729 | 0.8540 | 0.8499 | 0.8704 | 0.8730 | 0.8682 | 0.8924 | flattened diffusion weights still underperformed both controls |
| `1.0` | 0.8628 | 0.8658 | 0.8509 | 0.8745 | 0.8719 | 0.8851 | 0.8740 | 0.8694 | 0.8924 | raw diffusion weights badly hurt out |
| `1.5` | 0.8052 | 0.8017 | 0.8191 | 0.8584 | 0.8554 | 0.8704 | 0.8716 | 0.8670 | 0.8900 | sharpened weights nearly collapsed to one checkpoint |
| `2.0` | 0.8389 | 0.8371 | 0.8460 | 0.8726 | 0.8694 | 0.8851 | 0.8750 | 0.8707 | 0.8924 | extreme sharpening was catastrophic relative to both controls |

Diagnostics:

- At `weight_power=0.5`, the selected weight vector still put about `58.6%` mass on one checkpoint.
- At `weight_power=1.0`, one checkpoint took about `96.8%` of the mass.
- At `weight_power=1.5`, one checkpoint took about `99.84%` of the mass.
- At `weight_power=2.0`, one checkpoint took about `99.9926%` of the mass.
- The selected checkpoint set itself changed across powers, so the sweep was not a perfectly clean apples-to-apples comparison. Even so, every weighted run lost to the simpler controls.

Interpretation:

- The graph-selected neighborhood was the useful object; the raw diffusion magnitudes were not.
- Using diffusion mass as final soup coefficients caused collapse toward an anchor-like near-single-checkpoint solution.
- This is an explicit negative result against the story that graph diffusion weights themselves should be the deployed coefficients.

## 4.11 Strict post-hoc non-soup projection and repair pilots on PACS art_painting

| Method | Key config | Art full | In | Out | Same-run baseline | Baseline full | Baseline in | Baseline out | Notes |
|---|---|---:|---:|---:|---|---:|---:|---:|---|
| `TrajectoryNuisanceProjection` | `last_k=24, rank=4, anchor=final, beta=0.25` | 0.8320 | 0.8304 | 0.8386 | `TrajectoryNuisanceProjection-uniform` | 0.8247 | 0.8237 | 0.8289 | real local gain over its same-window uniform baseline, but far below the live leaderboard |
| `FisherRashomonProjection` | `anchor=bestmean@600, alpha=0.85, witnesses=2` | 0.8579 | 0.8578 | 0.8582 | `FisherRashomonProjection-barycenter` | 0.8813 | 0.8786 | 0.8924 | the projection hurt badly; the strong object was the witness barycenter, which is effectively another tiny soup |
| `LogitCovarianceDebias` | `anchor=final, gamma=0.0, ridge=1e-3` | 0.8213 | 0.8182 | 0.8337 | `LogitCovarianceDebias-anchor` | 0.8208 | 0.8188 | 0.8289 | the selected edit was the no-op `gamma=0`; this is effectively a null result for actual covariance debiasing |
| `JacobianCanalizationRepair` | `anchor=final, jacobian_lambda=1.0, val_loss_weight=1.0, anchor_l2=1e-4, lr=5e-4` | 0.8115 | 0.8139 | 0.8020 | `JacobianCanalizationRepair-anchor` | 0.8208 | 0.8188 | 0.8289 | the Jacobian-regularized head repair beat its matched plain repair but still damaged the anchor badly, especially on out |

Interpretation:

- `TrajectoryNuisanceProjection` is the only one of the four that produced a genuine method-level gain over its own same-run baseline.
- That gain is still small in absolute terms and nowhere near the best subset-soup or PRISM-style art-painting results.
- `FisherRashomonProjection` failed as a projection method. The within-run barycenter baseline was much stronger than the projected point, so the useful object here was the tiny witness soup, not the Fisher/Rashomon correction.
- `LogitCovarianceDebias` did not validate its core mechanism. The chosen `gamma=0.0` means the method preferred not to apply any covariance edit at all.
- `JacobianCanalizationRepair` is a negative result as a practical method. Its Jacobian term helped relative to the matched `JacobianCanalizationRepair-plain` control (`0.8115 / 0.8139 / 0.8020` versus `0.8042 / 0.8054 / 0.7995`), but both repaired heads were worse than leaving the anchor untouched at `0.8208 / 0.8188 / 0.8289`.

## 4.12 2026-04-13 selector-family sweep on PACS `art_painting`

Artifacts:

- `claude_workspace/results/selector_family_sweep_painting_mgpu4_v1`

Fixed scaffold for this sweep:

- replay bank: `erm_replay_bank_painting`
- family constructor operates on the full checkpoint bank, not a pre-selected graph-diff subset
- deployment object: uniform soup over the selected family
- deterministic BN refresh: `true`
- BN refresh view: `eval_noaug`
- BN refresh seed: `0`
- BN refresh workers: `0`

This sweep evaluates family-construction rules only. Each row builds a checkpoint family from the full replay bank, applies deterministic BN refresh on `eval_noaug`, and reports the final deployed soup result. Controls are included because they anchor the family-only comparison.

| Method | Description | Key hyperparameters | Family size | Art full | In | Out | Scheme |
|---|---|---|---:|---:|---:|---:|---|
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=prob_0.9` | 30 | 0.8813 | 0.8749 | 0.9071 | `topological_persistence_selector__feature_persistence_prob_0p9` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=second_0.0025` | 2 | 0.8813 | 0.8798 | 0.8875 | `stochastic_dominance_selector__order_slack_second_0p0025` |
| control | Uniform soup over the known 24-step graph-diff family, used only as a reference control. | `control=fixed_graphdiff24_uniform` | 24 | 0.8784 | 0.8768 | 0.8851 | `control_fixed_graphdiff24_uniform` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=second_0.001` | 6 | 0.8779 | 0.8713 | 0.9046 | `stochastic_dominance_selector__order_slack_second_0p001` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=loss_0.02` | 169 | 0.8765 | 0.8737 | 0.8875 | `dpp_repulsive_subset__feature_gainfloor_loss_0p02` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=first_0.01` | 71 | 0.8760 | 0.8737 | 0.8851 | `stochastic_dominance_selector__order_slack_first_0p01` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=prob_0.8` | 60 | 0.8755 | 0.8707 | 0.8949 | `topological_persistence_selector__feature_persistence_prob_0p8` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=prob_0.02` | 169 | 0.8755 | 0.8725 | 0.8875 | `dpp_repulsive_subset__feature_gainfloor_prob_0p02` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=loss_0.05` | 110 | 0.8755 | 0.8731 | 0.8851 | `dpp_repulsive_subset__feature_gainfloor_loss_0p05` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=prob_0.7` | 90 | 0.8750 | 0.8700 | 0.8949 | `topological_persistence_selector__feature_persistence_prob_0p7` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=loss_0.01` | 209 | 0.8750 | 0.8719 | 0.8875 | `dpp_repulsive_subset__feature_gainfloor_loss_0p01` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=loss_0.2` | 49 | 0.8750 | 0.8731 | 0.8826 | `dpp_repulsive_subset__feature_gainfloor_loss_0p2` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=prob_0.5` | 150 | 0.8745 | 0.8688 | 0.8973 | `topological_persistence_selector__feature_persistence_prob_0p5` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=prob_0.6` | 120 | 0.8745 | 0.8694 | 0.8949 | `topological_persistence_selector__feature_persistence_prob_0p6` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=prob_0.01` | 214 | 0.8745 | 0.8713 | 0.8875 | `dpp_repulsive_subset__feature_gainfloor_prob_0p01` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=prob_0.05` | 106 | 0.8745 | 0.8719 | 0.8851 | `dpp_repulsive_subset__feature_gainfloor_prob_0p05` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=loss_0.1` | 77 | 0.8745 | 0.8719 | 0.8851 | `dpp_repulsive_subset__feature_gainfloor_loss_0p1` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=prob_0.1` | 69 | 0.8740 | 0.8707 | 0.8875 | `dpp_repulsive_subset__feature_gainfloor_prob_0p1` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=first_0.005` | 78 | 0.8740 | 0.8725 | 0.8802 | `stochastic_dominance_selector__order_slack_first_0p005` |
| control | Uniform soup over the full replay bank. | `control=full_bank` | 300 | 0.8735 | 0.8688 | 0.8924 | `control_full_bank_uniform` |
| dpp_repulsive_subset | Greedy DPP MAP family with explicit subset repulsion and quality-weighted kernels. | `feature_gainfloor=prob_0.2` | 43 | 0.8735 | 0.8713 | 0.8826 | `dpp_repulsive_subset__feature_gainfloor_prob_0p2` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=first_0.001` | 90 | 0.8735 | 0.8719 | 0.8802 | `stochastic_dominance_selector__order_slack_first_0p001` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=first_0.0025` | 85 | 0.8735 | 0.8725 | 0.8778 | `stochastic_dominance_selector__order_slack_first_0p0025` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=first_0.0` | 128 | 0.8711 | 0.8700 | 0.8753 | `stochastic_dominance_selector__order_slack_first_0p0` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=loss_0.6` | 120 | 0.8701 | 0.8652 | 0.8900 | `topological_persistence_selector__feature_persistence_loss_0p6` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=32_0.0025` | 26 | 0.8696 | 0.8652 | 0.8875 | `prequential_regret_selector__blocks_penalty_32_0p0025` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=32_0.005` | 24 | 0.8687 | 0.8646 | 0.8851 | `prequential_regret_selector__blocks_penalty_32_0p005` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=32_0.01` | 20 | 0.8682 | 0.8627 | 0.8900 | `prequential_regret_selector__blocks_penalty_32_0p01` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=loss_0.5` | 150 | 0.8682 | 0.8627 | 0.8900 | `topological_persistence_selector__feature_persistence_loss_0p5` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=loss_0.9` | 30 | 0.8662 | 0.8603 | 0.8900 | `topological_persistence_selector__feature_persistence_loss_0p9` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=loss_0.7` | 90 | 0.8662 | 0.8609 | 0.8875 | `topological_persistence_selector__feature_persistence_loss_0p7` |
| topological_persistence_selector | Persistent-component selector over checkpoint geometry, using long-lived branches as family representatives. | `feature_persistence=loss_0.8` | 60 | 0.8652 | 0.8597 | 0.8875 | `topological_persistence_selector__feature_persistence_loss_0p8` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=32_0.001` | 28 | 0.8652 | 0.8609 | 0.8826 | `prequential_regret_selector__blocks_penalty_32_0p001` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=32_0.0` | 31 | 0.8628 | 0.8572 | 0.8851 | `prequential_regret_selector__blocks_penalty_32_0p0` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=second_0.0` | 49 | 0.8623 | 0.8603 | 0.8704 | `stochastic_dominance_selector__order_slack_second_0p0` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=16_0.0` | 16 | 0.8540 | 0.8475 | 0.8802 | `prequential_regret_selector__blocks_penalty_16_0p0` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=16_0.001` | 16 | 0.8540 | 0.8475 | 0.8802 | `prequential_regret_selector__blocks_penalty_16_0p001` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=16_0.0025` | 16 | 0.8540 | 0.8475 | 0.8802 | `prequential_regret_selector__blocks_penalty_16_0p0025` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=16_0.005` | 15 | 0.8516 | 0.8444 | 0.8802 | `prequential_regret_selector__blocks_penalty_16_0p005` |
| prequential_regret_selector | Dynamic-programming selector that keeps the checkpoint specialists actually used by the minimum-regret switching path. | `blocks_penalty=16_0.01` | 15 | 0.8516 | 0.8444 | 0.8802 | `prequential_regret_selector__blocks_penalty_16_0p01` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=loss_0.02` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_loss_0p02` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=prob_0.02` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_prob_0p02` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=loss_0.05` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_loss_0p05` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=prob_0.05` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_prob_0p05` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=loss_0.1` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_loss_0p1` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=prob_0.1` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_prob_0p1` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=loss_0.2` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_loss_0p2` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=prob_0.2` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_prob_0p2` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=loss_0.4` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_loss_0p4` |
| minimum_description_length | Greedy MDL family that adds checkpoints only when fit-plus-code-length improves. | `feature_beta=prob_0.4` | 1 | 0.8262 | 0.8212 | 0.8460 | `minimum_description_length__feature_beta_prob_0p4` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=second_0.005` | 1 | 0.8262 | 0.8212 | 0.8460 | `stochastic_dominance_selector__order_slack_second_0p005` |
| stochastic_dominance_selector | Distributional frontier selector based on empirical stochastic dominance instead of mean-loss ranking. | `order_slack=second_0.01` | 1 | 0.8262 | 0.8212 | 0.8460 | `stochastic_dominance_selector__order_slack_second_0p01` |
| control | Best single checkpoint under held-out validation loss. | `control=best_validation_singleton` | 1 | 0.7939 | 0.7944 | 0.7922 | `control_best_validation_singleton` |

Interpretation:

- Best run: `topological_persistence_selector__feature_persistence_prob_0p9` at `0.8813 / 0.8749 / 0.9071` with a 30-checkpoint family.
- Best compact run: `stochastic_dominance_selector__order_slack_second_0p0025` at `0.8813 / 0.8798 / 0.8875` with only 2 checkpoints: `[250, 7600]`.
- Best family-only selector beat the fixed `graphdiff24` uniform control (`0.8784 / 0.8768 / 0.8851`) but still did not beat the current best weighted `D-COLA+pool-graphdiff` result (`0.8843 / 0.8798 / 0.9022`).
- The strongest new family constructors in this sweep were topological persistence and stochastic dominance; DPP and prequential regret helped somewhat, while MDL collapsed badly on this bank.

## 4.13 2026-04-14 corrected 12x6 adaptive selector-family sweep on PACS `art_painting`

Artifacts:

- HPC output root: `/project/jje239_dgxpublicai25/jwje228/work/results/selector_family_sweep_painting_mgpu8_novel12x6_v3`

Fixed scaffold for this sweep:

- replay bank: `erm_replay_bank_painting`
- family constructor operates on the full checkpoint bank, not a pre-selected graph-diff subset
- deployment object: uniform soup over the selected family
- deterministic BN refresh: `true`
- BN refresh view: `eval_noaug`
- BN refresh seed: `0`
- BN refresh workers: `0`
- corrected deterministic source-view bank construction
- `12` selector families with `6` variants each (`72` novel schemes total)
- controls:
  - `control_full_bank_uniform`
  - `control_best_validation_singleton`
  - `control_fixed_graphdiff24_uniform`

Headline result summary:

- total successful schemes: `75 / 75`
- failed schemes: `0`
- best control baseline: `control_fixed_graphdiff24_uniform = 0.8784 / 0.8768 / 0.8851`
- novel schemes beating the best control on full: `8 / 72`

Top overall schemes:

| Rank | Family | Key hyperparameters | Family size | Art full | In | Out | Scheme |
|---|---|---|---:|---:|---:|---:|---|
| 1 | blackwell_target_set_selector | `target_epsilon=0.0` | 3 | 0.8877 | 0.8859 | 0.8949 | `blackwell_target_set_selector__target_epsilon_0p0` |
| 2 | blackwell_target_set_selector | `target_epsilon=0.01` | 3 | 0.8857 | 0.8810 | 0.9046 | `blackwell_target_set_selector__target_epsilon_0p01` |
| 3 | blackwell_target_set_selector | `target_epsilon=0.015` | 3 | 0.8857 | 0.8810 | 0.9046 | `blackwell_target_set_selector__target_epsilon_0p015` |
| 4 | version_space_compression_selector | `margin=0.5, mismatch_tolerance=0.05` | 18 | 0.8838 | 0.8798 | 0.8998 | `version_space_compression_selector__margin_eps_0p5_0p05` |
| 5 | blackwell_target_set_selector | `target_epsilon=0.005` | 4 | 0.8833 | 0.8847 | 0.8778 | `blackwell_target_set_selector__target_epsilon_0p005` |
| 6 | blackwell_target_set_selector | `target_epsilon=0.02` | 2 | 0.8823 | 0.8774 | 0.9022 | `blackwell_target_set_selector__target_epsilon_0p02` |
| 7 | version_space_compression_selector | `margin=0.6, mismatch_tolerance=0.1` | 8 | 0.8818 | 0.8780 | 0.8973 | `version_space_compression_selector__margin_eps_0p6_0p1` |
| 8 | version_space_compression_selector | `margin=0.5, mismatch_tolerance=0.1` | 8 | 0.8813 | 0.8798 | 0.8875 | `version_space_compression_selector__margin_eps_0p5_0p1` |
| 9 | version_space_compression_selector | `margin=0.6, mismatch_tolerance=0.05` | 19 | 0.8784 | 0.8761 | 0.8875 | `version_space_compression_selector__margin_eps_0p6_0p05` |
| 10 | control | `control=fixed_graphdiff24_uniform` | 24 | 0.8784 | 0.8768 | 0.8851 | `control_fixed_graphdiff24_uniform` |
| 11 | version_space_compression_selector | `margin=0.5, mismatch_tolerance=0.02` | 31 | 0.8770 | 0.8737 | 0.8900 | `version_space_compression_selector__margin_eps_0p5_0p02` |
| 12 | bootstrap_stability_selector | `subsample_fraction=0.85, frequency_threshold=0.5` | 16 | 0.8770 | 0.8755 | 0.8826 | `bootstrap_stability_selector__fraction_freq_0p85_0p5` |

Best scheme per family:

| Rank | Family | Best hyperparameters | Family size | Art full | In | Out | Best scheme |
|---|---|---|---:|---:|---:|---:|---|
| 1 | blackwell_target_set_selector | `target_epsilon=0.0` | 3 | 0.8877 | 0.8859 | 0.8949 | `blackwell_target_set_selector__target_epsilon_0p0` |
| 2 | version_space_compression_selector | `margin=0.5, mismatch_tolerance=0.05` | 18 | 0.8838 | 0.8798 | 0.8998 | `version_space_compression_selector__margin_eps_0p5_0p05` |
| 3 | bootstrap_stability_selector | `subsample_fraction=0.85, frequency_threshold=0.5` | 16 | 0.8770 | 0.8755 | 0.8826 | `bootstrap_stability_selector__fraction_freq_0p85_0p5` |
| 4 | stochastic_dominance_selector | `order=first, slack=0.01` | 51 | 0.8765 | 0.8719 | 0.8949 | `stochastic_dominance_selector__order_slack_first_0p01` |
| 5 | checkpoint_banzhaf_selector | `positive_mass_threshold=0.5` | 56 | 0.8765 | 0.8725 | 0.8924 | `checkpoint_banzhaf_selector__positive_mass_0p5` |
| 6 | dpp_repulsive_subset | `feature_view=loss, gain_floor=0.1` | 74 | 0.8760 | 0.8725 | 0.8900 | `dpp_repulsive_subset__feature_gainfloor_loss_0p1` |
| 7 | prequential_regret_selector | `n_blocks=16, switch_penalty=0.0025` | 14 | 0.8740 | 0.8682 | 0.8973 | `prequential_regret_selector__blocks_penalty_16_0p0025` |
| 8 | conformal_ambiguity_coverage_selector | `alpha=0.1, coverage_target=0.9` | 300 | 0.8735 | 0.8688 | 0.8924 | `conformal_ambiguity_coverage_selector__alpha_target_0p1_0p9` |
| 9 | topological_persistence_selector | `feature_view=prob, persistence_quantile=0.5` | 150 | 0.8730 | 0.8682 | 0.8924 | `topological_persistence_selector__feature_persistence_prob_0p5` |
| 10 | tangentprop_invariance_selector | `invariance_threshold=0.005` | 15 | 0.8589 | 0.8536 | 0.8802 | `tangentprop_invariance_selector__threshold_0p005` |
| 11 | refined_kernel_herding_selector | `feature_view=prob, residual_epsilon=0.1` | 1 | 0.8521 | 0.8536 | 0.8460 | `refined_kernel_herding_selector__feature_epsilon_prob_0p1` |
| 12 | minimum_description_length | `feature_view=loss, beta=0.02` | 1 | 0.8521 | 0.8536 | 0.8460 | `minimum_description_length__feature_beta_loss_0p02` |

Interpretation:

- `blackwell_target_set_selector` is the clear breakout result in the corrected adaptive-family sweep.
- The best adaptive family-only run is `blackwell_target_set_selector__target_epsilon_0p0` at `0.8877 / 0.8859 / 0.8949` with only `3` checkpoints.
- That result beats the fixed `graphdiff24` uniform control by about `+0.93` art-full points and is the first adaptive uniform family constructor in this project history to clearly pass the graph-diff uniform reference on full.
- `blackwell_target_set_selector` also shows a useful trade-off family: `target_epsilon in {0.01, 0.015}` reaches `0.9046` on out while staying at `0.8857` on full.
- The second strong adaptive family is `version_space_compression_selector`, whose best run reached `0.8838 / 0.8798 / 0.8998` with an 18-checkpoint family. This is below Blackwell on full but still above the graph-diff uniform control.
- `bootstrap_stability_selector` is respectable but did not beat the fixed graph-diff control.
- `stochastic_dominance_selector` and `checkpoint_banzhaf_selector` remained viable but not competitive enough to beat the best control on full.
- `conformal_ambiguity_coverage_selector` effectively collapsed to the full bank (`family_size=300`) across its best variants and therefore did not produce a useful adaptive family on this bank.
- `topological_persistence_selector` no longer reproduced the earlier `0.8813` headline from the older 53-run sweep. Under the corrected deterministic-source pipeline, its best family in this rerun was only `0.8730 / 0.8682 / 0.8924`, so the older topological headline should be treated as superseded by this corrected sweep.
- `tangentprop_invariance_selector`, `refined_kernel_herding_selector`, and `minimum_description_length` are clear negative results on this bank.

## 4.14 2026-04-15 focused family-local nonuniform weighting sweeps on PACS `art_painting`

These runs evaluated the same `65` weighting schemes on two fixed checkpoint families:

- original Blackwell family:
  - steps `[350, 1000, 13300]`
  - output root `/project/jje239_dgxpublicai25/jwje228/work/results/focused_family_weight_sweep_painting_blackwell_og_v1`
- original version-space family:
  - steps `[50, 100, 400, 550, 1400, 1600, 1700, 2350, 3250, 5650, 6100, 9050, 9100, 10500, 10600, 12600, 12700, 13450]`
  - output root `/project/jje239_dgxpublicai25/jwje228/work/results/focused_family_weight_sweep_painting_version_space_og_v1`

Methods included:

- previously exercised weighting rules:
  - `pivotality_shift_guard`
  - `redundancy_guarded_pivotality`
  - `soup_marginal_contribution`
  - `phase_canceling_pair`
- new weighting rules:
  - `blackwell_dual_target_weights`
  - `pacbayes_second_order_weights`
  - `nash_domain_bargaining_weights`
  - `ot_target_transport_weights`
- control:
  - `control_dcola_family_weights`

### 4.14.1 Original Blackwell family (`[350, 1000, 13300]`)

Best methods:

| Rank | Method | Best hyperparameters | Art full | In | Out |
|---|---|---|---:|---:|---:|
| 1 | `ot_target_transport_weights` | `ot_epsilon=0.0025` | 0.8887 | 0.8865 | 0.8973 |
| 2 | `blackwell_dual_target_weights` | `entropy_lambda=0.02` | 0.8882 | 0.8865 | 0.8949 |
| 3 | `phase_canceling_pair` | `temperature=0.01` | 0.8877 | 0.8859 | 0.8949 |
| 4 | `nash_domain_bargaining_weights` | `entropy_lambda=0.0` | 0.8877 | 0.8859 | 0.8949 |
| 5 | `control_dcola_family_weights` | control | 0.8872 | 0.8853 | 0.8949 |
| 6 | `pivotality_shift_guard` | `alpha=0.75` | 0.8857 | 0.8829 | 0.8973 |

Method-level negatives:

- `pacbayes_second_order_weights` peaked at only `0.8843 / 0.8816 / 0.8949`
- `redundancy_guarded_pivotality` was strongly harmful on this tiny 3-checkpoint family; even its best run reached only `0.8623 / 0.8603 / 0.8704`

Interpretation:

- The original uniform Blackwell family from the corrected selector sweep was `0.8877 / 0.8859 / 0.8949`.
- The best nonuniform refinement is therefore only a small lift: `+0.0010` art-full absolute (`+0.10` percentage points).
- `ot_target_transport_weights` is the top result on this family, with `blackwell_dual_target_weights` very close behind.
- Several methods effectively collapse back to the uniform result on this already-curated 3-checkpoint family, which suggests there is limited room for heuristic weighting gains once the family is this small.

### 4.14.2 Original version-space family (18 checkpoints)

Best methods:

| Rank | Method | Best hyperparameters | Art full | In | Out |
|---|---|---|---:|---:|---:|
| 1 | `redundancy_guarded_pivotality` | `alpha=0.9` | 0.8857 | 0.8822 | 0.8998 |
| 2 | `phase_canceling_pair` | `temperature=0.07` | 0.8857 | 0.8847 | 0.8900 |
| 3 | `pivotality_shift_guard` | `alpha=0.05` | 0.8848 | 0.8804 | 0.9022 |
| 4 | `soup_marginal_contribution` | `power=1.0` | 0.8848 | 0.8804 | 0.9022 |
| 5 | `blackwell_dual_target_weights` | `entropy_lambda=0.02` | 0.8843 | 0.8804 | 0.8998 |
| 6 | `ot_target_transport_weights` | `ot_epsilon=0.005` | 0.8843 | 0.8804 | 0.8998 |
| 7 | `nash_domain_bargaining_weights` | `entropy_lambda=0.0` | 0.8838 | 0.8798 | 0.8998 |
| 8 | `control_dcola_family_weights` | control | 0.8804 | 0.8749 | 0.9022 |

Method-level negatives:

- `pacbayes_second_order_weights` underperformed the stronger baselines here as well, peaking at `0.8770 / 0.8725 / 0.8949`
- the family-specific behavior is the opposite of the 3-checkpoint Blackwell case: redundancy-aware weighting is now useful rather than destructive

Interpretation:

- The original uniform version-space family from the corrected selector sweep was `0.8838 / 0.8798 / 0.8998`.
- The best weighted result is `0.8857 / 0.8822 / 0.8998`, a gain of `+0.0019` art-full absolute (`+0.19` percentage points).
- Unlike the tiny Blackwell family, the larger version-space family benefits more from explicit redundancy control and classic family-local weighting rules.
- The strongest methods here are old weighting rules, not the newly proposed ones.

### 4.14.3 Cross-family interpretation

- Across the two completed focused sweeps, the best overall weighted result is still the Blackwell family:
  - `ot_target_transport_weights__ot_epsilon_0p0025`
  - `0.8887 / 0.8865 / 0.8973`
- The Blackwell family remains the strongest object overall, but nonuniform weighting only nudges it upward slightly.
- The version-space family gains more from weighting than the Blackwell family does, but still does not surpass the best Blackwell-weighted result.
- `control_dcola_family_weights` is not the winner on either family.
- `pacbayes_second_order_weights` underperformed on both families.
- `redundancy_guarded_pivotality` is strongly family-size-dependent:
  - harmful on the tiny Blackwell family
  - best overall on the 18-checkpoint version-space family
- The planned `graphdiff24` focused weighting sweep was not run because of GPU budget constraints.

## 4.15 2026-04-15 partial live snapshot from the resumed expanded selector-family sweep on PACS `art_painting`

This snapshot comes from the resumed expanded selector sweep after disabling `blackwell_barycenter_merge_selector` and letting the run continue on the existing output root.

Important caveat:

- this is a live in-progress snapshot, not a finalized sweep summary
- ranks and family winners may still move as the remaining variants finish

Snapshot context:

- resumed output root: `/project/jje239_dgxpublicai25/jwje228/work/results/selector_family_sweep_painting_mgpu8_blackwell_controls_v1`
- barycenter-merge Blackwell family disabled/skipped for the resumed run
- baseline used in the live board delta column: `control_full_bank_uniform = 0.8735 / 0.8688 / 0.8924`

Top live schemes at the captured snapshot:

| Rank | Family | Key hyperparameters | Family size | Art full | In | Out | Scheme |
|---|---|---|---:|---:|---:|---:|---|
| 1 | stability_pool_blackwell_selector | `frequency_threshold=0.35` | 3 | 0.8877 | 0.8859 | 0.8949 | `stability_pool_blackwell_selector__frequency_threshold_0p35` |
| 2 | blackwell_clique_selector | `merge_tau=0.04` | 6 | 0.8872 | 0.8853 | 0.8949 | `blackwell_clique_selector__merge_tau_0p04` |
| 3 | version_space_compression_selector | `margin=0.5, mismatch_tolerance=0.05` | 18 | 0.8838 | 0.8798 | 0.8998 | `version_space_compression_selector__margin_eps_0p5_0p05` |
| 4 | blackwell_family_eval_selector | `target_epsilon=0.0` | 8 | 0.8828 | 0.8804 | 0.8924 | `blackwell_family_eval_selector__target_epsilon_0p0` |
| 5 | blackwell_target_set_selector | `target_epsilon=0.02` | 2 | 0.8823 | 0.8774 | 0.9022 | `blackwell_target_set_selector__target_epsilon_0p02` |
| 6 | blackwell_bootstrap_family_eval_selector | `ucb_lambda=0.25` | 16 | 0.8823 | 0.8786 | 0.8973 | `blackwell_bootstrap_family_eval_selector__ucb_lambda_0p25` |
| 7 | blackwell_residual_coverage_selector | `threshold=0.65` | 8 | 0.8794 | 0.8731 | 0.9046 | `blackwell_residual_coverage_selector__threshold_0p65` |
| 8 | blackwell_cvar_selector | `tail_alpha=0.25` | 15 | 0.8784 | 0.8737 | 0.8973 | `blackwell_cvar_selector__tail_alpha_0p25` |
| 9 | checkpoint_banzhaf_selector | `positive_mass_threshold=0.7` | 94 | 0.8750 | 0.8707 | 0.8924 | `checkpoint_banzhaf_selector__positive_mass_0p7` |
| 10 | stochastic_dominance_selector | `order=first, slack=0.0025` | 56 | 0.8750 | 0.8707 | 0.8924 | `stochastic_dominance_selector__order_slack_first_0p0025` |
| 11 | prequential_regret_selector | `n_blocks=16, switch_penalty=0.01` | 14 | 0.8740 | 0.8682 | 0.8973 | `prequential_regret_selector__blocks_penalty_16_0p01` |
| 12 | control | `control=full_bank_uniform` | 300 | 0.8735 | 0.8688 | 0.8924 | `control_full_bank_uniform` |

Current live family leaderboard at the captured snapshot:

| Rank | Family | Variants finished | Best family size | Art full | In | Out | Best scheme |
|---|---|---:|---:|---:|---:|---:|---|
| 1 | stability_pool_blackwell_selector | 2 / 6 | 3 | 0.8877 | 0.8859 | 0.8949 | `stability_pool_blackwell_selector__frequency_threshold_0p35` |
| 2 | blackwell_clique_selector | 4 / 6 | 6 | 0.8872 | 0.8853 | 0.8949 | `blackwell_clique_selector__merge_tau_0p04` |
| 3 | version_space_compression_selector | 2 / 6 | 18 | 0.8838 | 0.8798 | 0.8998 | `version_space_compression_selector__margin_eps_0p5_0p05` |
| 4 | blackwell_family_eval_selector | 4 / 6 | 8 | 0.8828 | 0.8804 | 0.8924 | `blackwell_family_eval_selector__target_epsilon_0p0` |
| 5 | blackwell_target_set_selector | 2 / 6 | 2 | 0.8823 | 0.8774 | 0.9022 | `blackwell_target_set_selector__target_epsilon_0p02` |
| 6 | blackwell_bootstrap_family_eval_selector | 4 / 6 | 16 | 0.8823 | 0.8786 | 0.8973 | `blackwell_bootstrap_family_eval_selector__ucb_lambda_0p25` |
| 7 | blackwell_residual_coverage_selector | 4 / 6 | 8 | 0.8794 | 0.8731 | 0.9046 | `blackwell_residual_coverage_selector__threshold_0p65` |
| 8 | blackwell_cvar_selector | 2 / 6 | 15 | 0.8784 | 0.8737 | 0.8973 | `blackwell_cvar_selector__tail_alpha_0p25` |
| 9 | checkpoint_banzhaf_selector | 3 / 6 | 94 | 0.8750 | 0.8707 | 0.8924 | `checkpoint_banzhaf_selector__positive_mass_0p7` |
| 10 | stochastic_dominance_selector | 2 / 6 | 56 | 0.8750 | 0.8707 | 0.8924 | `stochastic_dominance_selector__order_slack_first_0p0025` |
| 11 | prequential_regret_selector | 2 / 6 | 14 | 0.8740 | 0.8682 | 0.8973 | `prequential_regret_selector__blocks_penalty_16_0p01` |
| 12 | conformal_ambiguity_coverage_selector | 3 / 6 | 300 | 0.8735 | 0.8688 | 0.8924 | `conformal_ambiguity_coverage_selector__alpha_target_0p2_0p9` |
| 13 | bootstrap_stability_selector | 2 / 6 | 9 | 0.8726 | 0.8719 | 0.8753 | `bootstrap_stability_selector__fraction_freq_0p5_0p5` |
| 14 | graphdiff_seeded_blackwell_selector | 2 / 6 | 2 | 0.8701 | 0.8707 | 0.8680 | `graphdiff_seeded_blackwell_selector__target_epsilon_0p0` |
| 15 | blackwell_error_budget_selector | 2 / 6 | 2 | 0.8701 | 0.8707 | 0.8680 | `blackwell_error_budget_selector__threshold_0p2` |
| 16 | blackwell_bnref_family_eval_selector | 2 / 6 | 2 | 0.8657 | 0.8694 | 0.8509 | `blackwell_bnref_family_eval_selector__pool_size_8` |
| 17 | minimum_description_length | 2 / 6 | 1 | 0.8521 | 0.8536 | 0.8460 | `minimum_description_length__feature_beta_prob_0p05` |
| 18 | tangentprop_invariance_selector | 2 / 6 | 1 | 0.8120 | 0.8145 | 0.8020 | `tangentprop_invariance_selector__threshold_0p05` |
| 19 | blackwell_ambiguity_selector | 4 / 6 | 1 | 0.8047 | 0.8048 | 0.8044 | `blackwell_ambiguity_selector__alpha_0p3` |

Interpretation of this live snapshot:

- The strongest in-progress family at the captured point was `stability_pool_blackwell_selector`, reaching `0.8877 / 0.8859 / 0.8949` with a 3-checkpoint family.
- `blackwell_clique_selector` was close behind at `0.8872 / 0.8853 / 0.8949`, but it remained both more restrictive and more computationally expensive than the simpler target-set Blackwell family from the earlier corrected 12x6 sweep.
- `version_space_compression_selector` remained alive and competitive at `0.8838 / 0.8798 / 0.8998`.
- Several runtime-heavy Blackwell variants were clearly competitive on full in this partial snapshot:
  - `blackwell_family_eval_selector`
  - `blackwell_bootstrap_family_eval_selector`
  - `blackwell_cvar_selector`
- `blackwell_residual_coverage_selector` remained one of the more attractive source-statistic Blackwell variants because it pushed `out` to `0.9046` while keeping full at `0.8794`.
- `conformal_ambiguity_coverage_selector` again collapsed to the full bank and therefore did not produce a useful compact adaptive family.
- `blackwell_ambiguity_selector`, `tangentprop_invariance_selector`, and `minimum_description_length` continued to look like clear negatives on this bank.

## 4.16 2026-04-15 crossed selector+weight sweep on PACS `art_painting`

This completed sweep crossed `4` selector schemes with `8` fixed weight schemes for `32` total selector+weight combinations.

Artifacts:

- output root: `/project/jje239_dgxpublicai25/jwje228/work/results/selector_weight_cross_sweep_painting_mgpu8_v3`

Selectors crossed:

- `blackwell_target_set_selector__target_epsilon_0p0`
- `version_space_compression_selector__margin_eps_0p5_0p05`
- `blackwell_residual_coverage_selector__threshold_0p65`
- `stability_pool_blackwell_selector__frequency_threshold_0p35`

Weights crossed:

- `pivotality_shift_guard__alpha_0p75`
- `redundancy_guarded_pivotality__alpha_0p9`
- `soup_marginal_contribution__power_1p0`
- `phase_canceling_pair__temperature_0p07`
- `blackwell_dual_target_weights__entropy_lambda_0p02`
- `ot_target_transport_weights__ot_epsilon_0p0025`
- `nash_domain_bargaining_weights__entropy_lambda_0p0`
- `control_dcola_family_weights__control_1`

Top overall combinations:

| Rank | Selector | Weight scheme | Family size | Art full | In | Out |
|---|---|---|---:|---:|---:|---:|
| 1 | `blackwell_target_set_selector__target_epsilon_0p0` | `ot_target_transport_weights__ot_epsilon_0p0025` | 3 | 0.8887 | 0.8865 | 0.8973 |
| 2 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `ot_target_transport_weights__ot_epsilon_0p0025` | 3 | 0.8887 | 0.8865 | 0.8973 |
| 3 | `blackwell_target_set_selector__target_epsilon_0p0` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 3 | 0.8882 | 0.8865 | 0.8949 |
| 4 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 3 | 0.8882 | 0.8865 | 0.8949 |
| 5 | `blackwell_target_set_selector__target_epsilon_0p0` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 3 | 0.8877 | 0.8859 | 0.8949 |
| 6 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 3 | 0.8877 | 0.8859 | 0.8949 |
| 7 | `blackwell_target_set_selector__target_epsilon_0p0` | `phase_canceling_pair__temperature_0p07` | 3 | 0.8872 | 0.8853 | 0.8949 |
| 8 | `blackwell_target_set_selector__target_epsilon_0p0` | `control_dcola_family_weights__control_1` | 3 | 0.8872 | 0.8853 | 0.8949 |
| 9 | `version_space_compression_selector__margin_eps_0p5_0p05` | `redundancy_guarded_pivotality__alpha_0p9` | 18 | 0.8857 | 0.8822 | 0.8998 |
| 10 | `version_space_compression_selector__margin_eps_0p5_0p05` | `phase_canceling_pair__temperature_0p07` | 18 | 0.8857 | 0.8847 | 0.8900 |

Family-level interpretation inside the crossed sweep:

- `blackwell_target_set_selector__target_epsilon_0p0` remained the strongest selector family overall once crossed with the curated weight methods.
- `stability_pool_blackwell_selector__frequency_threshold_0p35` produced numerically identical top rows to the Blackwell target-set winner under several weight methods, which strongly suggests that on this bank it is selecting the same or functionally equivalent 3-checkpoint family.
- `version_space_compression_selector__margin_eps_0p5_0p05` remained the strongest clearly distinct alternative family, with `redundancy_guarded_pivotality__alpha_0p9` as its best weight rule.
- `blackwell_residual_coverage_selector__threshold_0p65` remained interesting for out-oriented behavior, but did not compete for the best full score.

Weight-rule interpretation inside the crossed sweep:

- On the tiny 3-checkpoint Blackwell family, the new Blackwell-aligned weighting methods stayed strongest:
  - `ot_target_transport_weights`
  - `blackwell_dual_target_weights`
  - `nash_domain_bargaining_weights`
- On the larger version-space family, the older family-local rules remained stronger:
  - `redundancy_guarded_pivotality`
  - `phase_canceling_pair`
  - `soup_marginal_contribution`
  - `pivotality_shift_guard`
- `redundancy_guarded_pivotality` stayed sharply family-size-dependent:
  - strong on the 18-checkpoint version-space family
  - strongly harmful on the tiny 3-checkpoint Blackwell family

Bottom line from the crossed sweep:

- The crossed selector+weight run did not discover a new regime beyond the focused Blackwell-family weighting sweep.
- It mostly confirmed the same headline result:
  - `blackwell_target_set_selector__target_epsilon_0p0`
  - plus `ot_target_transport_weights__ot_epsilon_0p0025`
  - yielding `0.8887 / 0.8865 / 0.8973`
- The best distinct non-Blackwell branch in the crossed sweep remained:
  - `version_space_compression_selector__margin_eps_0p5_0p05`
  - plus `redundancy_guarded_pivotality__alpha_0p9`
  - yielding `0.8857 / 0.8822 / 0.8998`

## 4.17 2026-04-15 completed crossed selector+weight sweep on PACS `cartoon`

This completed sweep uses the same `4 x 8` selector+weight design as the `art_painting` cross, but evaluated on the PACS `cartoon` split instead.

Important caveat:

- this split produced singleton families for both `blackwell_target_set_selector__target_epsilon_0p0` and `stability_pool_blackwell_selector__frequency_threshold_0p35`
- three old weighting rules are not singleton-safe in the current implementation:
  - `pivotality_shift_guard__alpha_0p75`
  - `redundancy_guarded_pivotality__alpha_0p9`
  - `soup_marginal_contribution__power_1p0`
- those rows produced `NaN` support/validation loss and near-chance accuracy, so they should be treated as implementation-affected diagnostic rows rather than clean empirical comparisons

Top completed combinations on `cartoon`:

| Rank | Selector | Weight scheme | Family size | Cartoon full | In | Out | Support loss | Validation loss |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `version_space_compression_selector__margin_eps_0p5_0p05` | `pivotality_shift_guard__alpha_0p75` | 21 | 0.8400 | 0.8406 | 0.8376 | 0.0831 | 0.1182 |
| 2 | `version_space_compression_selector__margin_eps_0p5_0p05` | `soup_marginal_contribution__power_1p0` | 21 | 0.8383 | 0.8385 | 0.8376 | 0.0833 | 0.1179 |
| 3 | `version_space_compression_selector__margin_eps_0p5_0p05` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 21 | 0.8383 | 0.8385 | 0.8376 | 0.0814 | 0.1145 |
| 4 | `version_space_compression_selector__margin_eps_0p5_0p05` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 21 | 0.8375 | 0.8380 | 0.8355 | 0.0810 | 0.1137 |
| 5 | `version_space_compression_selector__margin_eps_0p5_0p05` | `ot_target_transport_weights__ot_epsilon_0p0025` | 21 | 0.8375 | 0.8385 | 0.8333 | 0.0845 | 0.1153 |
| 6 | `version_space_compression_selector__margin_eps_0p5_0p05` | `phase_canceling_pair__temperature_0p07` | 21 | 0.8375 | 0.8390 | 0.8312 | 0.0827 | 0.1390 |
| 7 | `blackwell_residual_coverage_selector__threshold_0p65` | `pivotality_shift_guard__alpha_0p75` | 8 | 0.8370 | 0.8358 | 0.8419 | 0.0909 | 0.1102 |
| 8 | `blackwell_residual_coverage_selector__threshold_0p65` | `soup_marginal_contribution__power_1p0` | 8 | 0.8370 | 0.8358 | 0.8419 | 0.0895 | 0.1057 |
| 9 | `blackwell_residual_coverage_selector__threshold_0p65` | `phase_canceling_pair__temperature_0p07` | 8 | 0.8302 | 0.8305 | 0.8291 | 0.0848 | 0.0999 |
| 10 | `blackwell_residual_coverage_selector__threshold_0p65` | `ot_target_transport_weights__ot_epsilon_0p0025` | 8 | 0.8294 | 0.8289 | 0.8312 | 0.0864 | 0.0958 |
| 11 | `version_space_compression_selector__margin_eps_0p5_0p05` | `redundancy_guarded_pivotality__alpha_0p9` | 21 | 0.8289 | 0.8294 | 0.8269 | 0.0769 | 0.1081 |
| 12 | `version_space_compression_selector__margin_eps_0p5_0p05` | `control_dcola_family_weights__control_1` | 21 | 0.8285 | 0.8289 | 0.8269 | 0.0825 | 0.0996 |
| 13 | `blackwell_residual_coverage_selector__threshold_0p65` | `redundancy_guarded_pivotality__alpha_0p9` | 8 | 0.8247 | 0.8252 | 0.8226 | 0.0839 | 0.0931 |
| 14 | `blackwell_residual_coverage_selector__threshold_0p65` | `control_dcola_family_weights__control_1` | 8 | 0.8238 | 0.8257 | 0.8162 | 0.0830 | 0.0854 |
| 15 | `blackwell_residual_coverage_selector__threshold_0p65` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 8 | 0.8234 | 0.8230 | 0.8248 | 0.0829 | 0.0900 |
| 16 | `blackwell_residual_coverage_selector__threshold_0p65` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 8 | 0.8225 | 0.8220 | 0.8248 | 0.0827 | 0.0897 |
| 17 | `blackwell_target_set_selector__target_epsilon_0p0` | `phase_canceling_pair__temperature_0p07` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 18 | `blackwell_target_set_selector__target_epsilon_0p0` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 19 | `blackwell_target_set_selector__target_epsilon_0p0` | `ot_target_transport_weights__ot_epsilon_0p0025` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 20 | `blackwell_target_set_selector__target_epsilon_0p0` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 21 | `blackwell_target_set_selector__target_epsilon_0p0` | `control_dcola_family_weights__control_1` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 22 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `phase_canceling_pair__temperature_0p07` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 23 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 24 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `ot_target_transport_weights__ot_epsilon_0p0025` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 25 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 26 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `control_dcola_family_weights__control_1` | 1 | 0.8020 | 0.8049 | 0.7906 | 0.0947 | 0.0926 |
| 27 | `blackwell_target_set_selector__target_epsilon_0p0` | `pivotality_shift_guard__alpha_0p75` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |
| 28 | `blackwell_target_set_selector__target_epsilon_0p0` | `redundancy_guarded_pivotality__alpha_0p9` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |
| 29 | `blackwell_target_set_selector__target_epsilon_0p0` | `soup_marginal_contribution__power_1p0` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |
| 30 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `pivotality_shift_guard__alpha_0p75` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |
| 31 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `redundancy_guarded_pivotality__alpha_0p9` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |
| 32 | `stability_pool_blackwell_selector__frequency_threshold_0p35` | `soup_marginal_contribution__power_1p0` | 1 | 0.1660 | 0.1706 | 0.1474 | `NaN` | `NaN` |

Interpretation:

- On `cartoon`, the strongest completed crossed branch is `version_space_compression_selector__margin_eps_0p5_0p05`, whose best row reaches `0.8400 / 0.8406 / 0.8376`.
- `blackwell_residual_coverage_selector__threshold_0p65` is the strongest non-singleton Blackwell-family branch on this split, and with `pivotality_shift_guard__alpha_0p75` or `soup_marginal_contribution__power_1p0` it reaches `0.8370 / 0.8358 / 0.8419`, much closer to the version-space leader than the earlier partial snapshot suggested.
- `blackwell_target_set_selector__target_epsilon_0p0` and `stability_pool_blackwell_selector__frequency_threshold_0p35` both collapse to singleton families on this split in the completed run.
- The singleton-family rows with `phase_canceling_pair`, `blackwell_dual_target_weights`, `ot_target_transport_weights`, `nash_domain_bargaining_weights`, and `control_dcola_family_weights` all reduce to the same effective 1-checkpoint model, which is why they are numerically identical.
- The near-chance singleton rows at ranks `27-32` are not evidence against the selector itself; they reflect the current singleton-unsafety of the leave-one-out-derived weighting rules listed above.

## 4.18 2026-04-16 version-space-only selector+weight sweeps on PACS `sketch` and `photo`

These completed sweeps froze the selector to `version_space_compression_selector__margin_eps_0p5_0p05` and crossed it with the same `8` curated weighting rules used in the earlier selector+weight crossings. This was run on the two PACS splits not covered by the completed `art_painting` and `cartoon` crossed results.

Artifacts:

- sketch output root: `/project/jje239_dgxpublicai25/jwje228/work/results/selector_weight_cross_sweep_sketch_versionspace_only_v1`
- photo output root: `/project/jje239_dgxpublicai25/jwje228/work/results/selector_weight_cross_sweep_photo_versionspace_only_v1`

Weights crossed:

- `pivotality_shift_guard__alpha_0p75`
- `redundancy_guarded_pivotality__alpha_0p9`
- `soup_marginal_contribution__power_1p0`
- `phase_canceling_pair__temperature_0p07`
- `blackwell_dual_target_weights__entropy_lambda_0p02`
- `ot_target_transport_weights__ot_epsilon_0p0025`
- `nash_domain_bargaining_weights__entropy_lambda_0p0`
- `control_dcola_family_weights__control_1`

Completed `sketch` results:

| Rank | Selector | Weight scheme | Family size | Sketch full | In | Out |
|---|---|---|---:|---:|---:|---:|
| 1 | `version_space_compression_selector__margin_eps_0p5_0p05` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 25 | 0.8430 | 0.8403 | 0.8535 |
| 2 | `version_space_compression_selector__margin_eps_0p5_0p05` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 25 | 0.8430 | 0.8403 | 0.8535 |
| 3 | `version_space_compression_selector__margin_eps_0p5_0p05` | `redundancy_guarded_pivotality__alpha_0p9` | 25 | 0.8425 | 0.8397 | 0.8535 |
| 4 | `version_space_compression_selector__margin_eps_0p5_0p05` | `pivotality_shift_guard__alpha_0p75` | 25 | 0.8414 | 0.8400 | 0.8471 |
| 5 | `version_space_compression_selector__margin_eps_0p5_0p05` | `soup_marginal_contribution__power_1p0` | 25 | 0.8412 | 0.8391 | 0.8497 |
| 6 | `version_space_compression_selector__margin_eps_0p5_0p05` | `ot_target_transport_weights__ot_epsilon_0p0025` | 25 | 0.8407 | 0.8375 | 0.8535 |
| 7 | `version_space_compression_selector__margin_eps_0p5_0p05` | `phase_canceling_pair__temperature_0p07` | 25 | 0.8290 | 0.8267 | 0.8382 |
| 8 | `version_space_compression_selector__margin_eps_0p5_0p05` | `control_dcola_family_weights__control_1` | 25 | 0.8239 | 0.8222 | 0.8306 |

Completed `photo` results:

| Rank | Selector | Weight scheme | Family size | Photo full | In | Out |
|---|---|---|---:|---:|---:|---:|
| 1 | `version_space_compression_selector__margin_eps_0p5_0p05` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 27 | 0.9719 | 0.9701 | 0.9790 |
| 2 | `version_space_compression_selector__margin_eps_0p5_0p05` | `pivotality_shift_guard__alpha_0p75` | 27 | 0.9713 | 0.9686 | 0.9820 |
| 3 | `version_space_compression_selector__margin_eps_0p5_0p05` | `control_dcola_family_weights__control_1` | 27 | 0.9713 | 0.9708 | 0.9731 |
| 4 | `version_space_compression_selector__margin_eps_0p5_0p05` | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 27 | 0.9707 | 0.9686 | 0.9790 |
| 5 | `version_space_compression_selector__margin_eps_0p5_0p05` | `redundancy_guarded_pivotality__alpha_0p9` | 27 | 0.9701 | 0.9686 | 0.9760 |
| 6 | `version_space_compression_selector__margin_eps_0p5_0p05` | `soup_marginal_contribution__power_1p0` | 27 | 0.9701 | 0.9686 | 0.9760 |
| 7 | `version_space_compression_selector__margin_eps_0p5_0p05` | `phase_canceling_pair__temperature_0p07` | 27 | 0.9689 | 0.9671 | 0.9760 |
| 8 | `version_space_compression_selector__margin_eps_0p5_0p05` | `ot_target_transport_weights__ot_epsilon_0p0025` | 27 | 0.9683 | 0.9678 | 0.9701 |

Cross-split version-space summary:

| Split | Best fixed selector+weight row | Family size | Full | In | Out |
|---|---|---:|---:|---:|---:|
| `art_painting` | `redundancy_guarded_pivotality__alpha_0p9` / `phase_canceling_pair__temperature_0p07` | 18 | 0.8857 | varies | varies |
| `cartoon` | `pivotality_shift_guard__alpha_0p75` | 21 | 0.8400 | 0.8406 | 0.8376 |
| `sketch` | `blackwell_dual_target_weights__entropy_lambda_0p02` / `nash_domain_bargaining_weights__entropy_lambda_0p0` | 25 | 0.8430 | 0.8403 | 0.8535 |
| `photo` | `blackwell_dual_target_weights__entropy_lambda_0p02` | 27 | 0.9719 | 0.9701 | 0.9790 |

Fixed-weigher comparison for `version_space_compression_selector__margin_eps_0p5_0p05` across all four PACS splits:

| Weight scheme | Art full | Cartoon full | Sketch full | Photo full | Mean full |
|---|---:|---:|---:|---:|---:|
| `pivotality_shift_guard__alpha_0p75` | 0.8843 | 0.8400 | 0.8414 | 0.9713 | 0.8843 |
| `blackwell_dual_target_weights__entropy_lambda_0p02` | 0.8843 | 0.8375 | 0.8430 | 0.9719 | 0.8842 |
| `nash_domain_bargaining_weights__entropy_lambda_0p0` | 0.8838 | 0.8383 | 0.8430 | 0.9707 | 0.8840 |
| `soup_marginal_contribution__power_1p0` | 0.8848 | 0.8383 | 0.8412 | 0.9701 | 0.8836 |
| `ot_target_transport_weights__ot_epsilon_0p0025` | 0.8833 | 0.8375 | 0.8407 | 0.9683 | 0.8825 |
| `redundancy_guarded_pivotality__alpha_0p9` | 0.8857 | 0.8289 | 0.8425 | 0.9701 | 0.8818 |
| `phase_canceling_pair__temperature_0p07` | 0.8857 | 0.8375 | 0.8290 | 0.9689 | 0.8803 |
| `control_dcola_family_weights__control_1` | 0.8804 | 0.8285 | 0.8239 | 0.9713 | 0.8760 |

Interpretation:

- `version_space_compression_selector__margin_eps_0p5_0p05` produced non-singleton families on all four PACS splits: size `18` on `art_painting`, size `21` on `cartoon`, size `25` on `sketch`, and size `27` on `photo`.
- The strongest fixed weigher by mean full accuracy is `pivotality_shift_guard__alpha_0p75`, but its margin over `blackwell_dual_target_weights__entropy_lambda_0p02` is negligible (`0.8843` vs `0.8842`).
- `blackwell_dual_target_weights__entropy_lambda_0p02` is the cleaner and more efficient fixed-weighting story: it wins or ties the best version-space result on `sketch`, wins `photo`, and remains close on `art_painting` and `cartoon`.
- Broad method development and search should be treated as paused after these results. Further work should be reporting, verification, bug cleanup, and presentation unless a specific reviewer-critical issue requires one targeted validation.

# 5. Current Empirical Conclusions

## 5.1 PRISM

- best clean domain-label-free PACS average in the current 4-split sweep: `PRISM`
- current `PRISM` vs `SWAD` margin is real but small
- current evidence still does not justify saying `PRISM` is decisively better than `SWAD`
- the best completed full-cap `art_painting` PRISM grid cell so far is `art_a015_e002_t002_m3` at `88.28`

## 5.2 SWING

- `SWING` is not invalid in the sense of broken math or broken implementation
- but the current `SWING` formulation has failed the more important empirical test: it does not clearly and consistently beat `SWING-uniform`
- best raw `SWING`: `0.8818` from `swing_art_rank2_auto_bn512`
- best explicit `SWING-uniform`: `0.8784` from `swing_art_rank3_tau1e3`
- best explicit within-run `SWING > SWING-uniform` gap: `+0.0034` from `swing_art_rank2_loc18`

That `+0.0034` gap is too small, especially combined with the multiple runs where `SWING` lost to the uniform safe-pool baseline.

## 5.3 Subset-soup follow-ups

- `GraphDiffusionSubsetSoup` is currently the clearest alive follow-up branch.
- The best current graph configuration is `cos + bestmean + alpha=0.4 + steps=1 + k=16`, which reached `0.8843 / 0.8816 / 0.8949`.
- The focused local graph sweep found a small plateau around that cell, but did not improve on it.
- `GibbsTopKSubsetSoup` is also alive; the full-lean rerun reached `0.8833 / 0.8798 / 0.8973`, which confirmed that the Gibbs branch can push out strongly.
- `SpectralSubsetSoup` should not be treated as a lead branch unless a later sweep materially changes the current result.
- The important methodological update is that at least two probe-derived sparse subset ideas translated into real deployable weight-space soups without collapsing back to their same-run uniform baselines.
- The graph branch is still configuration-sensitive, but the focused sweep showed a more stable winning pocket around `cos + bestmean`.
- `GraphDiffusionWeightedSubsetSoup` is now a completed negative result: raw diffusion magnitudes collapsed toward a single checkpoint and consistently underperformed both selected-uniform and full-bank uniform controls.
- So the remaining evidence supports graph diffusion as a subset finder, not as a final coefficient generator.
- The best completed subset-soup object is still the plain uniform soup over the selected graph-diffusion or Gibbs subset, not a weighted variant.

## 5.4 Strict non-soup projection pilots

- `TrajectoryNuisanceProjection` is the only strict non-soup pilot that showed a real within-run gain over its own local baseline.
- Even that result is not competitive with the best live subset-soup branch, so it should be treated as a weak survival signal, not a new mainline.
- `FisherRashomonProjection` is a methodological failure in its current form: the projection underperformed its own barycenter baseline by a large margin.
- `LogitCovarianceDebias` is effectively a null result for the debiasing idea itself, because the selected edit was the no-op `gamma=0.0`.
- `JacobianCanalizationRepair` also failed as a practical post-hoc method in its first instantiation: the Jacobian penalty improved over the matched plain head repair, but the untouched anchor was still clearly better than either repaired head.
- Taken together, these four pilots do not change the current leaderboard or the current main conclusion that the strongest completed branch remains the graph/Gibbs subset-soup family.

## 5.5 Final decision on current SWING

- Stop treating the current `SWING` formulation as the headline method.
- Keep it as:
  - a completed negative-result branch
  - an ablation against future methods
  - a useful source of infrastructure: safe-pool construction, diagnostics, replay reporting, and the `SWING-uniform` baseline

## 5.6 Adaptive family selection after the corrected 12x6 sweep

- The strongest adaptive family-only selector in the corrected deterministic-source sweep is now `blackwell_target_set_selector`.
- The best adaptive family-only run is `blackwell_target_set_selector__target_epsilon_0p0` at `0.8877 / 0.8859 / 0.8949` with a family of only `3` checkpoints.
- This is methodologically important because it beats the fixed `graphdiff24` uniform control (`0.8784 / 0.8768 / 0.8851`) without using a hand-chosen family size like `k=24`.
- On full accuracy, that Blackwell family-only result also edges past the best completed deterministic graphdiff-weighted cross result (`0.8867` full), although the graphdiff-weighted branch still has stronger out-oriented variants.
- The second strongest adaptive family in the corrected sweep is `version_space_compression_selector` at `0.8838 / 0.8798 / 0.8998`.
- The old selector-family headline from `2026-04-13` should no longer be treated as current. In particular, `topological_persistence_selector` did not survive the corrected deterministic-source rerun and should be treated as superseded by the new adaptive-family results.
- The current best family-selection story is therefore:
  - exploratory fixed-family upper bound: weighted graph-diffusion families
  - strongest clean adaptive family-only result: `blackwell_target_set_selector`
  - strongest runner-up adaptive family: `version_space_compression_selector`

## 5.7 Family-local weighting after the focused Blackwell and version-space sweeps

- The best completed weighted result on the original Blackwell family is `0.8887 / 0.8865 / 0.8973` from `ot_target_transport_weights__ot_epsilon_0p0025`.
- That is only a small gain over the original uniform Blackwell family (`0.8877 / 0.8859 / 0.8949`), so weighting on the 3-checkpoint Blackwell family should be treated as a refinement, not a new regime change.
- The best completed weighted result on the original version-space family is `0.8857 / 0.8822 / 0.8998` from `redundancy_guarded_pivotality__alpha_0p9`.
- The version-space family benefits more from weighting than the Blackwell family does, but still does not overtake the best Blackwell-weighted result.
- The new weighting methods are more promising on the Blackwell family than on the version-space family:
  - `ot_target_transport_weights` is the winner on Blackwell
  - `blackwell_dual_target_weights` is a close runner-up on Blackwell
- The older weighting rules remain stronger on the version-space family:
  - `redundancy_guarded_pivotality`
  - `phase_canceling_pair`
  - `pivotality_shift_guard`
  - `soup_marginal_contribution`
- `pacbayes_second_order_weights` is a negative empirical result on both completed family-local sweeps.
- The current practical recommendation after these two completed focused sweeps is:
  - if the goal is the single strongest completed result, keep the Blackwell family and use either uniform averaging or the best OT-weighted variant
  - if the goal is to study which families actually respond to weighting, the version-space family is the more informative object
  - for the tiny 3-checkpoint Blackwell family, an exact simplex search is a more natural next step than yet another large heuristic weighting sweep

## 5.8 Selector+weight crossing after the completed 4x8 sweep

- The completed crossed selector+weight sweep confirms that the overall best combined selector+weight object is still:
  - `blackwell_target_set_selector__target_epsilon_0p0`
  - plus `ot_target_transport_weights__ot_epsilon_0p0025`
  - at `0.8887 / 0.8865 / 0.8973`
- `stability_pool_blackwell_selector__frequency_threshold_0p35` should not be treated as a clearly distinct winner unless later inspection shows it is selecting a genuinely different family. The identical metrics across multiple weight methods strongly suggest it is reproducing the same effective 3-checkpoint Blackwell family on this bank.
- The strongest clearly distinct alternative branch remains:
  - `version_space_compression_selector__margin_eps_0p5_0p05`
  - plus `redundancy_guarded_pivotality__alpha_0p9`
  - at `0.8857 / 0.8822 / 0.8998`
- The crossed sweep therefore reinforces, rather than overturns, the current recommendation:
  - use the Blackwell target-set family as the main adaptive selector result
  - if nonuniform weighting is allowed, use the OT-weighted variant as the strongest completed combined method
  - if the next goal is more improvement rather than more heuristics, the most natural next experiment is an exact simplex search over the 3-checkpoint Blackwell family

## 5.9 Cartoon selector+weight cross-sweep caveat

- The PACS `cartoon` crossed selector+weight leaderboard should be read separately from the `art_painting` sweep and not compared directly on absolute accuracy.
- On the completed `cartoon` leaderboard, the strongest branch is `version_space_compression_selector__margin_eps_0p5_0p05`, not the Blackwell target-set family.
- `blackwell_target_set_selector__target_epsilon_0p0` and `stability_pool_blackwell_selector__frequency_threshold_0p35` both collapsed to singleton families on this split.
- The identical singleton rows with `phase_canceling_pair`, `blackwell_dual_target_weights`, `ot_target_transport_weights`, `nash_domain_bargaining_weights`, and `control_dcola_family_weights` are expected: all of those effectively reduce to the same single checkpoint.
- The `0.1660` rows with `NaN` support and validation loss are not trustworthy empirical evidence. They are caused by a known singleton-family bug in the leave-one-out-derived weighting rules:
  - `pivotality_shift_guard`
  - `redundancy_guarded_pivotality`
  - `soup_marginal_contribution`

## 5.10 Stop-search recommendation after full version-space PACS coverage

- Broad method development and search are paused for the time being.
- The practical reporting candidate across PACS is now `version_space_compression_selector__margin_eps_0p5_0p05` with one fixed weigher.
- The best mean fixed weigher over the four recorded PACS splits is `pivotality_shift_guard__alpha_0p75`, but its margin over `blackwell_dual_target_weights__entropy_lambda_0p02` is negligible.
- If the final writeup prioritizes pure mean score, report `pivotality_shift_guard__alpha_0p75`.
- If the final writeup prioritizes a cleaner and more efficient method story, report `blackwell_dual_target_weights__entropy_lambda_0p02`.
- Additional work should be limited to verification, bug cleanup, and presentation, not new selector/weigher exploration.
