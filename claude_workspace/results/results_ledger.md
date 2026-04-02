---
title: Results Ledger
description: Consolidated ledger of real completed PRISM and SWING-related empirical results, baselines, ablations, and key diagnostic runs. Planning-only rows have been removed.
created: 2026-03-30 22:05
last_modified: 2026-04-01 12:20
last_modified_by: agent
status: active
related_files: claude_workspace/results/swing_lessons_learned.md, domaingen/posthoc/swing.py
key_functions:
  - Preserve completed PRISM and SWING empirical results in one place
  - Remove placeholder-only entries such as TBD, running, queued, and submitted rows
  - Make the current empirical conclusions easy to recover later
latest_change: Merged the former PRISM and SWING ledgers into one consolidated results ledger and removed all non-real planning entries.
change_log:
  - 2026-03-30 22:05: Initial PRISM-only ledger created
  - 2026-04-01 09:40: Initial SWING-only ledger created
  - 2026-04-01 12:20: Merged PRISM and SWING ledgers into one completed-results-only ledger
---

# Scope

This file is the current source of truth for completed PRISM and SWING-related results discussed in this project.

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

# 4. Current Empirical Conclusions

## 4.1 PRISM

- best clean domain-label-free PACS average in the current 4-split sweep: `PRISM`
- current `PRISM` vs `SWAD` margin is real but small
- current evidence still does not justify saying `PRISM` is decisively better than `SWAD`
- the best completed full-cap `art_painting` PRISM grid cell so far is `art_a015_e002_t002_m3` at `88.28`

## 4.2 SWING

- `SWING` is not invalid in the sense of broken math or broken implementation
- but the current `SWING` formulation has failed the more important empirical test: it does not clearly and consistently beat `SWING-uniform`
- best raw `SWING`: `0.8818` from `swing_art_rank2_auto_bn512`
- best explicit `SWING-uniform`: `0.8784` from `swing_art_rank3_tau1e3`
- best explicit within-run `SWING > SWING-uniform` gap: `+0.0034` from `swing_art_rank2_loc18`

That `+0.0034` gap is too small, especially combined with the multiple runs where `SWING` lost to the uniform safe-pool baseline.

## 4.3 Final decision on current SWING

- Stop treating the current `SWING` formulation as the headline method.
- Keep it as:
  - a completed negative-result branch
  - an ablation against future methods
  - a useful source of infrastructure: safe-pool construction, diagnostics, replay reporting, and the `SWING-uniform` baseline
