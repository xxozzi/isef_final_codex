---
title: SWING: Source-Reweighting-Induced Eigen-Shrinkage for Single-Run Post-hoc Domain Generalization
description: Research memo proposing a checkpoint-weight basin edit that contracts deployable models along directions that are unstable under plausible source-support reweightings, using a generalized fit-versus-fragility geometry.
created: 2026-03-31 14:48
last_modified: 2026-03-31 14:48
last_modified_by: agent
status: draft
related_files:
  - claude_workspace/research/reweighting_invariant_weight_averaging.md
  - claude_workspace/research/occam_prism_srm_pacbayes_proposal.md
  - claude_workspace/papers/tribe_neurips/main.tex
  - claude_workspace/papers/d_cola/d_cola_neurips.tex
  - domaingen/posthoc/prism.py
  - domaingen/posthoc/dcola.py
key_functions:
  - Record the narrowed post-critique research direction
  - Define a new full-weight post-hoc action family distinct from checkpoint selection and last-layer repair
  - State the theorem targets that look believable after harsh review
latest_change: Initial memo for the post-critique SWING proposal.
change_log:
  - 2026-03-31 14:48: Initial draft
---

# Bottom Line

The best new direction after the literature sweep and harsh review is:

> **Do not chase a fancier global soup objective.**
> Build a strong connected checkpoint basin as usual, choose a good deployable reference model, and then **shrink only the weight directions that swing under plausible source-support reweightings**.

That yields a new method:

- **`SWING`**: **S**ource-re**W**eighting-**I**nduced ei**N**-shrin**G**age

The simple slogan is:

> **Directions that swing under source reweightings should not survive deployment at full strength.**

This is intentionally narrower and cleaner than the earlier anisotropic-contraction sketch.

- It uses **one** fragility notion only: source-support reweighting sensitivity.
- It gives a **deterministic single-model output**.
- It stays **single-run**, **post-hoc**, and **domain-label-free**.
- It is still about **checkpoint weights**, not target-time adaptation, not last-layer-only repair, and not multi-run soups.

# Why This Version Survives Better

The harsh review on the earlier idea identified three serious problems:

1. it was too close to `TRIBE`,
2. it was too close to `MonoSoup`,
3. and its shrinkage coefficients were not tied to a coherent mathematical object.

`SWING` fixes those points as follows.

## 1. Not `TRIBE`

`TRIBE` performs a **local robust last-layer repair** after fixing an anchor.

`SWING` instead introduces a new **full-weight deployable action family**:

```text
theta(beta) = mu + U V diag(beta) V^T U^T (theta_ref - mu),
0 <= beta_j <= 1.
```

The decision variable is not a repaired classifier head.
It is a **full-model basin edit** inside a low-rank checkpoint-weight subspace.

## 2. Not `MonoSoup`

`MonoSoup` performs **layer-wise spectral reweighting of a single checkpoint update** to improve the ID/OOD tradeoff.

`SWING` instead:

- starts from a **single-run connected checkpoint basin**,
- uses **source data** to estimate a DG-specific fragility operator,
- and shrinks in a **generalized fit-versus-fragility basis**, not a raw layer SVD basis.

The central object is not “high-energy vs low-energy singular directions.”
It is “well-supported vs reweighting-sensitive directions.”

## 3. Not a Heuristic Buffet

The earlier sketch mixed together:

- bootstrap instability,
- checkpoint disagreement,
- support perturbations,
- and generic loss instability.

That is too loose.

`SWING` uses just one fragility object:

> **How much does the preferred local descent direction move when the source support is slightly reweighted?**

That is observable from source data and ties directly to DG-style hidden-subpopulation reasoning.

# Core Principle

`SWAD` says:

> flat minima generalize better.

`SWING` says:

> **stable weight directions generalize better than directions whose utility swings under plausible source-support reweightings.**

The conceptual move is:

- `SWAD` is isotropic around a flat region,
- `SWING` is anisotropic inside a connected basin.

So the new claim is not “pick a better basin.”
It is:

> once a good basin has been found, **do not trust all directions inside that basin equally**.

# The Method

## 1. Build a safe pool

As in the strongest local methods, start with a connected, low-loss, soup-safe pool `C` from one dense run.

This stage can reuse the best existing machinery:

