---
title: Spectral Subset Soup
description: Comprehensive research proposal for a single-run post-hoc DG method that selects a sparse noncontiguous checkpoint subset by spectral embedding of checkpoint prediction geometry and deploys a uniform soup over that subset.
created: 2026-04-03 19:45
last_modified: 2026-04-03 19:45
last_modified_by: codex
status: draft
related_files:
  - claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json
  - claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json
  - domaingen/posthoc/moonshot_2.py
key_functions:
  - Define a spectral-subset checkpoint-selection method grounded in prediction geometry
  - State the core empirical motivation, mathematical construction, theorem targets, and evaluation plan
  - Record novelty risk, failure modes, and kill criteria before implementation
latest_change: Initial comprehensive proposal based on the winning moonshot spectral-subset probes.
---

# Spectral Subset Soup

## 1. Executive Summary

This memo proposes a new main candidate for single-run post-hoc domain generalization:

> **Spectral Subset Soup (S3)**: build a checkpoint-similarity graph from held-out source predictions, compute a low-dimensional spectral embedding of the checkpoint bank, select a sparse noncontiguous subset that covers that embedding, and deploy a uniform weight-space soup over that subset.

The proposal is motivated by the strongest new `moonshot_2` signal that did **not** collapse back into late-window averaging or naive checkpoint weighting:

- `spectral_subset_cos_k024_r04 = 0.87109375` full / `0.8948655256723717` out
- `spectral_subset_corr_k024_r04 = 0.87109375` full / `0.8948655256723717` out

from [moonshot_2_summary.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json).

Against the strong uniform-all baseline

- `uniform_all_prob = 0.8642578125` full / `0.882640586797066` out

from [shotgun_summary.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json),

the best spectral subset gains are:

- `+0.0068359375` on art full
- `+0.0122249388753057` on out

The more difficult comparison is the best balanced shotgun baseline:

- `even_018_prob = 0.87158203125` full / `0.8924205378973105` out

Here the spectral subset slightly loses on full but wins on out:

- `-0.00048828125` full
- `+0.0024449877750612` out

So Spectral Subset Soup is **not yet the best overall point**, but it is the cleanest new family that:

- beats uniform on both full and out,
- is sparse and deployable,
- preserves the “uniform soup over actual checkpoints” principle,
- and is meaningfully different from safe-window / contiguous averaging.

## 2. Why This Proposal Exists

The current project record now supports three strong conclusions.

First, simple central averaging is very strong.

Second, continuous reweighting of a full checkpoint bank has repeatedly failed to justify itself as a deployed object.

Third, the most persistent positive signal in the large replay-only probe banks is **noncontiguous complementary subsets**, not carefully tuned continuous weights.

That was already visible in `shotgun`, where:

- `diverse_supporttail_k007_l10 = 0.8798828125` full / `0.8679706601466992` out
- `topval_supporttail_024_prob = 0.87646484375` full / `0.8875305623471883` out
- `even_018_prob = 0.87158203125` full / `0.8924205378973105` out

from [shotgun_summary.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json).

`moonshot_2` then sharpened that story: the strongest genuinely new out-of-distribution probe family was not augmentation-heavy inference, not notch filtering, and not covariance-center weighting. It was **spectral subset selection on checkpoint prediction geometry**.

That is exactly the family this memo turns into a real method.

## 3. Position Relative to Existing Literature

This proposal is adjacent to several established families:

- SWA and SWAD average many checkpoints in or near a wide basin.
- Model soups average multiple models without extra inference cost.
- DiWA exploits diversity across independently trained models.
- Spectral clustering and graph embedding methods use eigenvectors of normalized similarity operators to reveal low-dimensional structure.

But Spectral Subset Soup does something narrower and different:

1. It operates on **one run**.
2. It uses **held-out source prediction geometry** rather than parameter-space distance.
3. It chooses a **sparse noncontiguous subset** by spectral coverage rather than contiguous locality or greedy validation filtering.
4. It still deploys a **uniform soup over actual checkpoints**.

So the novelty claim is modest:

> I do not know of a standard post-hoc DG method that selects a sparse checkpoint soup by running spectral embedding on checkpoint-to-checkpoint prediction similarity and then covering that embedding with a farthest-first subset.

This is a plausible novelty claim, not a certainty. The proposal carries moderate novelty risk because it sits near classical spectral clustering, model soups, and subset-selection ideas.

## 4. Core Hypothesis

The central hypothesis is:

