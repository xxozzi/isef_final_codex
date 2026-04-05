---
title: Jacobian Canalization Repair for post-hoc domain generalization
description: Research proposal for a post-hoc domain-label-free repair method that shrinks the sample-weight Jacobian of validation risk, aiming to make a trained model locally insensitive to source-mixture perturbations rather than flatter in parameter space.
created: 2026-04-05 22:05
last_modified: 2026-04-05 22:05
last_modified_by: codex
status: draft
related_files:
  - claude_workspace/convo_recap/convo.md
  - claude_workspace/results/results_ledger.md
  - claude_workspace/research/reweighting_invariant_weight_averaging.md
  - claude_workspace/papers/riwa_neurips/main.tex
key_functions:
  - Define a post-hoc repair objective based on the Jacobian of validation behavior with respect to source-mixture perturbations
  - Separate the clean central idea from weaker surrounding implementation choices
  - Record theorem targets, novelty limits, failure modes, and kill criteria before any implementation
latest_change: Added the first formalized JCR proposal derived from the conversation recap, with literature grounding, theory targets, failure modes, and falsifiability criteria.
---

# Jacobian Canalization Repair

## 1. Executive Summary

This memo proposes a post-hoc repair method for domain generalization:

> **Jacobian Canalization Repair (JCR): repair a trained model so that held-out validation behavior becomes locally insensitive to small redistributions of source support mass.**

The central object is not:

- flatness in parameter space,
- checkpoint selection,
- subset-soup weighting,
- hidden-environment discovery,
- or trajectory consensus.

It is:

- the **Jacobian of validation risk with respect to source-mixture weights**.

The motivating thesis is narrow:

> A model that is highly sensitive to nearby source-mixture perturbations is likely to be brittle under unseen source-supported shifts. A post-hoc repair should therefore minimize validation loss **and** shrink that source-mixture Jacobian.

This is conceptually cleaner than most of the recent local proposals because it is centered on one mathematical object. It is also more genuinely distinct from flatness than the recent subset-soup and trajectory-consensus branches.

However, the proposal also has real novelty and feasibility risk:

- it is close in spirit to `RIWA`, which already moved from parameter-space flatness to distribution-space robustness;
- it relies on influence-style Hessian approximations or tractable local surrogates;
- and it could collapse empirically into “generic constrained post-hoc fine-tuning” unless the Jacobian term adds clear value over matched controls.

So the correct status is:

- **serious research candidate**
- **not validated**
- **not yet a headline method**
- **worth implementing only with hard kill criteria**

## 2. Bottom Line

If I strip away all marketing language, the proposal is:

1. start from one trained anchor model `theta_0`:
   - plain ERM is allowed
   - a soup anchor is allowed but not required
2. define how validation loss would change if the source mixture were slightly reweighted
3. repair the model inside a small post-hoc family so that:
   - validation loss is good
   - nearby source-mixture sensitivity is small
4. output one repaired model

The central novelty claim is therefore:

> **Post-hoc DG should be framed as shrinking distribution-space sensitivity, not just parameter-space sensitivity.**

That is the strongest honest claim. Stronger claims, such as “JCR is a new universal DG principle” or “JCR is guaranteed to beat flatness-based methods,” would be indefensible.

## 3. Why This Proposal Exists

The local empirical record in [results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/results_ledger.md) is clear enough now:

- `SWING` did not consistently beat `SWING-uniform`
- `TSF` collapsed badly
- weighted graph diffusion failed
- the live branches are still subset-soup methods like `GraphDiffusionSubsetSoup` and `GibbsTopKSubsetSoup`
- strict non-soup projection pilots mostly failed

The important conclusion is not “checkpoint methods are useless.” It is:

> the project has spent too much time on choosing checkpoints and too little time on changing the **trained model’s local response to shift**.

That is the gap JCR is trying to occupy.

It is especially motivated by the current project tension:

- the user wants something **beyond flatness**
- but still:
  - post-hoc,
  - domain-label-free,
  - model-agnostic,
  - and one final deployed model

JCR is one of the few ideas that still fits that box while changing the object of study in a nontrivial way.

## 4. The Central Idea in Plain English

Imagine the source data as a recipe with many ingredients.

A brittle model works only when the recipe has exactly the same proportions as training.

If you slightly upweight some source examples and downweight others, a brittle model’s validation behavior changes sharply.

JCR says:

