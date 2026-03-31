---
title: Occam-PRISM: A Theory-First Upgrade of PRISM via Deterministic Structural Risk Minimization, with Held-Out-Prior PAC-Bayes as an Optional Phase-2 Refinement
description: Detailed research proposal for an improved PRISM method that replaces manual candidate-family tuning with a finite-family deterministic SRM/Occam selector over deployable soup families, while preserving PRISM's domain-label-free hidden-subpopulation regret core.
created: 2026-03-31 10:20
last_modified: 2026-03-31 10:58
last_modified_by: agent
status: draft
related_files:
  - claude_workspace/papers/prism_neurips/main.tex
  - claude_workspace/results/prism_results_ledger.md
  - claude_workspace/research/srm_prism_bound_minimizing_updates.md
  - claude_workspace/research/stable_pool_prism.md
key_functions:
  - Diagnose the real limitations of current PRISM without overstating them
  - Propose a theory-first improved PRISM method with explicit finite-family complexity control
  - Separate established facts from target theorem forms and conjectures
  - Provide a concrete replay-first implementation and evaluation plan
latest_change: Clarified that alpha is an exogenous robustness target, defined the global validation anchor and admissible tractable family set, replaced the lambda_occam surrogate with the canonical bound-shaped score, and simplified the high-school explanation so PAC-Bayes remains clearly optional.
change_log:
  - 2026-03-31 10:20: Initial draft
  - 2026-03-31 08:36: Revised after strict multi-agent review; fixed the formal objective indexing, changed the main branch to deterministic SRM/Occam-PRISM, and tightened the complexity story
  - 2026-03-31 10:58: Revised after second strict review; fixed alpha framing, anchor notation, tractability definition, and implementation-score consistency
---

# Executive Summary

This memo proposes a new mainline PRISM update:

> **Occam-PRISM**: keep PRISM's domain-label-free hidden-subpopulation regret objective on actual deployable soups, but replace manual candidate-family tuning with a finite-family deterministic structural-risk-minimization selector. A held-out-prior PAC-Bayes refinement is kept as an optional phase-2 extension rather than the core main branch.

The proposal is deliberately narrow.

- It **does not** claim that candidate-family choice is the dominant empirical bottleneck in current PRISM.
- It **does** claim that candidate-family choice is the clearest remaining **theory gap** in current PRISM.
- It **does** give a concrete upgraded method whose selection rule is much more first-principles than the current manual search over family knobs $(\varepsilon,\tau,M)$ at fixed robustness target $\alpha$.

The core recommendation is:

1. Keep PRISM's hidden-subpopulation regret primitive.
2. Keep deployment alignment: the scored object must still be the actual deployed soup.
3. Make family choice itself part of the method through a complexity-controlled deterministic selector over finite deployable soup families.
4. Treat bootstrap stability only as a diagnostic, not as the central theorem-bearing mechanism.

The reason for this proposal is simple. Current PRISM is only partly theorem-governed. The current paper is explicit that the key consistency theorem is only **“conditional on a fixed candidate family”** and that the barrier screen is **“an anchor-based locality heuristic rather than a certificate”** in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L457) and [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L682). Occam-PRISM is designed to close that gap without giving up domain-label freedom or exact soup deployment.

# 1. What Is Wrong with Current PRISM

## 1.1 The empirical situation is promising but not decisive

On the clean four-split PACS replay sweep, the current domain-label-free comparison is:

| Split | ERM | SWAD | PRISM |
|---|---:|---:|---:|
| art_painting | 82.08 | 87.60 | 87.26 |
| cartoon | 81.57 | 82.38 | 81.57 |
| photo | 94.55 | 97.07 | 97.54 |
| sketch | 78.32 | 81.73 | 83.53 |
| average | 84.13 | 87.19 | 87.47 |

