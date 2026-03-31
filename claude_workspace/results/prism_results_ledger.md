---
title: PRISM Results Ledger
description: Running ledger for verified PRISM-related empirical results, comparison baselines, ablations, and planned grid searches.
created: 2026-03-30 22:05
last_modified: 2026-03-31 09:05
last_modified_by: agent
status: active
related_files: claude_workspace/resume.md, claude_workspace/research/srm_prism_bound_minimizing_updates.md, response.md
key_functions:
  - Preserve the current PRISM empirical record in one place
  - Distinguish clean results from historical or stale context
  - Track planned and completed PRISM grid-search runs
latest_change: Added the next six completed feasible full-cap art_painting PRISM grid results and updated the best-so-far summary.
change_log:
  - 2026-03-30 22:05: Initial ledger with current results and planned art_painting PRISM grid
  - 2026-03-30 22:31: Marked the first 10 art_painting PRISM grid runs as running and added stdout tail commands
  - 2026-03-30 22:39: Added the remaining submitted grid jobs, distinguishing running vs queued runs
  - 2026-03-30 23:02: Added a separate full-cap resubmission table for the art_painting PRISM grid using prism_max_actions=2000000
  - 2026-03-31 08:35: Recorded the first six completed full-cap grid results and marked the best-so-far setting
  - 2026-03-31 09:05: Recorded the next six completed feasible full-cap grid results and refreshed the summary statistics
---

# Scope

This file is the running source of truth for PRISM-related results discussed in this project.

Conventions:

- Results labeled **clean** come from the current up-to-date replay banks and should be preferred.
- Results labeled **historical** are still useful context but should not override the clean banks.
- PACS environment names use the true PACS labels: `art_painting`, `cartoon`, `photo`, `sketch`.
- The “art partition” replay bank in this repo is:
  - `results/erm_replay_bank_painting`
  - which holds out `art_painting`

# 1. Clean Current Results

## 1.1 PACS 4-split domain-label-free replay sweep

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

## 1.2 Fresh canonical `erm_replay_bank` seed-1 comparison

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

## 1.3 Cross-pool ablation on fresh canonical bank

| Variant | Runner | Pool | Art full | In | Out |
|---|---|---|---:|---:|---:|
| baseline_dcola | D-COLA | D-COLA | 0.8901 | 0.8908 | 0.8875 |
| dcola_on_prism_pool | D-COLA | PRISM | 0.8877 | — | — |
| baseline_prism | PRISM | PRISM | 0.8833 | 0.8853 | 0.8753 |
| prism_on_dcola_pool | PRISM | D-COLA | 0.8672 | 0.8676 | 0.8655 |

Interpretation:

- The strongest current reading is that PRISM’s remaining weakness is not only the candidate pool.
- The cross-pool result is consistent with an objective-level limitation in current PRISM.

## 1.4 Verified D-COLA ablations

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

# 2. Additional Up-to-Date `erm_cora` Results

## 2.1 Up-to-date `erm_cora` replay-bank comparisons

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
- The effect of loosening the pool was mixed; `alpha` mattered more than simply making soups larger.

# 3. Historical Context

## 3.1 Older verified local workspace leaderboard

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

- these results are still useful for project history
- but the clean current banks above should be preferred for claims

# 4. Current Conclusions

As of this ledger version:

- best overall method with domain labels allowed: `D-COLA`
- best domain-label-free method by clean PACS average: `PRISM`
- current PRISM-vs-SWAD margin is real but small
- current evidence does **not** justify saying PRISM is decisively better than SWAD
- the strongest unresolved question is whether PRISM still has headroom through tuning, or whether it needs a structural update

# 5. Planned Grid Search: PRISM Replay on `art_painting`

Target bank:

- `/project/jje239_dgxpublicai25/jwje228/work/results/erm_replay_bank_painting`

Goal:

- measure how much headroom still exists in the current PRISM formulation before changing the method

Stage-1 search design:

- fixed `M = 3`
- `alpha in {0.15, 0.20, 0.25}`
- `epsilon in {0.02, 0.03, 0.05}`
- `tau in {0.02, 0.03, 0.05}`

This gives 27 replay jobs.

## 5.1 Planned run table

