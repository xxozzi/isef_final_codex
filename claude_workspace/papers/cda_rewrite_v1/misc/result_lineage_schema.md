# Result Lineage Schema

Every reported manuscript number must map to a row in `misc/result_lineage.csv`. A result is not reportable if any required field is missing, manually typed, or derived from a non-artifact source.

## Primary Key

The primary key is:

\[
(\texttt{claim\_id},\texttt{table\_or\_figure},\texttt{run\_id},\texttt{artifact\_id},\texttt{dataset},
\texttt{target\_domain},\texttt{seed},\texttt{method},\texttt{selector},
\texttt{weight\_rule},\texttt{bn\_refresh},\texttt{checkpoint\_bank\_hash},
\texttt{metric\_name},\texttt{metric\_split}).
\]

## Required Columns

- `claim_id`
- `table_or_figure`
- `run_id`
- `artifact_id`
- `artifact_parent_ids`
- `artifact_kind`
- `artifact_path`
- `artifact_sha256`
- `dataset`
- `target_domain`
- `source_domains`
- `split_id`
- `seed`
- `method`
- `selector`
- `weight_rule`
- `run_dir`
- `replay_dir`
- `diagnostics_dir`
- `checkpoint_bank_hash`
- `checkpoint_list_path`
- `config_hash`
- `commit_hash`
- `command`
- `code_path`
- `python_env_hash`
- `data_root_hash`
- `metric_name`
- `metric_value`
- `metric_split`
- `bn_refresh`
- `selection_rule`
- `selection_inputs`
- `selection_artifact_id`
- `selector_code_path`
- `target_labels_used`
- `target_samples_used`
- `target_metadata_used`
- `artifact_status`
- `created_utc`
- `immutable`

## Allowed Artifact Status Values

- `verified`
- `literature_only`
- `incomplete`
- `delete`

Only `verified` rows may support CDA result claims. `literature_only` rows may support related-work comparisons only if clearly labeled.

## Artifact Roots

Raw and derived artifacts must be separated.

- `artifacts/raw_runs/`: immutable training or replay outputs copied from execution roots.
- `artifacts/replays/`: immutable replay outputs with manifests.
- `artifacts/diagnostics/`: derived diagnostics tied to one or more replay artifacts.
- `artifacts/tables/`: generated `.csv`, `.tex`, and `.md` tables.
- `artifacts/figures/`: generated `.pdf`, `.png`, and `.svg` figures.

No artifact may be overwritten. A new run creates a new `run_id`; a new derived file creates a new `artifact_id`. Validators must fail if `immutable` is not `true` for a final result row.

## Source-Only Selection Audit

For every source-only claim, validators must verify:

- `target_labels_used=false`;
- `target_samples_used=false` unless the row is explicitly marked target-aware and excluded from CDA claims;
- `target_metadata_used=false` unless the metadata is part of the public split definition and not a selection input;
- `source_domains` excludes `target_domain`;
- `selection_inputs` lists only source validation losses, source-domain losses, checkpoint metadata, or frozen hyperparameters;
- `selection_artifact_id` points to a manifest that records selected checkpoints and soup weights;
- `selector_code_path` matches the final method name in the manuscript.

## Failure Conditions

- Missing raw `results.jsonl`, replay manifest, diagnostics JSON, or generated CSV source.
- Missing commit hash, command, seed, dataset, target domain, or method.
- Any `target_labels_used=true` row supporting a source-only claim.
- Any missing or nonunique `run_id` or `artifact_id`.
- Any duplicate primary key.
- Any final row with `immutable=false`.
- Any missing `source_domains`, `selection_inputs`, `selection_artifact_id`, or `selector_code_path`.
- Any result copied from `.tex`, manually typed notes, poster figures, screenshots, or hard-coded plotting arrays.
- Any reported number in `src/**/*.tex` with no matching `claim_id`.
- Any table or figure whose generation script contains typed metric arrays instead of artifact loaders.
