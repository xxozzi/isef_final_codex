---
title: D-COLA 10-Run Tuning Plan
description: Fixed 10-run follow-up plan for the strongest current D-COLA branch on PACS art_painting.
created: 2026-04-09 00:10
last_modified: 2026-04-09 00:42
last_modified_by: agent
status: completed
related_files:
  - claude_workspace/results/results_ledger.md
  - domaingen/posthoc/dcola.py
  - domaingen/scripts/collect_art_painting_replays.py
key_functions:
  - Lock the exact 10-run grid around the current best D-COLA variant
  - Preserve canonical replay names and hyperparameters for later attribution
  - Keep the next tuning step fixed rather than ad hoc
latest_change: Marked the 10-run D-COLA tuning grid complete and recorded dcola_lambda_cov=0.08 as the current best setting on PACS art_painting.
change_log:
  - 2026-04-09 00:10: Created the fixed 10-run plan for D-COLA tuning on PACS art_painting
  - 2026-04-09 00:42: Completed the 10-run sweep; continuation start_mult=2.0 and lambda_cov=0.08 are currently best
---

# Goal

Improve on the current best D-COLA-family result on `erm_replay_bank_painting`:

- `D-COLA+covweighted+smoothmax+cont = 0.8838 / 0.8822 / 0.8900`

Primary selection metric:

- `art_painting_full_acc`

Secondary diagnostics:

- `test_env0_out_acc`
- `test_env0_in_acc`

# Fixed 10-Run Grid

All 10 runs keep the same winning scaffold:

- `dcola_cov_weighting=domain_loss`
- `dcola_source_risk=smooth_max`
- `dcola_continuation_mode=regularizers`

## Block A: Continuation Strength (4 runs)

Hold:

- `dcola_source_smooth_temp=20.0`
- `dcola_lambda_cov=0.1`

Sweep:

1. `dcola_continuation_start_mult=2.0`
2. `dcola_continuation_start_mult=3.0`
3. `dcola_continuation_start_mult=6.0`
4. `dcola_continuation_start_mult=8.0`

## Block B: Smooth-Max Temperature (4 runs)

Hold:

- `dcola_continuation_start_mult=4.0`
- `dcola_lambda_cov=0.1`

Sweep:

5. `dcola_source_smooth_temp=8.0`
6. `dcola_source_smooth_temp=12.0`
7. `dcola_source_smooth_temp=30.0`
8. `dcola_source_smooth_temp=40.0`

## Block C: Covariance Strength (2 runs)

Hold:

- `dcola_continuation_start_mult=4.0`
- `dcola_source_smooth_temp=20.0`

Sweep:

9. `dcola_lambda_cov=0.08`
10. `dcola_lambda_cov=0.15`

# Canonical Replay Names

1. `dcola_tune_cont2_painting_v1`
2. `dcola_tune_cont3_painting_v1`
3. `dcola_tune_cont6_painting_v1`
4. `dcola_tune_cont8_painting_v1`
5. `dcola_tune_temp8_painting_v1`
6. `dcola_tune_temp12_painting_v1`
7. `dcola_tune_temp30_painting_v1`
8. `dcola_tune_temp40_painting_v1`
9. `dcola_tune_cov008_painting_v1`
10. `dcola_tune_cov015_painting_v1`

# Decision Rule

- If any run reaches `art_painting_full_acc >= 0.8844`, it becomes the new empirical leader over the current `0.8843` top art-painting result.
- If several runs are close on full, prefer the one with the highest `test_env0_out_acc`.
- If none beat `0.8838`, stop this branch and do not widen the sweep immediately.

# Outcome

Best continuation:

- `dcola_continuation_start_mult=2.0`

Best temperature:

- `dcola_source_smooth_temp=20.0`

Best covariance strength:

- `dcola_lambda_cov=0.08`

Current best tuned variant:

- `D-COLA+tune-cov008 = 0.8887 / 0.8877 / 0.8924`

Conclusion:

- The fixed 10-run sweep succeeded in establishing a new best D-COLA-family full result on `erm_replay_bank_painting`.
- Any further search should be a very small local refinement around `dcola_lambda_cov=0.08`, not another broad grid.
