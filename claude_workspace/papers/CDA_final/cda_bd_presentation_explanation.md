---
title: CDA-BD Presentation Explanation
description: Presentation-ready explanation of the CDA-BD checkpoint weighting rule, including equations, intuition, slide structure, and speaker script.
last_modified: 2026-04-25 00:00
last_modified_by: codex
status: active
key_functions:
  - Explain why CDA-BD is the cleaner checkpoint weighting rule to present
  - Connect CDA-BD to source-mixture shift and balanced source-domain risk
  - Provide slide-ready equations and a spoken explanation
latest_change: Added a presentation note for choosing and explaining CDA-BD over CDA-Piv.
---

# CDA-BD Presentation Explanation

## Recommendation

Present **CDA-BD**, not CDA-Piv.

The reason is that **CDA-BD has the cleaner scientific story**. CDA-Piv is defensible, but it is harder to explain without sounding like a scoring heuristic: remove each checkpoint, measure leave-one-out pivotality, z-score the pivotality, subtract a sensitivity z-score, then normalize. That is too many moving pieces for a short presentation.

CDA-BD is easier to explain because it has one central idea:

> After CDA selects a checkpoint family, CDA-BD chooses weights so the final soup moves toward the best source-domain loss profile that the family can achieve.

That connects directly to the main CDA thesis: the deployed model should not only have low average source loss. It should have a **low and balanced source-domain loss vector**, because a balanced source-loss vector is less fragile under source-mixture shift.

## Setup

Suppose the retained family has \(k\) checkpoints and there are \(E\) source domains.

Build the source-loss matrix

\[
R\in\mathbb{R}^{E\times k},
\]

where

\[
R_{e,j}=L_e(\theta_j).
\]

Each column of \(R\) is one checkpoint's source-domain loss vector:

\[
r_j=
\begin{bmatrix}
L_1(\theta_j)\\
L_2(\theta_j)\\
\vdots\\
L_E(\theta_j)
\end{bmatrix}.
\]

The final checkpoint soup uses weights

\[
w\in\Delta^k,
\qquad
\sum_{j=1}^{k}w_j=1,
\qquad
w_j\ge 0.
\]

The approximate source-loss vector of the weighted family is

\[
Rw.
\]

## The CDA-BD Target

CDA-BD defines an ideal source-loss target vector \(b\). For each source domain, it asks which retained checkpoint performed best on that domain:

\[
b_e=\min_{1\le j\le k}R_{e,j}.
\]

So

\[
b=(b_1,\dots,b_E)^\top.
\]

This does not mean one checkpoint achieves all entries of \(b\). Usually, no single checkpoint is best on every source domain. The point is different: \(b\) is the best per-domain loss profile visible inside the retained family.

CDA-BD then asks:

> Can we choose weights \(w\) so the soup's source-loss vector \(Rw\) gets close to this ideal target \(b\)?

## The CDA-BD Objective

CDA-BD solves

\[
\min_{w\in\Delta^k}
\frac{1}{E}\|Rw-b\|_2^2
+
\lambda_{\rm ent}\mathrm{KL}(w\|u),
\]

where

\[
u=\frac{1}{k}\mathbf{1}.
\]

The first term is the target-projection term:

\[
\frac{1}{E}\|Rw-b\|_2^2.
\]

It says: choose checkpoint weights so the weighted source-loss vector \(Rw\) is close to the best source-domain loss target \(b\).

The second term is the entropy regularizer:

\[
\lambda_{\rm ent}\mathrm{KL}(w\|u).
\]

It says: do not collapse too sharply onto one checkpoint unless the loss-target term strongly justifies it. In presentation language, this keeps the soup from becoming an unnecessarily brittle pseudo-singleton.

## Why This Matches CDA

CDA is built around the source-mixture certificate

\[
\bar z(w)+\rho\|P_\perp z(w)\|_2,
\]

where \(z(w)\) is the source-domain loss vector induced by the weighted family.

The first part,

\[
\bar z(w),
\]

is ordinary source fit.

The second part,

\[
\rho\|P_\perp z(w)\|_2,
\]

is the source-mixture sensitivity penalty. It is small when the source-domain losses are balanced.

CDA-BD supports this goal because moving \(Rw\) toward a low per-domain target \(b\) tends to produce a source-loss vector that is both low and more balanced. That is exactly what you want if the unseen target may behave like a nearby reweighting of the source domains.

## Slide Outline

Use one slide titled **CDA-BD: Weighting the Retained Checkpoints**.

1. **Input:** VSC gives a retained checkpoint family

\[
S=\{\theta_1,\dots,\theta_k\}.
\]

2. **Represent each checkpoint by source-domain losses**

\[
R_{e,j}=L_e(\theta_j).
\]

3. **Define the per-domain best target**

\[
b_e=\min_j R_{e,j}.
\]

4. **Choose soup weights by projection**

\[
\min_{w\in\Delta^k}
\frac{1}{E}\|Rw-b\|_2^2
+
\lambda_{\rm ent}\mathrm{KL}(w\|u).
\]

5. **Interpretation:** The final soup tries to match the best source-domain loss profile available in the family, while staying smoothly weighted.

## Speaker Script

> Once CDA has selected a retained checkpoint family, we still need to decide how much weight each checkpoint receives in the final soup. CDA-BD does this in source-loss-vector space. Each checkpoint has a vector of losses across the source domains. For each domain, we look at the best loss achieved by any checkpoint in the family, giving an ideal target vector \(b\). The final soup cannot usually achieve every coordinate of \(b\) at once, so CDA-BD projects toward that target: it chooses weights \(w\) so that \(Rw\) is close to \(b\), while entropy regularization prevents the weights from collapsing too sharply. This directly supports CDA's goal: a low, balanced source-loss vector is less sensitive to source-mixture shift.

## How To Avoid Overcomplicating It

Do not lead with the phrase **Blackwell-dual** unless there is a backup question. It sounds more technical than the audience needs.

Use this phrase instead:

> CDA-BD is a target-set projection weighting rule.

That is accurate enough for the main presentation. If someone asks why it is called BD, then explain that it is inspired by the idea of steering a vector-valued payoff toward a desirable target set. Here, the vector is the source-domain loss vector.

## Why Not CDA-Piv

CDA-Piv uses leave-one-out pivotality:

\[
\pi_j=\Phi(u^{(-j)})-\Phi(u),
\]

then guards against source-mixture sensitivity:

\[
a_j=\operatorname{zscore}(\pi)_j-\alpha\operatorname{zscore}(s)_j.
\]

This is reasonable, but it requires more explanation for less conceptual payoff. The audience has to understand leave-one-out removal, the CDA proxy \(\Phi\), the sensitivity score \(s_j\), z-scoring, and positive-score normalization. CDA-BD avoids that overhead.

## Plain Explanation

CDA-BD says: each checkpoint may be good on different source domains, so do not just average them uniformly. First, look at the best loss any checkpoint achieves on each source domain. Then choose soup weights that make the final averaged model get as close as possible to that best source-domain loss profile. The entropy term keeps the weights from collapsing too aggressively onto one checkpoint. This is a clean presentation choice because it directly supports the core CDA idea: a model with low, balanced source-domain losses is less fragile when the source mixture changes.
