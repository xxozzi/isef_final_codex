---
title: Submodular coverage optimization of uniform trajectory soups for label-free single-run post-hoc domain generalization
description: Research proposal for SCOUT, a theory-first post-hoc DG method that directly optimizes a robust subset-selection objective over soup-safe checkpoints, combining DG bounds, DRO, model soup locality, and submodular diminishing returns.
created: 2026-03-22 14:20
last_modified: 2026-03-22 14:20
last_modified_by: agent
status: active
related_files: claude_workspace/results/ablation_results_dcola.json, literature/swad_tex_source/2.theoretical_analysis.tex, literature/diwa_tex_source/sections/theory/theory_bvc.tex, literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex, claude_workspace/research/cora_consensus_of_rashomon_averaging.md
key_functions: N/A
latest_change: Added a new theory-first proposal, SCOUT, that reframes post-hoc DG as robust submodular subset selection over soup-safe trajectory checkpoints.
change_log:
  - 2026-03-22 14:20: Created the SCOUT proposal after synthesizing D-COLA ablations with SWAD, DiWA, model soups, DRO, and robust submodular selection.
---

# Bottom line

The best new candidate I can defend after combining the literature with the
local replay and ablation results is:

- **`SCOUT` = `Submodular Coverage Optimization of Uniform Trajectory soups`**

The central claim is:

> **Among soup-safe, near-optimal checkpoints from one run, the best post-hoc DG
> model is the uniform soup over the subset that most robustly covers the
> hardest plausible source examples.**

This is the first proposal in this project that I think is simultaneously:

- theory-first rather than heuristic-first,
- domain-label-free,
- single-run and post-hoc,
- architecture-agnostic in principle,
- and directly optimized by the proposed algorithm rather than justified
  after the fact.

# Why a new method is needed

The methods we have tried so far each got something important right, but none
of them fully aligned theory and algorithm:

- `SWAD` has the right DG ambition and a strong flatness story, but its theory
  is about robust empirical loss while its algorithm is a flat-valley
  trajectory heuristic.
- `STAWA` had a clean story about functional stationarity, but the replay
  evidence showed that it mostly collapsed to single-checkpoint selection.
- `CORA` and `ROAR` were more principled than `D-COLA`, but they still lagged
  behind the best replay numbers.
- `D-COLA` is the current empirical champion, but much of its objective is still
  a hand-designed surrogate rather than the direct optimizer of a single clean
  theoretical quantity.

The proposal below is aimed at fixing exactly that mismatch.

# The empirical facts the theory must explain

The most informative artifact right now is:

- [claude_workspace/results/ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)

This file is newline-delimited JSON. On the `erm_cora` checkpoint bank, the
ablations gave:

| Variant | Art full | In | Out |
| --- | ---: | ---: | ---: |
| `baseline` | `0.8750` | `0.8749` | `0.8753` |
| `uniform` | `0.8745` | `0.8743` | `0.8753` |
| `early` | `0.8687` | `0.8688` | `0.8680` |
| `no_loc` | `0.8667` | `0.8664` | `0.8680` |
| `pooled_anchor` | `0.8638` | `0.8646` | `0.8606` |
| `contiguous` | `0.8613` | `0.8646` | `0.8484` |
| `no_cov` | `0.8594` | `0.8603` | `0.8557` |

The main conclusions are:

1. **Exact final weights are not the main story.**
   `uniform` is almost tied with `baseline`.

2. **Complementarity matters a lot.**
   `no_cov` is the worst ablation.

3. **Noncontiguity matters.**
   `contiguous` loses badly.

4. **Locality matters, but less than complementarity.**
   `no_loc` hurts, but not as much as `no_cov`.

5. **Hard-case selection matters.**
   `pooled_anchor` is worse than the baseline anchor rule.

So the next theory should not be about fancy final simplex weights. It should be
about **robust selection of a soup-safe, nonredundant checkpoint subset**.

# Theoretical ingredients that already exist

## 1. SWAD: DG wants a robust loss, not just ordinary validation loss

The local SWAD source says:

> "the test loss ... is bounded by three terms"  
> Source: [literature/swad_tex_source/2.theoretical_analysis.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex)

The robust empirical loss is defined there as

$$
\hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\theta)
:=
\max_{\|\Delta\|\leq\gamma}
\hat{\mathcal{E}}_{\mathcal{D}}(\theta+\Delta).
$$

