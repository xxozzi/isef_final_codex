---
title: SRM-PRISM: Bound-Minimizing Updates for Post-Hoc Hidden-Subpopulation Regret
description: Detailed research proposal for upgrading PRISM from empirical regret minimization over one heuristic candidate family to a theory-first structural-risk-minimization or PAC-Bayes selector over nested deployable soup families.
created: 2026-03-30 20:45
last_modified: 2026-03-30 21:40
last_modified_by: agent
status: draft
related_files: claude_workspace/research/prism_posthoc_regret_implicit_subpopulations.md, claude_workspace/research/stable_pool_prism.md, claude_workspace/papers/prism_neurips/main.tex, claude_workspace/resume.md
key_functions:
  - Record a theory-first upgrade path for PRISM
  - Separate principled fixes from heuristic add-ons
  - Define formal selector updates, theorem targets, and replay-first experiments
latest_change: Added a final plain-English high-school-level walkthrough explaining the full proposal from problem to fix.
change_log:
  - 2026-03-30 20:45: Initial draft
  - 2026-03-30 21:20: Revised after strict multi-agent review; clarified theory-vs-empirical claims and corrected the main SRM formulation to hold alpha fixed
  - 2026-03-30 21:27: Tightened the target oracle inequality after second-pass theory review by adding an explicit proof-dependent penalty constant
  - 2026-03-30 21:31: Polished summary wording and oracle-inequality interpretation after final theory review
  - 2026-03-30 21:40: Added a plain-English walkthrough at the end of the memo
---

# Summary

The current PRISM formulation combines two components:

- a regret-based selector over deployable soups inside one fixed candidate family;
- a front-end family definition controlled by a semantic robustness target $\alpha$ together with family-definition parameters $(\varepsilon,\tau,M)$.

The first component is the clean part of the method. The second component is only weakly integrated into the present theorem story. This memo explores one possible repair:

> **SRM-PRISM**: replace single-family empirical regret minimization with structural-risk-minimization or PAC-Bayes selection over a finite hierarchy of deployable soup families.

The proposal keeps the deployed object and the regret primitive unchanged. The proposed change is only to the way candidate families are defined, compared, and regularized.

This memo should be read as a theory-first proposal, not as a settled empirical diagnosis. The current record suggests that candidate-family control is a real theoretical gap in PRISM. It does **not** yet prove that this is the dominant empirical source of PRISM’s remaining gap.

# 1. Why This Update Is Needed

## 1.1 The empirical issue

The current empirical picture says that `PRISM` is real, but not yet strong enough.

On the clean four-split PACS replay sweep, the domain-label-free comparison is:

| Split | ERM | SWAD | PRISM |
|---|---:|---:|---:|
| art_painting | 82.08 | 87.60 | 87.26 |
| cartoon | 81.57 | 82.38 | 81.57 |
| photo | 94.55 | 97.07 | 97.54 |
| sketch | 78.32 | 81.73 | 83.53 |
| average | 84.13 | 87.19 | 87.47 |

So `PRISM` is only `+0.28` ahead of `SWAD` on average, and the gains are split-dependent rather than broad.

On the fresh canonical `erm_replay_bank` seed-1 bank, in the same percentage scale:

| Method | Art full | In | Out |
|---|---:|---:|---:|
| ERM | 80.66 | 80.96 | 79.46 |
| SWAD | 87.94 | 87.86 | 88.26 |
| PRISM | 88.62 | 88.83 | 87.78 |

Again, `PRISM` is competitive, but not dominant. It gains on art and in-distribution metrics, but loses on the out metric.

The strongest empirical clue comes from the cross-pool ablation:

| Variant | Runner | Pool | Art full |
|---|---|---|---:|
| baseline_dcola | D-COLA | D-COLA | 0.8901 |
| dcola_on_prism_pool | D-COLA | PRISM | 0.8877 |
| baseline_prism | PRISM | PRISM | 0.8833 |
| prism_on_dcola_pool | PRISM | D-COLA | 0.8672 |

This pattern matters.

- `D-COLA` stays strong even on the `PRISM` pool.
- `PRISM` drops much harder on the `D-COLA` pool.

These results are consistent with the view that the present PRISM objective-family combination is still leaving performance on the table. They do **not** isolate candidate-family regularization as the dominant empirical bottleneck. A more direct reading is that PRISM’s current objective may underuse strong candidate sets.