from [prism_results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/prism_results_ledger.md#L38).

So current PRISM is real, but the average gain over replayed SWAD is only `+0.28`, and the wins are split-dependent rather than broad.

On the fresh canonical seed-1 bank, the comparison is:

| Method | Art full | In | Out |
|---|---:|---:|---:|
| ERM | 0.8066 | 0.8096 | 0.7946 |
| SWAD | 0.8794 | 0.8786 | 0.8826 |
| PRISM | 0.8862 | 0.8883 | 0.8778 |

from [prism_results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/prism_results_ledger.md#L55).

That tells us:

- PRISM is competitive and nontrivial.
- PRISM is not yet a broad empirical replacement for SWAD.
- The remaining gap is small enough that overinterpreting one tuned run would be a mistake.

## 1.2 The cross-pool ablation does **not** support a “pool-only” diagnosis

The clean cross-pool result is:

| Variant | Runner | Pool | Art full | In | Out |
|---|---|---|---:|---:|---:|
| baseline_dcola | D-COLA | D-COLA | 0.8901 | 0.8908 | 0.8875 |
| dcola_on_prism_pool | D-COLA | PRISM | 0.8877 | — | — |
| baseline_prism | PRISM | PRISM | 0.8833 | 0.8853 | 0.8753 |
| prism_on_dcola_pool | PRISM | D-COLA | 0.8672 | 0.8676 | 0.8655 |

from [prism_results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/prism_results_ledger.md#L70).

The asymmetry matters:

- D-COLA stays strong on the PRISM pool.
- PRISM drops much more on the D-COLA pool.

The cleanest empirical reading is therefore:

> current PRISM likely has an **objective-level limitation**, not just a candidate-pool limitation.

That point is crucial because it tells us what this proposal **is not** claiming.

Occam-PRISM is **not** being proposed because the evidence proves that pool choice is the main empirical bottleneck.
It is being proposed because candidate-family choice is the largest place where current PRISM still falls back to manual tuning rather than theorem-governed selection.

## 1.3 The current theorem story is only half complete

Current PRISM already gets one important thing right: the selector scores the actual deployable soup actions.

The abstract in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L79) explicitly presents PRISM as a method whose decision variable is the averaged-state soup scored by the second stage. The paper repeatedly emphasizes exact alignment between the scored action and the deployed object.

That is the strong part.

The weak part is that the theory only governs the second stage after the candidate family is already fixed.

The current paper says:

> “Consistency of the second-stage selector conditional on a fixed candidate family”

in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L457).

And the discussion says:

> “The barrier screen is likewise an explicit modeling choice; it is an anchor-based locality heuristic rather than a certificate”

in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L682).

So current PRISM is already theory-controlled **at the second stage inside one fixed family**, but the outer family choice is not part of the theorem.

That is the exact gap Occam-PRISM is meant to repair.

# 2. Design Requirements for the Improved Method

The subagent reviews on earlier proposals converged on four constraints that the next PRISM branch must respect.

## 2.1 Preserve deployment alignment

The selector must still optimize the kind of object it deploys:

- actual soups,
- over an explicit deployable action family,
- not a proxy objective defined on some unrelated front-end screening statistic.

This is PRISM’s strongest current principle. We should not lose it.

## 2.2 Preserve domain-label freedom

The method must stay domain-label-free:

- pooled source holdout only,
- no source-domain identities,
- no importing D-COLA’s domainwise covariance term literally.

Any improvement that quietly uses source-domain partitions is not an improved PRISM. It is a different method class.

## 2.3 Repair the theory at the family-selection level

The next theory-first step must address the actual unresolved object:

- not just the score of a soup **within** a fixed family,
- but the choice **among** families defined by $(\varepsilon,\tau,M)$ and optionally $\alpha$.

## 2.4 Avoid fake “first-principles” moves

Earlier proposals failed because they mixed real theorems with unjustified bridges:

- bootstrap variance masquerading as uniform stability,
- VC-dimension claims on the wrong object,
- domain-labeled covariance imported into a domain-label-free method,
- closed-form $\alpha^\star$ formulas with no theorem behind them.

This memo avoids those moves explicitly.

# 3. Literature Anchors

This section records only the literature that genuinely supports the proposed direction.

## 3.1 Complexity-regularized model selection is the right high-level principle

