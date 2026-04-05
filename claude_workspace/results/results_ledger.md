---
title: Results Ledger
description: Consolidated ledger of real completed PRISM, SWING, TSF, probe-battery, subset-soup, and strict post-hoc projection empirical results, baselines, ablations, and key diagnostic runs. Planning-only rows have been removed.
created: 2026-03-30 22:05
last_modified: 2026-04-05 20:05
last_modified_by: agent
status: active
related_files: claude_workspace/results/swing_lessons_learned.md, domaingen/posthoc/swing.py, domaingen/posthoc/tsf.py, domaingen/posthoc/shotgun.py, domaingen/posthoc/moonshot_2.py, domaingen/posthoc/subset_soups.py
key_functions:
  - Preserve completed PRISM, SWING, TSF, probe-battery, subset-soup, and strict post-hoc projection empirical results in one place
  - Remove placeholder-only entries such as TBD, running, queued, and submitted rows
  - Make the current empirical conclusions easy to recover later
latest_change: Added the first strict post-hoc non-soup projection pilots on PACS art_painting and updated the conclusions to reflect that they did not beat the leading subset-soup baselines.
change_log:
  - 2026-03-30 22:05: Initial PRISM-only ledger created
  - 2026-04-01 09:40: Initial SWING-only ledger created
  - 2026-04-01 12:20: Merged PRISM and SWING ledgers into one completed-results-only ledger
  - 2026-04-04 00:35: Added SpectralSubsetSoup, GraphDiffusionSubsetSoup, and GibbsTopKSubsetSoup replay results on PACS art_painting
  - 2026-04-05 18:05: Added TSF, SHOTGUN, MOONSHOT-2, the full-lean Gibbs rerun, and the 16-cell graph-diffusion ablation on PACS art_painting
  - 2026-04-05 19:10: Added the focused 12-cell local graph-diffusion sweep and updated the subset-soup conclusions
  - 2026-04-05 20:05: Added TrajectoryNuisanceProjection, FisherRashomonProjection, and LogitCovarianceDebias pilot runs on PACS art_painting
---

# Scope

This file is the current source of truth for completed PRISM, SWING, subset-soup, and strict post-hoc projection results discussed in this project.

Conventions:

- Only completed, real entries are included here.
- Planning-only rows such as `TBD`, `running`, `queued`, and `submitted` have been intentionally removed.
- `SWING-uniform` means the plain uniform average of the accepted safe candidate set from the same run.
- PACS `art_painting` corresponds to replay bank:
  - `/project/jje239_dgxpublicai25/jwje228/work/results/erm_replay_bank_painting`

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

## 4.3 MOONSHOT-2 nuclear probe sweep on PACS art_painting

| Run | Best full probe | Best full / out | Best out probe | Best full / out | Best balanced probe | Best full / out | Wins vs uniform on both full and out | Notes |
|---|---|---|---|---|---|---|---:|---|
| `moonshot_2_painting_nuclear_v1` | `gibbs_recency_supporttail_t0p01_logit` | `0.8784 / 0.8753` | `spectral_subset_cos_k024_r04` | `0.8711 / 0.8949` | `diffuse_cos_bestmean_a06_s01_logit` | `0.8745 / 0.8900` | 36 | no `MOONSHOT-2` probe beat `even_018_prob` on both full and out simultaneously |

Interpretation:

- `MOONSHOT-2` confirmed that graph/diffusion and Gibbs-style ranking were alive, while pure center weighting and several other exotic families were not.
- The earlier `MOONSHOT` pass had only `10` probes beating uniform on both full and out; `MOONSHOT-2` raised that count to `36`.
- The strongest new deployable directions coming out of probe space were graph diffusion and Gibbs top-`k`, not spectral subset alone.
- These are probe-space results over cached predictions, not final weight-space soups.

## 4.4 First probe-to-weight-space translations on PACS art_painting

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

## 4.5 Full-lean Gibbs rerun on PACS art_painting

| Method | Prior | Loss | Temperature | k | Art full | In | Out | Same-run uniform full | Same-run uniform in | Same-run uniform out | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `GibbsTopKSubsetSoup` | `recency` | `supporttail` | 0.01 | 24 | 0.8833 | 0.8798 | 0.8973 | 0.8726 | 0.8682 | 0.8900 | tail-heavy Gibbs improved out strongly but moved full only slightly beyond the earlier Gibbs run |

Interpretation:

- This run showed that `out` was no longer the bottleneck in the Gibbs branch.
- Pushing harder on `supporttail` mainly bought `out`, not a decisive jump in `full`.
- That result motivated the later shift toward graph-focused ablations for the next push.

## 4.6 `GraphDiffusionSubsetSoup` 16-cell art_painting ablation

| Config | Similarity | Anchor | Alpha | Steps | k | Art full | In | Out | Delta vs same-run uniform full | Delta vs same-run uniform out | Notes |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| best full | `cos` | `bestmean` | 0.4 | 1 | 16 | 0.8843 | 0.8816 | 0.8949 | +0.0112 | +0.0049 | current best art-full subset-soup result so far |
| best out | `corr` | `bestval` | 0.6 | 1 | 24 | 0.8774 | 0.8719 | 0.8998 | +0.0044 | +0.0122 | current best out among the graph-diffusion ablation cells |

Interpretation:

- Only `2 / 16` tested graph-diffusion configurations were nonnegative against their same-run uniform baselines on both full and out.
- `bestmean` was the stronger anchor for full, while `bestval` was the stronger anchor for out.
- `k=16` beat `k=24` on the best full-oriented branch.
- `GraphDiffusionSubsetSoup` is now ahead of the earlier Gibbs runs on art full, and the best full configuration also exceeded the best completed PRISM full-cap art-full result.

## 4.7 Focused 12-cell local `GraphDiffusionSubsetSoup` sweep around the winning region

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

## 4.8 First strict post-hoc non-soup projection pilots on PACS art_painting

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
- The most likely path to `89+` is now a deployment change inside that winning pocket, not another broad discrete-subset search.

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
