---
title: SWING Lessons Learned
description: Lessons learned from the SWING experimental branch, including methodological takeaways, diagnostic lessons, and the final decision to pivot away from the current formulation.
created: 2026-04-01 12:00
last_modified: 2026-04-01 12:00
last_modified_by: agent
status: active
related_files: claude_workspace/results/results_ledger.md, domaingen/posthoc/swing.py
key_functions:
  - Preserve the conceptual lessons from the SWING branch
  - Separate what worked from what did not
  - Make the pivot decision legible for future work
latest_change: Added a dedicated lessons-learned note summarizing what the SWING experiments actually established and why the project should pivot away from the current formulation.
change_log:
  - 2026-04-01 12:00: Initial lessons-learned document for the SWING branch
---

# Core Lessons

## 1. The safe basin is real

The strongest and most stable empirical signal from this branch was not the directional shrinkage itself. It was the existence of a useful post-hoc safe basin:

- barrier-filtered checkpoint pools were repeatedly strong
- averaging within those safe pools was repeatedly strong
- widening the safe pool moderately helped, as long as the local regression cloud stayed local

This is the most important positive result from the branch.

## 2. Uniform safe-pool averaging is the real baseline

The experiments made it clear that the right baseline is not plain ERM. It is:

- `safe-pool construction`
- plus `uniform averaging over the accepted safe checkpoints`

Against that baseline, the current `SWING` directional edit did not win clearly or consistently.

That changes the burden of proof for any future method:

- beating ERM is not enough
- beating the safe-pool uniform soup is the real test

## 3. The current SWING shrinkage rule is too weak as a method claim

The current source-reweighting eigen-shrinkage idea was mathematically coherent and implementable, but empirically it did not justify itself.

Observed failure pattern:

- sometimes `SWING` beat the uniform safe-pool baseline, but only by tiny margins
- often it tied or lost
- `rank=3` did not rescue the method
- adding isotropic inflation `tau` improved conditioning but did not reliably improve performance

So the issue is not merely “the solver was bad.” The issue is that the method itself has not shown strong enough value.

## 4. Over-shrink was a real issue, but not the whole story

One early hypothesis was that `SWING` was failing because the fit curvature was too weak and the fragility penalty was overwhelming everything.

Evidence supporting that:

- very large generalized eigenvalues
- shrinkage factors near zero
- successful runs that looked almost identical to the basin center / uniform average

But later experiments also showed:

- even after reducing over-shrink with nonzero `tau`, `SWING` still often underperformed uniform

So over-shrink was real, but fixing over-shrink did not fix the deeper problem.

## 5. Rank support and geometry matter a lot

The branch clarified the progression of bottlenecks:

- early on, the main issue was safe-pool size
- then the main issue became local-cloud selection
- then the issue became source-fit conditioning

In other words:

- the project moved from “not enough safe checkpoints”
- to “too global a local cloud”
- to “the current estimator is still not informative enough even when the geometry is technically supported”

That diagnostic progression is useful for future methods.

# Implementation Lessons

## 6. Diagnostics were worth building

Several important truths only became obvious after the diagnostics/reporting work:

- whether the fit solver really converged
- whether a line search failed
- whether the generalized-eigen closed form matched the direct linear solve
- whether a run was numerically approximate rather than clean
- whether the uniform baseline was actually better within the same run

Without that instrumentation, the branch would have been much harder to evaluate honestly.

## 7. The non-fatal continuation path was useful, but it only exposed the truth

Allowing the source-fit solver to continue with the last accepted iterate was the right engineering choice for exploration:

- it let higher-rank runs complete
- it exposed what the method actually does in numerically delicate regimes

But the continuation path did not “save” the method. It mainly made the method easier to falsify honestly.

That is a good outcome.

## 8. Auxiliary baselines need first-class treatment

Once `SWING-uniform` existed, it had to be treated as a real selector:

- separate results rows
- separate manifest entries
- separate checkpoint artifacts
- proper rerun cleanup

This was worth doing because the within-run comparison against the uniform baseline became the key scientific comparison.

# Research Lessons

## 9. A negative result can still be highly productive

This branch did not produce the hoped-for headline method, but it was not wasted.

It established:

- a stronger baseline
- a stronger empirical standard
- a safer implementation/reporting stack
- a clearer picture of what kind of method is actually supported by the evidence

That is real progress.

## 10. The project has moved back toward a SWAD-like center

The experiments effectively brought the project back toward a simpler conclusion:

- interiority / centrality inside a stable basin seems more reliable than a fragile directional edit

That does not mean “just do SWAD again.”
It means the evidence now favors a new method whose core claim is closer to:

- certified safe basin construction
- principled interior-point selection inside that basin

rather than:

- source-reweighting eigen-shrinkage of basin directions

# Final Recommendation

The current `SWING` formulation should be treated as:

- a completed branch
- a negative-result ablation
- and a tool for future comparisons

The next method should start from the empirically supported core:

- safe basin construction
- uniform or central basin aggregation

and only add complexity if that complexity can plausibly beat the safe-pool uniform baseline by a clear and repeatable margin.
