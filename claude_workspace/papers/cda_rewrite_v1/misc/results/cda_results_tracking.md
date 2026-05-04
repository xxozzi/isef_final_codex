# CDA Results Tracking

Date created: 2026-04-30

This file tracks the current result state for the final CDA method:

\[
\text{CDA}=\text{VSC}+\text{CDA-BD}.
\]

The current source of truth is `claude_workspace/results/results_ledger.md`. The PACS SWAD versus CDA comparison is now treated as a real result because the ledger contains the values and the user confirmed from memory that the two runs used the same seed. The exact HPC result locations and Slurm log directories still need to be filled in when recovered.

## Final Method Definition

| Item | Value |
|---|---|
| Paper method | `VSC + CDA-BD` |
| Selector implementation | `version_space_compression_selector__margin_eps_0p5_0p05` |
| Weight implementation | `blackwell_dual_target_weights__entropy_lambda_0p02` |
| Selector hyperparameters | margin \(0.5\), mismatch tolerance \(0.05\) |
| Weight hyperparameter | \(\lambda_{\mathrm{ent}}=0.02\) |
| Current evidence status | accepted PACS real result from ledger plus same-seed user confirmation |
| Paper status | final method identity frozen; PACS result accepted; broader benchmark results not yet frozen |

## Accepted PACS Same-Seed Result

The SWAD and CDA rows below are recorded as the same-seed PACS comparison. The same-seed statement comes from user confirmation on 2026-04-30; the ledger itself records the values but does not expose the seed field for these four-split summaries.

| Dataset | Target domain | SWAD full | CDA full | Delta | Result location | Slurm log directory | Evidence status |
|---|---|---:|---:|---:|---|---|---|
| PACS | art_painting | 0.8760 | 0.8843 | 0.0083 |  |  | accepted real result; HPC paths pending |
| PACS | cartoon | 0.8238 | 0.8375 | 0.0137 |  |  | accepted real result; HPC paths pending |
| PACS | photo | 0.9707 | 0.9719 | 0.0012 |  |  | accepted real result; HPC paths pending |
| PACS | sketch | 0.8173 | 0.8430 | 0.0257 |  |  | accepted real result; HPC paths pending |
| PACS | mean | 0.8719 | 0.8842 | 0.0123 |  |  | accepted real result; HPC paths pending |

## Current PACS CDA-BD Rows

These are the current four PACS target-domain rows for `VSC + CDA-BD`.

| Dataset | Target domain | Family size | Full | In | Out | Result location | Slurm log directory | Source |
|---|---|---:|---:|---:|---:|---|---|---|
| PACS | art_painting | 18 | 0.8843 | 0.8804 | 0.8998 |  |  | `results_ledger.md`, version-space family-local weighting block |
| PACS | cartoon | 21 | 0.8375 | 0.8380 | 0.8355 |  |  | `results_ledger.md`, cartoon selector+weight block |
| PACS | sketch | 25 | 0.8430 | 0.8403 | 0.8535 |  |  | `results_ledger.md`, version-space-only sketch block |
| PACS | photo | 27 | 0.9719 | 0.9701 | 0.9790 |  |  | `results_ledger.md`, version-space-only photo block |
| PACS | mean | -- | 0.8842 | 0.8822 | 0.8920 |  |  | full mean from ledger; in/out means computed from rows above |

## Nearby Fixed-Weighter Comparison

All rows use the same VSC selector, `version_space_compression_selector__margin_eps_0p5_0p05`.

| Paper-facing role | Weight implementation | Art full | Cartoon full | Sketch full | Photo full | Mean full | Result location | Slurm log directory | Status |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| CDA-Piv ablation | `pivotality_shift_guard__alpha_0p75` | 0.8843 | 0.8400 | 0.8414 | 0.9713 | 0.8843 |  |  | ablation only |
| Final CDA | `blackwell_dual_target_weights__entropy_lambda_0p02` | 0.8843 | 0.8375 | 0.8430 | 0.9719 | 0.8842 |  |  | final method |
| Alternate domain-bargaining weight | `nash_domain_bargaining_weights__entropy_lambda_0p0` | 0.8838 | 0.8383 | 0.8430 | 0.9707 | 0.8840 |  |  | ablation only |
| Contribution-style weight | `soup_marginal_contribution__power_1p0` | 0.8848 | 0.8383 | 0.8412 | 0.9701 | 0.8836 |  |  | ablation only |
| Transport-style weight | `ot_target_transport_weights__ot_epsilon_0p0025` | 0.8833 | 0.8375 | 0.8407 | 0.9683 | 0.8825 |  |  | ablation only |
| Older guarded pivotality | `redundancy_guarded_pivotality__alpha_0p9` | 0.8857 | 0.8289 | 0.8425 | 0.9701 | 0.8818 |  |  | ablation only |
| Pair-canceling weight | `phase_canceling_pair__temperature_0p07` | 0.8857 | 0.8375 | 0.8290 | 0.9689 | 0.8803 |  |  | ablation only |
| VSC + uniform | uniform family weights | 0.8804 | 0.8285 | 0.8239 | 0.9713 | 0.8760 |  |  | required ablation |

