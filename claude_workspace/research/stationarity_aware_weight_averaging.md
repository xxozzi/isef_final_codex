---
title: Stationarity-aware weight averaging for label-free post-hoc domain generalization
description: Research memo proposing a simple label-free post-hoc DG method based on the principle that checkpoints with low functional drift under ongoing training dynamics generalize better under shift.
created: 2026-03-16 04:18
last_modified: 2026-03-16 04:18
last_modified_by: agent
status: active
related_files: claude_workspace/workspace_index.md, claude_workspace/research/reweighting_invariant_weight_averaging.md, claude_workspace/papers/d_cola/d_cola_neurips.tex, literature/swad_tex_source/main.tex
key_functions: N/A
latest_change: Added a new simple label-free post-hoc DG candidate based on functional stationarity and predictive churn reduction.
change_log:
  - 2026-03-16 04:18: Added a new simple label-free post-hoc DG candidate based on functional stationarity and predictive churn reduction.
---

# Bottom Line

If the goal is a **simpler, cleaner, more slogan-like** idea than `RIWA`, the best candidate I found is:

- **`STAWA` = Stationarity-Aware Weight Averaging**

Core claim:

> **Checkpoints that have stopped changing functionally under ongoing SGD generalize better under distribution shift.**

This is closer to the shape of a `SWAD`-level idea:

- `SWAD`: flat minima generalize better.
- `STAWA`: functionally stationary checkpoints generalize better.

It is:

- post-hoc,
- label-free with respect to domains,
- single-run,
- architecture-agnostic,
- task-agnostic for predictive models with a proper output divergence,
- and simpler to explain than local DRO over sample-weight space.

# Why This Idea Is Different

## The missing object in SWAD

`SWAD` probes stability in **parameter space**.

But deep networks can move in weight space without much functional change, and they can also keep changing their function even inside a region that looks geometrically benign in pooled loss.

Domain generalization is fundamentally about the stability of the **learned function** under the real training dynamics that extracted it, not just about local Euclidean perturbations of the weights.

So the new principle is:

- do not ask whether the weights are easy to perturb,
- ask whether the **predictions have entered a stable plateau**.

## Cross-field inspiration

This idea is supported by three different lines of work:

1. **Statistical algorithmic stability for non-convergent training**
   - Chandramoorthy et al. show that even when SGD does not converge to a fixed point, the stability of the time-asymptotic behavior relates to generalization.
   - Their abstract states: networks that "`train stably generalize better`."

2. **Checkpoint ensembles**
   - Single-run checkpoint methods already exploit the fact that one trajectory contains useful generalization information.
   - But they use checkpoints mainly for averaging, not for defining a DG-specific stationarity score.

3. **Predictive churn reduction**
   - In deployment literature, prediction flips across model updates are treated as a reliability problem.
   - That literature is not about DG, but it gives a strong clue: unstable predictions often mean the model is still moving between incompatible local explanations.

# The Proposed Principle

## Functional stationarity

Let a single training run produce checkpoints `theta_1, ..., theta_K`.

Take a held-out source set `U` and optionally a labeled validation set `V`.

For checkpoint `theta_t`, define its **future predictive drift** over a horizon `H` by

```text
D_t = (1 / H) sum_{h=1}^H d( f_{theta_t}(U), f_{theta_{t+h}}(U) ).
```

Here `d` is a task-appropriate output divergence:

- KL divergence between predictive distributions for classification,
- squared prediction difference for regression,
- token-level KL for sequence models,
- or any proper prediction-space discrepancy.

Interpretation:

- if `D_t` is large, the function is still moving,
- if `D_t` is small, the function has entered a stable attractor or plateau.

## Plateau-constrained score

Define the stationarity score

```text
J_t = lambda_1 * mean_drift_t + lambda_2 * spread_drift_t.
```

Then gate by source fit:

```text
A_epsilon = { t : L_V(theta_t) <= min_s L_V(theta_s) + epsilon }.
```

The selector is:

```text
t_star = arg min_{t in A_epsilon} J_t
W = connected component around t_star inside
    { t in A_epsilon : J_t <= J_{t_star} + delta }.
```

If `W` is too short, expand it to a minimum window size using the nearest
admissible checkpoints on either side. Then average that plateau-constrained
window.

This is the version I would actually bet on after seeing the first real run:
it prevents the main failure mode of the original memo, namely selecting
functionally calm but still undertrained checkpoints too early in training.

# Why This Could Beat SWAD

## A more direct object

`SWAD` relies on the hypothesis:

- flatter parameter basins imply better DG.

`STAWA` relies on the stronger, more directly DG-relevant hypothesis:

- checkpoints whose **functions** are stable under the real source-training dynamics are better universal predictors.

That matters because:

- weight symmetries can make parameter-space geometry misleading,
- low curvature does not guarantee that the decision rule has stabilized,
- and DG failures often come from late-stage specialization to brittle source regularities.

## What STAWA sees that SWAD misses

Two checkpoints can have:

- similar source validation loss,
- similar pooled flatness,
- similar local Hessian statistics,

yet differ strongly in whether their predictions keep drifting over the next `H` checkpoints.

`SWAD` cannot distinguish them if the pooled geometry looks similar.
`STAWA` can.

## Intuition about spurious features

The simplest mental model is:

