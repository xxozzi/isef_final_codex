---
title: Gibbs Top-K Subset Soup
description: Comprehensive research proposal for a single-run post-hoc DG method that uses Gibbs-style checkpoint weights only as a ranking mechanism, then deploys a sparse uniform soup over the highest-mass checkpoints.
created: 2026-04-03 19:45
last_modified: 2026-04-03 19:45
last_modified_by: codex
status: draft
related_files:
  - claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json
  - claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json
  - domaingen/posthoc/moonshot_2.py
key_functions:
  - Define a Gibbs-ranking sparse-soup method motivated by support-loss curves and priors over checkpoints
  - Separate the useful posterior-ranking signal from the failed direct soft-weight deployment template
  - Record the theory-friendly aspects, novelty limits, and failure modes
latest_change: Initial comprehensive proposal based on the strongest moonshot Gibbs-weighting probes.
---

# Gibbs Top-K Subset Soup

## 1. Executive Summary

This memo proposes a more theory-friendly but lower-novelty candidate:

> **Gibbs Top-K Subset Soup (GTS)**: form a Gibbs distribution over checkpoints using a held-out source loss curve and a simple prior, then convert that Gibbs mass into a sparse subset and deploy a uniform soup over the selected checkpoints.

The proposal is motivated by two successful `moonshot_2` probes:

- `gibbs_uniform_supportmean_t0p02_prob = 0.87158203125` full / `0.8924205378973105` out
- `gibbs_recency_supporttail_t0p01_logit = 0.87841796875` full / `0.8753056234718827`

from [moonshot_2_summary.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json).

The first of those exactly ties the best balanced shotgun baseline `even_018_prob` on both reported metrics. The second gives a very strong full-accuracy point.

So Gibbs weighting is clearly not dead. But the proposal here is deliberately **not** to deploy the raw full-bank Gibbs weights. The project’s history with soft weighting is too negative for that.

Instead, this memo treats the Gibbs weights as a **ranking device** and turns them into a sparse uniform soup.

## 2. Why This Proposal Exists

This family is attractive for one reason above all:

> it is the cleanest bridge between empirical success and a plausible theory story.

Unlike the graph-diffusion and spectral-subset families, Gibbs weighting is already naturally connected to:

- exponential weights,
- posterior-like model averaging,
- PAC-Bayes / Gibbs-posterior intuition,
- and held-out empirical risk minimization with a prior.

The empirical signal is also real:

- the strongest out-performing Gibbs probe used `uniform` prior + `supportmean` loss + temperature `0.02`;
- the strongest full-performing Gibbs probe used `recency` prior + `supporttail` loss + temperature `0.01`.

That suggests the family is worth pursuing, but with a crucial correction:

**use the Gibbs distribution to rank checkpoints, not to define the deployed continuous weights.**

## 3. Position Relative to Existing Literature

This method is the least novel of the three proposed tracks.

It is adjacent to:

- exponential-weights aggregation,
- Gibbs posteriors,
- PAC-Bayesian model averaging,
- and standard score-plus-prior model selection.

The novelty claim therefore cannot be “Gibbs weighting is new.” It is not.

The narrower claim is:

> In this project’s single-run post-hoc DG setting, a Gibbs posterior over trajectory checkpoints is used only as a sparse ranking-and-truncation operator, with the final deployment object still a uniform soup over real checkpoints.

That is narrower, safer, and more honest.

## 4. Core Hypothesis

The main hypothesis is:

> Held-out source loss curves do contain useful information about which checkpoints should survive into a soup, but the information is too noisy to trust as exact deployment weights. A Gibbs posterior smooths the ranking problem, and a top-\(k\) uniform soup extracts the useful part of that ranking while avoiding brittle weight estimation.

This fits the local evidence very well:

- exact optimized weights have repeatedly underdelivered,
- but score curves still help identify promising checkpoints,
- and sparse subset soups remain much more reliable deployment objects.

## 5. Formal Construction

### 5.1 Setup

Let checkpoints be
\[
\theta_1,\dots,\theta_T.
\]

Let \(\ell_t\) denote a held-out source score for checkpoint \(t\), such as:

\[
\ell_t^{\mathrm{mean}},
\qquad
\ell_t^{\mathrm{tail}},
\qquad
\ell_t^{\mathrm{combo}}.
\]

Let \(\pi_t\) be a prior over checkpoints, for example:

- uniform prior,
- recency prior,
- center prior.

### 5.2 Gibbs distribution

For temperature \(\tau > 0\), define
\[
w_t
=
\frac{\pi_t \exp(-\ell_t/\tau)}{\sum_{s=1}^T \pi_s \exp(-\ell_s/\tau)}.
\]

