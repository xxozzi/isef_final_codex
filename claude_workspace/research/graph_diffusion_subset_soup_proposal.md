---
title: Graph Diffusion Subset Soup
description: Comprehensive research proposal for a single-run post-hoc DG method that diffuses mass from a support-selected checkpoint anchor over a checkpoint graph, then sparsifies that mass into a deployable uniform soup.
created: 2026-04-03 19:45
last_modified: 2026-04-03 19:45
last_modified_by: codex
status: draft
related_files:
  - claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json
  - claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json
  - domaingen/posthoc/moonshot_2.py
key_functions:
  - Define a graph-diffusion checkpoint-selection method grounded in support-prediction geometry
  - State the empirical trigger, theoretical motivation, and sparse deployment strategy
  - Record the main risks, redundancy observations, and implementation plan
latest_change: Initial comprehensive proposal based on the winning moonshot graph-diffusion probes.
---

# Graph Diffusion Subset Soup

## 1. Executive Summary

This memo proposes a second main candidate:

> **Graph Diffusion Subset Soup (GDSS)**: choose a checkpoint anchor from held-out source behavior, diffuse probability mass from that anchor over a checkpoint-similarity graph, convert the diffusion mass into a sparse subset, and deploy a uniform soup over that subset.

The empirical trigger is the strongest new balanced `moonshot_2` family:

- `diffuse_cos_bestmean_a06_s01_logit = 0.87451171875` full / `0.8899755501222494` out

with the same metrics for the corresponding correlation versions and for diffusion steps `1, 2, 4, 8, 16, 32`.

Compared with the strong uniform-all baseline

- `0.8642578125` full / `0.882640586797066` out

this is:

- `+0.01025390625` full
- `+0.0073349633251834` out

Compared with the balanced shotgun baseline `even_018_prob = 0.87158203125 / 0.8924205378973105`, GDSS is:

- `+0.0029296875` full
- `-0.0024449877750612` out

So graph diffusion gives a new tradeoff point that is not the best on either single axis, but is clearly alive.

## 2. Why This Proposal Exists

The winning diffusion probes say something more specific than “weighting may work.”

They say:

- a **good anchor** matters;
- **prediction-space neighborhood structure** matters;
- smoothing away from the anchor helps;
- but deploying the raw 300-way soft weights is probably the wrong object.

That last point is crucial. The successful probe used a full-bank diffusion vector, but the project history is full of failures where a promising soft weighting object died when turned into a deployed method. So this proposal deliberately **does not** make the diffusion weights the deployed model. It uses diffusion only as a ranking-and-neighborhood operator.

## 3. Position Relative to Existing Literature

This proposal sits near:

- graph diffusion and Personalized PageRank style smoothing on graphs;
- model soups and uniform checkpoint averaging;
- anchor-based post-hoc selection;
- graph-regularized semi-supervised learning ideas.

But it is not just generic graph smoothing. The concrete object is unusual:

- nodes are **checkpoints from one run**;
- edges come from **held-out source prediction similarity**;
- the source of mass is a **support-selected anchor checkpoint**;
- and the final deployed model is a **uniform weight-space soup over a sparse subset** induced by diffusion mass.

This is a reasonable narrow novelty claim, not a guaranteed one.

## 4. Core Hypothesis

The central hypothesis is:

> The most transferable checkpoints are not isolated single points. They form a local community around a good anchor in checkpoint prediction geometry. Diffusing from the anchor over that graph is a way to find that community more robustly than either taking the anchor alone or averaging the whole bank.

This fits the best `moonshot_2` result:

- anchor = `bestmean`
- diffusion strength \(\alpha = 0.6\)
- logit-space deployment in the probe

The fact that diffusion steps `1, 2, 4, 8, 16, 32` all tied is also informative. It suggests the step count is not the real control knob. The real signal seems to be:

- anchor identity,
- graph structure,
- and diffusion strength.

That means the next method should simplify aggressively and avoid pretending the step-count grid is meaningful.

## 5. Formal Construction

### 5.1 Setup

Let checkpoints be
\[
\theta_1,\dots,\theta_T.
\]

Let support predictions define checkpoint vectors
\[
z_t \in \mathbb R^{nC}.
\]

Build a nonnegative checkpoint similarity matrix
\[
S \in \mathbb R^{T\times T}.
\]

Normalize rows to obtain a transition matrix
\[
P = \operatorname{row\_normalize}(S).
\]

### 5.2 Anchor selection

Choose an anchor checkpoint \(a\) by a held-out source criterion. The winning probe used:

\[
a = \arg\min_t \ell_t^{\mathrm{support\ mean}},
\]

which in the code is `bestmean`.

### 5.3 Diffusion

Let \(e_a\) be the one-hot vector at anchor \(a\). Define the diffused weight vector recursively:

\[
w^{(0)} = e_a,
\qquad
w^{(m+1)} = (1-\alpha)e_a + \alpha P^\top w^{(m)}.
\]

The successful probe used \(\alpha = 0.6\).

In practice, the `moonshot_2` probe family implemented:

\[
w = (1-\alpha)e_a + \alpha P^\top e_a
\]
for one step, then renormalized after each step; see [_diffuse_anchor_weights](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot_2.py#L216).

### 5.4 Sparse deployment

The probe deployed the whole weight vector over all 300 checkpoints. This memo rejects that as the final method.

Instead define a sparse subset by either:

1. top-\(k\) truncation:
\[
\mathcal S_k = \operatorname{TopK}(w,k),
\]

or

2. cumulative-mass truncation:
\[
\mathcal S_q = \min\left\{\mathcal S: \sum_{t\in\mathcal S} w_t \ge q\right\}.
\]

Then deploy the uniform soup
\[
\bar\theta_{\mathcal S}
=
\frac{1}{|\mathcal S|}\sum_{t\in\mathcal S}\theta_t.
\]

This is the core change that makes the proposal compatible with the project’s negative results on continuous full-bank weighting.

## 6. Why This Could Work

### 6.1 Better anchor neighborhoods than local windows

Contiguous windows assume time-local neighborhoods. Graph diffusion assumes **behavioral neighborhoods**, which is much more flexible.

### 6.2 Stabilized anchor selection

A single chosen anchor is brittle. Diffusion can gather nearby checkpoints that behave similarly without requiring the bank to be contiguous in time.

### 6.3 Built-in denoising

Small, noisy similarity perturbations around the anchor are smoothed by diffusion. That may be why this family stayed strong despite using the full checkpoint bank in the probe.

### 6.4 Natural bridge to sparse deployment

Diffusion gives a principled ranking of checkpoints by “graph proximity to a good anchor.” That ranking is exactly what we need to turn a soft probe into a sparse soup.

## 7. Theory Program

Again, this is not a theorem yet. But the theory path is believable.

### 7.1 Assumptions

1. **Graph locality.**
   Similar checkpoints in support-prediction space have similar target transfer behavior.

2. **Anchor adequacy.**
   The chosen anchor lies in or near a target-relevant community.

3. **Community smoothness.**
   The target-relevant community has larger within-community similarity than cross-community similarity.

### 7.2 First theorem target

A plausible first target is a community-recovery statement:

> If the checkpoint graph contains a target-relevant low-conductance community around the anchor, then one-step or few-step diffusion from that anchor concentrates mass in that community.

That would make top-\(k\) truncation meaningful rather than heuristic.

### 7.3 Second theorem target

If the selected high-mass checkpoints are merge-compatible, then the final soup can be bounded by:

\[
R^\star(\bar\theta_{\mathcal S})
\le
\min_{t \in \mathcal C(a)} R^\star(t)

+ \varepsilon_{\mathrm{selection}}
+ \varepsilon_{\mathrm{merge}},
\]

where \(\mathcal C(a)\) is the target-relevant anchor community.

This is still a challenging theorem program because the mergeability term is the bottleneck.

## 8. Concrete Algorithm

1. Run checkpoints on the support set.
2. Build checkpoint similarity matrix \(S\) from support predictions.
3. Pick anchor \(a\) by `bestmean` or a small shortlist of held-out source criteria.
4. Compute one-step diffusion weights \(w\).
5. Convert \(w\) into a sparse subset by top-\(k\) or cumulative-mass thresholding.
6. Uniformly average those checkpoints in weight space.

Recommended first grid:

- similarity: `cos`, `corr`
- anchor: `bestmean`, `besttail`, `bestval`
- diffusion strength \(\alpha \in \{0.4, 0.6, 0.8\}\)
- subset size \(k \in \{12, 18, 24, 32\}\)

Do **not** spend time on large diffusion-step grids initially. The probe ties strongly suggest that step count is not the main axis.

## 9. Evaluation Plan

Mandatory checks:

- actual weight-space soup vs probe-time diffusion result
- top-\(k\) vs cumulative-mass truncation
- anchor sensitivity
- similarity-metric sensitivity

Required baselines:

- uniform-all
- even-spacing subset
- quality subset
- spectral subset

This proposal should be evaluated head-to-head with Spectral Subset Soup. They are the two strongest new families.

## 10. Main Risks

### 10.1 Diffusion may just recreate uniform averaging

If the graph is too dense or too homogeneous, diffusion will blur toward the whole bank.

### 10.2 Anchor failure

If the anchor is wrong, diffusion spreads mass from the wrong place.

### 10.3 Soft-weight artifact

The probe may have looked good because soft weighting over 300 checkpoints is a different object than any sparse deployable soup.

### 10.4 Redundant step count

The step-count tie pattern may indicate the family has less real dimensionality than it appears to.

## 11. Kill Criteria

Drop the method if:

- sparse truncation destroys the probe-time advantage;
- the selected subset mostly collapses to contiguous late windows;
- the best variant does not beat uniform-all on both full and out;
- Spectral Subset Soup strictly dominates it in replayed weight-space deployment.

## 12. Recommendation

This should be the **second implementation track**.

It is weaker than Spectral Subset Soup as a pure post-hoc method, but it is conceptually rich and the empirical signal is real. Most importantly, it suggests a new primitive:

> not “average all neighbors,” but “grow a sparse community around a good anchor in checkpoint-geometry space.”
