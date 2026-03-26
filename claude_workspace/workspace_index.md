---
title: Workspace index
description: Index for the current domain generalization post-hoc research work and links to the main label-free memo, the consensus-core candidate, the simpler stationarity candidate, the main domain-labeled memo, and supporting precursor memos.
created: 2026-03-16 00:45
last_modified: 2026-03-17 19:35
last_modified_by: agent
status: active
related_files: claude_workspace/research/cora_consensus_of_rashomon_averaging.md, claude_workspace/research/reweighting_invariant_weight_averaging.md, claude_workspace/research/stationarity_aware_weight_averaging.md, claude_workspace/research/recoverability_oriented_weight_averaging.md, claude_workspace/research/minimum_adaptation_information_weight_averaging.md, claude_workspace/research/consensus_overlap_weight_averaging.md
key_functions: N/A
latest_change: Promoted the new CORA memo as the main label-free recommendation after synthesizing local diagnostics from D-COLA and STAWA with adjacent literature on predictive multiplicity, model soups, and non-convergent dynamics.
change_log:
  - 2026-03-17 19:35: Promoted the new CORA memo as the main label-free recommendation after synthesizing local diagnostics from D-COLA and STAWA with adjacent literature on predictive multiplicity, model soups, and non-convergent dynamics.
  - 2026-03-16 04:19: Added the simpler stationarity-aware memo as a new label-free candidate while keeping RIWA as the more theory-heavy main recommendation.
  - 2026-03-16 03:12: Promoted the label-free reweighting-invariant memo to the main recommendation and kept ROWA as the best domain-labeled alternative.
  - 2026-03-16 01:30: Promoted the recoverability-oriented memo to the main recommendation and kept the adaptation-information and COWA memos as supporting alternatives.
  - 2026-03-16 01:11: Promoted the adaptation-information memo to the main recommendation and kept the earlier COWA memo as a precursor.
  - 2026-03-16 00:53: Normalized the file to ASCII and kept the index linked to the main research memo.
  - 2026-03-16 00:45: Created the workspace index and linked the main research memo.
---

# Workspace Index

Current main memo:

- [Consensus-of-Rashomon averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/cora_consensus_of_rashomon_averaging.md)

Previous main label-free memo:

- [Reweighting-invariant weight averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/reweighting_invariant_weight_averaging.md)

Simplest new label-free candidate:

- [Stationarity-aware weight averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/stationarity_aware_weight_averaging.md)

Best domain-labeled alternative:

- [Recoverability-oriented weight averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/recoverability_oriented_weight_averaging.md)

Secondary memo:

- [Minimum adaptation information weight averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/minimum_adaptation_information_weight_averaging.md)

Precursor memos:

- [Consensus overlap weight averaging](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/consensus_overlap_weight_averaging.md)

Current conclusion:

- `CORA` (Consensus-of-Rashomon Averaging) is now the strongest label-free candidate because it reframes post-hoc DG around predictive multiplicity: build the connected near-optimal checkpoint set, identify the consensus core of examples on which good checkpoints agree, and output the single soup that matches that core while hedging on the high-multiplicity fringe.
- `RIWA` remains the strongest support-perturbation alternative because it is single-run, post-hoc, architecture-agnostic, and does not require domain labels: it selects checkpoints by whether validation performance is locally insensitive to adversarial reweightings of the source support.
- `STAWA` (Stationarity-Aware Weight Averaging) is the simplest new label-free candidate: it selects checkpoints by whether their predictions have become dynamically stable under the ongoing training trajectory rather than by parameter-space flatness.
- `ROWA` (Recoverability-Oriented Weight Averaging) remains the strongest domain-labeled alternative because it directly probes cross-domain recoverability, but it cannot satisfy the no-domain-label requirement.
- `MAIWA` is still the deeper theoretical alternative, but it is heavier and less likely to spread quickly if it only works with careful posterior approximations.
- `COWA` remains useful as a geometric precursor and as a second-order surrogate for more transfer-centered objectives.
- The existing local draft at [`literature/tawa.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/tawa.tex) is not sufficient as-is because its main theory assumes a generic "quality metric" already correlated with OOD accuracy, which makes the core claim circular.