This is exactly the form implemented in [_gibbs_weights](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/domaingen/posthoc/moonshot_2.py#L433).

### 5.3 Sparse selection

Instead of deploying the weighted full-bank soup, define either:

1. top-\(k\) subset
\[
\mathcal S_k = \operatorname{TopK}(w,k),
\]

or

2. mass-threshold subset
\[
\mathcal S_q = \min\left\{\mathcal S : \sum_{t\in\mathcal S} w_t \ge q\right\}.
\]

Then deploy
\[
\bar\theta_{\mathcal S}
=
\frac{1}{|\mathcal S|}\sum_{t\in\mathcal S}\theta_t.
\]

This is the entire design principle: soft posterior for ranking, hard sparse soup for deployment.

## 6. Why This Could Work

### 6.1 Ranking is easier than weighting

A held-out source score may be good enough to rank checkpoints even when it is not good enough to produce trustworthy exact weights.

### 6.2 Temperature controls conservatism

Large temperature keeps many checkpoints alive. Small temperature collapses to a few. This is a useful bias-variance control on the ranking problem.

### 6.3 Prior encodes weak inductive bias

A recency prior and a uniform prior correspond to two different beliefs:

- late checkpoints are better unless the support curve says otherwise;
- every checkpoint is equally plausible until the support curve says otherwise.

The probe evidence suggests both beliefs are useful in different parts of the tradeoff frontier.

### 6.4 Sparse deployment avoids the old failure mode

The method does not ask the final model to trust precise full-bank weights. That is the exact correction learned from the failed reweighting families.

## 7. Theory Program

This is the most theory-friendly proposal of the three.

### 7.1 Assumptions

1. **Loss alignment.**
   The chosen held-out source loss curve is weakly aligned with target desirability.

2. **Mass concentration.**
   The Gibbs posterior places most of its mass on a reasonably small subset.

3. **Subset compatibility.**
   The high-mass checkpoints are merge-compatible.

### 7.2 First theorem target

A first target is a mass concentration statement:

> If the loss gap between a “good” subset \(G\) and the rest of the checkpoints exceeds a temperature-scaled margin, then the Gibbs posterior concentrates most of its mass on \(G\).

Schematically, if
\[
\ell_t \le \ell^\star + \Delta_{\mathrm{in}}
\quad \text{for } t \in G
\]
and
\[
\ell_t \ge \ell^\star + \Delta_{\mathrm{out}}
\quad \text{for } t \notin G,
\]
then
\[
\sum_{t\notin G} w_t
\]
can be bounded in terms of
\[
\exp\!\left(-\frac{\Delta_{\mathrm{out}}-\Delta_{\mathrm{in}}}{\tau}\right)
\]
times a prior-mass factor.

That gives a clean justification for top-\(k\) truncation.

### 7.3 Second theorem target

If the soup over \(G\) is stable, then
\[
R^\star(\bar\theta_{\mathcal S})
\le
\min_{t \in G} R^\star(t)

+ \varepsilon_{\mathrm{trunc}}
+ \varepsilon_{\mathrm{merge}}.
\]

Again, the mergeability term is the real hard part.

## 8. Concrete Algorithm

1. Compute a held-out source loss curve \(\ell_t\) over checkpoints.
2. Choose prior \(\pi_t\).
3. Compute Gibbs weights \(w_t\).
4. Convert \(w_t\) to a sparse subset by top-\(k\) or mass-thresholding.
5. Uniformly average that subset in weight space.

Recommended first grid:

- losses: `supportmean`, `supporttail`, `valtail`
- priors: `uniform`, `recency`
- temperatures: `0.01`, `0.02`, `0.05`
- subset sizes: `12`, `18`, `24`, `32`

Anchor points from the probes:

- `uniform + supportmean + 0.02`
- `recency + supporttail + 0.01`

## 9. Evaluation Plan

This family needs especially careful comparison to simpler baselines because its novelty is lower.

Must compare against:

- top-\(k\) quality subset
- even spacing subset
- spectral subset
- graph diffusion subset
- uniform-all

Key question:

> Does Gibbs ranking produce a sparse soup that is genuinely better than the simpler “pick the best-looking checkpoints” heuristics?

If not, this family may still be useful as a diagnostic, but not as a headline method.

## 10. Main Risks

### 10.1 Low novelty

This is the biggest issue. The method may read as “quality ranking plus a soft prior.”

### 10.2 Collapse to quality subset

At low temperature, Gibbs ranking may be little more than a smoothed top-\(k\) loss selector.

### 10.3 Probe-to-soup mismatch

As with every soft-weight family, the full-bank probe may not translate cleanly to a sparse weight-space soup.

### 10.4 Support overfitting

The method may simply overfit whichever support loss curve is used.

## 11. Kill Criteria

Drop the method as a mainline candidate if:

- the sparse Gibbs soup is no better than direct top-\(k\) quality ranking;
- Spectral Subset Soup and Graph Diffusion Subset Soup both dominate it empirically;
- or the best settings only reproduce already-known sparse-spacing behavior.

## 12. Recommendation

This should be the **third implementation track**.

It is valuable because:

- it is empirically alive,
- it is theory-friendly,
- and it gives a clean control experiment for whether the new signal is really geometric or just a better ranking distribution.

But it should not be the flagship unless it clearly beats the more structurally novel geometry-based methods.
