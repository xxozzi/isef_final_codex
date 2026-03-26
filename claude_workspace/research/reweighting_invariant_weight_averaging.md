---
title: Reweighting-invariant weight averaging for label-free post-hoc domain generalization
description: Research memo proposing a domain-label-free post-hoc method that selects checkpoints by local invariance to sample-weight perturbations, inspired by TangentProp, influence functions, and distributionally robust optimization.
created: 2026-03-16 02:24
last_modified: 2026-03-16 03:14
last_modified_by: agent
status: active
related_files: claude_workspace/workspace_index.md, claude_workspace/research/recoverability_oriented_weight_averaging.md, literature/swad_tex_source/main.tex, literature/tawa.tex
key_functions: N/A
latest_change: Added a canalization framing to the label-free post-hoc DG candidate based on invariance to sample-weight perturbations.
change_log:
  - 2026-03-16 03:14: Added a canalization framing to the label-free post-hoc DG candidate based on invariance to sample-weight perturbations.
  - 2026-03-16 02:24: Added a new label-free post-hoc DG candidate based on invariance to sample-weight perturbations.
---

# Bottom Line

This is the strongest second candidate I found once the requirements changed to:

- no domain labels,
- post-hoc,
- single-run,
- architecture-agnostic,
- task-agnostic,
- and simple enough to plausibly spread like `SWAD`.

The core claim is:

> **A checkpoint generalizes to unseen shifts when its post-hoc performance is insensitive to small reweightings of the training support.**

That gives a simple method:

- **`RIWA` = Reweighting-Invariant Weight Averaging**

`SWAD` seeks invariance in parameter space.
`RIWA` seeks invariance in data-distribution space.

That is the crucial conceptual jump.

## Biological Intuition: Canalization

In evolutionary biology, `canalization` means that a phenotype remains stable despite perturbations to the underlying developmental process or environment.

`RIWA` imports that principle into post-hoc model selection:

- the "phenotype" is validation behavior after a tiny update,
- the perturbations are local changes in which support examples matter more,
- and a good checkpoint is one whose behavior is canalized against those local redistributions.

This is not needed for the algorithm, but it is a useful way to understand why the method is trying to identify something more fundamental than pooled flatness.

# The New Principle

## Distributional Tangent Invariance

`TangentProp` argued that good generalization can come from low directional derivatives along nuisance directions in input space.

`RIWA` transfers the same idea to the empirical distribution:

- each nearby test environment is approximated by a small perturbation of sample weights,
- the relevant nuisance directions are therefore directions in the simplex of training weights,
- a good checkpoint is one whose validation loss changes very little along those directions.

This is label-free because the directions come from reweighting training examples, not from source-domain IDs.

## Why This Is Closer To DG Than Flatness

Flatness asks:

- if I perturb the weights, does the loss stay small?

`RIWA` asks:

- if the data distribution shifts slightly toward some latent subpopulation, does the post-hoc loss stay small?

That is much closer to domain shift.

# The Proposed Method: RIWA

## Core setup

Let `U = {z_i}_{i=1}^m` be a held-out source set used to estimate support perturbations, and let `V` be a validation set for model selection.

At checkpoint `theta_t`, define:

- training-example gradients `g_{i,t} = grad_theta l(z_i; theta_t)`,
- average support gradient `gbar_t = (1/m) sum_i g_{i,t}`,
- validation gradient `g_val,t = grad_theta L_V(theta_t)`.

Let `P_t` be a simple positive semidefinite preconditioner:

- identity for the simplest version,
- or a diagonal second-moment/Fisher approximation.

Now consider perturbed sample weights:

```text
alpha = (1/m) 1 + delta,
sum_i delta_i = 0,
||delta||_2 <= rho.
```

The weighted support gradient becomes:

```text
g_U(theta_t; alpha) = gbar_t + sum_i delta_i (g_{i,t} - gbar_t).
```

Take one virtual adaptation step:

```text
theta_t(alpha) = theta_t - eta P_t g_U(theta_t; alpha).
```

The exact robust score is:

```text
S_t^exact = max_{alpha in A_rho} L_V(theta_t(alpha)).
```

This is post-hoc and does not need retraining.

