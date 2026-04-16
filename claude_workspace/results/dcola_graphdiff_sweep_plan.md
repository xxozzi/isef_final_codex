---
title: D-COLA Graph-Diffusion Sweep Plan
description: Focused replay sweep around the current best stable D-COLA graph-diffusion-pool result on PACS art_painting.
created: 2026-04-09 19:50
last_modified: 2026-04-09 19:50
last_modified_by: agent
status: active
related_files: claude_workspace/results/results_ledger.md, domaingen/posthoc/dcola.py, domaingen/posthoc/subset_soups.py
key_functions:
  - Lock the next graph-diffusion-pool D-COLA replay sweep to a small set of high-value runs
  - Preserve the fixed scaffold so results remain directly comparable to the current stable winner
  - Avoid another broad or underpowered hyperparameter search
latest_change: Created a 6-run sweep around the current graph-diffusion-pool D-COLA winner, varying only subset size, anchor choice, and walk alpha.
change_log:
  - 2026-04-09 19:50: Initial graph-diffusion-pool D-COLA sweep plan created
---

# Goal

Push the current stable D-COLA graph-diffusion-pool branch above the current `0.8843` art-painting full result without changing the D-COLA objective or adding continuation.

# Fixed Scaffold

All runs in this plan keep the following fixed:

- `dcola_deterministic_bn_refresh=true`
- `dcola_bn_refresh_view=eval_noaug`
- `dcola_bn_refresh_seed=0`
- `dcola_bn_refresh_num_workers=0`
- `dcola_pool_source=graph_diffusion_subset`

Reference winner:

- `D-COLA+pool-graphdiff = 0.8843 / 0.8798 / 0.9022`
- baseline settings:
  - `graph_diffusion_subset_k=24`
  - `graph_diffusion_subset_anchor=bestmean`
  - `graph_diffusion_subset_walk_alpha=0.60`

# Sweep

This plan runs exactly 6 replay jobs:

1. `k=16`
2. `k=32`
3. `anchor=bestval`
4. `anchor=besttail`
5. `walk_alpha=0.45`
6. `walk_alpha=0.75`

# Stopping Rule

- If any run exceeds `0.8900` full, stop and lock that branch.
- If no run exceeds the current `0.8843` winner, do not broaden this sweep further without a new structural reason.