- treat those small source-mixture changes as the local stand-in for hidden domain shift
- measure how sensitive the model is to them
- then repair the model so that this sensitivity is small

So the method is not:

- “make the weights flatter”

It is:

- “make the model less dependent on the exact source mixture”

That is why it is beyond flatness in a meaningful sense.

## 5. Formal Setup

Let:

- `U = {(x_i, y_i)}_{i=1}^n` be a held-out labeled source support split
- `V` be a disjoint labeled source validation split
- `theta_0` be the trained model before post-hoc repair

Define the weighted support risk

\[
R_w(\theta) = \sum_{i=1}^n w_i \,\ell_i(\theta),
\qquad w \in \Delta^n.
\]

Let `u = (1/n, ..., 1/n)` be the uniform source mixture.

For a local training operator, define `theta^\star(w)` as the local post-repair minimizer or one-step repaired model associated with support weights `w`.

Then define the validation-on-repaired map

\[
F(w) = L_V(\theta^\star(w)).
\]

The central JCR object is the sample-weight Jacobian

\[
J(\theta) = \nabla_w F(w)\big|_{w=u}.
\]

Interpretation:

- `J_i` measures how much validation would change if source example `i` mattered slightly more in the support distribution
- large `J` means the model is fragile to nearby source-composition shifts
- small `J` means the model is locally canalized against those shifts

## 6. First-Order Approximation

If `theta^\star(w)` is approximated by a local optimizer around `theta`, then influence-style implicit differentiation gives the familiar approximation

\[
J_i(\theta)
\approx
- \nabla_\theta L_V(\theta)^\top
H_\theta^{-1}
\big(\nabla_\theta \ell_i(\theta) - \bar g(\theta)\big),
\]

where

\[
\bar g(\theta) = \frac{1}{n}\sum_{i=1}^n \nabla_\theta \ell_i(\theta),
\qquad
H_\theta \approx \nabla_\theta^2 R_u(\theta).
\]

This already reveals the structure:

- `g_i - ḡ` is the local direction induced by reweighting example `i`
- `H^{-1}` maps that perturbation through the local training geometry
- `∇L_V` asks whether that induced change helps or hurts held-out validation

So JCR is a repair method based on the same family of ideas that made `RIWA` conceptually interesting, but with a different decision variable:

- `RIWA`: use local reweighting sensitivity to **score checkpoints**
- `JCR`: use local reweighting sensitivity to **repair one model**

## 7. The Repair Objective

Let `F_r(theta_0)` be a small local patch family around the anchor model.

Examples:

- classifier head only
- final block low-rank adapter
- tiny readout-adjacent LoRA-style patch
- another bounded local patch that still yields one final model

Then the clean JCR objective is

\[
\min_{\delta \in \mathcal F_r(\theta_0)}
L_V(\theta_0 + \delta)
\;+\;
\lambda \,\Psi\!\big(J(\theta_0 + \delta)\big),
\]

where `Psi` is a robust norm or tail functional on the Jacobian, such as:

- `||J||_2`
- `||J||_\infty`
- `CVaR` of signed Jacobian entries
- a weighted top-tail norm if hard slices matter more than average slices

The contribution is the objective, not any specific patch family.

That distinction matters. If the paper is good, the headline is:

> post-hoc DG repair should penalize source-mixture sensitivity

not:

> here is a new head-tuning recipe

## 8. Why This Is Beyond Flatness

