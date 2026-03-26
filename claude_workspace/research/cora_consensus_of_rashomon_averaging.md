---
title: Consensus-of-Rashomon averaging for label-free single-run post-hoc domain generalization
description: Research memo proposing CORA, a post-hoc DG method that selects and soups checkpoints by the predictive consensus core of the connected trajectory Rashomon set rather than by flatness or checkpoint calmness alone.
created: 2026-03-17 19:35
last_modified: 2026-03-17 19:35
last_modified_by: agent
status: active
related_files: claude_workspace/workspace_index.md, claude_workspace/research/stationarity_aware_weight_averaging.md, claude_workspace/papers/d_cola/d_cola_neurips.tex, literature/swad_tex_source/3.method.tex, literature/diwa_tex_source/sections/02_theory.tex
key_functions: N/A
latest_change: Added a new main candidate that reframes post-hoc DG around predictive multiplicity and the consensus core of the trajectory Rashomon set.
change_log:
  - 2026-03-17 19:35: Added the CORA memo after synthesizing local diagnostics, local papers, and adjacent literature on multiplicity, churn, soups, and non-convergent dynamics.
---

# Bottom line

The strongest new candidate I can defend after looking at `SWAD`, `DiWA`,
`D-COLA`, `STAWA`, `MIRO`, and adjacent literature is:

- **`CORA` = `Consensus-of-Rashomon Averaging`**

The core claim is:

> **Good post-hoc DG models are not the flattest checkpoints or the calmest checkpoints. They are the checkpoints or soups that sit closest to the predictive center of the connected set of near-optimal models.**

That is the conceptual jump.

`SWAD` says: find a flat late basin.

`D-COLA` says: use a safe soup of complementary checkpoints.

`STAWA` says: prefer checkpoints whose predictions have stopped drifting.

`CORA` says:

> **Construct the connected trajectory Rashomon set, identify its predictive consensus core, and output the single soup that best matches that core while hedging on the high-multiplicity fringe.**

I think this is the first candidate here that:

- is still single-run,
- still post-hoc,
- uses no domain labels,
- is architecture-agnostic,
- is simple enough to explain in one sentence,
- and actually changes the object being optimized.

# Why this follows from the evidence we already have

## What `SWAD` got right

`SWAD` works because dense checkpoints inside one broad, pre-overfit, connected
basin are usually safer to average than isolated best-validation checkpoints.

The local SWAD source explicitly motivates:

- robust empirical loss,
- flat connected regions,
- and dense averaging inside a late trajectory window.

But the method still leaves one big thing unmodeled:

- **which predictions are actually shared across the good checkpoints, and which are arbitrary disagreements inside the good-model set.**

Flatness alone cannot answer that.

## What `D-COLA` got right

On the observed replay evidence, `D-COLA` won by doing three things `SWAD` and
`STAWA` did not do together:

- it did not collapse to one checkpoint,
- it used nonuniform weights over noncontiguous checkpoints,
- and it exploited complementary early/late checkpoints while staying soup-safe.

The local diagnostics show exactly that:

- `D-COLA` used candidates `[350, 500, 850, 1150, 1700, 1800, 8450, 8500]`
  with learned nonuniform weights,
- most of the final signal came from diversity/covariance shaping rather than
  the locality penalty alone,
- and the best source-balanced anchor was early, not late.

So the important lesson is not “covariance is magic.”

It is:

> **there exists useful predictive complementarity inside one trajectory that contiguous-window methods are throwing away.**

## What `STAWA` got wrong

`STAWA-old` and `STAWA-new` each collapsed to a single checkpoint on the replay.

The local diagnostics show the exact failure mode:

- `STAWA-old` was still dominated by validation loss,
- `STAWA-new` gated so hard on the loss plateau that only one checkpoint
  survived,
- and neither version actually used averaging in the way `SWAD` or `D-COLA`
  did.

So the problem is not that functional instability is irrelevant.

The problem is that:

> **global checkpoint calmness is the wrong granularity.**

The useful signal is not “which checkpoint is calmest overall?”

The useful signal is:

- which **examples** are stable across good checkpoints,
- which examples lie in a disagreement fringe,
- and which soup best preserves the stable consensus while refusing to overfit
  the fringe.

# The new principle

## Predictive multiplicity is the DG object, not flatness alone

Adjacent work on the Rashomon set and predictive churn says that near-optimal
models can disagree substantially on individual predictions even when their
average loss is almost identical.

That is exactly the object DG should care about.

Why:

- predictions shared by many near-optimal checkpoints are more likely to come
  from invariant structure,
- predictions that flip across near-optimal checkpoints are more likely to be
  source-underdetermined, shortcut-driven, or fragile under shift.

So the right post-hoc selector is not:

- “lowest validation loss,”
- “widest basin,”
- or “lowest future drift.”

