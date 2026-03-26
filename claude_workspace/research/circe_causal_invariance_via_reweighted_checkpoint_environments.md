---
title: Causal invariance via reweighted checkpoint environments for label-free single-run post-hoc domain generalization
description: Research proposal for CIRCE, a theory-first post-hoc DG method that adapts invariant causal prediction and invariant risk minimization to the single-run, no-domain-label setting by treating bounded source reweightings as latent environments and selecting soup-safe checkpoint subsets whose optimal readout remains invariant across them.
created: 2026-03-22 15:10
last_modified: 2026-03-22 15:10
last_modified_by: agent
status: active
related_files: claude_workspace/research/scout_submodular_coverage_uniform_trajectory_soups.md, claude_workspace/results/ablation_results_dcola.json, literature/diwa_tex_source/sections/theory/theory_bvc.tex, literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex
key_functions: N/A
latest_change: Added a new causal-theory research proposal, CIRCE, that reframes label-free post-hoc DG as selecting soup-safe checkpoint subsets whose optimal decision rule is invariant across adversarial source reweightings.
change_log:
  - 2026-03-22 15:10: Created the CIRCE proposal after synthesizing causal inference, causal representation learning, IRM critiques, anchor regression, and local D-COLA ablations.
---

# Bottom line

As a causal-inference-inspired branch, the best serious proposal I can defend is:

- **`CIRCE` = `Causal Invariance via Reweighted Checkpoint Environments`**

The core claim is:

> **A good post-hoc DG soup is one for which the same simple decision rule remains
> optimal across all plausible source-supported distribution shifts.**

That is a direct adaptation of invariant causal prediction and invariant risk
minimization to the setting we actually have:

- one training trajectory,
- no domain labels,
- dense checkpoints,
- a source holdout set,
- and a need to deploy one single soup.

Unlike `SCOUT`, which is built around robust nonredundant coverage, `CIRCE` is
built around **causal invariance of the predictor mechanism**.

I do **not** think this causal branch is automatically stronger than `SCOUT`.
But it is a legitimate first-principles alternative, and it is much cleaner than
trying to bolt causal language onto a heuristic after the fact.

# Why look at causality here at all

The causal literature is attractive because it starts from a different premise
than standard DG:

- the goal is not merely to perform well on a family of empirical domains,
- the goal is to recover a predictor based on mechanisms that stay stable under
  interventions or environment changes.

That is exactly the kind of story you wanted:

- theoretically motivated,
- not circular,
- and not "we saw this work, so let's justify it later."

The problem is that most causal DG methods assume **observed environments** or
anchor variables. We do not have those. So the proposal has to adapt the causal
principle to the no-domain-label setting without pretending that missing
structure is magically available.

# What the causal literature actually says

## 1. Invariant Causal Prediction

The key ICP idea is:

> "the mechanism of the response is the same in all settings"  
> Source: [Research seminar summary of ICP](
> https://www.wu.ac.at/en/statmath/details-news-statmath/detail/research-seminar-lucas-kook)

More concretely, the JRSSB ICP paper is about identifying predictors for which
the conditional law of the response remains invariant across environments.

Open search anchors:

- https://academic.oup.com/jrsssb/article-abstract/78/5/947/7040653
- https://stat.ethz.ch/~nicolai/invariant.pdf

This principle is conceptually stronger than plain robust risk minimization:

- low worst-case loss says "the predictor survives the shifts we tested,"
- invariant conditional structure says "the underlying predictive mechanism stays
  the same across those shifts."

## 2. IRM

Arjovsky et al. state:

> "the optimal classifier ... is the same for all environments"  
> Source: [IRM PDF, Definition 3](
> http://leon.bottou.org/publications/pdf/tr-irm-2019.pdf)

The formal definition in the paper is:

$$
w \in \arg\min_{\bar w:H\to Y} R^e(\bar w \circ \Phi)
\qquad \text{for all } e \in \mathcal E.
$$

The same source also writes:

> "the invariance of the predictor"  
> Source: [IRM PDF, penalized objective section](
> http://leon.bottou.org/publications/pdf/tr-irm-2019.pdf)

This is the important causal bridge:

- a representation is good if **one shared classifier** is simultaneously optimal
  across environments.

That is exactly the object I want to adapt post-hoc.

## 3. Why naive IRM is not enough

Kamath et al. show:

> "IRM ... can fail to capture 'natural' invariances"  
> Source: [Does Invariant Risk Minimization Capture Invariance?](
> https://proceedings.mlr.press/v130/kamath21a.html)

They further note that:

> "IRM is extremely fragile to sampling"  
> Source: same as above

This critique matters a lot. It means we should **not** imitate IRMv1 blindly.
If we build a causal post-hoc method, it should:

- avoid the brittle linear dummy-classifier surrogate,
- define environments carefully,
- and directly optimize the intended invariance object as much as possible.

## 4. Anchor regression

Anchor regression is useful because it gives a causal-statistical notion of
robustness under structured perturbations.

Rothenhausler et al. write:

> "optimizes worst-case prediction risk over a class of perturbations"  
> Source: [Anchor regression: Heterogeneous data meet causality](
> https://people.math.ethz.ch/~peterbu/publications/anchor-JRSSB.pdf)

They also write:

> "improved replicability of variable selection"  
> Source: same as above

And they are explicit about the scope:

> "not leading to robust prediction when the heterogeneity ... is different from
> the restricted set of shift interventions"  
> Source: same as above

This is exactly the kind of honesty we need. If we borrow causal ideas, we need
to state the shift family we are protecting against.

## 5. Causal representation learning from multiple distributions

Zhang et al. 2024 matter because they relax the "hard intervention" obsession.
They write:

> "without assuming hard interventions behind distribution changes"  
> Source: [Causal Representation Learning from Multiple Distributions: A General Setting](
> https://proceedings.mlr.press/v235/zhang24br.html)

This is very helpful for us. It means a causal branch does **not** need to
pretend we have perfect intervention labels. A family of multiple distributions
can already be enough to talk meaningfully about causal representations.

# What the local ablations tell us a causal method must respect

The relevant local artifact is:

- [claude_workspace/results/ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)

Key ablation facts on the `erm_cora` checkpoint bank:

- `baseline = 0.8750`
- `uniform = 0.8745`
- `no_cov = 0.8594`
- `contiguous = 0.8613`
- `no_loc = 0.8667`

This implies:

1. final simplex weighting is secondary,
2. complementarity is crucial,
3. noncontiguous checkpoint sets matter,
4. locality matters,
5. a good method must not collapse to one checkpoint.

So a causal proposal that ignores complementarity or soup safety is almost
certainly wrong for this project.

# The gap in the current methods

`D-COLA` is strong because it captures useful complementarity and soup safety.
But it does not explicitly ask the causal question:

> **does there exist one stable predictive mechanism on top of the selected soup
> that remains optimal across the relevant shifts?**

`SCOUT` asks for robust coverage of hard examples, which is principled and
strong. But it is still not explicitly a **mechanism invariance** method.

That is the niche for `CIRCE`.

# CIRCE: the main proposal

## Principle

Treat plausible target shifts as a family of **latent environments** induced by
bounded source-example reweightings. Then choose the soup-safe checkpoint subset
whose uniform soup admits the most **environment-invariant optimal readout**.

This is the direct causal adaptation:

- environments are not observed domains,
- they are the family of admissible reweightings supported by source holdout
  data.

# Formal setup

Let:

- \(\{\theta_t\}_{t\in\mathcal T}\) be dense checkpoints from one training run,
- \(V\) be a labeled pooled source validation split,
- \(U=\{(x_i,y_i)\}_{i=1}^n\) be a labeled pooled source support split,
- \(a\) be the anchor checkpoint minimizing \(L_V\).

Define the soup-safe candidate pool

$$
\mathcal C
=
\left\{
t\in\mathcal T :
L_V(\theta_t)\le L_V^\star + \varepsilon,
\;
B(t,a)\le \tau
\right\}.
$$

For a subset \(S\subseteq\mathcal C\), define the uniform soup

$$
\bar\theta_S
=
\frac1{|S|}\sum_{t\in S}\theta_t.
$$

Let \(\Phi_S(x)\) denote a post-hoc representation derived from the soup. The
simplest default is just the soup logits:

$$
\Phi_S(x) := f(x;\bar\theta_S).
$$

Now define the family of latent environments as the KL-ball of source example
reweightings:

$$
\mathcal R_\rho
=
\left\{
r\in\Delta_n :
\mathrm{KL}\!\left(r \middle\| \tfrac1n\mathbf 1\right)\le \rho
\right\}.
$$

For a simple readout \(w\) acting on \(\Phi_S\), define the reweighted risk

$$
L_r(w,\Phi_S)
:=
\sum_{i=1}^n r_i \,\ell\!\left(w(\Phi_S(x_i)), y_i\right).
$$

# Causal invariance criterion

Adapt IRM directly:

> \(\Phi_S\) is invariant if there exists a single \(w\) that is simultaneously
> optimal for all environments in \(\mathcal R_\rho\).

Formally,

$$
\exists w
\quad\text{s.t.}\quad
w \in \arg\min_{\bar w} L_r(\bar w,\Phi_S)
\;\;\text{for all } r\in\mathcal R_\rho.
$$

Under differentiable convex losses in \(w\), this is equivalent to the
first-order condition

$$
\nabla_w L_r(w,\Phi_S)=0
\qquad \text{for all } r\in\mathcal R_\rho.
$$

This is the exact object `CIRCE` wants to optimize.

# CIRCE objective

The direct constrained formulation is:

$$
\min_{S\subseteq\mathcal C,\; |S|\le K}
\;\inf_w\;
\sup_{r\in\mathcal R_\rho}
L_r(w,\Phi_S)
$$

subject to

$$
\sup_{r,r'\in\mathcal R_\rho}
\left\|
\nabla_w L_r(w,\Phi_S)
- \nabla_w L_{r'}(w,\Phi_S)
\right\|_2^2
\le
\delta.
$$

This says:

- low worst-case predictive risk,
- and near-equality of the optimality conditions across all plausible
  environments.

The penalized Lagrangian form is:

$$
\mathcal J(S,w)
=
\sup_{r\in\mathcal R_\rho} L_r(w,\Phi_S)
+
\lambda_{\mathrm{inv}}
\sup_{r,r'\in\mathcal R_\rho}
\left\|
\nabla_w L_r(w,\Phi_S)
- \nabla_w L_{r'}(w,\Phi_S)
\right\|_2^2
+
\eta |S|.
$$

Then

$$
(S^\star,w^\star)
\in
\arg\min_{S\subseteq\mathcal C,\; |S|\le K,\; w}
\mathcal J(S,w).
$$

# Why this is causal rather than just robust

The difference between `CIRCE` and pure DRO is the second term.

Pure DRO would only solve:

$$
\min_{S,w}\sup_{r\in\mathcal R_\rho} L_r(w,\Phi_S).
$$

That protects against hard reweightings, but it does **not** say the same
decision mechanism is optimal across them.

`CIRCE` instead asks for:

- one shared low-risk readout,
- whose first-order optimality conditions line up across environments.

That is a direct adaptation of the causal invariance idea behind IRM/ICP.

# Why this is not circular

The proposal is not:

- "D-COLA liked some checkpoints, therefore those must be causal."

Instead, the logic is:

1. causal theory says invariant mechanisms matter,
2. invariant mechanisms are characterized by shared optimality across
   environments,
3. without domain labels, we model environments as a principled family of
   bounded reweightings,
4. we directly optimize for low robust loss plus environment-invariant
   optimality of the deployed soup representation.

That is a real theoretical derivation, not a post-hoc patch.

# Why the assumptions are at least defensible

## Assumption A1. The relevant target shifts are source-supported

We assume:

$$
\mathcal E_{\mathrm{target}}
\subseteq
\mathcal R_\rho
$$

in the sense that the unseen target environments can be approximated by bounded
reweightings of source-support examples.

Why this is justified:

- we have no domain labels,
- source-supported reweighting is the cleanest label-free environment family
  available,
- and it is already standard in DRO.

Why this is limited:

- if the target introduces entirely unseen support, the certificate weakens.

## Assumption A2. Soup locality is required

We rely on the same locality condition as `SCOUT` and `D-COLA`:

- the candidate pool must stay inside a soup-safe region.

This is justified by the local DiWA theory:

> "seek a good trade-off between diversity and locality"  
> Source: [theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex)

## Assumption A3. A simple readout class is enough to test mechanism invariance

We should not let \(w\) be arbitrarily expressive, or the invariance test
becomes vacuous. So `CIRCE` should use a restricted readout class:

- scalar temperature,
- diagonal temperature matrix,
- shallow linear readout on logits,
- or a tiny calibrated head.

Why this is principled:

- the soup itself is the representation,
- the readout is only there to test whether one common mechanism suffices across
  shifts.

This also directly addresses the main IRMv1 criticism:

- we do not rely on a dummy linear penalty to stand in for invariance,
- we optimize an explicit cross-environment optimality mismatch for a chosen
  readout class.

# Relationship to SCOUT

`SCOUT` and `CIRCE` are not the same proposal.

`SCOUT` asks:

> which soup-safe subset best covers hard examples under plausible shifts?

`CIRCE` asks:

> which soup-safe subset yields a representation whose optimal decision rule is
> invariant across plausible shifts?

So:

- `SCOUT` is about **coverage and complementarity**,
- `CIRCE` is about **mechanism invariance**.

If we later find that `D-COLA` is winning mostly because of complementarity,
`SCOUT` may still be the stronger branch.
If we find that many `D-COLA` candidates are actually spurious but complementary,
`CIRCE` could be the cleaner next step.

# Relationship to D-COLA

`D-COLA`'s implicit story is:

- pick complementary checkpoints,
- keep them averageable,
- avoid collapsing to one window.

`CIRCE` says that is not enough.

The subset should also satisfy:

> the same readout should remain optimal under all plausible reweighted
> environments.

That is the key additional causal filter.

In practical terms, `CIRCE` would beat `D-COLA` only if:

- some of `D-COLA`'s "useful" complementary checkpoints are actually relying on
  incompatible spurious mechanisms,
- and the invariance constraint removes those while preserving the truly stable
  ones.

# A plausible optimization strategy

I would optimize `CIRCE` with an outer-inner loop:

1. Build \(\mathcal C\) with validation slack and locality filtering.
2. Start from a finite active set of reweightings
   \(\{r^{(1)},\dots,r^{(m)}\}\subset\mathcal R_\rho\).
3. For the current active set, solve
   $$
   \min_{S,w}
   \max_{j\le m} L_{r^{(j)}}(w,\Phi_S)
   +
   \lambda_{\mathrm{inv}}
   \max_{j,k\le m}
   \|\nabla_w L_{r^{(j)}} - \nabla_w L_{r^{(k)}}\|^2
   +
   \eta |S|.
   $$
4. Add the hardest new reweighting by mirror ascent / exponentiated gradient.
5. Repeat until no significantly worse environment is found.

This is still difficult, but at least it optimizes the same thing the method is
supposed to optimize.

# What would make CIRCE convincing experimentally

The key experiments would be:

1. Compare `CIRCE` to `D-COLA`, `SCOUT`, and `SWAD` on the same checkpoint bank.
2. Show the invariance penalty is not just another worst-case risk penalty.
3. Inspect the selected checkpoint subsets and show that `CIRCE` removes
   checkpoints with environment-specific optimal readouts.
4. Plot the gradient mismatch term against OOD accuracy across candidate subsets.

# Main risks

This branch is promising, but it has real risks:

1. **Environment misspecification**
   The KL-ball may not capture the target shifts that matter.

2. **Over-restrictive invariance**
   Some beneficial complementarity may look "non-invariant" even if it helps DG.

3. **Optimization difficulty**
   The exact subset-plus-readout minimax problem is harder than `SCOUT`.

4. **Causal identifiability limits**
   Without real environments or anchors, no method can honestly claim full
   causal recovery.

So this is a real proposal, but it is more assumption-heavy than `SCOUT`.

# My current stance

If the goal is:

- the cleanest overall next method with the strongest immediate empirical odds,

then I still prefer `SCOUT`.

If the goal is:

- a serious causal branch that is genuinely first-principles and not a heuristic
  retrofit,

then `CIRCE` is the best version of that I can currently defend.

It is especially valuable because it says exactly what the causal object is:

> **environment-invariant optimality of the deployed soup representation under a
> principled family of latent environments.**

# Source anchors

## External primary sources

- IRM:
  http://leon.bottou.org/publications/pdf/tr-irm-2019.pdf
- IRM critique:
  https://proceedings.mlr.press/v130/kamath21a.html
- IRM games:
  https://proceedings.mlr.press/v119/ahuja20a.html
- Anchor regression:
  https://people.math.ethz.ch/~peterbu/publications/anchor-JRSSB.pdf
- Causal representation learning from multiple distributions:
  https://proceedings.mlr.press/v235/zhang24br.html
- ICP anchors:
  https://academic.oup.com/jrsssb/article-abstract/78/5/947/7040653
  https://stat.ethz.ch/~nicolai/invariant.pdf

## Local sources

- D-COLA ablations:
  [claude_workspace/results/ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)
- DiWA BVCL decomposition:
  [literature/diwa_tex_source/sections/theory/theory_bvc.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_bvc.tex)
- DiWA locality discussion:
  [literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex)
- SCOUT proposal:
  [claude_workspace/research/scout_submodular_coverage_uniform_trajectory_soups.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/scout_submodular_coverage_uniform_trajectory_soups.md)

# Short exact quotes used above

- IRM:
  "the optimal classifier ... is the same for all environments"
- Kamath et al.:
  "can fail to capture 'natural' invariances"
- Kamath et al.:
  "IRM is extremely fragile to sampling"
- Anchor regression:
  "optimizes worst-case prediction risk over a class of perturbations"
- Anchor regression:
  "improved replicability of variable selection"
- Zhang et al.:
  "without assuming hard interventions behind distribution changes"

All longer mathematical statements in this memo are paraphrased and specialized
to the post-hoc checkpoint-soup setting.