## First-order closed-form score

For small `eta`, first-order expansion yields:

```text
L_V(theta_t(alpha))
approx
L_V(theta_t)
- eta <g_val,t, P_t gbar_t>
- eta sum_i delta_i <g_val,t, P_t (g_{i,t} - gbar_t)>.
```

Maximizing over the centered `l2` ball gives:

```text
S_t^fo =
L_V(theta_t)
- eta <g_val,t, P_t gbar_t>
+ eta rho sqrt( sum_i <g_val,t, P_t (g_{i,t} - gbar_t)>^2 ).
```

Equivalently, if

```text
C_t = (1/m) sum_i (g_{i,t} - gbar_t)(g_{i,t} - gbar_t)^T
```

is the example-gradient covariance, then:

```text
S_t^fo =
L_V(theta_t)
- eta <g_val,t, P_t gbar_t>
+ eta rho sqrt( m g_val,t^T P_t C_t P_t g_val,t ).
```

This is the practical score.

Interpretation:

- the second term rewards progress that also helps validation,
- the third term penalizes sensitivity to latent support shifts.

So `RIWA` prefers checkpoints that are both useful and canalized against reweighting perturbations.

## Window selection and averaging

Exactly as in `SWAD`, define

```text
t_star = arg min_t S_t
W = { t : S_t <= S_{t_star} + delta }.
```

Then average a contiguous low-score window.

# Theory Sketch

## The population object

Let `rho` be a distribution over latent micro-environments or support components. A test shift is modeled as a nearby change in their mixture weights.

The object `RIWA` targets is the local distributionally robust risk:

```text
R_rho(theta_t)
= max_{Q: D(Q, P_src) <= epsilon}
L_Q(theta_t after one source-family step).
```

For empirical data, nearby distributions become sample reweightings.

So `RIWA` is selecting checkpoints by a local DRO criterion over the support, rather than by pooled flatness.

## Why the score has a clean worst-case interpretation

The first-order score is not a heuristic.

It is exactly the support function of an `l2` ambiguity set in sample-weight space. Therefore:

```text
max_{||delta||_2 <= rho, 1^T delta = 0}
sum_i delta_i a_i
= rho ||a - mean(a) 1||_2.
```

With

```text
a_i = - eta <g_val,t, P_t (g_{i,t} - gbar_t)>,
```

the robust penalty is the norm of the validation-direction sensitivity to reweighting.

## The conceptual theorem

Under local smoothness of `L_V` and bounded per-example gradients, the exact robust score satisfies:

```text
S_t^exact
<=
L_V(theta_t)
- eta <g_val,t, P_t gbar_t>
+ eta rho sqrt(m g_val,t^T P_t C_t P_t g_val,t)
+ O(eta^2).
```

So minimizing the first-order `RIWA` score minimizes an upper bound on the exact local robust validation loss.

## Why SWAD is the special case where reweighting sensitivity is invisible

If every example or latent support component produces nearly the same gradient at checkpoint `t`, then `C_t` is small and the robust penalty vanishes.

In that case, distributional perturbations barely matter locally, and the problem reduces to selecting a stable low-loss checkpoint. That is exactly the regime where flatness-based ideas like `SWAD` are enough.

But when latent support components pull in different directions, `C_t` is large. Then pooled flatness can be misleading, while `RIWA` can still detect fragility.

# Why This Could Beat SWAD

## 1. It targets the shift itself

`SWAD` is indirect:

- weight perturbation robustness.

`RIWA` is direct:

- robustness to nearby support shifts.

## 2. It does not need domain labels

That makes it usable in many settings where:

- domains are unavailable,
- domains are artificial,
- or the true shift does not align with the provided domain partition anyway.

## 3. It is architecture- and task-agnostic

Any differentiable task with a validation loss and checkpoint trajectory can use it:

- vision,
- NLP,
- tabular,
- graph,
- regression,
- classification,
- multimodal training.

## 4. It connects to post-hoc selection more broadly

The 2024 post-hoc reversal work shows that post-hoc transforms can reverse the ranking of checkpoints and that selecting for the transformed objective can be much better than naive model selection.

`RIWA` uses exactly that philosophy:

