---
title: Harsh Review of Trajectory Spectral Filtering Proposal
description: Consolidated hostile review of the TSF research proposal from novelty, theory, empirical, and meta-review perspectives.
created: 2026-04-02 17:20
last_modified: 2026-04-02 17:20
last_modified_by: codex
status: active
related_files:
  - claude_workspace/research/trajectory_spectral_filtering_proposal.md
  - claude_workspace/results/results_ledger.md
  - claude_workspace/results/swing_lessons_learned.md
key_functions:
  - Preserve the main reviewer objections to TSF
  - Record the strongest positive and negative arguments
  - Define go/no-go criteria before implementation
latest_change: Initial consolidated harsh review memo for TSF.
---

# Harsh Review Summary

This memo summarizes four hostile review passes over [trajectory_spectral_filtering_proposal.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/trajectory_spectral_filtering_proposal.md):

- novelty/literature
- theory/assumptions
- empirical/project-history
- meta-review / area-chair synthesis

## Overall verdict

The reviewers did **not** reject TSF as nonsense, but they did reject it as a ready-made headline method.

The consensus position was:

- **interesting enough to test cheaply**
- **not justified enough to bet the project on**
- **must beat trivial smoothing baselines to count as real**

## Strongest positive arguments

1. TSF is genuinely different from the specific local failure pattern of:
   - safe-basin subset selection
   - safe-basin center finding
   - source-fit or witness-based continuous weight optimization

2. The stripped-down version is much better than the original extrapolation variant:
   - no infinite-horizon claims
   - no inference-time ensemble
   - one final deployable model

3. The construction is mathematically clean:
   - define groupwise update sequences
   - apply a checkpoint-axis transform
   - attenuate selected modes
   - reconstruct the endpoint from the filtered path

4. There is at least moderate support for the broad motivation from adjacent literature:
   - trajectories can matter
   - iterate smoothing can help
   - post-hoc weight-space transforms can alter generalization behavior

## Strongest negative arguments

1. **The novelty claim must stay narrow.**
   TSF is not a new broad family. It is a specific trajectory operator inside an already crowded checkpoint/iterate literature.

2. **The theory story is too weak if framed as domain-generalization theory.**
   The defensible theorem is a denoising theorem on the observed trajectory, not a theorem that checkpoint-axis low frequencies are robust and high frequencies are spurious.

3. **The checkpoint axis does not have strong native frequency semantics.**
   A DCT over checkpoint index is mathematically fine, but its semantic meaning depends on save density, optimizer schedule, and training regime.

4. **The nearest real baseline may be ordinary smoothing.**
   If update EMA or moving-average smoothing matches TSF, then the spectral story is not pulling its weight.

5. **Full-trajectory use is the proposal's most fragile choice.**
   The local project record repeatedly found that locality matters. Using the entire trajectory risks reintroducing incompatible regimes.

6. **The OOD story is speculative.**
   The literature supports only a weak analogy. It does not establish that checkpoint-axis low-band components are the ones that transfer best.

## Reviewer-specific takeaways

### Novelty reviewer

- The proposal originally overclaimed conceptual novelty.
- The only defensible novelty is:
  - groupwise filtering of checkpoint-to-checkpoint updates
  - along the checkpoint axis
  - with reconstruction of one final endpoint

### Theory reviewer

- The original theory leaned too hard on a semantic decomposition.
- The revised defensible statement is:
  - under a toy signal model on the observed trajectory,
  - TSF can reduce error to a latent smoothed path,
  - and any loss improvement is conditional on local smoothness.

### Empirical reviewer

- The real baseline is still:
  - same-run safe-pool uniform averaging
  - plus trivial update smoothing baselines
- If TSF cannot beat those by a clear margin, it should be dropped.

### Meta-reviewer

- As a proposal: `Weak Reject`
- As a cheap falsification study: `Accept`

## Go / No-Go criteria

Proceed only if the experimental plan is tight enough to answer these:

1. Does TSF beat update EMA and moving-average smoothing?
2. Does TSF beat the same-run safe-pool uniform baseline?
3. Does TSF remain stable under checkpoint subsampling?
4. Does the full-trajectory version matter, or does performance only appear once the method collapses to a late local window?

If the answer to any of these goes the wrong way, TSF should not become the headline method.

## Final recommendation

Treat TSF as:

- a serious but high-risk proposal
- a falsifiable experiment
- and a bounded attempt to escape the already-failed "safe basin + clever correction" template

Do **not** treat it as:

- the next mainline method
- a theory-led DG contribution
- or a claim that trajectory-frequency filtering is already established as the right abstraction
