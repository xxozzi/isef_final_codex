# CDA HPC Layout

This file records the filesystem layout for the CDA checkpoint-bank and replay runs.

Final CDA method:

\[
\mathrm{CDA}=\mathrm{VSC}+\mathrm{CDA\text{-}BD}.
\]

## Current Scope

All five DomainBed image datasets are now installed and verified on the HPC.
The immediate launch can still be PACS-only as a smoke batch:

\[
4\ \text{PACS targets}\times 3\ \text{seeds}\times 5\ \text{bank producers}
=60\ \text{checkpoint banks}.
\]

The full DomainBed config grid is already generated:

\[
22\ \text{target splits}\times 3\ \text{seeds}\times 5\ \text{bank producers}
=330\ \text{checkpoint banks}.
\]

The five bank producers are `ERM`, `ERMPlusPlus` (`ERM++`), `CORAL`, `SAM`, and `DGSAM`.

## Training Settings

Use the SWAD/DomainBed-compatible setting unless a method-specific paper setting overrides it:

- `PACS`, `VLCS`, `OfficeHome`, `TerraIncognita`: `steps: 5001`, so the final saved checkpoint is `model_step5000.pkl`.
- `DomainNet`: `steps: 15001`, so the final saved checkpoint is `model_step15000.pkl`.
- Per-domain train batch size: `32`.
- Learning rate: \(5\times 10^{-5}\) for `ERM`, `ERMPlusPlus`, `CORAL`, and `SAM`.
- Weight decay: `0.0` for `ERM`, `ERMPlusPlus`, `CORAL`, and `SAM`.
- BatchNorm: frozen during training for `ERM`, `CORAL`, `SAM`, and `DGSAM`, matching the SWAD/DomainBed-style run setting.
- Checkpoint/evaluation frequency for CDA banks: `25` for `PACS`, `VLCS`, `OfficeHome`, and `TerraIncognita`; `50` for `DomainNet`.
- `DGSAM` uses the dataset-specific paper table:
  - `PACS`: `lr: 3e-5`, `weight_decay: 1e-4`, `resnet_dropout: 0.5`, `rho: 0.03`.
  - `VLCS`: `lr: 1e-5`, `weight_decay: 1e-4`, `resnet_dropout: 0.5`, `rho: 0.03`.
  - `OfficeHome`: `lr: 1e-5`, `weight_decay: 1e-6`, `resnet_dropout: 0.5`, `rho: 0.1`.
  - `TerraIncognita`: `lr: 1e-5`, `weight_decay: 1e-6`, `resnet_dropout: 0.2`, `rho: 0.05`.
  - `DomainNet`: `lr: 2e-5`, `weight_decay: 1e-4`, `resnet_dropout: 0.5`, `rho: 0.1`.
- `ERMPlusPlus` uses the official ERM++ loop components that fit `domaingen`: unfrozen BatchNorm, `linear_steps: 500`, `sma: true`, and `sma_start_iter: 600`.
- Exact ERM++ paper reproduction also uses the official `resnet_timm_augmix` initialization; that is not represented by these same-backbone bank configs unless we add that backbone path separately.

## HPC Root

```text
/project/jje239_dgxpublicai25/jwje228/work
```

## Configs

Generated bank configs live in:

```text
/project/jje239_dgxpublicai25/jwje228/work/domaingen/configs/generated/cda_domainbed_v1/train_banks
```

Local source path:

```text
domaingen/configs/generated/cda_domainbed_v1/train_banks
```

Manifest:

```text
domaingen/configs/generated/cda_domainbed_v1/bank_manifest.csv
```

## Results

All outputs should stay under one experiment namespace:

```text
/project/jje239_dgxpublicai25/jwje228/work/results/cda_domainbed_v1
```

Planned structure:

```text
results/cda_domainbed_v1
+-- banks
|   +-- ERM/<dataset>/<target_env>/seed_<seed>
|   +-- ERMPlusPlus/<dataset>/<target_env>/seed_<seed>
|   +-- CORAL/<dataset>/<target_env>/seed_<seed>
|   +-- SAM/<dataset>/<target_env>/seed_<seed>
|   +-- DGSAM/<dataset>/<target_env>/seed_<seed>
+-- replays
|   +-- ERM/<dataset>/<target_env>/seed_<seed>
|   +-- ERMPlusPlus/<dataset>/<target_env>/seed_<seed>
|   +-- CORAL/<dataset>/<target_env>/seed_<seed>
|   +-- SAM/<dataset>/<target_env>/seed_<seed>
|   +-- DGSAM/<dataset>/<target_env>/seed_<seed>
+-- cda
|   +-- ERM/<dataset>/<target_env>/seed_<seed>
|   +-- ERMPlusPlus/<dataset>/<target_env>/seed_<seed>
|   +-- CORAL/<dataset>/<target_env>/seed_<seed>
|   +-- SAM/<dataset>/<target_env>/seed_<seed>
|   +-- DGSAM/<dataset>/<target_env>/seed_<seed>
+-- ablations
+-- tables
+-- figures
+-- manifests
```

Use these target environment codes:

- PACS: `A`, `C`, `P`, `S`
- VLCS: `C`, `L`, `S`, `V`
- OfficeHome: `A`, `C`, `P`, `R`
- TerraIncognita: `L100`, `L38`, `L43`, `L46`
- DomainNet: `clip`, `info`, `paint`, `quick`, `real`, `sketch`

## Slurm Logs

Use stage-specific Slurm log roots:

```text
slurm_output/cda_domainbed_v1/train
slurm_output/cda_domainbed_v1/replay
slurm_output/cda_domainbed_v1/cda
slurm_output/cda_domainbed_v1/ablations
```

The submission scripts read `DOMAINGEN_SLURM_LOG_ROOT`, so set it before each stage.

Before any bank submission, run:

```bash
python domaingen/scripts/validate_cda_domainbed_configs.py
```

The validator must pass for all `330` generated configs. It catches YAML type
problems such as `lr` loading as a string, manifest/config mismatches, wrong
step counts, wrong checkpoint frequencies, wrong held-out domains, and result
paths outside the expected HPC tree.

## Fixed CDA Selector

For final CDA runs, use:

```text
selector: version_space_compression_selector__margin_eps_0p5_0p05
weights:  blackwell_dual_target_weights__entropy_lambda_0p02
```