| Run name | alpha | epsilon | tau | M | Status | Art full | In | Out | Tail stdout | Notes |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| art_a015_e002_t002_m3 | 0.15 | 0.02 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t002_m3_139185.out` | job `139185` |
| art_a015_e002_t003_m3 | 0.15 | 0.02 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t003_m3_139186.out` | job `139186` |
| art_a015_e002_t005_m3 | 0.15 | 0.02 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t005_m3_139187.out` | job `139187` |
| art_a015_e003_t002_m3 | 0.15 | 0.03 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t002_m3_139188.out` | job `139188` |
| art_a015_e003_t003_m3 | 0.15 | 0.03 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t003_m3_139189.out` | job `139189` |
| art_a015_e003_t005_m3 | 0.15 | 0.03 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t005_m3_139190.out` | job `139190` |
| art_a015_e005_t002_m3 | 0.15 | 0.05 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t002_m3_139191.out` | job `139191` |
| art_a015_e005_t003_m3 | 0.15 | 0.05 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t003_m3_139192.out` | job `139192` |
| art_a015_e005_t005_m3 | 0.15 | 0.05 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t005_m3_139193.out` | job `139193` |
| art_a020_e002_t002_m3 | 0.20 | 0.02 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t002_m3_139194.out` | job `139194` |
| art_a020_e002_t003_m3 | 0.20 | 0.02 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t003_m3_139197.out` | job `139197` |
| art_a020_e002_t005_m3 | 0.20 | 0.02 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t005_m3_139198.out` | job `139198` |
| art_a020_e003_t002_m3 | 0.20 | 0.03 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t002_m3_139199.out` | job `139199` |
| art_a020_e003_t003_m3 | 0.20 | 0.03 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t003_m3_139200.out` | job `139200` |
| art_a020_e003_t005_m3 | 0.20 | 0.03 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t005_m3_139201.out` | job `139201` |
| art_a020_e005_t002_m3 | 0.20 | 0.05 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t002_m3_139202.out` | job `139202` |
| art_a020_e005_t003_m3 | 0.20 | 0.05 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t003_m3_139203.out` | job `139203` |
| art_a020_e005_t005_m3 | 0.20 | 0.05 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t005_m3_139204.out` | job `139204` |
| art_a025_e002_t002_m3 | 0.25 | 0.02 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t002_m3_139205.out` | job `139205` |
| art_a025_e002_t003_m3 | 0.25 | 0.02 | 0.03 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t003_m3_139206.out` | job `139206` |
| art_a025_e002_t005_m3 | 0.25 | 0.02 | 0.05 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t005_m3_139207.out` | job `139207` |
| art_a025_e003_t002_m3 | 0.25 | 0.03 | 0.02 | 3 | running | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t002_m3_139208.out` | job `139208` |
| art_a025_e003_t003_m3 | 0.25 | 0.03 | 0.03 | 3 | queued | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t003_m3_139209.out` | job `139209`, pending |
| art_a025_e003_t005_m3 | 0.25 | 0.03 | 0.05 | 3 | queued | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t005_m3_139210.out` | job `139210`, pending |
| art_a025_e005_t002_m3 | 0.25 | 0.05 | 0.02 | 3 | queued | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t002_m3_139211.out` | job `139211`, pending |
| art_a025_e005_t003_m3 | 0.25 | 0.05 | 0.03 | 3 | queued | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t003_m3_139212.out` | job `139212`, pending |
| art_a025_e005_t005_m3 | 0.25 | 0.05 | 0.05 | 3 | queued | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t005_m3_139213.out` | job `139213`, pending |

Note:

- The `Tail stdout` column stores the exact live command for the stdout log.
- The matching stderr command follows the same pattern with `.err` instead of `.out`.

## 5.2 Full-cap resubmission table

Full-cap resubmission settings:

- replay root: `/project/jje239_dgxpublicai25/jwje228/work/results/replays/prism_grid_art_painting_fullcap`
- `prism_max_actions = 2000000`
- `prism_auto_cap = 2000000`
- time limit: `11:00:00`
- memory: `32G`
- CPUs per task: `8`
- `M = 3`

This pass is meant to brute-force cells that failed in the original grid because the exact PRISM action set grew too large under the default cap.

| Run name | alpha | epsilon | tau | M | Status | Art full | In | Out | Tail stdout | Notes |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|---|
| art_a015_e002_t002_m3 | 0.15 | 0.02 | 0.02 | 3 | done | 88.28 | 88.35 | 88.02 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t002_m3_fullcap_139222.out` | full-cap rerun, job `139222`; best so far |
| art_a015_e002_t003_m3 | 0.15 | 0.02 | 0.03 | 3 | done | 87.74 | 87.74 | 87.78 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t003_m3_fullcap_139223.out` | full-cap rerun, job `139223` |
| art_a015_e002_t005_m3 | 0.15 | 0.02 | 0.05 | 3 | done | 87.16 | 87.37 | 86.31 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e002_t005_m3_fullcap_139224.out` | full-cap rerun, job `139224` |
| art_a015_e003_t002_m3 | 0.15 | 0.03 | 0.02 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t002_m3_fullcap_139225.out` | full-cap rerun, job `139225` |
| art_a015_e003_t003_m3 | 0.15 | 0.03 | 0.03 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t003_m3_fullcap_139226.out` | full-cap rerun, job `139226` |
| art_a015_e003_t005_m3 | 0.15 | 0.03 | 0.05 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e003_t005_m3_fullcap_139227.out` | full-cap rerun, job `139227` |
| art_a015_e005_t002_m3 | 0.15 | 0.05 | 0.02 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t002_m3_fullcap_139228.out` | full-cap rerun, job `139228` |
| art_a015_e005_t003_m3 | 0.15 | 0.05 | 0.03 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t003_m3_fullcap_139229.out` | full-cap rerun, job `139229` |
| art_a015_e005_t005_m3 | 0.15 | 0.05 | 0.05 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a015_e005_t005_m3_fullcap_139230.out` | full-cap rerun, job `139230` |
| art_a020_e002_t002_m3 | 0.20 | 0.02 | 0.02 | 3 | done | 86.43 | 86.09 | 87.78 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t002_m3_fullcap_139231.out` | full-cap rerun, job `139231` |
| art_a020_e002_t003_m3 | 0.20 | 0.02 | 0.03 | 3 | done | 88.04 | 87.86 | 88.75 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t003_m3_fullcap_139232.out` | full-cap rerun, job `139232`; tied best out so far |
| art_a020_e002_t005_m3 | 0.20 | 0.02 | 0.05 | 3 | done | 87.74 | 87.55 | 88.51 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e002_t005_m3_fullcap_139233.out` | full-cap rerun, job `139233` |
| art_a020_e003_t002_m3 | 0.20 | 0.03 | 0.02 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t002_m3_fullcap_139234.out` | full-cap rerun, job `139234` |
| art_a020_e003_t003_m3 | 0.20 | 0.03 | 0.03 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t003_m3_fullcap_139235.out` | full-cap rerun, job `139235` |
| art_a020_e003_t005_m3 | 0.20 | 0.03 | 0.05 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e003_t005_m3_fullcap_139236.out` | full-cap rerun, job `139236` |
| art_a020_e005_t002_m3 | 0.20 | 0.05 | 0.02 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t002_m3_fullcap_139237.out` | full-cap rerun, job `139237` |
| art_a020_e005_t003_m3 | 0.20 | 0.05 | 0.03 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t003_m3_fullcap_139238.out` | full-cap rerun, job `139238` |
| art_a020_e005_t005_m3 | 0.20 | 0.05 | 0.05 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a020_e005_t005_m3_fullcap_139239.out` | full-cap rerun, job `139239` |
| art_a025_e002_t002_m3 | 0.25 | 0.02 | 0.02 | 3 | done | 87.94 | 88.16 | 87.04 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t002_m3_fullcap_139240.out` | full-cap rerun, job `139240` |
| art_a025_e002_t003_m3 | 0.25 | 0.02 | 0.03 | 3 | done | 87.01 | 86.88 | 87.53 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t003_m3_fullcap_139241.out` | full-cap rerun, job `139241` |
| art_a025_e002_t005_m3 | 0.25 | 0.02 | 0.05 | 3 | done | 87.16 | 87.31 | 86.55 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e002_t005_m3_fullcap_139242.out` | full-cap rerun, job `139242` |
| art_a025_e003_t002_m3 | 0.25 | 0.03 | 0.02 | 3 | done | 87.11 | 86.70 | 88.75 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t002_m3_fullcap_139243.out` | full-cap rerun, job `139243`; tied best out so far |
| art_a025_e003_t003_m3 | 0.25 | 0.03 | 0.03 | 3 | done | 87.45 | 87.68 | 86.55 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t003_m3_fullcap_139244.out` | full-cap rerun, job `139244` |
| art_a025_e003_t005_m3 | 0.25 | 0.03 | 0.05 | 3 | done | 87.79 | 87.55 | 88.75 | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e003_t005_m3_fullcap_139245.out` | full-cap rerun, job `139245` |
| art_a025_e005_t002_m3 | 0.25 | 0.05 | 0.02 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t002_m3_fullcap_139246.out` | full-cap rerun, job `139246` |
| art_a025_e005_t003_m3 | 0.25 | 0.05 | 0.03 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t003_m3_fullcap_139247.out` | full-cap rerun, job `139247` |
| art_a025_e005_t005_m3 | 0.25 | 0.05 | 0.05 | 3 | submitted | TBD | TBD | TBD | `tail -f /project/jje239_dgxpublicai25/jwje228/work/slurm_output/replay_art_a025_e005_t005_m3_fullcap_139248.out` | full-cap rerun, job `139248` |

Early read from completed full-cap cells:

- completed feasible cells so far: `12`
- best art full so far: `art_a015_e002_t002_m3` at `88.28`
- best in so far: `art_a015_e002_t002_m3` at `88.35`
- best out so far is tied at `88.75` by `art_a020_e002_t003_m3`, `art_a025_e003_t002_m3`, and `art_a025_e003_t005_m3`
- the current best art-full setting is already above the earlier non-full-cap `art_painting` PRISM result (`87.26`)
- among the completed feasible cells, the strongest region is still the tighter `epsilon = 0.02` corner, especially with `alpha = 0.15`

# 6. Next Update Policy

When new PRISM replay results come in, add them here in this order:

1. mark the corresponding planned row as `submitted`, `running`, `done`, or `failed`
2. fill in `Art full`, `In`, and `Out`
3. add a short note if there was a selector failure, action-cap warning, or anything unusual
4. if a new best setting emerges, add it to Section 1 or Section 2 as a promoted result
