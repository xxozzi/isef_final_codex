# Final CDA Method

Date frozen: 2026-04-30

The final CDA method for the rewritten paper is:

\[
\text{CDA}=\text{VSC}+\text{CDA-BD}.
\]

## Paper Name

- Main method name: `CDA`
- Explicit method stack: `VSC + CDA-BD`
- Ablation-only comparison: `VSC + CDA-Piv`

## Implementation Mapping

- Selector:
  - paper name: `VSC`
  - implementation label: `version_space_compression_selector__margin_eps_0p5_0p05`
  - frozen selector hyperparameters:
    \[
    \text{margin}=0.5,\qquad \varepsilon_{\mathrm{vsc}}=0.05.
    \]

- Weighting rule:
  - paper name: `CDA-BD`
  - implementation label: `blackwell_dual_target_weights__entropy_lambda_0p02`
  - frozen weighting hyperparameter:
    \[
    \lambda_{\mathrm{ent}}=0.02.
    \]

## Reporting Rule

The rewritten paper should report `VSC + CDA-BD` as the CDA method. Other selector or weighting variants may appear only as ablations, diagnostics, or historical development notes. Old method names from local experiment files should not become paper-facing method names.

