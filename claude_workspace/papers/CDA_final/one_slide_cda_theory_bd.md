---
title: One-Slide CDA Theory and CDA-BD Explanation
description: One-slide presentation plan for explaining CDA source-mixture shift, flatness/diversity theory, and CDA-BD checkpoint weighting.
last_modified: 2026-04-25 00:00
last_modified_by: codex
status: active
key_functions:
  - Condense CDA theory and CDA-BD into one presentation slide
  - Provide slide text, equations, layout, and speaker notes
  - Keep the presentation focused on source-mixture shift, mergeability, diversity cancellation, and target-set weighting
latest_change: Added a one-slide CDA explanation plan based on the presentation discussion.
---

# One-Slide CDA Theory and CDA-BD Explanation

## Slide Title

**CDA: Building a Soup Stable Under Source-Mixture Shift**

## Main Slide Layout

Use a **three-block horizontal layout** if possible:

1. **CDA Certificate**
2. **Why Flatness + Diversity Help**
3. **CDA-BD Weighting**

Keep the slide visually sparse. The equations are the center of the slide. The bullets should be short.

---

## Block 1: CDA Certificate

Put:

\[
L_T(\theta)
\le
\bar L(\theta)
+
\rho\|P_\perp L(\theta)\|_2
+
\epsilon_{\rm app}
\]

Tiny labels:

- \(\bar L(\theta)\): average source loss
- \(\|P_\perp L(\theta)\|_2\): source-mixture sensitivity

One sentence:

> CDA prefers models with **low and balanced** source-domain losses.

---

## Block 2: Why Flatness + Diversity Help

Put the soup certificate:

\[
L_T(\bar\theta(w))
\le
\bar z(w)
+
\rho\|P_\perp z(w)\|_2
+
(E^{-1/2}+\rho)M(w)
+
\epsilon_{\rm app}
\]

Then two mini-lines:

**Flatness controls mergeability**

\[
M(w)=\|L(\bar\theta(w))-z(w)\|_2
\]

**Diversity controls sensitivity when weaknesses cancel**

\[
\|P_\perp z(w)\|_2^2
=
\sum_j w_j^2\|c_j\|_2^2
+
2\sum_{i<j}w_iw_j\langle c_i,c_j\rangle
\]

Tiny note:

> Useful diversity means \(\langle c_i,c_j\rangle<0\): source-domain weaknesses cancel.

---

## Block 3: CDA-BD Weighting

Put:

\[
R_{e,j}=L_e(\theta_j),
\qquad
b_e=\min_j R_{e,j}
\]

\[
\min_{w\in\Delta^k}
\frac{1}{E}\|Rw-b\|_2^2
+
\lambda_{\rm ent}\mathrm{KL}(w\|u)
\]

Tiny labels:

- \(R\): source-domain losses of retained checkpoints
- \(b\): best loss achieved on each source domain
- \(w\): final soup weights

One sentence:

> CDA-BD weights checkpoints so the soup moves toward the best balanced source-loss profile.

---

# Slide Speaker Notes

Say this:

> CDA starts from the idea that the unseen target may behave like a nearby reweighting of the source domains. Under that assumption, target risk is controlled by two source-only quantities: average source loss and source-mixture sensitivity. So CDA does not just ask whether the model is good on average. It asks whether the model is good in a balanced way across source domains.

Then:

> This also explains why flatness and diversity methods work. Flatness controls \(M(w)\), the mergeability error, which measures whether the averaged weight-space soup actually behaves like the checkpoints we averaged. Diversity controls the source-mixture sensitivity term, but only when the checkpoints have complementary source-domain weaknesses. If their centered loss vectors point in opposite directions, the inner product is negative and averaging cancels sensitivity.

Then:

> CDA-BD is the checkpoint weighting rule I use to turn this theory into a deployment decision. Each checkpoint has a loss vector across source domains. For each domain, I define the best loss achieved by any checkpoint in the retained family. CDA-BD then chooses weights so the final soup gets as close as possible to that best source-domain loss profile, while entropy regularization prevents the weights from collapsing too sharply onto one checkpoint.

---

# Ultra-Short Spoken Version

If time is tight, say:

> CDA says a good post-hoc model should have low average source loss and low sensitivity to source-domain reweighting. Flatness helps because it makes the soup mergeable: the averaged model behaves like the checkpoints being averaged. Diversity helps when checkpoint weaknesses cancel across source domains. CDA-BD then chooses weights that move the final soup toward the best source-domain loss profile available in the retained checkpoint family, while keeping the weights from collapsing onto one checkpoint.

---

# What To Avoid On This One Slide

Do not include both CDA-Piv and CDA-BD.

Do not include full theorem names or proof steps.

Do not lead with the word **Blackwell**. Use **target-set projection weighting** instead.

Do not over-explain \(\alpha=u_E+\delta\) on this slide unless someone asks. If asked, say:

\[
\alpha=u_E+\delta,
\qquad
\mathbf{1}^\top\delta=0,
\qquad
\|\delta\|_2\le\rho.
\]

Then explain that this represents a **small nearby reweighting of source-domain mass**, not an arbitrary extreme reweighting.

---

# Plain Explanation

This one slide should say: CDA makes a post-hoc model robust by looking for low and balanced source-domain losses. Flatness helps because it makes checkpoint averaging safe. Diversity helps when different checkpoints fail on different source domains and those failures cancel. CDA-BD then chooses checkpoint weights that make the final soup move toward the best source-domain loss profile available inside the retained checkpoint family.