Bartlett and Mendelson write that model-selection bounds “take the form of a sum of two terms: some sample-based estimate of performance and a penalty term that is large for more complex models” in [JMLR 2002](https://www.jmlr.org/papers/volume3/bartlett02a/bartlett02a.pdf), lines 22–24.

That is exactly the design pattern we want:

- empirical PRISM regret,
- plus a principled complexity penalty on the searched family.

Mohri’s lecture notes on finite hypothesis classes make the same Occam point explicitly:

> “for a finite hypothesis set, whp” the risk is empirical risk plus a `log |H|` complexity term,

and then interpret `log2 |H|` as the number of bits needed to encode the hypothesis in [lecture notes PDF](https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf), lines 389–439.

This is the cleanest off-the-shelf theory language for PRISM because, conditional on validation data, PRISM’s action family is finite.

## 3.2 Held-out-data PAC-Bayes supports an optional second-stage refinement

Dziugaite et al. show that held-out-data priors are not just heuristics. Their abstract says:

> “a stronger bound is obtained by using a data-dependent oracle prior, i.e., a conditional expectation of the posterior, given a subset of the training data that is then excluded from the empirical risk term”

and

> “using data can mean the difference between vacuous and nonvacuous bounds”

in [On the role of data in PAC-Bayes bounds](https://arxiv.org/abs/2006.10929), lines 42–44.

That directly supports the general pattern of:

- using the validation split to define a prior or family,
- and using the support split to evaluate empirical regret.

This is the right way to keep data dependence legal. It does **not** by itself prove the full Occam-PRISM regret selector. It only supports the held-out-prior construction pattern.

## 3.3 PAC-Bayes over finite classifier sets is conceptually relevant

Sahu and Hemachandra’s abstract says:

> “PAC-Bayesian set up involves a stochastic classifier characterized by a posterior distribution on a classifier set”

and

> “We consider a finite classifier set”

with a trade-off between empirical risk and KL-based model complexity in [PMLR 2019](https://proceedings.mlr.press/v101/sahu19a.html).

That does not prove Occam-PRISM directly, but it strongly supports the right formal object:

- a finite family of actions,
- a prior over that family,
- and a risk-plus-KL selection rule.

## 3.4 Why not stability as the main theorem story?

Bousquet and Elisseeff absolutely do support stability as a route to generalization:

> they “define notions of stability” and “derive generalization error bounds”

in [JMLR 2002](https://www.jmlr.org/papers/v2/bousquet02a.html).

But those results are about **uniform stability of a learning algorithm**, not bootstrap standard deviation of PRISM regret under support resampling. Stability can still be useful as a diagnostic, but not as the central theorem-bearing repair unless we do substantially more work.

That is why this proposal does **not** make bootstrap stability the main method.

# 4. The Proposed Method: Deterministic Occam-PRISM

## 4.1 Core idea

Occam-PRISM upgrades PRISM by moving candidate-family choice into the selector itself.

Instead of:

1. pick one family manually by tuning family knobs $(\varepsilon,\tau,M)$, and in practice also choosing $\alpha$ outside the theorem-governed family selector,
2. run PRISM inside that family,

Occam-PRISM does:

1. define a finite collection of candidate families,
2. score all deployable soup actions across all families,
3. choose the action-family pair that minimizes empirical PRISM regret plus an explicit complexity penalty.

The deployed object is still a **single actual soup**.

## 4.2 Data split

We keep the same basic split logic:

- $\mathcal V$:
  validation split, used only to define families and optional priors
- $\mathcal U = \{Z_i\}_{i=1}^n$:
  support split, used only to compute empirical regret scores

This separation is essential.

It means that once we condition on $\mathcal V$, the searched family is a fixed finite object from the perspective of the support sample.

## 4.3 Family index

For the main method, we fix $\alpha$ and let the family index be

$$
\gamma = (\varepsilon,\tau,M)\in\Gamma.
$$

This is deliberate.

- $\alpha$ changes the robustness target itself.
- $\varepsilon,\tau,M$ change the searched deployable family at fixed robustness target.
- In the mainline method, $\alpha$ is therefore treated as an **exogenous scientific choice** about what subgroup mass we want to protect, not as an inner search variable. If we later want to search across a small grid of $\alpha$ values, that should be added as a separate outer union-bound extension rather than silently folded into the core selector.

We also make the anchor explicit. Let

$$
a(\mathcal V)\in \arg\min_t L_{\mathcal V}(\theta_t)
$$

be the single validation-best checkpoint. The barrier score $B(t,a(\mathcal V))$ is always computed relative to this fixed validation-defined anchor. In this proposal, the anchor is **global and family-independent**. A family-dependent anchor would change the admissible family itself and should be treated as a different method.

Finally, we make tractability part of the method rather than an afterthought. Let $K_{\max}$ be a fixed global exact-search budget and define the admissible family index set

$$
\Gamma_{\mathrm{adm}}(\mathcal V)
=
\left\{
\gamma\in\Gamma:
|\mathcal A_\gamma(\mathcal V)| \le K_{\max}
\right\}.
$$

Only families in $\Gamma_{\mathrm{adm}}(\mathcal V)$ are searched. This is not a learned hyperparameter. It is a predeclared computational constraint that keeps the method in the exact finite-family regime it is designed to analyze.

For each $\gamma$, the validation split defines:

1. the checkpoint candidate pool
   $$
   \mathcal C_\gamma(\mathcal V)
   =
   \left\{
   t :
   L_{\mathcal V}(\theta_t)\le L_{\mathcal V}^\star+\varepsilon,
   \;
   B(t,a(\mathcal V))\le \tau
   \right\},
   $$
2. the deployable soup action family
   $$
   \mathcal A_\gamma(\mathcal V)
   =
   \left\{
   S\subseteq \mathcal C_\gamma(\mathcal V) :
   1\le |S|\le M
   \right\}.
   $$

This keeps the PRISM action class exactly where it belongs: on real soups.

## 4.4 Inner score: keep PRISM’s empirical regret, but index it by family

Throughout the algorithmic selector definition, we use a bounded support-loss surrogate satisfying

$$
0 \le \ell_i(S) \le 1,
$$

obtained by a fixed clipping-and-rescaling rule declared once globally before the experiments. This keeps the deterministic Occam penalty parameter-free at the method level. The proof section is still allowed to carry universal constants, but the deployed selector itself should not introduce an extra penalty-scale hyperparameter.

For every $S\in\mathcal A_\gamma(\mathcal V)$, define the family-indexed empirical hidden-subpopulation regret on the support split:

$$
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U)
=
\sup_{q\in\mathcal Q_\alpha^n}
\left[
\sum_{i=1}^n q_i \ell_i(S)
-
\min_{S'\in \mathcal A_\gamma(\mathcal V)}
\sum_{i=1}^n q_i \ell_i(S')
\right].
$$

This is still PRISM’s core regret idea, but written correctly for the multi-family setting. The same soup can receive different regret values in different families because the witness class changes with $\gamma$.

## 4.5 Outer score: explicit complexity penalty

The main deterministic selector is:

$$
(\widehat{\gamma},\widehat{S})
\in
\arg\min_{\gamma\in\Gamma_{\mathrm{adm}}(\mathcal V),\; S\in\mathcal A_\gamma(\mathcal V)}
\left\{
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U)

+\;
\sqrt{
\frac{
\log \frac{1}{\pi_\Gamma(\gamma)}
\;+\;
\;2\log |\mathcal A_\gamma(\mathcal V)|
\;+\;
\log \frac{1}{\delta}
}{
n
}
}
\right\}.
$$

This is the core deterministic Occam-PRISM rule.

Interpretation:

- the first term is empirical PRISM regret,
- the second term is a family/witness complexity cost,
- $\pi_\Gamma$ is a prior over family indices.

The simplest family prior is:

$$
\pi_\Gamma(\gamma)=\frac{1}{|\Gamma|},
$$

Then the score reduces to:

$$
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U)
\;+\;
\sqrt{
\frac{
\log |\Gamma|
\;+\;
2\log |\mathcal A_\gamma(\mathcal V)|
\;+\;
\log \frac{1}{\delta}
}{
n
}
}.
$$

Why the factor of `2`? Because PRISM’s score for one action is defined by comparison to witnesses inside the same family. The relevant finite object for concentration is the ordered-pair witness class, whose cardinality is at most $|\mathcal A_\gamma(\mathcal V)|^2$.

That is the clean deterministic SRM/Occam version.

### Why this is the right complexity term

Because $\mathcal A_\gamma(\mathcal V)$ is finite, the right primitive is **log cardinality of the searched pairwise witness class**, not the VC dimension of some unrelated subset-indicator class.

This avoids one of the main mathematical problems in the stable-pool memo.

## 4.6 Optional phase-2 held-out-prior PAC-Bayes refinement

The previous score is the main branch. The PAC-Bayes extension is intentionally optional and should not be treated as the core method until a regret-level derivation is written.

The proposed PAC-Bayes refinement is to let the within-family prior depend on validation data only:

$$
\pi_{\gamma,\mathcal V}(S)
\propto
\exp\!\big(
-\beta \,\widetilde{L}_{\mathcal V}(S)
\big),
$$

where $\widetilde{L}_{\mathcal V}(S)$ is a validation-only score, for example:

- validation loss of the scored soup,
- or validation loss plus a validation-only locality term.

Because $\mathcal V$ is excluded from the support empirical regret term, this is compatible with the held-out-data prior pattern studied by Dziugaite et al. It should be understood as a plausible extension, not as something already justified for PRISM’s exact regret functional.

This gives a more informative prior than uniform counting, but it does **not** break deployment alignment:

- the posterior can still be a point mass on one action,
- so the deployed object is still a single actual soup.

## 4.7 Optional multi-$\alpha$ extension

If we eventually want to select $\alpha$ inside the method instead of outside it, the clean way is not to pretend $\alpha$ is a nuisance parameter.

Instead define a finite robustness-target grid $\mathcal A$ and enlarge the outer index:

$$
\omega = (\alpha,\gamma,S).
$$

Then Occam-PRISM chooses:

$$
\widehat{\omega}
\in
\arg\min_{\alpha\in\mathcal A,\;\gamma\in\Gamma,\;S\in\mathcal A_\gamma(\mathcal V)}
\left\{
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U)
\;+\;
\text{complexity penalty including } -\log \pi_\alpha(\alpha)
\right\}.
$$

This is valid, but conceptually different.

Choosing among $\alpha$ values is choosing among robustness targets, not just tuning a front-end family parameter.

For that reason, the main proposal keeps $\alpha$ fixed and treats multi-$\alpha$ selection as a second-stage extension.

# 5. Why This Direction Avoids the Earlier Problems

## 5.1 It does not misread the cross-pool result

This proposal does **not** claim that candidate-pool repair is the main empirical bottleneck.

Instead it says:

- the current evidence still points more strongly to an objective limitation,
- but candidate-family choice is the clearest remaining **theory** gap,
- and Occam-PRISM is the cleanest theory-first repair of that gap.

That is a narrower and defensible claim.

## 5.2 It does not pretend bootstrap variance is a theorem

Bootstrap stability is not a core term in the method.

If used at all, it appears only as:

- a diagnostic,
- or a secondary empirical ablation.

This avoids falsely presenting a resampling heuristic as uniform-stability theory.

## 5.3 It does not use the wrong complexity notion

The proposal uses:

- finite family size,
- prior mass,
- and held-out-data PAC-Bayes ideas.

It does **not** rely on the incorrect “VC dimension of subset soups” argument that earlier proposals used.

## 5.4 It preserves domain-label freedom

No source-domain labels are used anywhere in the main method.

That means:

- no domainwise covariance matrices,
- no source-domain validation partitions,
- no D-COLA-style explicit domain supervision.

## 5.5 It preserves deployment alignment

The searched object is still:

- a concrete soup action $S$,
- from a concrete deployable family $\mathcal A_\gamma(\mathcal V)$.

This is exactly the principle the current PRISM paper wanted to preserve.

# 6. Theory Status: Established, Target, Conjectural

This section is intentionally explicit so we do not repeat the earlier proposal failures.

## 6.1 Established facts we can rely on now

### Established fact A: current PRISM already gives asymptotic consistency conditional on a fixed family

This is already in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L457).

So once the family is fixed independently of the support split, the second-stage selector is already on solid ground.

### Established fact B: finite-family concentration supports an Occam penalty

For finite hypothesis sets, standard uniform convergence gives a `log |H|` penalty.

Mohri’s finite-class notes make this explicit in [lecture notes PDF](https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf), lines 389–439.

That is the direct reason to use:

- $\log |\mathcal A_\gamma(\mathcal V)|$,
- or more generally a prior-mass penalty on the searched family object,

as the basic complexity object.

### Established fact C: held-out-data PAC-Bayes priors are legitimate

Dziugaite et al. explicitly support using one part of the data to define a prior that is then excluded from the empirical risk term:

> “given a subset of the training data that is then excluded from the empirical risk term”

in [arXiv 2020](https://arxiv.org/abs/2006.10929), lines 42–44.

This is why using $\mathcal V$ to define the prior and $\mathcal U$ to define empirical regret is a theoretically natural next route. It should be read as support for the split pattern, not as a proof of the full selector.

## 6.2 Target theorem forms for Occam-PRISM

These are **not** claimed as already proved in the repo today. They are the theorem targets the improved method is designed around.

### Target Theorem 1: conditional finite-sample uniform deviation over the validation-defined pairwise witness union

Condition on $\mathcal V$.
Then the relevant finite object is

$$
\Omega_{\mathrm{pair}}(\mathcal V)
=
\bigcup_{\gamma\in\Gamma_{\mathrm{adm}}(\mathcal V)}
\left\{
\left(\gamma,S,S'\right) : S,S'\in\mathcal A_\gamma(\mathcal V)
\right\}
$$

which is finite.

The target theorem form is:

$$
 \sup_{\gamma\in\Gamma_{\mathrm{adm}}(\mathcal V),\;S\in\mathcal A_\gamma(\mathcal V)}
\left|
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U) - \Psi^{(\gamma,\mathcal V)}_{\alpha}(S)
\right|
\le
c_1 L_{\max}
\sqrt{
\frac{
\log |\Omega_{\mathrm{pair}}(\mathcal V)|
\;+\;
\log \frac{1}{\delta}
}{
n
}
}
$$

under the normalized selector loss convention $0\le \ell_i(S)\le 1$.

with probability at least $1-\delta$ over the support sample.

This is the finite-sample strengthening of the current fixed-family consistency story.

### Target Theorem 2: SRM oracle inequality

Let

$$
(\widehat{\gamma},\widehat{S})
\in
\arg\min_{\gamma\in\Gamma_{\mathrm{adm}}(\mathcal V),\;S\in\mathcal A_\gamma(\mathcal V)}
\left\{
\widehat{\Psi}^{(\gamma,\mathcal V)}_\alpha(S;\mathcal U)
\;+\;
\mathrm{pen}(\gamma,S)
\right\}.
$$

The target result is an oracle inequality of the form:

$$
\Psi^{(\widehat{\gamma},\mathcal V)}_\alpha(\widehat{S})
\le
\inf_{\gamma\in\Gamma_{\mathrm{adm}}(\mathcal V),\;S\in\mathcal A_\gamma(\mathcal V)}
\left\{
\Psi^{(\gamma,\mathcal V)}_\alpha(S)
\;+\;
c_2\,L_{\max}
\sqrt{
\frac{
\log \frac{1}{\pi_\Gamma(\gamma)}

+\;
\;2\log |\mathcal A_\gamma(\mathcal V)|
\;+\;
\log \frac{1}{\delta}
}{
n
}
}
\right\}.
$$

Interpretation:

- Occam-PRISM is nearly as good as the best action in the best family,
- up to the exact family/action complexity cost.

### Target Theorem 3: optional PAC-Bayes point-mass specialization

If the PAC-Bayes posterior is restricted to a point mass on one action, the stochastic theorem should specialize to the deterministic Occam-PRISM selector.

This is important because it preserves deployment alignment:

- we do not need to deploy a stochastic posterior or Gibbs classifier,
- only a single soup.

## 6.3 What this proposal does **not** claim

This proposal does **not** claim:

- that Occam-PRISM is already proven in the repo,
- that finite-family control solves the likely complementarity gap,
- that it will automatically beat SWAD by a large margin,
- that it proves current PRISM’s objective is optimal,
- or that $\alpha$ can be chosen in closed form.

Those would all be overclaims.

# 7. What This Proposal Predicts Empirically

Occam-PRISM has a specific empirical prediction:

> it should reduce PRISM’s sensitivity to bank-specific or split-specific family tuning, especially the need to hand-search $(\varepsilon,\tau,M)$.

It does **not** predict a guaranteed large jump over SWAD.

A realistic empirical prediction is narrower:

- lower variance across banks,
- fewer catastrophic large-family choices,
- similar or slightly better average performance than best tuned current PRISM,
- and a much cleaner method definition.

If Occam-PRISM does **not** improve or stabilize PRISM, that would mean:

- the family-selection gap was not the main empirical issue,
- and the next branch should target the objective itself, but only through a new theorem-backed derivation.

# 8. Concrete Replay-First Implementation Plan

## 8.1 Phase 1: deterministic SRM-PRISM

Implement the simplest version first:

- fixed $\alpha$
- small family grid, e.g.
  - $\varepsilon \in \{0.02,0.03\}$
  - $\tau \in \{0.02,0.03\}$
  - $M \in \{2,3\}$
- fixed exact-search budget $K_{\max}$, chosen once globally before the experiments
- uniform prior inside each family
- family prior either uniform or mildly size-favoring

Operational score:

$$
\text{Score}_{\mathrm{SRM}}(\gamma,S)
=
\widehat{\Psi}^{(\gamma,\mathcal V)}_{\alpha}(S;\mathcal U)
\;+\;
\sqrt{
\frac{
\log \frac{1}{\pi_\Gamma(\gamma)}
\;+\;
2\log |\mathcal A_\gamma(\mathcal V)|
\;+\;
\log \frac{1}{\delta}
}{
n
}
}.
$$

This is intentionally the **same score shape as the method definition in Section 4.5**, not a new tuned proxy. For the replay prototype, we should instantiate it with:

- a fixed global $\delta$ such as `0.05`,
- a fixed admissible family set $\Gamma_{\mathrm{adm}}(\mathcal V)$ determined by $K_{\max}$,
- a fixed clipping-and-rescaling rule so the selector loss lies in `[0,1]`,
- and a simple non-tuned family prior such as uniform over the admissible grid.

The important point is that there is **no replacement tuning knob** like $\lambda_{\mathrm{occam}}$ or a free penalty multiplier. If we later introduce a cheaper proxy score for engineering convenience, it must be labeled explicitly as a heuristic approximation rather than the main Occam-PRISM method.

## 8.2 Phase 2: held-out-prior PAC-Bayes PRISM

Then add the validation-defined prior:

- soup prior proportional to validation score,
- still point-mass posterior at deployment,
- same empirical regret term.

This is the more refined version, but it should come second because it adds another design layer and needs a regret-level derivation beyond the current memo.

## 8.3 Evaluation

Use the existing four PACS replay banks:

- art_painting
- cartoon
- photo
- sketch

Compare:

- ERM
- SWAD
- current PRISM
- Occam-PRISM

Main questions:

1. Does Occam-PRISM beat untuned current PRISM on average?
2. Does it match or beat the best current tuned PRISM settings without manual per-bank search?
3. Does it reduce variance across splits?
4. Does it reduce pathological large-family selections?

# 9. Risks and Falsification Criteria

## Risk 1: the empirical bottleneck is mostly objective-level, not family-level

This is the biggest risk, and the current evidence already hints at it.

**Falsification signal:**
Occam-PRISM gives little or no gain over current PRISM, even though family selection becomes cleaner.

Interpretation:
the theory gap was real, but not the main empirical bottleneck.

## Risk 2: the Occam penalty is too loose

Finite-family bounds can be numerically loose.

**Falsification signal:**
the bound always picks overly tiny families or underfits relative to tuned PRISM.

Interpretation:
the theory object is right, but the practical penalty needs PAC-Bayes priors or better constants.

## Risk 3: held-out priors do not materially help

**Falsification signal:**
PAC-Bayes prior version does no better than the simple SRM count penalty.

Interpretation:
validation-informed priors are unnecessary overhead for this problem scale.

# 10. Recommendation

If the goal is:

- **the cleanest next theory-first PRISM branch**,  
then this is the correct direction.

If the goal is:

- **the most likely immediate empirical gain regardless of theorem cleanliness**,  
then the answer is less certain, because the evidence still points to a likely objective-level limitation too.

So the honest recommendation is:

> Build **deterministic SRM/Occam-PRISM** next as the main theory-first branch, while being explicit that it repairs PRISM’s most important theorem gap, not necessarily its only empirical gap. Treat held-out-prior PAC-Bayes as a second-phase refinement, not the main branch.

# 11. High-School-Level Explanation

Here is the simple version.

Right now, PRISM works like this:

1. We train one model and save lots of checkpoints.
2. We throw away checkpoints that look bad.
3. We make soups out of the remaining checkpoints.
4. We choose the soup that looks safest against hidden hard groups of examples.

That last part is the smart, theory-motivated part.

The weaker part is step 2.

Right now, we still have to manually choose rules like:

- how close a checkpoint must be to the best validation loss,
- how strict the barrier/locality rule should be,
- and how many checkpoints a soup is allowed to contain.

So the current PRISM method is only half automatic and half theorem-driven.

Occam-PRISM tries to fix exactly that.

The idea is:

- instead of hand-picking one family of allowed soups,
- let the method compare **many possible soup families**,
- but punish more complicated families unless they really earn it.

So it becomes:

> “Choose the soup that has the best hidden-subpopulation regret score, but only after paying a price for coming from a very large or complicated search family.”

That is the same basic idea as “don’t trust a very flexible explanation unless it clearly helps.”

Why this is called “Occam”:

There is an old principle called Occam’s razor:

> simpler explanations should be preferred unless a more complicated one gives a real advantage.

That is exactly what we are doing here.

We are **not** saying:

- “smaller soups are always better,”
- or “simpler is always better.”

We are saying:

- “if two options look equally good on the data, prefer the one that came from the simpler family.”

Why this is better than the older “stable-pool” idea:

- the stable-pool idea tried to use bootstrap stability as a main method ingredient
- but that was not really backed by the exact theorem it wanted to use
- Occam-PRISM uses cleaner theory:
  - finite-family generalization,
  - structural risk minimization,
  - and, only as a later optional refinement, PAC-Bayes with held-out data

Why this still might not solve everything:

Our results suggest PRISM may still have an objective-level weakness too.
So Occam-PRISM might fix the **clean method-definition problem** without fully solving the **last bit of performance gap**.

But if we want a method that is truly motivated from first principles instead of more engineering tricks, this is the cleanest next step:

- keep the good PRISM idea,
- stop hand-tuning the soup family,
- and make the method itself choose the family in a principled way.

# 12. Sources Used

- Current PRISM paper draft: [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex)
- Current verified result ledger: [prism_results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/prism_results_ledger.md)
- Bartlett & Mendelson, *Rademacher and Gaussian Complexities: Risk Bounds and Structural Results* (JMLR 2002): https://www.jmlr.org/papers/volume3/bartlett02a/bartlett02a.pdf
- Bousquet & Elisseeff, *Stability and Generalization* (JMLR 2002): https://www.jmlr.org/papers/v2/bousquet02a.html
- Mohri course notes on finite hypothesis classes: https://cs.nyu.edu/~mohri/mls/ml_learning_with_finite_hypothesis_sets.pdf
- Dziugaite et al., *On the role of data in PAC-Bayes bounds* (arXiv 2020): https://arxiv.org/abs/2006.10929
- Sahu & Hemachandra, *Optimal PAC-Bayesian Posteriors for Stochastic Classifiers and their use for Choice of SVM Regularization Parameter* (PMLR 2019): https://proceedings.mlr.press/v101/sahu19a.html
- Duchi & Namkoong, *Learning Models with Uniform Performance via Distributionally Robust Optimization*: https://arxiv.org/abs/1810.08750
- Li, Namkoong, Xia, *Evaluating Model Performance under Worst-case Subpopulations* (NeurIPS 2021): https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf
- Agarwal & Zhang, *Minimax Regret Optimization for Robust Machine Learning under Distribution Shift* (PMLR 2022): https://proceedings.mlr.press/v178/agarwal22b.html