## Blank Main Benchmark Table

Fill this only from accepted run evidence. For current PACS, the accepted evidence is the ledger plus same-seed user confirmation; for future HPC runs, fill the result path and Slurm log path as soon as the run is located.

| Dataset | Target domain | ERM | Best source-val singleton | VSC + uniform | VSC + CDA-BD | Seeds | Result location | Slurm log directory | Evidence status |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| PACS | art_painting | | | | | | | | |
| PACS | cartoon | | | | | | | | |
| PACS | photo | | | | | | | | |
| PACS | sketch | | | | | | | | |
| VLCS | Caltech101 | | | | | | | | |
| VLCS | LabelMe | | | | | | | | |
| VLCS | SUN09 | | | | | | | | |
| VLCS | VOC2007 | | | | | | | | |
| OfficeHome | Art | | | | | | | | |
| OfficeHome | Clipart | | | | | | | | |
| OfficeHome | Product | | | | | | | | |
| OfficeHome | Real_World | | | | | | | | |
| TerraIncognita | location_38 | | | | | | | | |
| TerraIncognita | location_43 | | | | | | | | |
| TerraIncognita | location_46 | | | | | | | | |
| TerraIncognita | location_100 | | | | | | | | |
| DomainNet | clipart | | | | | | | | |
| DomainNet | infograph | | | | | | | | |
| DomainNet | painting | | | | | | | | |
| DomainNet | quickdraw | | | | | | | | |
| DomainNet | real | | | | | | | | |
| DomainNet | sketch | | | | | | | | |

## Blank Ablation Table

| Ablation group | Method row | Selector | Weight rule | PACS mean | VLCS mean | OfficeHome mean | TerraIncognita mean | DomainNet mean | Result location | Slurm log directory | Evidence status |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| Main stack | Best source-val singleton | singleton | none | | | | | | | | |
| Main stack | VSC + uniform | VSC | uniform | | | | | | | | |
| Main stack | VSC + CDA-Piv | VSC | CDA-Piv | | | | | | | | |
| Main stack | VSC + CDA-BD | VSC | CDA-BD | | | | | | | | |
| Weight ablation | VSC + CDA-BD, no entropy | VSC | CDA-BD with \(\lambda_{\mathrm{ent}}=0\) | | | | | | | | |
| Selector ablation | VSC, stricter tolerance | VSC with \(\varepsilon_{\mathrm{vsc}}=0.02\) | CDA-BD | | | | | | | | |
| Selector ablation | VSC, looser tolerance | VSC with \(\varepsilon_{\mathrm{vsc}}=0.10\) | CDA-BD | | | | | | | | |
| BN ablation | CDA-BD with `eval_noaug` BN refresh | VSC | CDA-BD | | | | | | | | |
| BN ablation | CDA-BD with `train_aug` BN refresh | VSC | CDA-BD | | | | | | | | |

## Blank Diagnostic Tracker

| Diagnostic | Dataset | Target domain | Method | Required value | Source file | Status |
|---|---|---|---|---|---|---|
| Source-average underidentification | PACS | all | all candidate soups | candidates with similar source average but different source-risk vectors | | |
| Certificate vs OOD scatter | PACS | all | checkpoints and soups | \(\bar L+\rho\|P_\perp L\|_2\), OOD accuracy | | |
| Mergeability residual | PACS | all | VSC + CDA-BD | \(M(w)=\|L(\bar\theta(w))-z(w)\|_2\) | | |
| Source-mixture residual | PACS | all | VSC + CDA-BD | \(\epsilon_{\mathrm{app}}\) | | |
| Failure case | any | any | VSC + CDA-BD | large \(\epsilon_{\mathrm{app}}\) or large \(M(w)\) with weak OOD result | | |

## Next Fill-In Work

- Fill the exact HPC result location and Slurm log directory for the accepted PACS SWAD and CDA rows.
- Verify selected checkpoint families and soup weights for each row.
- Check source-only selection fields: no target labels, no target samples, no target metadata.
- Add extra seeds later if the final submission needs uncertainty bars, but keep the current same-seed PACS comparison as the accepted result for now.
- Keep five-benchmark rows blank until real runs exist for every target domain.