One more empirical caveat matters here. The current `SWAD` comparison is replay-based, and [resume.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/resume.md#L363) explicitly notes that replayed `SWAD` is approximate rather than a perfect reconstruction of native training-time `SWAD`. Since the average PRISM-over-SWAD margin is small, that caveat should stay attached to any empirical interpretation.

The cleanest summary of the current evidence is:

- `PRISM` is competitive and real,
- `PRISM` is not yet uniformly stronger than `SWAD`,
- and the main negative evidence still points at an unresolved objective-level weakness, especially around complementarity.

## 1.2 The deeper empirical clue from the D-COLA ablations

The local D-COLA ablations are:

| Variant | Art full |
|---|---:|
| baseline | 0.8750 |
| uniform | 0.8745 |
| early | 0.8687 |
| no_loc | 0.8667 |
| pooled_anchor | 0.8638 |
| contiguous | 0.8613 |
| no_cov | 0.8594 |

Three lessons matter.

1. Exact optimized weights are not the main story. `uniform` is almost tied with `baseline`.
2. Noncontiguity matters. `contiguous` is materially worse.
3. Complementarity / nonredundancy matters a lot. `no_cov` is the worst ablation.

The most important implication is that **better subset quality matters more than fancier weight optimization**.

That supports looking at candidate-family control, but it does not by itself identify SRM/PAC-Bayes regularization, rather than a stronger complementarity-aware objective, as the empirically preferred next fix.

## 1.3 The current PRISM theory is only half first-principles

The current PRISM paper already points to the theoretical weakness clearly.

In [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L457), the main consistency result is:

> “Consistency of the second-stage selector conditional on a fixed candidate family.”

And in [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L682), the discussion says:

> “an anchor-based locality heuristic rather than a certificate.”

That is the key gap.

Current PRISM proves the back half of the method well, but the front half is still a modeling choice outside the main selector theorem.

That is the gap SRM-PRISM is meant to repair on the theory side.

# 2. Literature Motivation

## 2.1 Why flatness alone is not enough

The motivation for moving beyond a flatness-only selector is not speculative. The literature supports it, but only up to a point.

SWAD’s own discussion states:

> “not a perfect and theoretically guaranteed solver for flat minima”

and

> “does not strongly utilize domain-specific information”

in [5.discussion.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/5.discussion.tex#L9) and [5.discussion.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/5.discussion.tex#L15).

Its own benchmark table reports:

- `SWAD`: `66.9`
- `Previous SOTA [CORAL] + SWAD`: `67.3`

in [besttable.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/tables/besttable.tex#L17).

So even SWAD’s paper supports the narrower point that flatness helps, but does not exhaust the problem.

DiWA makes this even sharper. It says:

> “not explained by [the SWAD theorem]”

and

> “trade-off between diversity and locality”

in [00_app_limit_hessian_swad.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/appendix/00_app_limit_hessian_swad.tex#L63) and [theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex#L5).

Its table reports:

- `SWAD`: `66.9`
- `DiWA†: M=60`: `68.0`

in [04_app_diversity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/appendix/04_app_diversity.tex#L75).

The literature-backed conclusion is therefore limited but useful: post-hoc DG behavior is not fully explained by flatness alone. The further step toward SRM/PAC-Bayes family control is an inference from that observation, not a statement already made in those papers.

## 2.2 Why hidden-subpopulation robustness is still the right PRISM core

The current PRISM core should be kept.

The regret primitive is still attractive because it explicitly compares each soup to the best feasible soup on each hidden subgroup, instead of conflating subgroup difficulty with excess loss.

That basic direction is aligned with:

- minimax regret under shift,
- worst-case hidden-subpopulation robustness,
- and domain-label-free robustness ideas from adjacent fairness and DRO literatures.

Two sources are especially relevant here:

- Agarwal and Zhang’s minimax regret formulation under shift ([PMLR 2022](https://proceedings.mlr.press/v178/agarwal22b.html));
- Li, Namkoong, and Xia’s worst-case subpopulation framework ([NeurIPS 2021 PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf)).

`Change is Hard` adds a useful warning at the empirical level: existing subgroup-robust methods “only improve subgroup robustness over certain types of shifts” after training “over 10,000 models” ([OpenReview PDF](https://openreview.net/attachment?id=wwR38qFs3i&name=pdf)). That is one reason not to over-interpret the current PRISM gains.

So the proposal is not to replace PRISM’s regret core.

It is to make the **selector that uses that core** more tightly integrated into a theorem-driven selection rule.

## 2.3 Why the fix should use explicit complexity control rather than another ad hoc term

Several theory traditions support a principle-first repair based on explicit complexity control, but none of them by themselves prove that SRM/PAC-Bayes is the unique or necessary next step for PRISM.

Vapnik’s 1991 risk-minimization framing is still the right design order:

> “State the problem in mathematical terms.”

> “Formulate a general principle.”

> “Develop an algorithm based on such general principle.”

([NeurIPS 1991 PDF](https://papers.nips.cc/paper_files/paper/1991/file/ff4d5fbbafdf976cfdc032e3bde78de5-Paper.pdf))

Dziugaite and Roy make the numerical point:

> “many learning bounds are quantitatively vacuous”

and

> “we need nonvacuous bounds”

([arXiv:1703.11008](https://arxiv.org/abs/1703.11008))

Bousquet and Elisseeff make the stability point:

> “define notions of stability”

to

> “derive generalization error bounds”

([JMLR 2002](https://www.jmlr.org/papers/v2/bousquet02a.html))

The design conclusion is therefore modest:

> if we want PRISM to become more first-principles, one natural repair is to control family selection through an explicit generalization principle rather than empirical regret alone.

# 3. The Proposed Update: SRM-PRISM

## 3.1 Data split and notation

We keep the PRISM data split:

- a validation split $\mathcal V$, used only to define candidate families;
- a support split $\mathcal U = \{Z_i\}_{i=1}^n$, used only to score candidate soups;
- the final target evaluation remains untouched.

We index selector families by

$$
\gamma = (\varepsilon,\tau,M) \in \Gamma,
$$

where:

- $\varepsilon$ is the validation-loss slack,
- $\tau$ is the barrier/locality threshold,
- $M$ is the maximum soup size.

The robustness parameter $\alpha$ is treated as fixed in the main SRM formulation. This is deliberate. Unlike $\varepsilon,\tau,M$, $\alpha$ changes the robustness target itself rather than only the searched action family.

For each $\gamma$, the validation stage defines:

$$
\mathcal C_\gamma(\mathcal V)
=
\{t : L_{\mathcal V}(\theta_t)\le L_{\mathcal V}^\star + \varepsilon,\; B(t,a)\le \tau\},
$$

and hence the exact deployable action family:

$$
\mathcal A_\gamma(\mathcal V)
=
\{S \subseteq \mathcal C_\gamma(\mathcal V) : 1 \le |S| \le M\}.
$$

For a fixed $\alpha$, the current PRISM empirical regret score on the support set stays:

$$
\widehat{\Psi}_{\alpha}(S),
$$

meaning empirical worst-case hidden-subpopulation regret over the actual deployable soup $S$.

## 3.2 The new selector

For fixed $\alpha$, the new selection rule is:

$$
(\hat\gamma,\hat S)
\in
\arg\min_{\gamma\in\Gamma,\; S\in\mathcal A_\gamma(\mathcal V)}
\widehat{\Psi}_{\alpha}(S)
+
\operatorname{pen}_{n,\alpha}(\gamma).
$$

The intended penalty is not a finished theorem, but a target finite-class form such as:

$$
\operatorname{pen}_{n,\alpha}(\gamma)
=
C(\alpha,L_{\max})
\sqrt{
\frac{\log N_\gamma(\mathcal V) + \log(|\Gamma|/\delta)}{n}
}.
$$

where $N_\gamma(\mathcal V)$ denotes the size of the actually scored pairwise regret class, not just the raw soup count. The exact constant and $\alpha$-dependence would need to come from an explicit uniform-convergence argument for the pairwise top-$\alpha$ regret functional.

It says:

- the empirical hidden-subpopulation regret is still the object we optimize;
- but the selector now pays a finite-sample complexity price for the family it searched over.

The intended effect is to compare candidate families using a common statistical criterion rather than empirical regret alone.

## 3.3 PAC-Bayes extension

A PAC-Bayes variant is also plausible, but it is best treated as an extension rather than as an equivalent finished selector.

The clean version would define a prior over the **joint** selector object $(\gamma,S)$, conditional on the validation split but independent of the support split, and then derive a point-mass or randomized-posterior bound using a standard PAC-Bayes theorem such as Seeger’s ([JMLR 2002](https://jmlr.org/papers/v3/seeger02a.html)).

At the level of selector form, this would look like:

$$
(\hat\gamma,\hat S)
\in
\arg\min_{\gamma\in\Gamma,\; S\in\mathcal A_\gamma(\mathcal V)}
\widehat{\Psi}_{\alpha}(S)
+
c
\sqrt{
\frac{-\log \pi(\gamma,S) + \log(1/\delta)}{n}
}.
$$

This extension is appealing because it lets us encode inductive bias without inventing extra objective terms. But it is not yet theorem-ready in the current memo; it would require a full statement of the prior, posterior, and applicable PAC-Bayes loss bound.

For example, the prior can prefer:

- smaller soups,
- more local / lower-barrier soups,
- soups closer to the anchor,
- families with fewer actions.

Conditional on a valid PAC-Bayes construction, this would provide one principled way to express “locality matters” or “smaller soups are easier to trust” without adding another free-standing heuristic penalty.

# 4. Why This Is Better Than the Current PRISM Pipeline

## 4.1 It puts candidate-family choice inside the theorem

This is the main theory-side repair.

Current PRISM’s main selector theorem only starts after $\mathcal A_\gamma(\mathcal V)$ is fixed.

SRM-PRISM instead treats $\gamma$ as part of the selection problem itself.

That means:

- $\varepsilon,\tau,M$ stop being merely tuning knobs;
- they become indices in a hierarchy of candidate families;
- the selector gains non-asymptotic model-class comparison over that hierarchy.

## 4.2 It uses the exact action family that is really searched

This is important because PRISM’s action set is finite once $\mathcal V$ is fixed.

That means we do not need to start with loose VC-style abstractions if we do not want to. We can directly penalize the exact scored family that the selector actually searched.

That is statistically cleaner and operationally more honest than regularizing with a quantity unrelated to the scored family, although the actually counted object should be the pairwise regret class rather than just the soup set.

## 4.3 It keeps the deployed object aligned with the optimized object

This remains one of PRISM’s main conceptual advantages.

The decision variable remains the actual soup that gets deployed:

$$
\bar\theta_S = \frac{1}{|S|}\sum_{t\in S}\theta_t.
$$

We are not reintroducing a predictive-mixture surrogate, a relaxed weight optimizer, or a proxy scoring rule detached from deployment.

## 4.4 It gives a clean place to express averageability and locality

Locality is still important. The evidence from DiWA and our own ablations says so.

But the right theory-first place for locality is:

- in the feasible family $\mathcal A_\gamma(\mathcal V)$, or
- in the prior $\pi_\gamma(S)$,

not as an extra objective term added late because it improves a validation score.

This is one of the main conceptual reasons to study SRM-PRISM before adding another heuristic objective term.

# 5. Target Theorem Forms (Not Yet Proved for the Current Method)

The statements in this section are target theorem forms for a revised method, not established guarantees for the current implementation. Any proof would require explicit assumptions on bounded regret, conditional independence induced by the split, exact family enumeration, and the treatment of validation-defined random action families.

Operationally, three caveats should stay attached to any future theorem statement:

- empty families $\mathcal A_\gamma(\mathcal V)=\varnothing$ must be skipped or handled explicitly;
- the clean theorem applies to exact family enumeration, not truncated search;
- post-selection BN refresh remains outside the selector theorem unless it is analyzed separately.

## 5.1 Uniform convergence over each fixed family

For each fixed $\gamma$, we want a result of the form:

$$
\sup_{S\in\mathcal A_\gamma(\mathcal V)}
\left|
\widehat{\Psi}_{\alpha}(S) - \Psi_{\alpha}(S)
\right|
\le
O\!\left(
C(\alpha,L_{\max})
\sqrt{
\frac{\log N_\gamma(\mathcal V) + \log(1/\delta)}{n}
}
\right).
$$

This would be the finite-sample replacement for the current asymptotic “conditional on a fixed candidate family” result.

## 5.2 Oracle inequality across the family hierarchy

The main theorem target should then say, with high probability conditional on the validation split,

$$
\Psi_{\alpha}(\hat S)
\le
\inf_{\gamma\in\Gamma}
\left[
\inf_{S\in\mathcal A_\gamma(\mathcal V)} \Psi_{\alpha}(S)
+
c_{\mathrm{OI}}\,\operatorname{pen}_{n,\alpha}(\gamma)
\right].
$$

Here $c_{\mathrm{OI}}\ge 2$ is a proof-dependent oracle-inequality constant that absorbs the usual comparison between the selected model and the best comparator family. This is the oracle-style inequality that motivates the proposal. Establishing it in the present setting is future work.

It says the selected soup is within the stated oracle penalty of the best soup in the best admissible family.

That is the kind of theorem currently missing from PRISM.

## 5.3 PAC-Bayes selector bound

If we use the prior-based variant, the corresponding theorem target would replace $\log N_\gamma$ with a prior-based complexity term on the joint selector object $(\gamma,S)$.

Conditional on the validation split, that yields a selector with a support-split-independent prior and a complexity term attached directly to the chosen soup.

This is attractive if we want:

- cleaner dependence on soup size,
- smoother tradeoffs than hard family-size penalties,
- and a more explicit inductive-bias interpretation.

## 5.4 Multi-alpha extension

If we want robustness to multiple subgroup masses, the clean version is not a heuristic averaged score. It is:

- a finite grid $\mathcal G_\alpha$,
- treated outside the main family-complexity index,
- with a union bound or tolerance-based model-selection rule.

This is mechanically straightforward, but it should be remembered that changing $\alpha$ changes the robustness target itself, so comparison across alphas is not the same as comparison across candidate-family sizes.

# 6. What This Proposal Explicitly Rejects

This memo is intentionally narrower than some earlier discussions.

## 6.1 No new heuristic covariance term as the main theory fix

Our results strongly suggest complementarity matters.

But adding a D-COLA-like covariance term directly into PRISM right now would pull the method back toward a composite surrogate objective.

A covariance/complementarity-aware repair remains the strongest empirically motivated alternative. The reason to study SRM-PRISM first is theoretical cleanliness, not because the current experiments have already shown family-complexity control to be the main missing empirical ingredient.

## 6.2 No bootstrap stability as the primary theorem repair

Bootstrap stability may still be a useful diagnostic or ablation.

But it is not the cleanest main repair, because it addresses sensitivity indirectly while leaving the core family-selection theorem incomplete.

The hierarchy-and-penalty route is cleaner.

## 6.3 No claim of universal dominance

This proposal does **not** claim:

- that SRM-PRISM will always beat SWAD,
- that it will always beat the strongest domain-labeled methods,
- or that it solves DG in full generality.

The point is narrower and more defensible:

> if hidden source-supported subgroup robustness is the right uncertainty family, then one natural repair is to minimize a bound for that object over a hierarchy of actual deployable soup families.

# 7. Concrete Replay-First Development Plan

## 7.1 Phase 1: selector-only implementation

Implement a replay-only SRM-PRISM variant in `domaingen`:

1. Fix a semantic robustness target $\alpha$, and enumerate a finite grid
   $$
   \Gamma = \{(\varepsilon,\tau,M)\}.
   $$

2. For each $\gamma$:
   - build $\mathcal C_\gamma(\mathcal V)$,
   - build $\mathcal A_\gamma(\mathcal V)$,
   - solve the exact PRISM subset problem over $\mathcal A_\gamma(\mathcal V)$,
   - compute the penalized score.

3. Pick the penalized minimizer over $\Gamma$.

This is the minimal engineering needed to instantiate the theory update.

## 7.2 Phase 2: fixed-grid, no hand retuning

The first serious evaluation should use one fixed grid across all replay banks.

For example, at fixed $\alpha = 0.20$:

- $\varepsilon \in \{0.02, 0.03\}$
- $\tau \in \{0.02, 0.03\}$
- $M \in \{2,3,4\}$

The point is to test whether explicit complexity control stabilizes the selector and improves transfer across banks. This is a theory-first experiment, not yet the empirically proven main bottleneck.

## 7.3 Phase 3: compare only the right baselines

The decisive comparisons are:

- current tuned `PRISM`
- `SRM-PRISM`
- `SWAD`

and, for diagnosis only:

- `D-COLA` where domain labels are allowed.

The main questions are:

1. Does SRM-PRISM reduce sensitivity to $(\varepsilon,\tau,M)$ at fixed $\alpha$?
2. Does it improve the weak splits where current PRISM collapses toward SWAD or ERM?
3. Does it narrow the cross-pool weakness?

# 8. Testable Hypotheses

This proposal should not be treated as a vague design philosophy. It makes concrete predictions.

## Prediction 1

At fixed $\alpha$, `SRM-PRISM` may be less sensitive to the exact choice of `epsilon`, `tau`, and `M` than current PRISM, because the selector explicitly pays for searching broader candidate families.

## Prediction 2

`SRM-PRISM` may choose smaller or more local families unless the empirical regret improvement is strong enough to justify broader families.

## Prediction 3

If frozen family choice is part of the current problem, the gap between “PRISM on PRISM pool” and “PRISM on D-COLA pool” should shrink. If it does not, that would point back toward an objective-level limitation.

## Prediction 4

If SRM-PRISM does **not** materially improve selector stability or cross-bank robustness, then the remaining weakness is unlikely to be primarily statistical family choice. At that point, a deeper objective change would be justified.

# 9. Risks and Failure Modes

## 9.1 The bound may be too weak numerically

This is a real risk for any complexity-controlled selector.

The selector may become too conservative, especially if the action families are large and the penalty dominates the empirical regret differences.

## 9.2 The real missing ingredient may still be complementarity

If the main empirical advantage in stronger selectors comes from a signal that PRISM’s regret family simply does not encode, then even a perfectly repaired theorem may not fully close the empirical gap.

This is exactly why the cross-pool ablation must remain the main diagnosis tool after implementation.

## 9.3 Finite-family penalties may still be crude

Even exact log-cardinality penalties do not capture all geometric structure of neural checkpoint families.

So the selector may become statistically cleaner without becoming dramatically stronger empirically.

That is acceptable if the goal is first-principles progress, but it should be acknowledged clearly.

# 10. Recommendation

An appropriate next step is to test the following update:

> **Replace single-family empirical regret minimization with SRM/PAC-Bayes selection over a hierarchy of actual deployable PRISM soup families.**

This update is attractive because it:

- addresses the main theoretical weakness,
- preserves PRISM’s best conceptual feature,
- avoids adding another heuristic term,
- and gives a clean, falsifiable next experiment.

If it works, PRISM gains a much stronger selector-theorem story. If it fails, that is also informative:

> the remaining weakness is not the lack of complexity control, but the regret objective itself.

# Sources

- SWAD paper: https://openreview.net/forum?id=zkHlu_3sJYU
- SWAD discussion source: [5.discussion.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/5.discussion.tex#L9)
- SWAD benchmark table: [besttable.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/tables/besttable.tex#L17)
- DiWA paper: https://arxiv.org/abs/2205.09739
- DiWA locality theory: [theory_locality_linearity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex#L5)
- DiWA flatness limitation note: [00_app_limit_hessian_swad.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/appendix/00_app_limit_hessian_swad.tex#L63)
- DiWA benchmark table: [04_app_diversity.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/appendix/04_app_diversity.tex#L75)
- Change is Hard: https://openreview.net/attachment?id=wwR38qFs3i&name=pdf
- Minimax regret under shift: https://proceedings.mlr.press/v178/agarwal22b.html
- Worst-case subpopulations: https://proceedings.neurips.cc/paper_files/paper/2021/file/908075ea2c025c335f4865f7db427062-Paper.pdf
- PRISM draft: [main.tex](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/prism_neurips/main.tex#L457)
- Dziugaite and Roy 2017: https://arxiv.org/abs/1703.11008
- Bousquet and Elisseeff 2002: https://www.jmlr.org/papers/v2/bousquet02a.html
- Seeger 2002 PAC-Bayes: https://jmlr.org/papers/v3/seeger02a.html

# Plain-English Walkthrough

Here is the same proposal in much simpler language.

Right now, PRISM is a good idea, but it is not beating SWAD by a huge amount. That does **not** mean PRISM is bad. It means PRISM seems to be getting part of the problem right, but not all of it. The part PRISM gets right is that it scores the **actual soup we would really deploy**, not some fake stand-in object. That is good and we want to keep it. But the part PRISM does less cleanly is how it decides **what collection of soups it is allowed to search over**. Right now, we still pick settings like how strict the validation filter is, how strict the barrier filter is, and how large a soup can be. Then PRISM finds the best soup only inside that chosen family. So one part is principled, but another part still depends on hand-picked settings.

Our results suggest this matters, but they also tell us to be careful. PRISM is only slightly ahead of SWAD on average in the four-split PACS replay comparison. It wins on some splits and loses on others. That means we cannot honestly say “PRISM is clearly better.” We can say it is competitive and promising. The cross-pool test is especially important. When a stronger selector objective was placed on the PRISM pool, it still worked well. But when PRISM was placed on that stronger selector’s pool, PRISM dropped more. In simple terms, that suggests PRISM is not being held back only by a bad checkpoint pool. It suggests that PRISM’s current way of scoring soups is still missing something important. So this memo is **not** saying “we already know family selection is the whole problem.” It is saying: even if objective-level weakness remains, the cleanest theory gap we can fix right now is the way PRISM chooses among candidate families.

So what is SRM-PRISM? The idea is simple. Instead of choosing one family of soups by hand and then running PRISM only inside that family, we create a small menu of possible families. Some are stricter. Some are looser. Some allow bigger soups. Some allow only smaller soups. Then, instead of deciding by hand which family to trust, we let the method compare them. But it does **not** compare them only by raw performance on the support set, because a bigger family usually has more ways to look good by luck. So SRM-PRISM adds a penalty for searching a larger or more flexible family. The method then chooses the family and soup that give the best **performance plus statistical caution**.

A good analogy is studying for a test. Imagine one student memorizes one short, clean formula sheet, while another student carries a giant binder full of special cases. If both do equally well on practice problems, we should trust the simpler strategy more. The giant binder has more ways to fit the practice set in a brittle way. SRM-PRISM applies that same idea to soup families. A larger family gives the method more chances to “get lucky” on the support set. A smaller family is harder to overfit with. So the selector should not ask only “which family gave the best score?” It should ask “which family gave the best score **after paying for being more complex?**”

That is why the proposal introduces a penalty term. In plain English, the new selector says: for each allowed family, find the best PRISM soup in that family, then add a penalty that gets larger when the family is bigger or more permissive. After that, pick the family and soup with the best penalized score. That is much more theory-driven than just adding another new term because it helped once in an experiment. It is saying: we are going to control how much freedom the selector had, using a standard statistical principle, instead of relying only on raw empirical regret.

There is one important subtlety about `alpha`. In PRISM, `alpha` is not just another tuning knob like the barrier threshold or the soup size. It changes what “robustness” actually means. A smaller `alpha` means “protect against smaller hidden subpopulations,” which is a harder goal. So in the main SRM version, we do **not** mix `alpha` into the ordinary family-complexity selection problem. We hold `alpha` fixed and only compare families over things like `epsilon`, `tau`, and `M`. That keeps the math cleaner and avoids quietly switching to an easier robustness target just because it gives a nicer score.

There is also an optional PAC-Bayes version of the same idea. In simple language, PAC-Bayes is another way to say “do well, but also pay for being too complicated.” Instead of only counting how large a family is, you give some soups a higher prior belief than others before seeing the support set. For example, smaller soups or more local soups could be treated as more plausible. Then the selector pays a penalty if it chooses a soup that was very unlikely under that prior. This can be elegant, but in the memo it is only an extension, not the main finished proposal, because it needs more careful theorem work.

The most important honesty point is this: SRM-PRISM fixes the **theory gap** in PRISM more directly than it fixes the **empirical gap**. Those are not the same thing. If SRM-PRISM works, great. That would mean PRISM was partly being held back by the fact that it searched one family at a time without a proper complexity-aware rule. But if SRM-PRISM does **not** work, that is also valuable information. It would mean the deeper problem is probably not family selection. It would mean PRISM’s current regret objective is still missing some important signal, likely something related to complementarity between checkpoints. So this proposal is a clean next step, not a promise that the full problem is solved.

The shortest version is this: PRISM already has a smart way to compare soups, but it still has a partly hand-picked way to decide what soups are on the table. SRM-PRISM says we should stop choosing that family by hand. Instead, we should let the method compare many possible soup families while penalizing ones that are too big or too flexible. That makes the selector more fair, more statistically disciplined, and more theory-driven. If it helps, then PRISM becomes a cleaner method. If it does not, then we learn that the real missing piece is inside PRISM’s objective itself, not just in how we pick the search space.

# Plain-English Walkthrough

Here is the same proposal in much simpler language.

Right now, PRISM is a good idea, but it is not crushing SWAD. The reason is not that PRISM is useless. The reason is that it seems to get part of the problem right, but not all of it. PRISM already has one very good feature: it judges the **actual soup we would really deploy**, not some fake proxy object. That part is important and we want to keep it. But the way PRISM currently decides **which family of soups it is even allowed to search over** is still partly hand-tuned. In simple terms, we first choose some settings like how strict we want to be, how many checkpoints we allow in a soup, and how much barrier/locality filtering we use, and then PRISM finds the best soup only inside that chosen family. So the second half is principled, but the first half is still partly “pick some settings and hope they were the right ones.”

Our results suggest this matters, but they also tell us to be careful. PRISM is slightly ahead of SWAD on average in the four-split PACS comparison, but only by a little. It wins on some splits and loses on others. That means we cannot honestly say “PRISM is clearly better.” We can say it is competitive and interesting. The cross-pool test is especially important here. When we put the stronger D-COLA objective on the PRISM pool, it still worked well. But when we put PRISM on the D-COLA pool, PRISM dropped more. In plain English, that suggests PRISM is not just being held back by a bad checkpoint pool. It suggests that PRISM’s current scoring rule still misses something important. So this memo is **not** saying “we already know family selection is the whole problem.” It is saying: even if objective-level weakness remains, the cleanest theory gap we can fix right now is the way PRISM chooses among candidate families.

So what is SRM-PRISM? The basic idea is very simple. Instead of choosing one set of hyperparameters and then running PRISM inside that one family, we create a small menu of possible families. Each family corresponds to a different choice of things like `epsilon`, `tau`, and `M`. Some families are small and strict. Some are larger and more permissive. Then, instead of choosing the family by hand, we let the selector compare them. But it does **not** compare them only by raw empirical regret, because that would always favor larger and more flexible families. Instead, it compares them by “empirical performance plus a penalty for searching a bigger family.” That is the whole structural-risk-minimization idea: if you search a bigger class, you have more ways to accidentally overfit, so you should have to earn that flexibility.

A very simple analogy is studying for a test. Suppose one student memorizes one short clean formula sheet, and another student carries around a giant binder of special cases. If both do equally well on the practice problems, we should trust the simpler, tighter strategy more. The giant binder has more chances to fit the practice set in a brittle way. SRM-PRISM applies the same idea to soup families. A very broad family might contain a soup that looks great on the support set just by luck. A smaller family is harder to overfit with. So the selector should not ask only “which family gave the best number?” It should ask “which family gave the best number **after paying for its complexity?**”

That is why the proposal introduces a penalty term. In plain English, the new selector says: for each allowed family, find the best PRISM soup in that family, then add a penalty that grows when the family is larger or more permissive. After that, pick the family and soup with the best penalized score. That is much more first-principles than adding another empirical term because it worked in one ablation. It is saying: we are going to control how much freedom the selector had, using a standard statistical idea, instead of relying only on a raw validation-style score.

There is one important subtlety about `alpha`. In PRISM, `alpha` is not just another tuning knob like the barrier threshold or soup size. It actually changes what robustness means. A smaller `alpha` means “protect against smaller hidden subpopulations,” which is a harder robustness target. So in the main SRM version, we do **not** mix `alpha` into the ordinary family-complexity selection. We hold `alpha` fixed and only compare families over `epsilon`, `tau`, and `M`. That keeps the math cleaner and avoids cheating by quietly switching to an easier robustness target.

There is also an optional PAC-Bayes version of the same idea. In very simple terms, PAC-Bayes is another way to say “do well, but pay for being too complicated.” Instead of only counting how large a family is, you put a prior over soups and say that some soups are more plausible than others before seeing the support set. For example, smaller soups or more local soups could get higher prior weight. Then the selector pays a penalty based on how surprising its chosen soup was under that prior. This is appealing, but in the memo it is only an extension, not the main finished proposal, because it needs more careful theorem work.

Now the most important honesty point: this proposal fixes the **theory gap** in PRISM more directly than it fixes the **empirical gap**. Those are not the same thing. If SRM-PRISM works, that would be great: it would mean PRISM was partly being held back by the fact that it searched one family at a time without a proper complexity-aware selection rule. But if SRM-PRISM does **not** work, that is also useful information. It would mean the deeper problem is probably not family selection. It would mean PRISM’s current regret objective is still missing some important signal, likely something related to complementarity between checkpoints. So this proposal is a clean next step, not a promise that the problem is solved.

The high-school version of the whole story is this: PRISM already has a smart way to compare soups, but it still has a somewhat hand-picked way to decide what soups are even on the table. SRM-PRISM says we should stop picking that family by hand. Instead, we should let the method compare many possible soup families, while penalizing families that are too big or too flexible. That makes the selector more fair, more statistically disciplined, and more theory-driven. If that helps, great. If it does not, then we have learned that the remaining weakness is deeper and lives inside the PRISM objective itself, not just in how we pick the search space.
