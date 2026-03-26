---
title: Minimum adaptation information weight averaging for single-run domain generalization
description: Research memo proposing a stronger post-hoc DG principle: select checkpoints and windows that act as universal priors by minimizing the information needed to specialize to each source domain.
created: 2026-03-16 01:11
last_modified: 2026-03-16 01:30
last_modified_by: agent
status: secondary
related_files: claude_workspace/workspace_index.md, claude_workspace/research/recoverability_oriented_weight_averaging.md, claude_workspace/research/consensus_overlap_weight_averaging.md, literature/swad_tex_source/main.tex, literature/diwa_tex_source/main.tex, literature/tawa.tex
key_functions: N/A
latest_change: Relegated this memo to a secondary option after finding a simpler transfer-based candidate that is closer to SWAD-level operational simplicity.
change_log:
  - 2026-03-16 01:30: Relegated this memo to a secondary option after finding a simpler transfer-based candidate that is closer to SWAD-level operational simplicity.
  - 2026-03-16 01:11: Added a stronger post-hoc DG memo that reframes checkpoint selection as minimum adaptation information from a shared posterior.
---

# Bottom Line

This memo remains a serious theoretical option, but it is no longer the main recommendation for a SWAD-level method. The current main candidate is [recoverability_oriented_weight_averaging.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/recoverability_oriented_weight_averaging.md), which is simpler and more operationally comparable to SWAD.

No: I do not think `COWA` is likely to change the entire field of domain generalization.

After checking newer literature, the more credible breakthrough-level direction is this:

> **A domain-general checkpoint should be a universal prior: a shared posterior from which each source domain can be reached with very little information.**

That principle is stronger than flatness and stronger than consensus volume alone. It produces a new single-run post-hoc method:

- **`MAIWA` = Minimum Adaptation Information Weight Averaging**

The core score is not "flat pooled basin" and not "generic quality metric." It is:

```text
average source risk
+ shared-posterior complexity
+ average KL needed to specialize that shared posterior to each source domain
+ optional robust penalty for cross-domain posterior dispersion
```

This is the first idea in this session that I would describe as having a plausible path to a real DG shift, because it changes the object of interest:

- from flat minima to universal priors,
- from deterministic checkpoints to local posteriors,
- from pooled geometry to information needed for domain specialization.

I still cannot honestly call it a verified field breakthrough. I can call it the strongest current research direction I found that remains single-run, post-hoc, DG-specific, and theoretically motivated.

# Why The Earlier COWA Memo Is Not Enough

## 1. Newer DG literature is already moving beyond naive pooled flatness