The local theorem package in
[literature/swad_tex_source/2.theoretical_analysis.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex)
argues that target loss is controlled by:

- a robust empirical term,
- a source-target discrepancy term,
- and a confidence term.

That is the right high-level objective, but `SWAD` then implements a
flat-valley selection heuristic rather than directly minimizing the robust
quantity.

## 2. DiWA: weight averaging succeeds only inside a locality regime

The local DiWA theory gives the key decomposition:

$$
\mathbb{E}_{L_S^M}\mathcal{E}_T(\theta_{\mathrm{WA}}(L_S^M))
=
\mathbb{E}_{(x,y)\sim p_T}
\left[
\mathrm{bias}^2(x,y)
+\frac{1}{M}\mathrm{var}(x)
+\frac{M-1}{M}\mathrm{cov}(x)
\right]
+ O(\Delta^2).
$$

Source:
[literature/diwa_tex_source/sections/theory/theory_bvc.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_bvc.tex)

The same local theory package explicitly states:

> "seek a good trade-off between diversity and locality"  
> Source: [literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex)

This is exactly what the `D-COLA` ablations suggested:

- diversity/complementarity is necessary,
- but averaging only works inside a soup-safe region.

## 3. Model Soups: soup quality tracks ensemble quality inside one basin

Wortsman et al. write:

> "relate the similarity of weight-averaging and logit-ensembling"  
> Source: [Model Soups, abstract](
> https://proceedings.mlr.press/v162/wortsman22a/wortsman22a.pdf)

They analytically connect soup-vs-ensemble similarity to:

- flatness,
- and prediction confidence,

inside a single low-error basin.

This matters because if we can define a good subset objective for the **ensemble**
over selected checkpoints, then soup deployment becomes justified once the
selected subset stays inside an averageable region.

## 4. DRO: domain-label-free robustness can be modeled as example reweighting

Namkoong and Duchi formulate the robust empirical objective

$$
\min_{x\in X}
\sup_{p\in\mathcal{P}_{\rho,n}}
\sum_{i=1}^n p_i \,\ell_i(x),
$$

where

$$
\mathcal{P}_{\rho,n}
=
\left\{
p\in\mathbb{R}^n_+ :
\mathbf{1}^\top p = 1,\;
D_f\!\left(p \middle\| \tfrac{1}{n}\mathbf{1}\right)\le \rho
\right\}.
$$

Source:
[Stochastic Gradient Methods for Distributionally Robust Optimization with f-divergences](
https://proceedings.neurips.cc/paper/2016/file/4588e674d3f0faf985047d4c3f13ed0d-Paper.pdf)

They also show the variance-style expansion

$$
\sup_{p\in\mathcal{P}_{\rho,n}}
\sum_{i=1}^n p_i\ell_i(x)
=
\frac{1}{n}\sum_{i=1}^n \ell_i(x)
+
\sqrt{\frac{\rho}{n}\operatorname{Var}(\ell(x;\xi))}
+
o(n^{-1/2}).
$$

This is important for us because it gives a clean, domain-label-free way to say:

> unseen DG shift is modeled as a bounded adversarial reweighting of source
> support examples.

That is much cleaner than inventing pseudo-domains.

## 5. Submodularity: diminishing returns is the right formal model for nonredundant coverage

Krause et al. write:

> "submodularity, an intuitive diminishing returns property"  
> Source: [Robust Submodular Observation Selection, abstract](
> https://jmlr.csail.mit.edu/papers/v9/krause08b.html)

Nemhauser, Wolsey, and Fisher show that for a normalized monotone submodular
set function \(F\), greedy achieves at least a \(1-1/e\) approximation:

$$
F(A_G)
\geq
\left(1-\frac{1}{e}\right)
\max_{|A|\le K} F(A).
$$

Source:
[An analysis of approximations for maximizing submodular set functions-I](
https://thibaut.horel.org/submodularity/papers/nemhauser1978.pdf)

This is the missing mathematical language for the local ablations:

- if the benefit of adding checkpoints exhibits diminishing returns,
- then the correct object is a submodular subset-selection objective,
- not a hand-designed pairwise covariance penalty.

# The core idea of SCOUT

`SCOUT` says the deployed model should be:

1. a **uniform soup**, not an arbitrary weighted soup,
2. over a **subset** of checkpoints, not necessarily a contiguous window,
3. chosen to **robustly cover hard examples** under adversarial but bounded
   source-support reweightings,
4. while staying inside a **soup-safe candidate pool**.

That aligns exactly with what the ablations imply.

# Formal proposal

## Step 1. Build a soup-safe candidate pool

Let the training run produce dense checkpoints
\(\{\theta_t\}_{t\in\mathcal{T}}\).

Choose an anchor checkpoint

$$
a \in \arg\min_{t\in\mathcal{T}} L_V(\theta_t),
$$

where \(L_V\) is pooled source validation loss on a source holdout \(V\).

Define the candidate pool

$$
\mathcal{C}
=
\left\{
t \in \mathcal{T} :
L_V(\theta_t)\le L_V^\star + \varepsilon,
\;
B(t,a)\le \tau
\right\},
$$

where:

- \(L_V^\star = \min_t L_V(\theta_t)\),
- \(B(t,a)\) is a barrier or interpolation-based soup-safety test,
- \(\varepsilon\) is a validation slack,
- \(\tau\) is a locality threshold.

This is the DiWA/model-soups part of the method.

## Step 2. Define per-example checkpoint competence

Given source holdout support data
\(U=\{(x_i,y_i)\}_{i=1}^n\),
define for each example \(i\) and checkpoint \(t\):

$$
a_{it}
:=
\exp\!\left(-\beta\,\ell\!\left(f_{\theta_t}(x_i), y_i\right)\right),
$$

with \(\beta>0\).

Interpretation:

- high \(a_{it}\) means checkpoint \(t\) handles example \(i\) well,
- low \(a_{it}\) means checkpoint \(t\) handles example \(i\) poorly.

For classification with cross-entropy,

$$
a_{it}
=
\exp\!\left(-\beta \cdot (-\log p_{\theta_t}(y_i\mid x_i))\right)
=
p_{\theta_t}(y_i\mid x_i)^{\beta}.
$$

So competence is just a transformed true-class probability.

## Step 3. Model DG shift as bounded source-example reweighting

Define the adversarial example-weight set

$$
\mathcal{R}_{\rho}
=
\left\{
r\in\Delta_n :
\mathrm{KL}\!\left(r \middle\| \tfrac{1}{n}\mathbf{1}\right)\le \rho
\right\}.
$$

This is the label-free DRO assumption:

- the target is not required to equal a source domain,
- it only needs to be approximable by a bounded reweighting of observed source
  support examples.

## Step 4. Select a fixed-size subset by robust concave coverage

For a checkpoint subset \(S\subseteq\mathcal{C}\) with \(|S|\le K\), define

$$
F_r(S)
:=
\sum_{i=1}^n r_i
\log\!\left(
\epsilon_0 + \sum_{t\in S} a_{it}
\right),
$$

for a tiny \(\epsilon_0>0\).

Then define the robust subset problem

$$
S^\star
\in
\arg\max_{S\subseteq \mathcal{C},\; |S|\le K}
\min_{r\in\mathcal{R}_{\rho}}
F_r(S).
$$

Equivalent minimization form:

$$
\Psi_\rho(S)
:=
\sup_{r\in\mathcal{R}_{\rho}}
\sum_{i=1}^n r_i
\left[
-\log\!\left(
\epsilon_0 + \sum_{t\in S} a_{it}
\right)
\right].
$$

The deployed model is the **uniform soup**

$$
\bar{\theta}_S
=
\frac{1}{|S|}\sum_{t\in S}\theta_t.
$$

# Why this is theoretically clean

## Proposition 1. For fixed \(r\), \(F_r\) is monotone submodular

For each example \(i\), the map

$$
S \mapsto \log\!\left(\epsilon_0 + \sum_{t\in S} a_{it}\right)
$$

is a concave function of a modular sum. Concave-over-modular set functions are
submodular; see Ahmed and Atamturk's discussion of
\(h(S)=f(\sum_{i\in S} a_i)\) with strictly concave increasing \(f\).
Since \(r_i\ge 0\), the weighted sum

$$
F_r(S)=\sum_i r_i \log\!\left(\epsilon_0 + \sum_{t\in S} a_{it}\right)
$$

is also monotone submodular.

This gives a direct formalization of **nonredundant complementarity**:

- adding a checkpoint that helps examples already covered yields small gain,
- adding a checkpoint that covers currently hard examples yields large gain.

That is exactly what the `no_cov` ablation was trying to tell us.

## Corollary 1. Greedy best response is approximation-certified

For fixed \(r\), greedy subset selection under \(|S|\le K\) satisfies

$$
F_r(S_{\mathrm{greedy}})
\ge
\left(1-\frac{1}{e}\right)
\max_{|S|\le K} F_r(S).
$$

So the selector is not arbitrary. It is directly optimizing a robust coverage
objective with the standard submodular guarantee.

## Proposition 2. Uniform soups are the right deployment object here

The local ablation result

$$
\texttt{baseline} = 0.8750,
\qquad
\texttt{uniform} = 0.8745
$$

shows that, on the key replay bank, **subset quality dominates exact final
weight optimization**.

That empirical fact is important because it lets the method stay theory-clean:

- the optimization variable is a subset \(S\),
- the deployment rule is the exact same uniform soup the theory is about.

We do not need a separate post-hoc weight optimizer to patch the method.

## Proposition 3. The locality gate justifies soup deployment

The DiWA BVCL decomposition gives

$$
\mathcal{E}_T(\theta_{\mathrm{WA}})
=
\mathcal{E}_T(f_{\mathrm{ENS}})
+ O(\Delta^2)
$$

up to the bias-variance-covariance terms and a locality remainder. So once
\(\mathcal{C}\) is constructed to be soup-safe, optimizing the ensemble-style
coverage utility over \(S\) is meaningful for the final soup as well.

This is precisely the role of the barrier/locality filter:

- not to define the whole objective,
- but to make the selected subset safe for weight averaging.

# Why SCOUT is less circular than the earlier ideas

The method-theory mapping is now direct:

1. **Theory object:** robust risk over example reweightings.
2. **Combinatorial structure:** diminishing returns over checkpoint coverage.
3. **Deployment constraint:** locality/averageability.
4. **Algorithm:** adversary updates \(r\), selector greedily maximizes the
   exact robust set utility, deployed model is the resulting uniform soup.

So unlike `SWAD`, the story is not:

- theorem about robust risk,
- heuristic about flatness valleys.

And unlike `D-COLA`, the story is not:

- empirically useful covariance/locality heuristics,
- with theory added later.

Instead, `SCOUT` starts from the robust objective and derives the selector from
it.

# Why I think SCOUT has a real chance against D-COLA

`D-COLA` currently wins because it captures:

- hard-case robustness,
- useful complementarity,
- and soup safety.

`SCOUT` keeps all three, but puts them on a cleaner footing:

- hard-case robustness comes from KL-DRO over examples,
- complementarity comes from submodular diminishing returns,
- soup safety comes from the candidate-pool locality gate,
- and exact final weights are removed because the ablations suggest they are
  not the main source of gain.

This gives two concrete advantages:

1. It should be **more stable** than weight-heavy methods because the deployed
   soup is uniform over a selected subset.
2. It should be **more interpretable** than `D-COLA` because every selected
   checkpoint has a marginal coverage contribution.

I cannot honestly claim this guarantees superiority to `D-COLA`. What I can say
is that this is the first proposal whose theoretical target matches the
empirical mechanism the ablations exposed.

# Assumptions and why they are justified

## Assumption A1. Target shift is approximable by bounded reweighting of source support

Formal assumption:

$$
p_T
\ll
p_U
\quad\text{and}\quad
\mathrm{KL}(p_T \,\|\, p_U)\le \rho.
$$

Why this is justified:

- we do not have domain labels,
- the user requirement is architecture- and task-agnostic post-hoc DG,
- example-level DRO is the cleanest label-free uncertainty model available in
  the cited literature.

What this does **not** claim:

- it does not claim arbitrary target domains are always representable this way,
- only that this is the modeling assumption under which the certificate is
  meaningful.

## Assumption A2. Soup deployment is only valid inside a locality regime

Why this is justified:

- DiWA explicitly shows the locality remainder term,
- model soups only work reliably inside one basin,
- and your `no_loc` ablation dropped performance.

So locality should be treated as a hard feasibility condition, not a decorative
regularizer.

## Assumption A3. Fixed-cardinality uniform soups are enough

Why this is justified:

- `uniform` nearly matched `baseline` in the local D-COLA ablations,
- which means subset identity is more important than final fine-grained weights.

This assumption is therefore not arbitrary. It is directly supported by the
observed replay evidence.

# Concrete algorithm

Let `SCOUT` use the following loop:

1. Build \(\mathcal{C}\) from validation slack and locality/barrier filtering.
2. Precompute \(a_{it}\) for \(i\in U\), \(t\in\mathcal{C}\).
3. Initialize \(r^{(0)} = \tfrac{1}{n}\mathbf{1}\).
4. For rounds \(m=0,\dots,M-1\):
   - approximately solve
     $$
     S^{(m)} \approx \arg\max_{|S|\le K} F_{r^{(m)}}(S)
     $$
     by greedy selection,
   - update \(r\) by exponentiated ascent on the current robust losses,
     projected back to \(\mathcal{R}_\rho\).
5. Output the best or averaged subset from the outer loop.
6. Deploy the uniform soup over the chosen subset and refresh BN statistics.

The important thing is that the algorithm is optimizing the same robust
coverage objective the theory is built around.

# Falsifiable predictions

If `SCOUT` is the right idea, the following should happen:

1. It should beat or match `D-COLA` with **uniform soup deployment** on the same
   candidate pool size.
2. Its selected subsets should remain **noncontiguous** in time.
3. Removing the DRO adversary should hurt more than changing the final soup
   weighting rule.
4. The selected checkpoints should have high marginal gains on different hard
   examples, not merely low pairwise distance.
5. On the `erm_cora` replay bank, it should outperform:
   - `STAWA-old`,
   - `STAWA-new`,
   - and likely `SWAD`,
   while being competitive with `D-COLA`.

# What could still go wrong

There are real risks:

- If the KL-ball is too coarse, `SCOUT` may over-focus on examples that do not
  represent true DG shift.
- If the locality gate is too strict, it may collapse back into a contiguous
  valley method.
- If the candidate pool is too broad, soup deployment may fail even though the
  subset objective looks good at the ensemble level.
- If the robust adversary mostly recovers already-known hard examples, it may
  add little beyond a well-designed `D-COLA` anchor.

So this is not a guaranteed breakthrough. It is a well-motivated next method.

# Why this is currently my main recommendation

The best summary is:

- `D-COLA` discovered the right empirical behavior.
- The ablations show that the key behavior is **subset complementarity under
  locality**, not intricate weighting.
- `SCOUT` is the cleanest theory-first method I can currently write down that
  optimizes exactly that object.

If the goal is a method that is:

- well motivated,
- non-circular,
- label-free,
- post-hoc,
- and still plausibly strong enough to challenge `D-COLA`,

then `SCOUT` is the best next proposal I have.

# Source anchors

## Local sources

- SWAD theory:
  [literature/swad_tex_source/2.theoretical_analysis.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex)
- DiWA BVCL decomposition:
  [literature/diwa_tex_source/sections/theory/theory_bvc.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_bvc.tex)
- DiWA locality discussion:
  [literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex)
- Local D-COLA ablations:
  [claude_workspace/results/ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)
- Local D-COLA draft:
  [claude_workspace/papers/d_cola/d_cola_neurips.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/d_cola/d_cola_neurips.tex)

## External primary sources

- Model soups:
  https://proceedings.mlr.press/v162/wortsman22a.html
- DRO with \(f\)-divergences:
  https://proceedings.neurips.cc/paper/2016/file/4588e674d3f0faf985047d4c3f13ed0d-Paper.pdf
- Robust submodular observation selection:
  https://jmlr.csail.mit.edu/papers/v9/krause08b.html
- Nemhauser-Wolsey-Fisher greedy guarantee:
  https://thibaut.horel.org/submodularity/papers/nemhauser1978.pdf
- Concave-over-modular submodular structure:
  https://link.springer.com/article/10.1007/s10107-009-0298-1
- Predictive churn and Rashomon-set motivation:
  https://arxiv.org/abs/2402.07745

# Short exact quotes used above

- SWAD local source:
  "the test loss ... is bounded by three terms"
- DiWA local source:
  "seek a good trade-off between diversity and locality"
- Model soups:
  "relate the similarity of weight-averaging and logit-ensembling"
- RSOS:
  "submodularity, an intuitive diminishing returns property"

All longer mathematical content in this memo is either reproduced as equations
or paraphrased from the cited sources.