- invariant or semantic predictors stabilize earlier and stay stable,
- spurious or shortcut predictors keep being traded against each other late in training,
- prediction churn is therefore a symptom of unresolved shortcut competition.

So `STAWA` should prefer the checkpoint where the stable part of the function has already formed but before further drift specializes it to accidental source regularities.

# Theory Sketch

## Population object

Let `A` denote the stochastic training operator that maps a checkpoint to its next-step updated predictor under SGD randomness.

Then the relevant object is not just the instantaneous predictor `f_theta`, but the short-horizon orbit

```text
f_theta, A f_theta, A^2 f_theta, ...
```

`STAWA` prefers checkpoints for which this orbit is already nearly stationary in prediction space on held-out source support.

## Stability principle

From statistical algorithmic stability for non-convergent training:

- if the time-asymptotic behavior of the learning process is stable,
- then generalization improves.

`STAWA` turns that qualitative principle into a post-hoc selector:

- estimate local time-asymptotic stability from dense checkpoints,
- then average inside a low-drift low-loss region.

## Prototype bound

A stylized bound should look like:

```text
R_T(theta_t)
<= R_src(theta_t)
 + c1 * Shift(src, T)
 + c2 * D_t
 + higher-order terms.
```

The idea is:

- source risk is the ordinary fit term,
- source-target shift remains uncontrollable,
- but functional drift `D_t` becomes a controllable selector term.

This is structurally similar to how `SWAD` turns robust source geometry into a controllable term, but the new term is dynamical and function-space based.

## Why window averaging is natural here

If a low-score interval is genuinely a functional plateau, then nearby checkpoints should:

- make similar predictions,
- have low barriers between them in function space,
- and averaging them should preserve the function while reducing residual stochastic variance.

That gives the same practical ending as `SWAD`, but the selection rule is no longer geometry-first.

# Why This Is Simpler Than RIWA

`RIWA` is stronger mathematically, but heavier conceptually:

- it uses local distributional adversaries in sample-weight space,
- covariance penalties,
- and a DRO interpretation.

`STAWA` has a cleaner slogan:

- **generalizable checkpoints are the ones whose predictions have stopped moving.**

That is easier to communicate, easier to visualize, and probably easier to sell as a new field-level lens if it works.

# Comparison To Other Candidate Ideas

## Compared with D-COLA

`D-COLA` is richer and more optimized, but it is not the same kind of idea:

- it is more of a carefully engineered post-hoc objective,
- it depends on source-domain balancing,
- and it does not satisfy the no-domain-label requirement.

`STAWA` is much closer to the `SWAD` simplicity bar.

## Compared with RIWA

`RIWA` asks:

- is the checkpoint robust to nearby source-support reweightings?

`STAWA` asks:

- has the checkpoint's function become dynamically stationary?

`RIWA` is the better principled local-DRO idea.
`STAWA` is the better simple field-slogan idea.

## Compared with layer rotation / neural collapse / margin ideas

Those are weaker candidates here because:

- layer rotation is interesting but not very DG-specific,
- neural collapse is too classification-specific,
- margin ideas are less task-agnostic,
- and tail-risk / CVaR selection is too close to existing robust-risk logic.

# Novelty Assessment

What I found in the literature:

- `SWAD` uses flatness and dense averaging for DG.
- `Checkpoint Ensembles` uses single-run checkpoint prediction averaging, but not DG-specific stationarity scoring.
- `Maintaining Stability and Plasticity for Predictive Churn Reduction` studies prediction consistency across model updates, but not DG and not post-hoc checkpoint selection for OOD transfer.
- `On the generalization of learning algorithms that do not converge` provides theory that stable time-asymptotic behavior relates to generalization, but does not turn that into a DG checkpoint selector.

So the idea seems to occupy a real gap:

- **use temporal functional stationarity itself as the post-hoc DG selection principle.**

I have not found a paper that already makes this exact move.

# The Strongest Version Of The Method

If we wanted the best practical variant rather than the absolute simplest one, I would use:

```text
S_t = L_V(theta_t)
    + lambda_1 D_t
    + lambda_2 Var_x[ d( f_{theta_t}(x), f_{theta_{t+H}}(x) ) ].
```

The variance term matters because we do not only want low average drift; we want drift not to concentrate on a hidden subset of examples.

But the cleanest first paper should probably keep only:

```text
S_t = L_V(theta_t) + lambda D_t.
```

# Honest Assessment

This is the first label-free idea in this search that I think has a real chance to be both:

- simple enough to spread,
- and meaningfully different from `SWAD`.

I still cannot honestly call it a guaranteed breakthrough.

What I can say is:

- it is simpler and more memorable than `RIWA`,
- more compatible with the no-domain-label constraint than `ROWA` or `D-COLA`,
- and it has a clearer gap in the literature than most other candidate principles I checked.

# Sources

- SWAD: https://openreview.net/forum?id=zkHlu_3sJYU
- On the generalization of learning algorithms that do not converge: https://arxiv.org/abs/2208.07951
- Checkpoint Ensembles: https://arxiv.org/abs/1710.03282
- Maintaining Stability and Plasticity for Predictive Churn Reduction: https://arxiv.org/abs/2305.04135
- Layer rotation: https://openreview.net/forum?id=B1g4DEB234