The CVPR 2025 paper [Towards Shared Flat Minima: A Perspective on Model Weight Averaging for Improving Domain Generalization](https://openaccess.thecvf.com/content/CVPR2025/html/Li_Towards_Shared_Flat_Minima_A_Perspective_on_Model_Weight_Averaging_CVPR_2025_paper.html) explicitly targets cross-domain flatness during training. Its abstract states:

> "we formulate a sufficient condition for Domain Generalization (DG) under weight averaging, namely, the existence of a consistent flat minimum shared across all source domains."

That matters for us because `COWA` is still, at heart, a geometry-consensus story. It is cleaner than SWAD, but the field is already moving in that direction.

## 2. Posterior aggregation has already entered DG, but not in the single-run checkpoint-selection form

The PTG paper [Bayesian Domain Invariant Learning via Posterior Generalization of Parameter Distributions](https://arxiv.org/abs/2502.11112) says in its abstract:

> "we propose a principled domain posterior aggregation approach inspired by Bayesian model averaging theory."

It also says:

> "we use the latent variable variational Bayesian inference framework to learn source domain-specific model parameters, while preserving domain shared model parameters."

So the field is already touching posterior aggregation. The gap is narrower than it looked. The remaining niche is more specific:

- no extra multi-run training,
- no per-domain fine-tuning loop,
- one ordinary training trajectory,
- post-hoc selection of a checkpoint or window that best behaves like a universal prior.

## 3. Therefore the actual open gap is not "better flatness"

The open gap is:

> **How do we turn one training trajectory into a source-domain universal prior whose expected information-to-specialize is minimal for a new domain?**

That is the gap `MAIWA` targets.

# The New Principle

## Universal-Prior Hypothesis For DG

Let source domains `e_1, ..., e_I` be draws from an environment distribution `rho`.

For a candidate checkpoint or window `t`, define a shared local posterior:

```text
Q_t(theta) approx N(mu_t, Sigma_t).
```

Interpret `Q_t` as a candidate universal prior or hyper-posterior for unseen domains.

For each source domain `e_i`, define the domain-specialized local posterior:

```text
Q_{i,t}(theta) approx p(theta | D_i, Q_t).
```

The central claim is:

> **A checkpoint generalizes to unseen domains when `Q_t` already contains most of what each source domain needs, so the KL needed to move from `Q_t` to `Q_{i,t}` is small on average.**

Formally, define the average adaptation information:

```text
A_t = (1 / I) sum_{i=1}^I KL(Q_{i,t} || Q_t).
```

Then the DG goal is not merely to find a flat `theta_t`. It is to find a `Q_t` with:

- low source risk,
- low `A_t`,
- moderate shared complexity,
- low cross-domain posterior dispersion.

## Why This Is More Fundamental Than Flatness

Flatness only says that many nearby parameters have low pooled loss.

But DG is harder:

- each domain can want a different local move,
- each domain can have a different local curvature,
- a checkpoint can be flat on the pooled objective while still requiring large domain-specific updates.

`MAIWA` says the right object is not "how broad is the pooled basin?" but:

> **how much information must each domain add before the model really fits that domain?**

That is a transfer principle, not a pure optimization principle.

# Theory Sketch

## Hierarchical-Bayes View

Treat DG as multi-task generalization:

- a new domain is a new task sampled from `rho`,
- the learner carries forward only a shared prior or hyper-posterior,
- good DG means low expected risk on a new task drawn from the same meta-distribution.

In a hierarchical PAC-Bayes style argument, the expected risk on a new domain is controlled by:

```text
empirical source-domain risk
+ complexity of the shared posterior
+ average divergence from the shared posterior to the task-specialized posteriors.
```

This is the key conceptual jump:

- SWAD mostly optimizes the first term and a flatness proxy for the second,
- `MAIWA` explicitly targets the third term, which is the transfer-specific one.

## Local Gaussian Form

Use a local Gaussian shared posterior:

```text
Q_t = N(mu_t, Sigma_t).
```

For each source domain, use a local Laplace or linearized update:

```text
Sigma_{i,t}^{-1} = Sigma_t^{-1} + eta F_{i,t}
mu_{i,t} = mu_t - eta Sigma_{i,t} g_{i,t}
```

where:

- `g_{i,t}` is the source-domain gradient at checkpoint or window `t`,
- `F_{i,t}` is the source-domain empirical Fisher or Gauss-Newton matrix.

Then:

```text
Q_{i,t} = N(mu_{i,t}, Sigma_{i,t}).
```

The Gaussian KL has closed form:

```text
KL(Q_{i,t} || Q_t)
= (1/2) [
  (mu_{i,t} - mu_t)^T Sigma_t^{-1} (mu_{i,t} - mu_t)
  + tr(Sigma_t^{-1} Sigma_{i,t})
  - log det(Sigma_t^{-1} Sigma_{i,t})
  - p
].
```

This decomposition is exactly why the idea is stronger than the earlier one:

- the mean-shift term measures how much the domain wants to move,
- the trace and log-det terms measure curvature and entropy mismatch,
- averaging this over domains gives a principled transfer score.

## Why COWA Falls Out As A Surrogate

If:

- `Sigma_t` is approximated by a diagonal or isotropic matrix,
- the domain updates are small,
- the local Gaussian approximation is linearized,

then the average KL reduces to terms of the same kind that appeared in `COWA`:

- gradient-disagreement penalties,
- Fisher-volume penalties,
- curvature mismatch penalties.

So `COWA` is not wasted. It becomes the cheap second-order approximation to `MAIWA`.

## Flatness As The Special Case

If all source domains share:

- the same local minimizer,
- the same local Fisher,
- negligible domain-specific mean shift,

then `Q_{i,t} = Q_t` for all `i`, so:

```text
A_t = 0.
```

In that degenerate aligned-domain case, the problem reduces to selecting a broad shared posterior, which is exactly when flatness-based ideas suffice.

So the relationship is:

- SWAD handles the aligned-domain limit,
- `COWA` handles geometry-consensus at second order,
- `MAIWA` handles the full local shared-prior problem.

# The Proposed Method: MAIWA

## Name

**`MAIWA` = Minimum Adaptation Information Weight Averaging**

## Inputs

- one standard training trajectory with dense checkpoints,
- source-domain train and held-out splits,
- no extra end-to-end retraining,
- optional SWA or SWAG-style trajectory windowing.

## Step 1: Build a shared posterior at each candidate checkpoint or window

For a checkpoint or local window around `t`, fit:

```text
Q_t = N(mu_t, Sigma_t).
```

Practical options:

- Laplace around one checkpoint,
- SWAG-style low-rank plus diagonal covariance on a short window,
- empirical Fisher inverse plus damping.

## Step 2: Build domain-specialized posteriors post hoc

For each source domain `i`, compute on a held-out split:

- `g_{i,t}`,
- `F_{i,t}`.

Then construct:

```text
Sigma_{i,t}^{-1} = Sigma_t^{-1} + eta F_{i,t}
mu_{i,t} = mu_t - eta Sigma_{i,t} g_{i,t}.
```

This needs no second training run. It is a local Bayesian update in the neighborhood already explored by the original training trajectory.

## Step 3: Score checkpoints by adaptation information

Use:

```text
B_t =
R_src(mu_t)
+ alpha KL(Q_t || P_0)
+ beta (1 / I) sum_i KL(Q_{i,t} || Q_t)
+ gamma Disp({Q_{i,t}}).
```

Where:

- `R_src(mu_t)` is average source validation risk,
- `P_0` is a simple reference prior,
- `Disp({Q_{i,t}})` is an optional robust dispersion penalty across the domain-specialized posteriors.

A practical robust choice is the trimmed mean pairwise Fisher-Rao distance among the `Q_{i,t}`.

## Step 4: Select a contiguous low-bound window

Let `t_star = arg min_t B_t`.

Define:

```text
W = { t : B_t <= B_{t_star} + delta }.
```

Then keep only checkpoints whose posterior barycenters stay in the same connected basin under a low-barrier source-loss check.

## Step 5: Average in posterior space, not only Euclidean weight space

Instead of plain arithmetic averaging of weights, compute either:

- the mean shared posterior over `W`,
- or the Fisher-weighted barycenter of the `Q_t`.

The final predictor is:

- the posterior mean of that barycenter,
- or the posterior predictive if compute permits.

# Why This Could Actually Beat SWAD

## On IID

If the selected posterior is broad but also low-information-to-specialize, it should remain in a low-risk region for the source domains. So IID should not collapse.

## On OOD

OOD improves if unseen domains resemble new draws from the same environment distribution, because a low-information shared posterior is exactly the object that transfers.

## Why The Gain Could Be Real

SWAD can still choose a checkpoint that is:

- flat in the pooled loss,
- but one source domain away from needing a large local move.

`MAIWA` rejects that checkpoint because its average adaptation KL is high.

This is the part that could matter in datasets like PACS, OfficeHome, TerraIncognita, and DomainNet where domains often agree only after nontrivial local corrections.

# Novelty Relative To Existing Work

## Relative to SWAD

SWAD:

- is deterministic,
- selects by validation and pooled flatness,
- does not represent source domains as local posteriors.

`MAIWA`:

- uses a shared posterior,
- measures how much each domain still needs to change that posterior,
- and stays post-hoc and single-run.

## Relative to the 2025 shared-flat-minima work

The CVPR 2025 shared-flat-minima paper is training-time and still centered on flat minima.

`MAIWA` is:

- post-hoc,
- single-run,
- posterior-based,
- and transfer-information based rather than flatness based.

## Relative to PTG

PTG uses posterior aggregation for DG, but it still learns domain-specific and shared parameter distributions through a dedicated Bayesian fine-tuning procedure.

`MAIWA` instead asks:

- given one ordinary training trajectory,
- which checkpoint or short window already acts like the best shared prior?

That is a different problem.

## Relative to model soups, SWAG, and model merging

Those works say how to average or merge models better.

`MAIWA` adds the DG-specific selection principle:

> choose the model or window whose posterior requires the least information to specialize across environments.

# Falsifiable Predictions

1. Average adaptation KL should correlate with OOD accuracy more strongly than Hessian trace, SWAD's loss-based window rule, or plain source validation accuracy.
2. The best `MAIWA` checkpoint should not always be the flattest checkpoint.
3. `COWA` should recover part of the gain, but the full Gaussian-KL score should perform better whenever source-domain mean shifts matter.
4. Posterior-space averaging should outperform Euclidean weight averaging when domain Fishers differ substantially.
5. Leave-one-domain-out source evidence computed from the shared posterior should predict which checkpoints transfer best to truly unseen domains.

# Failure Modes

## 1. Exchangeability can fail

If the unseen domain is not plausibly drawn from the same environment family as the sources, no shared-prior story can rescue performance.

## 2. Local Gaussian approximations can be too crude

If the trajectory window crosses disconnected basins or strongly nonquadratic regions, the local posterior approximation can be misleading.

## 3. Fisher estimates can be too noisy

This is especially serious on small held-out source-domain splits. Diagonal or low-rank stabilization will matter.

## 4. Some DG benchmarks are driven more by representation defects than by posterior transport

If the backbone never learned transferable features, better post-hoc posterior selection may not fix the problem.

# Minimal Experimental Program

1. Implement domain-wise gradients and diagonal Fishers on held-out source splits for every saved checkpoint.
2. Fit a SWAG-style local shared posterior on short windows.
3. Compare:
   - ERM last,
   - SWA,
   - SWAD,
   - `COWA`,
   - `MAIWA` with Euclidean final averaging,
   - `MAIWA` with posterior barycenter averaging.
4. Evaluate on PACS, OfficeHome, TerraIncognita, and DomainNet using the standard DomainBed protocol.
5. Report:
   - IID,
   - OOD,
   - average adaptation KL,
   - leave-one-domain-out evidence,
   - posterior dispersion,
   - compute overhead.

# The Real Assessment

If you ask me whether this is already a field breakthrough, the honest answer is still no.

If you ask whether this is the first idea in the session that has a credible path to being a field-level contribution, my answer is yes.

The reason is not cosmetic novelty. It is that the theory changes the target:

- not flatness,
- not just cross-domain curvature agreement,
- but the minimum information needed to specialize from a shared posterior to each environment.

That is a different governing principle.

# Sources

Primary sources used here:

- Local SWAD TeX sources:
  - [`literature/swad_tex_source/2.theoretical_analysis.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex)
  - [`literature/swad_tex_source/3.method.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/3.method.tex)
  - [`literature/swad_tex_source/4.empirical_results.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/4.empirical_results.tex)
- Local DiWA TeX sources:
  - [`literature/diwa_tex_source/sections/02_theory.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/02_theory.tex)
  - [`literature/diwa_tex_source/sections/03_approach.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/03_approach.tex)
  - [`literature/diwa_tex_source/sections/04_analysis.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/04_analysis.tex)
- [Towards Shared Flat Minima: A Perspective on Model Weight Averaging for Improving Domain Generalization](https://openaccess.thecvf.com/content/CVPR2025/html/Li_Towards_Shared_Flat_Minima_A_Perspective_on_Model_Weight_Averaging_CVPR_2025_paper.html)
- [Bayesian Domain Invariant Learning via Posterior Generalization of Parameter Distributions](https://arxiv.org/abs/2502.11112)
- [Fishr: Invariant Gradient Variances for Out-of-distribution Generalization](https://proceedings.mlr.press/v162/rame22a.html)
- [Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time](https://proceedings.mlr.press/v162/wortsman22a.html)
- [A Simple Baseline for Bayesian Uncertainty in Deep Learning](https://papers.neurips.cc/paper_files/paper/2019/hash/118921efba23fc329e6560b27861f0c2-Abstract.html)
- [Not All Weights Are Worth Averaging](https://arxiv.org/abs/2410.22311)
