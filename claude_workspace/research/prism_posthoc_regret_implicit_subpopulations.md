---
title: PRISM: Post-hoc regret on implicit subpopulations for single-run domain generalization
description: Research proposal for PRISM, a theory-first post-hoc DG method that selects actual averageable uniform checkpoint soups by minimizing worst-case regret over hidden source-supported subpopulations, motivated by recent minimax-regret, worst-case-subpopulation, and robust-optimization theory plus local D-COLA ablations.
created: 2026-03-22 18:45
last_modified: 2026-03-22 18:45
last_modified_by: agent
status: active
related_files: claude_workspace/results/results.jsonl, claude_workspace/results/ablation_results_dcola.json, literature/swad_tex_source/5.discussion.tex, literature/diwa_tex_source/sections/theory/theory_bvc.tex, literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex
key_functions: N/A
latest_change: Added a new theory-first method proposal, PRISM, centered on worst-case hidden-subpopulation regret of actual averageable soups rather than surrogate checkpoint scores or predictive-mixture objectives.
change_log:
  - 2026-03-22 18:45: Created the PRISM proposal after a literature pass through minimax regret, worst-case subpopulation robustness, outlier-robust DRO, fairness without demographics, model soups, and the local D-COLA ablations.
---

# Bottom line

After another literature pass and a re-read of our own failures, the strongest
new proposal I can defend is:

- **`PRISM` = `Post-hoc Regret on Implicit Subpopulations of Model soups`**

The central idea is:

> **A good post-hoc DG soup is not the flattest checkpoint, the calmest checkpoint,
> or even the soup with the smallest worst-case raw loss. It is the actual
> averageable soup whose performance has the smallest worst-case regret to the
> best averageable soup on every sufficiently large hidden subpopulation
> supported by the source data.**

This fixes the main conceptual problems we ran into:

- `SWAD` has a real theory about robust risk and flatness, but the deployed
  algorithm is still a heuristic valley finder.
- `SCOUT` tried to be more direct, but the deployed object was still separated
  from the theory by a predictive-mixture bridge.
- `D-COLA` works well, but its objective is still best understood as a strong
  heuristic approximation rather than the exact object we truly care about.

`PRISM` is the first proposal here where the **actual deployed soup** is the
decision variable in the theory.

# Why I think the SCOUT critique is basically right

The critique you gave is directionally correct.

The decisive point is this:

- the `SCOUT` paper talks about a robust objective over a predictive mixture,
- but the deployed object is a single weight-averaged network.

That creates a theory-to-method gap. Our own replay results strongly suggest the
gap is real:

- on the `erm_cora` checkpoint bank, the small-pool degenerate `SCOUT` run that
  effectively reduced to a uniform soup over three candidates reached roughly
  `0.8706` art accuracy;
- when we loosened the pool and allowed the optimizer to genuinely move, the
  score dropped to roughly `0.8477`.

That is exactly the pattern you would expect if:

- the **candidate subset** is the right object,
- but the **continuous weight optimizer** is not.

So the next method should not be another better checkpoint score and not
another better continuous soup weight optimizer. It should directly solve a
robust decision problem over the actual subset soups we are willing to deploy.

# What the local evidence says

The most informative local artifact is:

- [ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)

On the `erm_cora` checkpoint bank, the ablations were:

- `baseline`: `0.8750`
- `uniform`: `0.8745`
- `early`: `0.8687`
- `no_loc`: `0.8667`
- `pooled_anchor`: `0.8638`
- `contiguous`: `0.8613`
- `no_cov`: `0.8594`

The important facts are:

1. **Exact final weights are not the main story.**
   `uniform` is almost tied with `baseline`.

2. **Nonredundant complementarity matters a lot.**
   `no_cov` is the worst ablation.

3. **Noncontiguity matters.**
   `contiguous` is substantially worse than baseline.

4. **Locality matters, but as a feasibility condition.**
   `no_loc` hurts, but less than `no_cov`.

5. **Hard-case protection matters.**
   `pooled_anchor` loses to baseline.

The replay leaderboard in
[results.jsonl](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/results.jsonl)
tells the same story on the same bank:

- `ERM-replay`: `0.7676`
- `SWAD-replay`: `0.8584`
- `STAWA-new`: `0.8643`
- `ROAR`: `0.8633`
- `D-COLA`: `0.8726`

So the empirical object we need to explain is:

> **A small, averageable, noncontiguous, complementary subset of checkpoints,
> typically with nearly uniform weights, beats flat contiguous valleys and
> single-checkpoint selectors.**

That is the fact pattern `PRISM` is designed to explain.

# The literature synthesis that leads to PRISM

## 1. SWAD gave the field a real principle, but not a direct solver

`SWAD` made flat minima central to post-hoc DG, and that mattered. But the
authors are also very explicit about the remaining gap. In their own discussion:

> "SWAD is not a perfect and theoretically guaranteed solver for flat minima, but a heuristic approximation with empirical benefits."  
> Source: [literature/swad_tex_source/5.discussion.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/5.discussion.tex)

So `SWAD` is a proof that a good high-level principle can matter enormously,
but it is also a warning not to confuse a theory about a desirable property with
an exact solver for that property.

## 2. DiWA identified the real structural trade-off

The most important equation in the post-hoc averaging literature for our
purposes is DiWA's bias-variance-covariance-locality decomposition:

$$
\mathbb{E}_{L_S^M}\mathcal{E}_T(\theta_{\text{WA}}(L_S^M))
=
\mathbb{E}_{(x,y)\sim p_T}
\left[
\operatorname{bias}^2(x,y)
\;+\;
\frac{1}{M}\operatorname{var}(x)
\;+\;
\frac{M-1}{M}\operatorname{cov}(x)
\right]
 + O(\Delta^2).
$$

Source:
[theory_bvc.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_bvc.tex)

DiWA then states the design problem plainly:

> "Overall, to reduce WA's error in OOD, we thus seek a good trade-off between diversity and locality."  
> Source: [theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex)

Our ablations line up almost perfectly with that statement:

- covariance reduction matters,
- locality matters,
- and uniform weights are often enough once the subset is right.

So the next theory should treat the **subset selection problem** as primary.

## 3. Minimax regret is a better primitive than worst-case raw risk

The best adjacent result I found is Agarwal and Zhang's MRO paper:

- [Minimax Regret Optimization for Robust Machine Learning under Distribution Shift](https://proceedings.mlr.press/v178/agarwal22b.html)

Their population objective is:

$$
f_{\mathrm{MRO}}
=
\arg\min_{f\in\mathcal F}
\sup_{P\in\mathcal P}
\operatorname{Regret}_P(f),
$$

where

$$
\operatorname{Regret}_P(\hat f)
=
R_P(\hat f) - \inf_{f\in\mathcal F} R_P(f).
$$

They argue explicitly that regret is the right object under heterogeneous shift:

> "We show that the DRO formulation does not guarantee uniformly small regret under distribution shift. We instead propose an alternative method called Minimax Regret Optimization (MRO)."  
> Source: [PMLR abstract](https://proceedings.mlr.press/v178/agarwal22b.html)

And in the paper:

> "Compared to DRO, MRO evaluates the regret of a candidate model f on each distribution P in P as opposed to the raw risk. As we show in the following sections, regret is comparable across distributions in a more robust manner than the risk, since the subtraction of the minimum risk for each distribution takes away the variance due to noise."  
> Source: [agarwal22b.pdf](https://proceedings.mlr.press/v178/agarwal22b/agarwal22b.pdf)

This is exactly the critique we kept running into when trying to optimize
worst-case raw loss over support examples: the adversary starts reacting to
noise, calibration artifacts, or outliers instead of genuine DG structure.

## 4. Hidden-subpopulation robustness is the right uncertainty family

Li, Namkoong, and Xia's NeurIPS paper gives a clean diagnostic notion of
robustness without requiring observed domains:

- [Evaluating model performance under worst-case subpopulations](https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf)

Their key dual formula is:

$$
W_\alpha(h)
:=
\sup_{Q_Z\in\mathcal Q_\alpha}
\mathbb E_{Z\sim Q_Z}[h(Z)]
=
\inf_{\eta\in\mathbb R}
\left\{
\frac{1}{\alpha}\mathbb E_P[(h(Z)-\eta)_+] + \eta
\right\}.
$$

They also make two points that are directly useful for us:

> "The worst-case subpopulation performance (2) automatically accounts for latent intersectionality."  
> Source: [NeurIPS 2021 PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf)

and

> "The threshold α* provides a certificate of robustness on the model θ(·), guaranteeing that all subpopulations larger than α* enjoy good performance."  
> Source: same PDF

This suggests a very natural DG object:

> **the post-hoc soup should remain near-optimal on every sufficiently large
> hidden subpopulation of the source support.**

That is much closer to the real DG goal than "be flat" or "have low churn."

## 5. Robustness without group labels is already a serious theme

The fairness literature reinforces that this is not a contrived move.

Hashimoto et al. explicitly framed robust optimization as protecting minority
groups without group identities:

> "We prove that this approach controls the risk of the minority group at each time step, in the spirit of Rawlsian distributive justice, while remaining oblivious to the identity of the groups."  
> Source: [PMLR abstract](https://proceedings.mlr.press/v80/hashimoto18a.html)

Lahoti et al. push the same direction:

> "How can we train a ML model to improve fairness when we do not even know the protected group memberships?"  
> Source: [NeurIPS 2020 abstract](https://papers.nips.cc/paper/2020/hash/07fc15c9d169ee48573edd749d25945d-Abstract.html)

For us, the analogy is:

- replace "protected groups" with "unseen DG-relevant latent subpopulations,"
- replace "train a model" with "choose one post-hoc soup from a single run."

## 6. DORO tells us how to avoid overreacting to outliers

Zhai et al. found a key failure mode of plain DRO:

> "we observe that DRO performs relatively poorly, and moreover has severe instability... sensitivity of DRO to outliers in the datasets."  
> Source: [DORO PDF](https://proceedings.mlr.press/v139/zhai21a/zhai21a.pdf)

and

> "At the core of this approach is a refined risk function which prevents DRO from overfitting to potential outliers."  
> Source: same PDF

This matters because any hidden-subpopulation regret method that allows an
adversary to concentrate on arbitrary pathological points will be too brittle.
So `PRISM` should include a trimmed or capped adversary, not an unconstrained
one.

# The core theoretical breakthrough

The main conceptual claim is:

> **The right primitive for single-run post-hoc DG is not flatness, stationarity,
> or consensus. It is persistent near-optimality of one averageable soup across
> a family of hidden source-supported subpopulation shifts.**

This is the post-hoc analogue of the "flat minima generalize better" move:

- `SWA/SWAD` said: generalization is about flatness of solutions.
- `PRISM` says: **domain generalization is about persistent near-optimality of
  an actual deployable soup across hidden subpopulation shifts.**

That is a different theoretical center of gravity.

# PRISM: the actual method

## Step 1. Build an averageable candidate pool

Let

- \(\{\theta_t\}_{t\in\mathcal T}\) be dense checkpoints from a single run,
- \(V\) be a labeled source validation split,
- \(U=\{(x_i,y_i)\}_{i=1}^n\) be a labeled source support split.

Choose the anchor

$$
a \in \arg\min_{t\in\mathcal T} L_V(\theta_t).
$$

Define the averageable candidate pool

$$
\mathcal C
=
\left\{
t\in\mathcal T:
L_V(\theta_t)\le L_V^\star + \varepsilon,
\;
B(t,a)\le \tau
\right\},
$$

where \(B(t,a)\) is a barrier / low-loss-connectivity test.

This is not cosmetic. It makes locality a **hard action-space restriction**
rather than an after-the-fact leftover term.

## Step 2. Make the action space the actual soups we can deploy

For a cardinality budget \(M\), define

$$
\mathcal A_M
=
\left\{
S \subseteq \mathcal C :
1 \le |S| \le M
\right\}.
$$

Each action \(S\in\mathcal A_M\) is the uniform soup

$$
\bar\theta_S
=
\frac{1}{|S|}\sum_{t\in S}\theta_t.
$$

This matters a lot:

- the action is the **actual deployed network**,
- not a predictive mixture,
- not a relaxed simplex point,
- and not a checkpoint proxy score.

## Step 3. Define hidden-subpopulation ambiguity directly on the support set

For the support set \(U\), let the per-example soup loss be

$$
\ell_i(S)
:=
\ell\big(f(x_i;\bar\theta_S), y_i\big).
$$

Define the capped adversarial reweighting set

$$
\mathcal Q_\alpha
:=
\left\{
q\in\Delta_n :
q_i \le \frac{1}{\alpha n}
\;\; \forall i
\right\},
$$

where \(\Delta_n\) is the probability simplex.

Interpretation:

- the adversary can choose any hidden subpopulation of effective size at least
  \(\alpha n\),
- without needing observed domain labels.

To reduce sensitivity to outliers, use a trimmed variant \(\mathcal Q_{\alpha,\xi}\)
or the equivalent DORO-style tail-trimmed objective. The exact trimming
parameter is a modeling choice; the main point is that the adversary should not
be allowed to focus on one or two pathological examples.

## Step 4. Optimize worst-case regret, not worst-case raw loss

Define the regret of soup \(S\) under reweighting \(q\) by

$$
\operatorname{Reg}(S;q)
:=
\sum_{i=1}^n q_i \ell_i(S)
-
\min_{S' \in \mathcal A_M}
\sum_{i=1}^n q_i \ell_i(S').
$$

Then the `PRISM` objective is

$$
\operatorname{PRISM}_\alpha(S)
:=
\sup_{q\in\mathcal Q_\alpha}
\operatorname{Reg}(S;q).
$$

The final selection rule is

$$
S^\star
\in
\arg\min_{S\in\mathcal A_M}
\operatorname{PRISM}_\alpha(S).
$$

This is the whole method.

No proxy score. No surrogate checkpoint statistic. No mixture-to-soup bridge.

## Optional robustness certificate

Pick a regret tolerance \(\tau_{\mathrm{reg}}\).
Define the smallest supported subpopulation size for which soup \(S\) is
acceptable:

$$
\alpha^\star_{\tau_{\mathrm{reg}}}(S)
:=
\inf
\left\{
\alpha\in(0,1]:
\operatorname{PRISM}_\alpha(S)\le \tau_{\mathrm{reg}}
\right\}.
$$

Smaller is better:

- if \(\alpha^\star\) is small, the soup stays near-optimal even on small hidden
  subpopulations;
- if \(\alpha^\star\) is large, the soup is brittle.

This gives a post-hoc analogue of a margin or robustness radius.

# Why this directly addresses the SCOUT and SWAD problems

## It fixes the "exact object" issue

`SCOUT` talked about a robust coverage objective, but the theory still had to
pass through a predictive-mixture surrogate. `PRISM` does not.

The theoretical object is:

- the actual averageable soup \(\bar\theta_S\),
- evaluated under actual hidden-subpopulation reweightings,
- with regret computed against the best feasible soup in the same action class.

So when we say we optimize worst-case subgroup regret, we mean exactly that.

## It fixes the leftover-locality issue

In `SCOUT`, locality entered as a residual transfer term outside the main
objective. Here locality is enforced by defining the feasible action class
\(\mathcal A_M\) itself through the barrier filter.

So the theorem can be about the same object the algorithm optimizes:

- actual soups inside the averageable Rashomon face.

## It fits the ablations better than continuous-weight objectives

The ablations say:

- exact weights are secondary,
- subset quality is primary.

`PRISM` makes subset choice primary by construction.

# Why PRISM should recover what D-COLA gets right

`D-COLA` seems to win because it approximates three real constraints:

1. protect hard cases,
2. avoid redundant checkpoints,
3. stay averageable.

`PRISM` explains all three directly:

1. **Hard cases / minority shifts**:
   the adversary \(q\in\mathcal Q_\alpha\) upweights the hardest hidden
   subpopulations.

2. **Complementarity**:
   if two checkpoints help different subpopulations, their uniform soup can have
   much lower worst-case regret than either alone.

3. **Locality**:
   actions outside the low-barrier set are never considered.

So the empirical behavior that made `D-COLA` work appears as a consequence of
the objective, not as a manually assembled bundle of penalties.

# Why I think this can outperform D-COLA

I want to be precise here.

I do **not** know yet that `PRISM` will beat `D-COLA`.
That still needs experiments.

What I do think is true is:

1. `D-COLA` looks like a low-order surrogate for `PRISM`.
2. When the surrogate is well aligned, `D-COLA` should remain strong.
3. When the surrogate is misaligned, `PRISM` has room to win because it solves
   the exact decision problem we actually care about.

The approximation story is:

- `D-COLA`'s covariance term approximates redundancy / overlap of checkpoint
  strengths,
- its barrier term approximates averageability,
- its anchor term approximates hard-case robustness.

`PRISM` removes that decomposition and directly asks:

> which actual soup has the smallest worst-case regret on hidden subpopulations?

That is cleaner and potentially stronger.

# Theorems I think are realistically provable

## Theorem 1. Hidden-subpopulation regret certificate

Assume the target environment corresponds to some
\(q^\star \in \mathcal Q_\alpha\) supported on the source support.
Then for every feasible soup \(S\in\mathcal A_M\),

$$
\operatorname{Regret}_{q^\star}(\bar\theta_S)
\le
\operatorname{PRISM}_\alpha(S).
$$

This is immediate from the definition of the supremum.

What it gives us:

- the optimized objective is an upper bound on target regret for the modeled
  family of hidden-subpopulation shifts,
- and the bound is about the actual deployed soup.

That already makes it more direct than `SCOUT`.

## Theorem 2. Exact finite-action optimization

Because \(\mathcal A_M\) is finite after candidate filtering, the minimax regret
problem is a finite robust decision problem.

In particular, if \(|\mathcal C|\) is modest, we can:

- enumerate all feasible subsets \(S\in\mathcal A_M\),
- compute \(\sup_{q\in\mathcal Q_\alpha}\operatorname{Reg}(S;q)\) for each,
- and pick the minimum exactly.

So unlike many training-time robust methods, the post-hoc regime actually gives
us a chance to solve the decision problem nearly exactly rather than via a loose
proxy.

## Theorem 3. Noncontiguous separation

There exist checkpoint banks and support losses such that:

- every contiguous interval soup in time has worst-case subgroup regret at least
  \(\gamma > 0\),
- but some noncontiguous feasible subset has regret \(0\) (or strictly smaller
  than \(\gamma\)).

The construction is straightforward:

- early checkpoint \(a\) is good on subgroup A and bad on subgroup B,
- mid checkpoint \(b\) is mediocre on both,
- late checkpoint \(c\) is good on subgroup B and bad on subgroup A,
- \(a\) and \(c\) are still averageable,
- uniform soup \(\{a,c\}\) dominates any contiguous interval centered on \(b\).

This theorem would formalize the empirical message from the `contiguous`
ablation.

## Theorem 4. Uniform-subset optimality in symmetric complementary cases

Under a symmetric two-subpopulation complementarity model,
if two or more candidate checkpoints have identical subgroup-specific regrets
up to permutation, then the optimal `PRISM` action is the uniform soup over the
complementary subset.

This theorem would explain why the `uniform` D-COLA ablation was nearly as good
as the full optimizer.

## Theorem 5. D-COLA as a second-order surrogate

Under a local expansion of the weighted subgroup regret around the anchor and
under a linearized soup-loss approximation, the `PRISM` objective reduces to:

- a mean hard-case term,
- plus a pairwise overlap / covariance penalty,
- plus a locality feasibility correction.

That gives a principled explanation for why `D-COLA` is good:

- it is approximating `PRISM`,
- not inventing an arbitrary objective from scratch.

# Why this is more principled than the paths we already tried

## Better than `STAWA`

`STAWA` asked whether a checkpoint is calm.
Our own results showed that calmness is too weak and often collapses to one
checkpoint.

`PRISM` instead asks:

- is the **deployed soup** persistently near-optimal across hidden shifts?

That is a decision-theoretic object, not a scalar trajectory diagnostic.

## Better than `CORA`

`CORA` centered on predictive consensus.
But the ablations strongly suggest that **useful disagreement** matters.

`PRISM` never asks for consensus.
It asks whether one soup remains near-optimal under reweighted subpopulations.
If disagreement is useful, `PRISM` keeps it.

## Better than `SCOUT`

`SCOUT` was the closest step in the right direction, but it still optimized the
wrong relaxed object. `PRISM` keeps the good parts:

- hidden-shift robustness,
- averageable candidate pools,
- post-hoc deployment,

and removes the part that failed:

- the continuous mixture-based optimizer.

# Assumptions and honesty about scope

This is still a conditional theory. The important assumptions are:

## A1. Target shift is source-supported hidden-subpopulation shift

We assume the target can be represented, or at least upper-bounded well, by a
reweighting in \(\mathcal Q_\alpha\) (or its trimmed variant).

This is not "all possible DG shifts."
It is a hidden-subpopulation / support-preserving DG theory.

That is narrower than full DG, but it is honest and testable.

## A2. Averageability is enforced by the barrier filter

We assume the barrier/locality screen is good enough that soups in
\(\mathcal A_M\) remain in one averageable region.

That is the same structural assumption the successful soup literature relies on.
It is still an assumption, but now it is used as a feasibility restriction, not
as a rhetorical afterthought.

## A3. Labeled source holdout data exists

This method is:

- **domain-label-free**,
- not fully label-free.

It uses labels on the pooled source support set to compute losses and regrets.

# Why I think this is the best next method to build

If the question is:

> "What new principle is analogous in spirit to 'flat minima generalize better'?"

then my answer is:

> **Persistent near-optimality across hidden subpopulation shifts is the right
> primitive for post-hoc DG.**

That is the real theoretical leap here.

From that principle, `PRISM` follows naturally:

- averageable checkpoint pool,
- actual subset soups as actions,
- worst-case subgroup regret as objective,
- exact or near-exact post-hoc robust decision over that finite action set.

This is much closer to a theory-first method than what we had before.

# Falsifiable predictions

If `PRISM` is the right theory, then we should see:

1. `PRISM` beat or match `D-COLA` on checkpoint banks where `uniform`
   `D-COLA` already nearly matches full `D-COLA`.

2. `PRISM` beat contiguous-valley methods more strongly on runs with multiple
   complementary training phases.

3. `PRISM` remain stable under moderate changes to \(M\), because the objective
   is about regret over subsets rather than delicate simplex tuning.

4. A trimmed `PRISM` variant outperform plain `PRISM` on noisy or mislabeled
   support sets, consistent with `DORO`.

5. `PRISM` selected soups have lower worst-case subgroup regret than `D-COLA`
   even when their average support loss is similar.

# What I would do next

If we decide this is the main branch, I would implement it in two stages.

## Stage 1. Minimal exact replay version

On an existing dense-checkpoint bank:

1. build the candidate pool with validation slack and barrier filtering;
2. enumerate all subsets up to size \(M\);
3. evaluate exact support losses of each uniform soup;
4. solve the finite robust regret problem;
5. compare against `D-COLA`, `uniform D-COLA`, and `SWAD`.

This is the fastest real test because the action set after filtering is usually
small enough to make enumeration practical.

## Stage 2. Paper-level theorem package

Write down:

1. the hidden-subpopulation regret certificate,
2. the exact finite-action solver or no-regret convergence,
3. the noncontiguous separation theorem,
4. the second-order bridge to `D-COLA`.

# Source list

Core DG / averaging sources:

- SWAD:
  https://openreview.net/forum?id=zkHlu_3sJYU
- DiWA:
  https://arxiv.org/abs/2205.09739
- Model soups:
  https://proceedings.mlr.press/v162/wortsman22a.html

Robustness / regret / subgroup sources:

- Minimax Regret Optimization for Robust Machine Learning under Distribution Shift:
  https://proceedings.mlr.press/v178/agarwal22b.html
- Evaluating model performance under worst-case subpopulations:
  https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf
- Fairness Without Demographics in Repeated Loss Minimization:
  https://proceedings.mlr.press/v80/hashimoto18a.html
- Fairness without Demographics through Adversarially Reweighted Learning:
  https://papers.nips.cc/paper/2020/hash/07fc15c9d169ee48573edd749d25945d-Abstract.html
- DORO: Distributional and Outlier Robust Optimization:
  https://proceedings.mlr.press/v139/zhai21a.html

Local empirical evidence:

- [results.jsonl](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/results.jsonl)
- [ablation_results_dcola.json](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/ablation_results_dcola.json)
