---
title: Adjacent literature sweep for label-free post-hoc DG ideas
description: Concise memo surveying adjacent literatures outside domain generalization for simple principles that could transfer to single-run, architecture-agnostic, domain-label-free post-hoc checkpoint selection or averaging.
created: 2026-03-17 17:44
last_modified: 2026-03-17 17:44
last_modified_by: agent
status: active
related_files: claude_workspace/research/stationarity_aware_weight_averaging.md, claude_workspace/research/reweighting_invariant_weight_averaging.md, claude_workspace/workspace_index.md
key_functions: N/A
latest_change: Added an external adjacent-literature sweep and distilled three candidate transferable principles for post-hoc checkpoint selection and averaging.
change_log:
  - 2026-03-17 17:44: Added an external adjacent-literature sweep and distilled three candidate transferable principles for post-hoc checkpoint selection and averaging.
---

# Bottom line

The most transferable ideas outside DG are not new training losses. They are
new ways to score checkpoints from a single trajectory by asking whether a
checkpoint is:

- functionally stable over time,
- part of a connected local posterior/consensus set,
- or insensitive to small changes in which source examples matter.

Those map cleanly onto single-run, post-hoc, domain-label-free selection.

# Most useful adjacent signals

## 1. Functional stationarity beats raw flatness as a selector

Best supporting line:

- non-convergent learning theory now explicitly argues that models that
  "`train stably generalize better`" even when weights do not converge.
- prediction-churn work treats unnecessary prediction flips across model
  updates as a real failure mode, not just noise.

Transferable principle:

- prefer checkpoints whose predictions on a held-out source pool have low
  short-horizon drift under the *actual* ongoing training dynamics.

Why this transfers well:

- single-run: needs only dense checkpoints from one run,
- post-hoc: no retraining,
- domain-label-free: uses unlabeled or pooled held-out source examples,
- architecture-agnostic: works in prediction space.

Closest method form:

- score each checkpoint by future predictive drift or churn on held-out source
  support, gate by source fit, then average the contiguous low-drift window.

Key sources:

- Chandramoorthy et al., 2022, *On the generalization of learning algorithms
  that do not converge*:
  [arXiv](https://arxiv.org/abs/2208.07951)
- Milani Fard et al., 2016, *Launch and Iterate: Reducing Prediction Churn*:
  [NeurIPS PDF](https://proceedings.neurips.cc/paper_files/paper/2016/file/dc5c768b5dc76a084531934b34601977-Paper.pdf)
- Haghighat et al., 2026, *Resolving Predictive Multiplicity for the Rashomon
  Set*:
  [arXiv](https://arxiv.org/abs/2601.09071)

## 2. Treat the late trajectory as a connected posterior, not just a window

Best supporting line:

- mode connectivity shows that good solutions are often connected by simple
  low-loss curves.
- model soups show that averaging models inside one basin can improve
  robustness without extra inference cost.
- SWAG turns late SGD iterates into an approximate Gaussian posterior and
  improves uncertainty/calibration through posterior averaging.

Transferable principle:

- do not average checkpoints just because they are nearby in time; average
  checkpoints that appear to belong to the same connected high-confidence
  posterior mass.

Why this transfers well:

- still single-run and post-hoc,
- architecture-agnostic as long as weights can be averaged or sampled from,
- gives a cleaner theoretical story than pure flatness: a local posterior or
  consensus region is the object, not a single best iterate.

Closest method form:

- identify a connected low-barrier subset of late checkpoints, weight them by a
  simple posterior proxy such as validation fit plus predictive agreement or
  calibration, then form a weighted soup.

Key sources:

- Garipov et al., 2018, *Loss Surfaces, Mode Connectivity, and Fast Ensembling
  of DNNs*:
  [arXiv](https://arxiv.org/abs/1802.10026)
- Wortsman et al., 2022, *Model soups*:
  [PMLR](https://proceedings.mlr.press/v162/wortsman22a.html)
- Maddox et al., 2019, *A Simple Baseline for Bayesian Uncertainty in Deep
  Learning*:
  [arXiv](https://arxiv.org/abs/1902.02476)
- Dziugaite and Roy, 2019, *Deterministic PAC-Bayesian generalization bounds
  for deep networks via generalizing noise-resilience*:
  [arXiv](https://arxiv.org/abs/1905.13344)

## 3. Robust checkpoints are insensitive to support perturbations, not only weight perturbations

Best supporting line:

- influence functions estimate how much a prediction changes when a training
  point is upweighted.
- core-set active learning recasts good subset choice as geometric coverage of
  the whole pool.
- Bayesian active learning emphasizes epistemic uncertainty over the support,
  not just point estimates.

Transferable principle:

- prefer checkpoints whose validation behavior changes little when the source
  support is slightly reweighted, thinned, or reduced to representative cores.

Why this transfers well:

- still post-hoc,
- compatible with no domain labels,
- more directly shift-aware than parameter flatness because it perturbs the
  empirical source distribution.

Closest method form:

- compute a worst-case small reweighting score, influence covariance score, or
  coverage-weighted core-set score on held-out source support, then select or
  average checkpoints with low sensitivity.

Key sources:

- Koh and Liang, 2017, *Understanding Black-box Predictions via Influence
  Functions*:
  [PMLR](https://proceedings.mlr.press/v70/koh17a.html)
- Sener and Savarese, 2018, *Active Learning for Convolutional Neural Networks:
  A Core-Set Approach*:
  [arXiv](https://arxiv.org/abs/1708.00489)
- Gal et al., 2017, *Deep Bayesian Active Learning with Image Data*:
  [PMLR](https://proceedings.mlr.press/v70/gal17a.html)
- Waddington-style canalization framing:
  [Oxford review](https://academic.oup.com/icb/article/47/3/390/631771)

# Candidate principles to actually pursue

## Candidate A: Churn-Plateau Averaging

Use short-horizon predictive drift on held-out source data as the primary
selector, then average a contiguous low-drift, low-loss plateau.

Why I would pursue it:

- simplest,
- no Hessian or influence approximation needed,
- strongest fit to the single-run post-hoc constraint.

## Candidate B: Connected Posterior Soup

Turn the late trajectory into a weighted soup only after filtering to a
connected low-barrier subset, with weights from a simple posterior proxy such
as agreement, calibration, or SWAG-style local covariance.

Why I would pursue it:

- clean bridge from SWA/SWAD/model soups/SWAG,
- preserves the good "averaging without extra inference cost" story,
- easy to explain as a better criterion for *which* checkpoints deserve to be
  in the soup.

## Candidate C: Core-Robust or Reweighting-Robust Averaging

Select checkpoints that are minimally changed by small support reweightings or
core-set replacements, then average them.

Why I would pursue it:

- most shift-relevant,
- best bridge to influence functions and active-learning geometry,
- but heavier than Candidate A.

# What I deprioritized

- plain calibration alone:
  useful as a tie-breaker, but too weak as the main selector.
- information bottleneck:
  good high-level lens, but the post-hoc operationalization is less clean.
- test-time adaptation:
  inspiring for entropy and minimal-adjustment ideas, but most methods assume
  target batches at deployment time.
- sequential Monte Carlo:
  useful posterior metaphor, but too much machinery for a simple first method.

# Recommendation

If the goal is one new simple method, pursue:

1. `Churn-Plateau Averaging`
2. `Connected Posterior Soup`
3. `Core-Robust Averaging`

In that order.