- loss filtering,
- barrier screening,
- noncontiguous selection,
- exact-soup action families if desired.

`SWING` does **not** need to replace that layer.

## 2. Fix a deployable reference model

Choose a deterministic reference model `theta_ref`.

Good options are:

- the best exact soup from `PRISM`,
- the best weighted soup from `D-COLA`,
- or a strong checkpoint/soup selected on pooled source validation.

The key is that `theta_ref` is already a strong deployable model.

## 3. Define a basin center and subspace

Let:

- `mu` be a basin center, such as the uniform average of `C`,
- `U in R^{d x r}` be a low-rank basis of checkpoint deviations in `C`.

The simplest choice for `U` is PCA on `theta_t - mu`.

This basis is only a **working subspace**.
It is not yet the shrinkage basis.

## 4. Estimate two operators on disjoint source splits

Split the pooled source holdout into disjoint parts.

### Fit operator `A`

Estimate a positive semidefinite matrix `A` on a fit split:

```text
A ~= U^T H_fit U
```

where `H_fit` is a local source-risk curvature surrogate around `theta_ref` or `mu`.

Practical approximations:

- directional finite differences of loss in the `U` basis,
- Gauss-Newton / empirical Fisher in the `U` basis,
- or diagonal / low-rank approximations if full estimation is too noisy.

Interpretation:

- large `A` along a direction means the source data really supports that direction.

### Fragility operator `B`

Estimate a reweighting-sensitivity matrix `B` on a separate shift split.

For each example `z_i`, define its subspace gradient:

```text
g_i = U^T nabla_theta ell(z_i; theta_ref) in R^r.
```

Then define:

```text
gbar = (1/n) sum_i g_i
B = Cov_i(g_i) = (1/n) sum_i (g_i - gbar)(g_i - gbar)^T.
```

Interpretation:

- if a direction has large variance in per-example subspace gradients,
- then slight source-support reweightings can swing the preferred update strongly in that direction,
- so that direction is fragile under hidden-subpopulation perturbations.

This is the only fragility notion in the main method.

## 5. Form the generalized shrinkage basis

Solve the generalized eigenproblem:

```text
B v_j = lambda_j A v_j.
```

Equivalently, whiten by `A` and diagonalize `A^{-1/2} B A^{-1/2}`.

These `v_j` are the right shrinkage directions.

Why this matters:

- raw trajectory PCs do **not** justify separable shrinkage,
- generalized eigenvectors of fit-versus-fragility **do**.

## 6. Shrink the reference coefficients

Let:

```text
z_ref = U^T (theta_ref - mu).
```

Rotate to the generalized basis:

```text
c = V^T z_ref,
```

where `V = [v_1, ..., v_r]`.

Shrink with:

```text
c'_j = beta_j c_j,
beta_j = 1 / (1 + rho lambda_j)
```

or with a slightly more general held-out-selected monotone map `beta_j = phi(lambda_j)`.

Then output:

```text
theta_swing = mu + U V c'.
```

This is one deterministic model.

# First-Principles Motivation

The robust-DG intuition is:

1. unseen domains can be approximated locally by **reweightings of source support**,
2. the directions most sensitive to those reweightings are the ones least trustworthy at deployment,
3. so post-hoc DG should penalize those directions more heavily.

This leads naturally to the local objective:

```text
J(z) = 1/2 (z - z_ref)^T A (z - z_ref) + rho z^T B z
```

over the basin subspace.

The first term says:

- stay close to the source-supported reference in directions the source fit cares about.

The second term says:

- penalize coefficients that are highly unstable under plausible source-support reweightings.

The minimizer is:

```text
z* = (A + 2 rho B)^(-1) A z_ref.
```

In the generalized basis, that becomes simple coordinate-wise shrinkage.

# Theorem Targets That Look Believable

These are the theorem forms that survive the harsh review.

## Theorem target 1: Quadratic robust surrogate gives generalized shrinkage

Under a local quadratic approximation of pooled source risk on the chosen subspace and a centered chi-square or `l2` ball model of source reweighting perturbations, the robust surrogate is upper-bounded by:

```text
1/2 (z - z_ref)^T A (z - z_ref) + rho z^T B z + const
```

and its minimizer is:

```text
z* = (A + 2 rho B)^(-1) A z_ref.
```

This is the cleanest theorem in the whole proposal.

## Theorem target 2: Generalized-basis shrinkage form

If `A` is positive definite on the chosen subspace and `B` is positive semidefinite, then after whitening by `A`, the minimizer reduces to:

```text
c'_j = c_j / (1 + 2 rho lambda_j).
```

This is the honest closed form.

## Theorem target 3: Conditional target-risk certificate on the restricted action family

If an unknown target risk is upper-bounded by the corresponding population robust surrogate over the restricted family:

```text
{ mu + U z : z in R^r },
```

and the empirical operators `Ahat`, `Bhat` uniformly approximate their population counterparts within `eps`, then the selected `theta_swing` inherits a target-risk certificate relative to `theta_ref` up to `O(eps)`.

This is believable because it is conditional and family-restricted.

## Optional theorem target 4: Subspace recovery

Under a spiked covariance model for checkpoint deviations, standard spectral perturbation arguments can control recovery of the chosen low-rank basin subspace.

This is optional.
It should not be oversold.

# Theorem Claims To Avoid

These claims should **not** appear.

- “We identify the true hidden target shift directions from source data.”
- “The generalized eigenvectors correspond exactly to causal/invariant directions.”
- “The target robust excess risk decomposes exactly per trajectory PCA direction.”
- “Source reweighting sensitivity consistently recovers the real target nuisance axes.”

Those are much too strong.

# Why This Could Actually Win Empirically

The local empirical lesson from the repo is:

> good checkpoint pools matter more than fancy simplex optimization.

That is good news for `SWING`.

It means `SWING` does not need to replace the best pool builder.
It can sit **on top of** the best existing pool/reference pipeline and ask a different question:

> after we already have a good deployable model, are there a few fragile directions we should attenuate?

That makes the empirical burden much lighter.

The most promising recipe is:

1. use the best connected pool available,
2. pick the strongest reference model from that pool,
3. apply low-rank generalized shrinkage only in a tiny subspace,
4. keep the rest of the model untouched.

If the basin already encodes useful robustness but the final reference is slightly over-specialized, this is exactly the setting where `SWING` should help.

# Critical Baselines

If `SWING` is real, it must beat all of these:

- `mu` alone,
- `theta_ref` alone,
- scalar interpolation `mu + alpha (theta_ref - mu)`,
- plain PCA truncation,
- `SWAD`,
- the best exact-soup baseline,
- `TRIBE`,
- and a `MonoSoup`-style spectral editing baseline adapted as closely as possible.

If it cannot beat scalar interpolation and the best exact soup, it should be abandoned.

# Novelty Assessment

## Relative to `SWAD`

- `SWAD` is about isotropic flat-center seeking.
- `SWING` is about anisotropic shrinkage inside a good basin.

## Relative to `DiWA`

- `DiWA` emphasizes diversity/covariance/locality for weight averaging.
- `SWING` does not optimize soup weights directly.
- It edits a strong deployable reference using a DG-specific fragility operator.

## Relative to `RIWA`

- `RIWA` uses reweighting invariance to **select or score checkpoints**.
- `SWING` uses reweighting sensitivity to define a **generalized weight-space shrinkage operator** after the reference model is already chosen.

This overlap must be acknowledged.
The novelty is not “reweighting matters.”
The novelty is “reweighting sensitivity defines the geometry of the deployable basin edit.”

## Relative to `TRIBE`

- `TRIBE` repairs the last layer.
- `SWING` edits the full weight vector in a basin subspace.

That distinction only matters if the action family is explicit and empirically necessary.

## Relative to `MonoSoup`

- `MonoSoup` is single-checkpoint update spectroscopy for ID/OOD tradeoffs.
- `SWING` is source-supported generalized shrinkage inside a connected single-run basin.

This distinction should be stated directly in any paper.

# Recommendation

Among the ideas currently on the table, `SWING` is the best next bet because it is:

- simple enough to explain in one sentence,
- novel enough to survive an informed review if carefully positioned,
- and theoretically narrow enough to support honest theorems.

The key sentence for the paper should be:

> **Post-hoc DG should not trust all directions in a good basin equally; directions that swing under plausible source reweightings should be shrunk.**

That is the version worth testing next.