`SWAD` says, in the authors’ words, that they “show that finding flat minima results in a smaller domain generalization gap” ([SWAD OpenReview](https://openreview.net/forum?id=zkHlu_3sJYU)).

JCR asks a different question.

Flatness asks:

- if I perturb parameters, does loss remain low?

JCR asks:

- if I perturb the source mixture, does held-out validation remain low after local repair?

That is a real change of geometry:

- `SWAD`: parameter-space geometry
- `JCR`: distribution-space geometry

The methods can disagree.

You can have:

- a flat solution that is highly sensitive to source-composition perturbations
- or a not-especially-flat solution whose validation behavior is locally stable across nearby source reweightings

That is the exact sense in which JCR is beyond flatness.

## 9. Why This Is Not Just Checkpoint Selection

JCR does not ask:

- which checkpoint is best?
- which subset should I soup?
- which weighting over checkpoints should I use?

It asks:

- given one trained model, how can I make its validation behavior less sensitive to nearby source-mixture perturbations?

That means:

- the decision variable is no longer a checkpoint ID
- and no longer a subset of checkpoints
- and no longer a soup coefficient vector

This is the main reason JCR is worth taking seriously at all.

## 10. Closest Local Ancestor: RIWA

JCR is not starting from zero. The closest local ancestor is `RIWA`, documented in:

- [reweighting_invariant_weight_averaging.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/reweighting_invariant_weight_averaging.md)
- [riwa_neurips/main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/riwa_neurips/main.tex)

`RIWA` already made the key philosophical move:

- from flatness in parameter space
- to local robustness in sample-weight space

That means JCR’s novelty claim must stay narrow.

The true novelty is not:

- “distribution-space robustness is new”

The true novelty is:

- “instead of using sample-weight sensitivity to score checkpoints, directly repair the model to shrink it”

So the correct novelty assessment is:

- **moderate at best**
- clearly not a brand-new theoretical continent
- but still distinct enough to justify a fresh proposal if the objective really does useful work

## 11. Literature Foundation

This proposal sits on a fairly clear literature chain.

### 11.1 Flatness as the incumbent DG story

`SWAD` is the canonical post-hoc DG baseline. The paper explicitly states that “finding flat minima results in a smaller domain generalization gap” ([SWAD OpenReview](https://openreview.net/forum?id=zkHlu_3sJYU)).

JCR is not denying that result. It is saying:

- flatness is one robustness object
- but source-mixture sensitivity is another, and potentially more DG-relevant one in the strict post-hoc setting

### 11.2 Directional robustness and invariance

`Tangent Prop` framed generalization in terms of controlling derivatives along chosen nuisance directions, describing this as “a powerful language for specifying what generalizations we wish the network to perform” ([NeurIPS 1991 abstract](https://proceedings.neurips.cc/paper/1991/hash/65658fde58ab3c2b6e5132a39fae7cb9-Abstract.html)).

JCR imports that idea into **distribution space**:

- the nuisance directions are no longer image distortions
- they are nearby directions in the simplex of source sample weights

### 11.3 Influence functions and tractable Jacobian estimation

Koh and Liang emphasize that influence-style approximations can be implemented with “gradients and Hessian-vector products” and still provide useful information even when ideal theory breaks down ([PMLR 2017](https://proceedings.mlr.press/v70/koh17a.html)).

That is the practical backbone for JCR:

- exact retraining Jacobians are intractable
- influence/HVP approximations make the object computable enough to test

### 11.4 Distributionally robust, group-oblivious objectives

Hashimoto et al. argue for objectives that remain “oblivious to the identity of the groups” while controlling minority risk through DRO ([PMLR 2018](https://proceedings.mlr.press/v80/hashimoto18a.html)).

This matters directly for JCR because the user’s domain-label-free requirement is not cosmetic.

JCR is trying to do the same kind of thing in a post-hoc DG setting:

- no group labels
- no domain labels
- robustness expressed through nearby reweightings

### 11.5 Distributional robustness against shifts

Anchor regression argues for “predictive guarantees in terms of distributional robustness against shifts” ([JRSSB 2021](https://academic.oup.com/jrsssb/article/83/2/215/7056043)).

JCR is not anchor regression. But the shared lesson is important:

- if the target problem is robustness to distributional shifts,
- then the mathematical object should probably live in **distribution space**, not only in parameter space

### 11.6 Practical final-model discipline

Model soups matter here because they showed that one can often improve accuracy “without increasing inference time” ([Model Soups](https://proceedings.mlr.press/v162/wortsman22a.html)).

That supports the user’s deployment constraint:

- one final model
- not a test-time ensemble

JCR respects that constraint.

## 12. Theorem Program

This section is the core of whether JCR is a paper or just a heuristic.

None of the statements below should be presented as already proved. These are the theorem targets that would make the method defensible.

### 12.1 Theorem A: Jacobian representation

Under local strong convexity or isolated-minimizer conditions for the repair operator:

\[
J_i(\theta)
=
- \nabla_\theta L_V(\theta)^\top
H_\theta^{-1}
\big(g_i(\theta) - \bar g(\theta)\big).
\]

Purpose:

- justify the first-order object
- make the source-mixture Jacobian more than just notation

What is plausible:

- this is standard implicit differentiation / influence-style structure

What is fragile:

- nonconvexity
- approximate Hessians
- mismatch between exact retraining and one-step local surrogates

### 12.2 Theorem B: Nearby-mixture robustness bound

Let `F(w)` denote validation risk after local repair under source-mixture `w`.
For small perturbations `Delta` around uniform weights:

\[
F(u+\Delta)
\le
F(u)
+
\langle J, \Delta \rangle
+
O(\|\Delta\|^2).
\]

Hence, for an `l_2` ambiguity set:

\[
\sup_{\|\Delta\|_2 \le \rho}
F(u+\Delta)-F(u)
\le
\rho \|J\|_2 + O(\rho^2).
\]

Purpose:

- establish that shrinking `||J||` is not arbitrary
- it directly controls first-order nearby-mixture worst-case validation risk

This is the theoretical spine of the method.

### 12.3 Theorem C: Repair guarantee

Suppose `delta_JCR` minimizes

\[
L_V(\theta_0+\delta) + \lambda \Psi(J(\theta_0+\delta))
\]

over a local repair family `F_r(theta_0)`.

Then, under regularity assumptions, `delta_JCR` improves first-order worst-case nearby-mixture risk relative to:

- the unmodified anchor
- and a matched plain validation repair without the Jacobian term

Purpose:

- separate JCR from generic local fine-tuning

Without a theorem or empirical analogue of this type, the Jacobian term risks being cosmetic.

### 12.4 Theorem D: Approximation error

Bound the gap between:

- exact retraining Jacobian
- influence/Hessian approximation
- practical finite-sample estimator

Purpose:

- show that the practical method estimates the intended object well enough to matter

This is especially important because otherwise reviewers can dismiss JCR as:

- conceptually clean
- but operationally unfaithful

### 12.5 Theorem E: Separation from checkpoint-only methods

Construct a simple setting where:

- no checkpoint or convex soup from a saved bank dominates the anchor under all admissible nearby source-supported shifts
- but a small local patch can

Purpose:

- justify why this is not just “another way to pick a model”

Without this separation, the paper is vulnerable to:

- “interesting objective, but still empirically dominated by subset soups”

## 13. What Is Established vs. What Is Conjectural

### Established or well supported

- flatness is not the only plausible robustness object
- local reweighting / DRO / influence ideas are mathematically legitimate
- one-final-model post-hoc methods are practically important
- sample-weight perturbations are a reasonable local proxy family

### Conjectural

- shrinking the source-mixture Jacobian will improve DG materially
- this object is more aligned with true OOD risk than flatness in this regime
- the practical estimator is accurate enough to beat strong matched controls
- the remaining headroom in the current benchmark is actually patch-repairable

That distinction has to remain explicit in any serious paper draft.

## 14. Why JCR Might Work

There are three plausible positive cases.

### 14.1 The anchor is close, but too source-mixture-sensitive

Then JCR can help by:

- preserving most of the anchor
- reducing sensitivity to small hidden shifts in support composition

This is the best-case story.

### 14.2 The remaining error is mostly head-adjacent

Then a local patch family can repair it without destabilizing the rest of the model.

This is why JCR should first be tested with:

- head-only
- or last-block low-rank

before broader patch families.

### 14.3 Flatness and checkpoint selection have already extracted most basin-level signal

If that is true, then the next source of gain is not picking a different checkpoint, but altering how the final model responds to source-supported perturbations.

That is exactly the scenario JCR is built for.

## 15. Why JCR Might Fail

This section matters more than the optimism section.

### 15.1 The Jacobian may mostly measure nuisance hardness

If high-sensitivity examples are just the hardest source examples, JCR may devolve into:

- another hard-example regularizer

rather than a true DG repair principle.

### 15.2 The nearby-mixture proxy may be too local

Real target shifts may not be well approximated by small source-supported reweightings.

If so, the method is well designed for the wrong perturbation family.

### 15.3 The patch family may dominate the objective

If a generic local repair with the same patch family and budget works just as well, then:

- the Jacobian object is not the real source of improvement

This is the most important empirical failure mode.

### 15.4 Hessian approximations may be too unstable

If practical HVP/influence estimates are noisy, JCR could become:

- conceptually elegant
- numerically brittle

That would kill adoption.

### 15.5 It may be RIWA with training bolted on

This is the novelty failure mode.

If reviewers see it as:

- “RIWA, but instead of selecting checkpoints you optimize the same score”

then the paper will need either:

- a strong separation theorem
- or an unmistakable empirical phenomenon

to survive.

## 16. Falsifiability

JCR is only worth pursuing if it survives strong matched controls.

### 16.1 Minimal matched-control test

Use the same:

- anchor
- patch family
- optimization budget
- validation split

Compare:

1. anchor only
2. plain validation repair
3. repair with a generic smoothness penalty
4. repair with raw-loss DRO
5. full JCR

If `JCR` does not beat `2-4`, the source-mixture Jacobian is not doing meaningful work.

### 16.2 Randomized-control test

Replace the Jacobian term with:

- random projected directions
- or permuted example-gradient assignments

If the effect survives, JCR is probably not the mechanism.

### 16.3 Patch-family robustness test

Run:

- head-only
- last-block low-rank
- slightly larger local patch

If gains appear only in one unstable patch family, the idea is weaker than it looks.

### 16.4 Benchmark-level kill criteria

JCR should be rejected quickly if:

- it does not beat the best matched non-Jacobian repair
- it does not threaten the best live subset-soup baseline
- or its gains vanish outside one favorable split

The current live baseline to beat is still the graph/Gibbs subset-soup family in [results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/results_ledger.md).

## 17. Minimal Experimental Protocol

The first experiment should be small and brutal.

### Stage 1: one anchor, one split

Anchor:

- best current graph-diffusion soup
- or plain ERM if the goal is the cleanest “beyond flatness” story

Patch family:

- head-only first

Compare:

- anchor
- plain validation repair
- JCR

If JCR loses here, stop.

### Stage 2: stronger matched controls

Add:

- raw-loss DRO repair
- generic Jacobian norm not tied to source-mixture perturbations
- randomized Jacobian controls

If JCR cannot separate from these, stop.

### Stage 3: broader patch family

Only after Stage 1 and 2 succeed:

- last-block low-rank patch
- maybe tiny adapter

### Stage 4: multi-split evaluation

Only after local success:

- full PACS sweep
- then other benchmarks if needed

## 18. Honest Novelty Claim

The novelty claim should be:

> We propose a post-hoc repair objective that penalizes the sample-weight Jacobian of validation risk, making the repaired model locally insensitive to nearby source-mixture perturbations.

It should **not** be:

> We discovered a fundamentally new principle of DG.

The first is defensible.
The second is not.

## 19. Recommendation

JCR is worth formalizing because it is one of the few ideas left in this project that is:

- centered on a single mathematical object
- genuinely beyond flatness
- genuinely beyond checkpoint selection
- still compatible with:
  - post-hoc,
  - no target data,
  - no domain labels,
  - and one final deployed model

But it is also high-risk.

The pragmatic recommendation is:

- **keep it**
- **test it hard**
- **kill it fast if the Jacobian term does not beat matched controls**

That is the right posture for this idea.

## 20. References and Primary Links

- SWAD: Junbum Cha et al., “SWAD: Domain Generalization by Seeking Flat Minima.” OpenReview / NeurIPS 2021.  
  [https://openreview.net/forum?id=zkHlu_3sJYU](https://openreview.net/forum?id=zkHlu_3sJYU)

- Tangent Prop: Patrice Simard et al., “Tangent Prop - A formalism for specifying selected invariances in an adaptive network.” NeurIPS 1991.  
  [https://proceedings.neurips.cc/paper/1991/hash/65658fde58ab3c2b6e5132a39fae7cb9-Abstract.html](https://proceedings.neurips.cc/paper/1991/hash/65658fde58ab3c2b6e5132a39fae7cb9-Abstract.html)

- Influence Functions: Pang Wei Koh and Percy Liang, “Understanding Black-box Predictions via Influence Functions.” ICML 2017 / PMLR.  
  [https://proceedings.mlr.press/v70/koh17a.html](https://proceedings.mlr.press/v70/koh17a.html)

- Fairness Without Demographics: Tatsunori Hashimoto et al., “Fairness Without Demographics in Repeated Loss Minimization.” ICML 2018 / PMLR.  
  [https://proceedings.mlr.press/v80/hashimoto18a.html](https://proceedings.mlr.press/v80/hashimoto18a.html)

- Anchor Regression: Dominik Rothenhäusler et al., “Anchor Regression: Heterogeneous Data Meet Causality Free.” JRSSB 2021.  
  [https://academic.oup.com/jrsssb/article/83/2/215/7056043](https://academic.oup.com/jrsssb/article/83/2/215/7056043)

- Model Soups: Mitchell Wortsman et al., “Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time.” ICML 2022 / PMLR.  
  [https://proceedings.mlr.press/v162/wortsman22a.html](https://proceedings.mlr.press/v162/wortsman22a.html)
