---
title: Results Ledger
description: Comprehensive ledger and method catalog for completed baselines, soups, probe batteries, strict post-hoc projection pilots, and replay-visible methods in the repo.
created: 2026-03-30 22:05
last_modified: 2026-04-05 14:52
last_modified_by: agent
status: active
related_files: claude_workspace/results/swing_lessons_learned.md, domaingen/posthoc/swing.py, domaingen/posthoc/tsf.py, domaingen/posthoc/shotgun.py, domaingen/posthoc/moonshot_2.py, domaingen/posthoc/subset_soups.py
key_functions:
  - Preserve completed PRISM, SWING, TSF, probe-battery, subset-soup, and strict post-hoc projection empirical results in one place
  - Describe what each tested method actually does mechanically, not just what score it reached
  - Track which replay-visible methods in the repo have and have not been empirically exercised
  - Remove placeholder-only entries such as TBD, running, queued, and submitted rows
  - Make the current empirical conclusions easy to recover later
latest_change: Expanded the ledger into a comprehensive project record with method descriptions, probe-suite implementation notes, replay-visible method inventory, and the missing weighted-graph failure branch.
change_log:
  - 2026-03-30 22:05: Initial PRISM-only ledger created
  - 2026-04-01 09:40: Initial SWING-only ledger created
  - 2026-04-01 12:20: Merged PRISM and SWING ledgers into one completed-results-only ledger
  - 2026-04-04 00:35: Added SpectralSubsetSoup, GraphDiffusionSubsetSoup, and GibbsTopKSubsetSoup replay results on PACS art_painting
  - 2026-04-05 18:05: Added TSF, SHOTGUN, MOONSHOT-2, the full-lean Gibbs rerun, and the 16-cell graph-diffusion ablation on PACS art_painting
  - 2026-04-05 19:10: Added the focused 12-cell local graph-diffusion sweep and updated the subset-soup conclusions
  - 2026-04-05 20:05: Added TrajectoryNuisanceProjection, FisherRashomonProjection, and LogitCovarianceDebias pilot runs on PACS art_painting
  - 2026-04-05 14:52: Added replay-visible method inventory, detailed SHOTGUN/MOONSHOT suite descriptions, and the GraphDiffusionWeightedSubsetSoup failure study
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
| `trajectory_nuisance_projection` | TrajectoryNuisanceProjection | Estimate unstable low-rank late-trajectory directions and shrink them in a single final state. | tested; small local gain only |
| `fisher_rashomon_projection` | FisherRashomonProjection | Move from an anchor toward a witness barycenter under a Fisher-style trust metric. | tested; projection lost to barycenter baseline |
| `logit_covariance_debias` | LogitCovarianceDebias | Apply a closed-form affine correction to the final classifier using support logit covariance. | tested; null result |

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

## 4.11 First strict post-hoc non-soup projection pilots on PACS art_painting

| Method | Key config | Art full | In | Out | Same-run baseline | Baseline full | Baseline in | Baseline out | Notes |
|---|---|---:|---:|---:|---|---:|---:|---:|---|
| `TrajectoryNuisanceProjection` | `last_k=24, rank=4, anchor=final, beta=0.25` | 0.8320 | 0.8304 | 0.8386 | `TrajectoryNuisanceProjection-uniform` | 0.8247 | 0.8237 | 0.8289 | real local gain over its same-window uniform baseline, but far below the live leaderboard |
| `FisherRashomonProjection` | `anchor=bestmean@600, alpha=0.85, witnesses=2` | 0.8579 | 0.8578 | 0.8582 | `FisherRashomonProjection-barycenter` | 0.8813 | 0.8786 | 0.8924 | the projection hurt badly; the strong object was the witness barycenter, which is effectively another tiny soup |
| `LogitCovarianceDebias` | `anchor=final, gamma=0.0, ridge=1e-3` | 0.8213 | 0.8182 | 0.8337 | `LogitCovarianceDebias-anchor` | 0.8208 | 0.8188 | 0.8289 | the selected edit was the no-op `gamma=0`; this is effectively a null result for actual covariance debiasing |

Interpretation:

- `TrajectoryNuisanceProjection` is the only one of the three that produced a genuine method-level gain over its own same-run baseline.
- That gain is still small in absolute terms and nowhere near the best subset-soup or PRISM-style art-painting results.
- `FisherRashomonProjection` failed as a projection method. The within-run barycenter baseline was much stronger than the projected point, so the useful object here was the tiny witness soup, not the Fisher/Rashomon correction.
- `LogitCovarianceDebias` did not validate its core mechanism. The chosen `gamma=0.0` means the method preferred not to apply any covariance edit at all.

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
- Taken together, these three pilots do not change the current leaderboard or the current main conclusion that the strongest completed branch remains the graph/Gibbs subset-soup family.

## 5.5 Final decision on current SWING

- Stop treating the current `SWING` formulation as the headline method.
- Keep it as:
  - a completed negative-result branch
  - an ablation against future methods
  - a useful source of infrastructure: safe-pool construction, diagnostics, replay reporting, and the `SWING-uniform` baseline