> When checkpoints are represented by their held-out source prediction behavior, the bank is not just a one-dimensional time chain; it has a low-dimensional geometry with redundant local neighborhoods and a smaller set of geometrically distinct phases. A sparse soup that covers those phases can outperform dense uniform averaging because it preserves complementarity without dragging in every redundant checkpoint.

This hypothesis fits the current local evidence:

- exact optimized weights matter little;
- nonredundancy matters a lot;
- noncontiguity matters a lot;
- broad trajectory coverage can help more than local late-window averaging.

## 5. Formal Construction

### 5.1 Setup

Let the training run produce checkpoints
\[
\theta_1,\theta_2,\ldots,\theta_T.
\]

Let the held-out pooled source support set be
\[
\mathcal U = \{x_i,y_i\}_{i=1}^n.
\]

For each checkpoint \(t\), define its support prediction vector
\[
z_t \in \mathbb R^{nC}
\]
by concatenating either:

- softmax probabilities \(p_t(y\mid x_i)\), or
- logits \(f_{\theta_t}(x_i)\),

over all support examples and classes.

In the successful `moonshot_2` probe, the live family used support probabilities and cosine/correlation similarity over the flattened support-prediction matrix; see [_spectral_embedding_subset](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot_2.py#L349).

### 5.2 Checkpoint graph

Construct a similarity matrix
\[
S \in \mathbb R^{T\times T}, \qquad S_{st} \ge 0,
\]
with one of:

\[
S_{st}^{\mathrm{cos}} = \frac{1}{2}\left(1 + \frac{\langle z_s, z_t\rangle}{\|z_s\|_2 \|z_t\|_2}\right),
\]

or

\[
S_{st}^{\mathrm{corr}} = \frac{1}{2}\left(1 + \frac{\langle z_s-\bar z_s,\, z_t-\bar z_t\rangle}{\|z_s-\bar z_s\|_2 \|z_t-\bar z_t\|_2}\right).
\]

Define the degree vector
\[
d_t = \sum_{s=1}^T S_{ts},
\]
and the normalized similarity operator
\[
M = D^{-1/2} S D^{-1/2},
\qquad
D = \operatorname{diag}(d_1,\dots,d_T).
\]

### 5.3 Spectral embedding

Let \(u_1,\dots,u_r\) be the top \(r\) eigenvectors of \(M\), collected as rows of
\[
U_r \in \mathbb R^{T\times r}.
\]

Checkpoint \(t\) is now represented by row \(U_r[t,:]\), which is a low-dimensional coordinate encoding the checkpoint’s position in prediction-geometry space.

### 5.4 Sparse coverage subset

Choose subset size \(k\). Define
\[
\mathcal S = \{t_1,\dots,t_k\} \subseteq \{1,\dots,T\}
\]
by farthest-first traversal in the embedded space:

1. choose an initial seed near the embedding center,
2. repeatedly add the checkpoint that maximizes its distance to the current selected set.

Equivalently, at each step choose
\[
t^\star
=
\arg\max_{t \notin \mathcal S}
\min_{s \in \mathcal S}
\|U_r[t,:] - U_r[s,:]\|_2^2.
\]

This is exactly the geometry used by the successful `moonshot_2` family.

### 5.5 Final deployed model

The final model is the uniform soup over the selected subset:
\[
\bar\theta_{\mathcal S}
=
\frac{1}{k}\sum_{t\in\mathcal S}\theta_t.
\]

That deployable object is the critical design choice. The method uses spectral geometry only for **selection**, not for final weighted deployment.

## 6. Why This Could Work

### 6.1 Redundancy removal

Dense averaging mixes many checkpoints that are almost prediction-equivalent. If the useful gain comes from a few distinct phases of the trajectory, then averaging every redundant neighbor may dilute those phases.

### 6.2 Implicit trajectory coverage

Even spacing in time already worked surprisingly well. Spectral coverage is a stronger version of that idea:

- not equal coverage in time,
- but equal coverage in **prediction geometry**.

### 6.3 Better complementarity than raw quality ranking

Quality-only subset selection tends to choose many checkpoints from the same local region. Spectral coverage pushes the method away from repeated near-duplicates.

### 6.4 More robust than soft full-bank weighting

The method avoids the failure mode of continuous reweighting because it does not deploy a fragile full-bank weight vector. It deploys a sparse uniform soup over real checkpoints.

## 7. Theory Program

This proposal is not yet backed by a theorem. But it has a believable theory program.

### 7.1 Assumptions

The theorem program would work under assumptions like:

1. **Low-dimensional checkpoint geometry.**
   The support prediction vectors \(z_t\) lie near a union of a small number of coherent phases or arcs.

2. **Transfer regularity.**
   Target risk changes smoothly over this geometry: if two checkpoints are close in the support-prediction geometry, their target behavior is not radically different.

3. **Complementary phase structure.**
   Useful checkpoints are not all confined to one tiny neighborhood.

### 7.2 Main theorem target

A realistic first target is a coverage-type theorem:

> If target risk is Lipschitz over the checkpoint-geometry embedding and the selected subset is a \(\rho\)-cover of the checkpoint bank in that embedding, then the best checkpoint available to the target is approximated within \(L\rho\) by some member of the selected subset.

Formally, if
\[
|R^\star(t)-R^\star(s)|
\le
L\|U_r[t,:]-U_r[s,:]\|_2
\]
for the relevant target-side risk functional \(R^\star\), and if every checkpoint \(t\) has some selected \(s\in\mathcal S\) with
\[
\|U_r[t,:]-U_r[s,:]\|_2 \le \rho,
\]
then
\[
\min_{s\in\mathcal S} R^\star(s)
\le
\min_{t} R^\star(t) + L\rho.
\]

This would not yet be a soup theorem. It would be a **subset coverage theorem**, which is the right first layer.

### 7.3 Second theorem target

The second target is a soup compatibility theorem:

> If the selected checkpoints lie in a shared mergeable region and the soup map is stable inside that region, then the uniform soup over the subset inherits the subset’s approximation quality up to an additional mergeability error term.

This would yield a bound of the schematic form
\[
R^\star(\bar\theta_{\mathcal S})
\le
\min_t R^\star(t) + L\rho + \varepsilon_{\mathrm{merge}}.
\]

The difficult term is \(\varepsilon_{\mathrm{merge}}\). This is where the proposal remains genuinely risky.

## 8. Concrete Algorithm

Given checkpoints \(\theta_1,\dots,\theta_T\):

1. Run all checkpoints on the pooled held-out support set.
2. Build flattened support prediction vectors \(z_t\).
3. Construct cosine or correlation similarity matrix \(S\).
4. Compute top-\(r\) eigenvectors of \(D^{-1/2}SD^{-1/2}\).
5. Select \(k\) checkpoints by farthest-first coverage in the embedding.
6. Uniformly average the selected checkpoints in weight space.
7. Evaluate the final soup.

Recommended first grid:

- similarity: `cos`, `corr`
- rank: `3, 4, 6`
- subset size: `12, 18, 24`

Seed configuration from the winning probe:

- similarity = cosine
- subset size \(k=24\)
- rank \(r=4\)

## 9. Evaluation Plan

Mandatory baselines:

- final checkpoint
- uniform-all soup
- even-spacing soup (`even_018`)
- best quality-only subset
- best diversity subset

Required ablations:

- cosine vs correlation similarity
- subset size \(k\)
- embedding rank \(r\)
- farthest-first vs random subset of same size
- support probabilities vs support logits

Key evaluation questions:

1. Does the actual weight-space soup preserve the probe-time gain?
2. Is the method still good when \(k\) is much smaller than `24`?
3. Does it generalize across other PACS target splits?

## 10. Main Risks

### 10.1 Geometry mismatch

The support prediction geometry may not align with target transfer geometry.

### 10.2 Probe-to-soup gap

A subset that looks strong in prediction-space probing may lose its edge after actual weight averaging.

### 10.3 Spectral artifacts

The eigenvectors may mostly reflect time ordering or calibration quirks rather than meaningful complementarity.

### 10.4 Novelty risk

The method may ultimately read as “spectral clustering plus uniform soup,” which is novel enough locally but not obviously field-defining.

## 11. Kill Criteria

Drop the method if any of the following happen:

- the actual weight-space soup does not reproduce the probe advantage;
- the best configuration does not beat uniform-all by a meaningful margin on both full and out;
- the method collapses to time-coverage heuristics like `even_018` with no extra gain;
- the same subset family does not replicate beyond `art_painting`.

## 12. Recommendation

This should be the **highest-priority next implementation**.

Why:

- it is the cleanest new out-performing family,
- it stays in the single-model post-hoc setting,
- it deploys a simple uniform soup,
- and it aligns with the project’s strongest empirical lesson: complementarity matters more than exact weighting.