It is:

> **closest to the predictive barycenter of the connected near-optimal checkpoint set, especially on low-multiplicity examples.**

This is the label-free post-hoc analog of canalization:

- many perturbations of the model-development path,
- one robust phenotype in prediction space.

# The proposed method: `CORA`

## Step 1: build a connected trajectory Rashomon set

From a single dense trajectory `{theta_t}_{t=1}^K`, compute pooled labeled
source-validation loss `L_V(theta_t)` with **no domain labels**.

Choose an anchor:

```text
a = argmin_t L_V(theta_t)
```

For each checkpoint, compute a locality / soupability score `B(t,a)`, for
example a linear interpolation barrier on the pooled validation set exactly in
the spirit of `D-COLA`.

Define the connected near-optimal candidate set:

```text
C = { t :
      L_V(theta_t) <= L_V^* + epsilon
      and
      B(t,a) <= tau }
```

This keeps the good part of `SWAD` and `D-COLA`:

- low loss,
- plus explicit soup safety,
- but no domain labels and no hard contiguity restriction.

## Step 2: estimate the predictive consensus core

On a pooled unlabeled support set `U = {x_i}_{i=1}^m`, cache checkpoint
predictions `p_t(x)`.

Define a soft candidate prior:

```text
rho_t propto exp( -beta [L_V(theta_t) - L_V^*] - nu B(t,a) )
```

Then define the trajectory committee barycenter:

```text
q(x) = sum_{t in C} rho_t p_t(x)
```

and the per-example predictive multiplicity:

```text
M(x) = sum_{t in C} rho_t d(p_t(x), q(x))
```

where `d` is:

- `KL` or Jensen-Shannon for classification,
- squared error for regression,
- any proper Bregman divergence for a task-compatible output space.

Now define the consensus-core weight:

```text
c(x) = exp(-kappa M(x))
```

Interpretation:

- `c(x)` near `1` means many good checkpoints agree on that example,
- `c(x)` near `0` means the example lies in the disagreement fringe of the
  trajectory Rashomon set.

This is where `STAWA` comes back in the right form:

- not as a checkpoint score,
- but as example-level instability inside the good-model set.

## Step 3: find the single soup that matches the core

Let the predictive mixture induced by soup weights `w in Delta^{|C|}` be

```text
p_w(x) = sum_{t in C} w_t p_t(x)
```

Optimize:

```text
J(w)
= L_V^ens(w)
 + lambda_core * (1/m) sum_{x in U} c(x) KL(q(x) || p_w(x))
 + lambda_fringe * (1/m) sum_{x in U} (1 - c(x)) * (-H(p_w(x)))
 + lambda_loc * b^T w
 + lambda_ent * sum_{t in C} w_t log w_t
```

where:

- `L_V^ens(w)` is the predictive-mixture validation loss on pooled labeled
  source validation data,
- the `core` term makes the soup match the trajectory barycenter on stable
  examples,
- the `fringe` term discourages brittle overconfidence on examples where the
  good-model set itself disagrees,
- `b_t = B(t,a)` is the locality vector,
- and the entropy term stabilizes the simplex optimization.

The final single test-time model is the weight soup:

```text
theta_CORA = sum_{t in C} w_t theta_t
```

## Why this is still practical

`CORA` is still:

- single-run,
- post-hoc,
- one-model at test time,
- and cache-based.

Like `D-COLA`, the optimization happens over cached predictions and cached
validation losses, not over a new training loop.

# Why this is simpler and more fundamental than it looks

The whole idea compresses to one sentence:

> **Choose the soup that best matches what the good checkpoints agree on, and do not overcommit where the good checkpoints themselves disagree.**

That is arguably more direct than:

- flatness,
- temporal calmness,
- or covariance penalties.

It also imports a genuinely different research object:

- the **connected trajectory Rashomon set**,
- and its **predictive multiplicity structure**.

That is not how DG has usually framed single-run post-hoc selection.

# Theory skeleton

## 1. Barycenter optimality

Under proper losses, the committee barycenter `q(x)` is the central predictive
object of the candidate set.

For log loss, `q(x)` is exactly the predictive Bayes act of the committee
distribution `rho`.

So forcing the soup to match `q(x)` on high-consensus examples is not an ad hoc
heuristic. It is the proper-loss center of the connected near-optimal set.

## 2. Multiplicity-core target-risk certificate

Let `T` be an unseen target distribution that reweights source support.

Suppose:

- low-multiplicity examples correspond to stable labels across the near-optimal
  set,
- high-multiplicity examples are the underdetermined fringe,
- and the target puts bounded mass on that fringe.

Then a natural certificate has the form:

```text
R_T(theta_CORA)
<=
L_V^ens(w)
+ gamma * E_{x ~ U}[ c(x) KL(q(x) || p_w(x)) ]
+ gamma * E_{x ~ U}[ (1 - c(x)) psi(M(x)) ]
+ localization error
+ concentration
```

This is the right kind of theorem target:

- it is not “CORA always beats SWAD,”
- it is “CORA explicitly controls a shift-relevant term that SWAD and STAWA do
  not model.”

## 3. Separation from flatness-only and stationarity-only selectors

A constructive separation argument should be possible:

- two checkpoints can have the same validation loss and similar local flatness,
- a third can have lower global drift,
- yet the checkpoint or soup closest to the Rashomon barycenter on low-
  multiplicity examples has lower target risk.

That would separate `CORA` from both:

- `SWAD`-style flatness,
- and `STAWA`-style global calmness.

## 4. Convexity

For classification:

- `L_V^ens(w)` is convex,
- `KL(q || p_w)` is convex in `w`,
- `-H(p_w)` is convex,
- `b^T w` is linear,
- simplex entropy regularization is convex.

So the post-hoc stage stays computationally clean.

# Why this could beat `SWAD`

`SWAD` assumes a broad late basin is the right object.

`CORA` says the right object is the center of the connected good-model set in
prediction space.

That matters when:

- the trajectory contains multiple soup-safe phases,
- some source examples are stable across all good checkpoints,
- and the rest are arbitrary disagreements or shortcut-driven fringe behavior.

In exactly that regime:

- `SWAD` wastes useful noncontiguous checkpoints,
- `STAWA` overvalues calmness,
- `D-COLA` sees diversity but not which examples the diversity is actually
  about,
- while `CORA` extracts the stable predictive core directly.

# Why this could beat `D-COLA`

`D-COLA` uses:

- worst-domain source risk,
- covariance,
- locality.

But it still treats diversity mostly as a checkpoint-level global statistic.

`CORA` does something more granular:

- it asks **where** the good checkpoints agree,
- where they disagree,
- and whether the final single model is matching the right part of that
  structure.

So `CORA` is the label-free successor to the part of `D-COLA` that seems most
real:

- nonuniform safe soups help,
- but the missing signal is examplewise consensus structure, not just global
  covariance.

# Why this is not just “model soups”

Plain model soups say:

- average good models in one basin.

`CORA` says:

- first define the connected near-optimal set,
- then identify the **consensus core** and the **disagreement fringe**,
- then solve for the single soup that matches the core and hedges on the
  fringe.

That is a different objective and a different theory story.

The closest adjacent literatures are:

- Rashomon sets / predictive multiplicity,
- predictive churn,
- model soups,
- mode connectivity,
- and non-convergent learning stability.

But I do not know a standard DG post-hoc method that uses those objects this
way.

# What would falsify this idea quickly

`CORA` is wrong if one or more of these turn out false:

1. Low-multiplicity source examples are not more target-stable than
   high-multiplicity ones.
2. The connected trajectory Rashomon set does not contain meaningful
   multi-phase complementarity beyond what `SWAD` already captures.
3. The consensus-core distillation term just collapses to uniform soups or
   best-validation soups.
4. The high-multiplicity fringe is not where OOD failure is concentrated.

These are all falsifiable.

# The first experiments I would run

1. Plot per-example multiplicity `M(x)` against target error for held-out target
   domains.
2. Compare `SWAD`, `D-COLA`, `STAWA-new`, and `CORA` on the exact same replayed
   checkpoint sets.
3. Show matched checkpoint sets with similar validation loss and barrier but
   different multiplicity-core structure.
4. Ablate:
   - no core term,
   - no fringe term,
   - no locality gate,
   - uniform `rho`,
   - and `CORA` without soft candidate prior.

# What extra files would help next

I do not need more files to state the method, but the next empirical pass would
be much tighter if we pull:

- raw per-checkpoint support-set logits or probabilities for the replayed
  checkpoints,
- full replay metrics for `SWAD` in a diagnostics JSON analogous to the local
  `STAWA` and `D-COLA` files,
- and, if available, per-example target errors for PACS test env `0`.

Those three artifacts would let me test the central `CORA` hypothesis directly:

> high trajectory multiplicity predicts target fragility, and the best single
> post-hoc soup is the one closest to the low-multiplicity consensus core.

# Current recommendation

If the goal is a new field-level post-hoc DG idea that is still:

- label-free with respect to domains,
- single-run,
- post-hoc,
- architecture-agnostic,
- and stronger than `STAWA`,

then `CORA` is the best candidate I have so far.

I would currently rank the label-free ideas:

1. `CORA`
2. `RIWA`
3. `STAWA`

because `CORA` is the first one that changes the object from:

- weight-space flatness,
- checkpoint calmness,
- or raw support perturbation sensitivity,

to:

- **predictive multiplicity and consensus structure of the connected good-model
  set itself.**