- select for the post-hoc robustified objective,
- not for the raw checkpoint metric.

# Practical Variants

## 1. Covariance form

Use the closed-form covariance penalty above.

Pros:

- cheap,
- elegant,
- architecture-agnostic.

## 2. Random-direction form

Sample `K` centered random reweightings `delta^(k)` and estimate:

```text
S_t^rand = max_k L_V(theta_t - eta P_t g_U(theta_t; alpha^(k))).
```

Pros:

- no explicit covariance matrix,
- easy with minibatch gradients.

## 3. Influence form

If inverse-Hessian products are available, use the parameter perturbation induced by sample reweighting through influence functions.

Pros:

- strongest theoretical link to exact retraining under data perturbation.

Cons:

- heavier than the other two.

The covariance form is the best first candidate.

# Novelty Relative To Existing Work

## Relative to SWAD

`SWAD`:

- selects by overfit-aware dense checkpoint averaging,
- motivated by flat minima and robust loss in parameter space.

`RIWA`:

- selects by invariance to sample-weight perturbations,
- motivated by local DRO and distributional tangent sensitivity.

## Relative to MAPLE and other sample-reweighting methods

MAPLE searches training weights through bilevel optimization.

`RIWA` does not retrain and does not optimize sample weights.
It uses reweighting only as a post-hoc probe for checkpoint robustness.

## Relative to influence-function work

Influence functions estimate how examples affect a model or prediction.

`RIWA` uses the same geometry for a different goal:

- checkpoint selection under unknown shift.

## Relative to TangentProp

TangentProp penalizes directional derivatives along known nuisance transformations in input space.

`RIWA` moves that idea to distribution space:

- penalize directional derivatives along unknown but local support perturbations.

That conceptual move is the real novelty.

# Failure Modes

## 1. The target shift may not be local

If the unseen target lies far outside the support hull of the source data, local sample reweighting robustness is not enough.

## 2. Validation data can be too small

The validation gradient `g_val,t` may be noisy in low-data regimes.

## 3. Example-level gradients can be expensive

This is why the random-direction minibatch estimator may be needed in practice.

## 4. Label shift can dominate

If the main test shift is class-prior shift rather than covariate/spurious-feature shift, a label-aware or prior-shift-specific correction may be more effective.

# Real Assessment

This is not a proven breakthrough.

But it clears the requirements better than the previous methods:

- no domain labels,
- post-hoc,
- simple,
- tied to old but deep ideas from invariance, robustness, and influence,
- and more directly aimed at distribution shift than pooled flatness.

If it works, this is the first label-free post-hoc idea here that I would describe as having a serious chance to matter at the level of `SWAD`.

# Sources

- [SWAD: Domain Generalization by Seeking Flat Minima](https://proceedings.neurips.cc/paper_files/paper/2021/hash/bcb41ccdc4363c6848a1d760f26c28a0-Abstract.html)
- [Diverse Weight Averaging for Out-of-Distribution Generalization](https://proceedings.neurips.cc/paper_files/paper/2022/hash/4c8d5f3ca0f17fae8ebc4b6fb8d0f2bc-Abstract-Conference.html)
- [Understanding Black-box Predictions via Influence Functions](https://proceedings.mlr.press/v70/koh17a.html)
- [Tangent Prop - A Formalism for Specifying Selected Invariances in an Adaptive Network](https://papers.nips.cc/paper/1991/hash/65658fde58ab3c2b6e5132a39fae7cb9-Abstract.html)
- [Variance-based Regularization with Convex Objectives](https://jmlr.org/beta/papers/v20/17-750.html)
- [Sample Complexity for Distributionally Robust Learning under chi-square divergence](https://www.jmlr.org/papers/v24/22-0881.html)
- [Model Agnostic Sample Reweighting for Out-of-Distribution Learning](https://proceedings.mlr.press/v162/zhou22d.html)
- [Stability and Generalization](https://www.jmlr.org/papers/v2/bousquet02a.html)
- [Post-Hoc Reversal: Are We Selecting Models Properly?](https://papers.neurips.cc/paper_files/paper/2024/file/a6805b5564bd8d813a81c4b5a97e5ca6-Paper-Conference.pdf)
