---
title: d_cola proposal
description: First-principles proposal for a post-hoc domain generalization method beyond SWAD using domain-balanced risk, covariance reduction, and locality constraints.
created: 2026-03-14 18:42
last_modified: 2026-03-14 18:42
last_modified_by: agent
status: draft
related_files: claude_workspace/workspace_index.md, literature/swad_tex_source/2.theoretical_analysis.tex, literature/swad_tex_source/3.method.tex, literature/swad_tex_source/4.empirical_results.tex, literature/diwa_tex_source/sections/02_theory.tex, literature/diwa_tex_source/sections/03_approach.tex, literature/diwa_tex_source/sections/05_expe.tex
key_functions: N/A
latest_change: Added a concrete post-hoc DG method proposal grounded in verified SWAD and DiWA findings.
change_log:
  - 2026-03-14 18:42: Added a concrete post-hoc DG method proposal grounded in verified SWAD and DiWA findings.
---

# Goal

Develop a post-hoc checkpoint-selection and weight-averaging method that:

1. beats SWAD on both IID and OOD,
2. remains a single-model test-time method,
3. is motivated by controllable terms in a DG generalization surrogate rather than by a purely heuristic windowing rule.

# Verified findings from the local literature

## 1. What SWAD actually proves

From [literature/swad_tex_source/2.theoretical_analysis.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\swad_tex_source\2.theoretical_analysis.tex), SWAD's main theoretical statement is:

```tex
\mathcal{E}_{\mathcal{T}}(\theta) < \hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\theta) +\frac{1}{2I}\sum_{i=1}^{I}\mathbf{Div}(\mathcal{D}_{i},\mathcal{T})+ \max_{k\in[1,N]} \sqrt{\frac{v_{k}\ln\left(m/v_{k}\right)+\ln(N/\delta)}{m}},
```

where:

```tex
\hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\theta):=\max_{\|\Delta\|\leq\gamma} \hat{\mathcal{E}}_{\mathcal{D}}(\theta+\Delta)
```

and Theorem 2 further bounds the test-domain suboptimality of the RRM optimum:

```tex
\mathcal{E}_{\mathcal{T}}(\hat{\theta}^{\gamma}) - \min_{\theta'}\mathcal{E}_{\mathcal{T}}\left(\theta'\right)
\leq
\hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\hat{\theta}^{\gamma}) - \min_{\theta''}\hat{\mathcal{E}}_{\mathcal{D}}(\theta'')
+ \frac{1}{I}\sum_{i=1}^{I}\mathbf{Div}(\mathcal{D}_{i},\mathcal{T})
+ \max_{k\in[1,N]} \sqrt{\frac{v_{k}\ln\left(m/v_{k}\right)+\ln\left(2N/\delta\right)}{m}}
+ \sqrt{\frac{v\ln\left(m/v\right) + \ln\left(2/\delta\right)}{m}}.
```

Interpretation:

- SWAD's theory is about minimizing a robust empirical loss term.
- The uncontrollable source-target divergence term remains.
- A post-hoc method should target the controllable part of the bound more directly than simple window averaging.

## 2. What SWAD actually does

From [literature/swad_tex_source/3.method.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\swad_tex_source\3.method.tex), SWAD is not an optimizer for the bound above. It is a heuristic checkpoint-averaging rule:

- dense sampling: average every iteration rather than sparse SWA snapshots,
- overfit-aware scheduling: find start iteration `t_s` and end iteration `t_e` from source-domain validation loss traces,
- uniform averaging over the contiguous interval `[t_s, t_e]`.

The exact rule used in the paper is:

```tex
\min_{i\in[0, \ldots, N_s-1]} \mathcal E_\text{val}^{(t_s + i)}=\mathcal E_\text{val}^{(t_s)}
```

for the start, and

```tex
\min_{i \in [0, 1, \ldots, N_e - 1]} \mathcal E_\text{val}^{(t_e + i)} > r \mathcal E_\text{val}^{(t_s)}
```

for the end.

The appendix pseudo-code in [literature/swad_tex_source/8.appendix.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\swad_tex_source\8.appendix.tex) confirms that SWAD outputs:

```tex
\theta^{\text{SWAD}} \leftarrow \frac{1}{t_e - t_s + 1}\sum^{t_e}_{i'=t_s} \theta^{i'}
```

This is the core gap: the theory is about robust risk, but the method is a uniform average over a validation-defined time window.

## 3. Verified SWAD numbers to beat

From [literature/swad_tex_source/tables/fulltable.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\swad_tex_source\tables\fulltable.tex), SWAD reports:

- PACS: `88.1 ± 0.1`
- VLCS: `79.1 ± 0.1`
- OfficeHome: `70.6 ± 0.2`
- TerraIncognita: `50.0 ± 0.3`
- DomainNet: `46.5 ± 0.1`
- Average: `66.9`

From [literature/swad_tex_source/tables/ablation.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\swad_tex_source\tables\ablation.tex), the strongest single-trajectory SWAD ablation on PACS+VLCS is the full method at:

- OOD average: `83.0`
- IID average: `91.9`

## 4. What DiWA adds and why it matters

From [literature/diwa_tex_source/sections/theory/theory_bvc.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\diwa_tex_source\sections\theory\theory_bvc.tex), DiWA derives:

```tex
\mathbb{E}_{L_S^M}\mathcal{E}_T(\theta_{\text{WA}}(L_S^M)) =
\mathbb{E}_{(x,y)\sim p_T}\Big[\biasb^2(x, y)+\frac{1}{M} \varb(x)+\frac{M-1}{M} \covb(x)\Big] + O(\Deltab^2)
```

This says weight averaging succeeds when:

- variance is large and can be reduced by averaging,
- covariance between members is low enough,
- locality remains small enough that weight averaging still approximates prediction ensembling.

From [literature/diwa_tex_source/sections/appendix/00_app_limit_hessian_swad.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\diwa_tex_source\sections\appendix\00_app_limit_hessian_swad.tex), DiWA explicitly criticizes SWAD's flatness-only explanation:

- flatness does not act on the source-target divergence term,
- SAM can be as flat or flatter yet worse on OOD,
- more flatness does not imply better OOD if diversity collapses.

From [literature/diwa_tex_source/tables/domainbed/db_main_results.tex](C:\Users\jayden\Desktop\RESEARCH\NEURIPS_2026_codex\literature\diwa_tex_source\tables\domainbed\db_main_results.tex), DiWA with LP reaches:

- Average: `68.0`

That is a stronger target than SWAD if we want a serious paper in 2026.

## 5. Quick primary-source sanity check beyond the local repo

I also checked primary-source paper pages:

- SWAD (NeurIPS 2021): [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2021/hash/bcb41ccdc4363c6848a1d760f26c28a0-Abstract.html)
- DiWA (NeurIPS 2022): [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2022/hash/46108d807b50ad4144eb353b5d0e8851-Abstract-Conference.html)
- EoA (NeurIPS 2022): [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2022/hash/372cb7805eaccb2b7eed641271a30eec-Abstract-Conference.html)

EoA reports an average of `68.0%` with pre-trained ResNet-50 and emphasizes that moving-average models improve validation-test rank correlation under shift.

Important caveat:

- I have not done an exhaustive 2023-2026 literature review.
- I did not find, in this quick pass, a paper that explicitly combines source-domain worst-risk, pairwise checkpoint covariance, and linear-mode-connectivity barriers for post-hoc checkpoint soups in DG.
- That makes the proposal below plausible, not guaranteed, as a novelty claim.

# Where SWAD still leaves headroom

## Gap A: theory-method mismatch

SWAD's theory is about minimizing a robust source empirical loss, but the actual rule is a contiguous uniform average chosen by validation patience heuristics.

## Gap B: no explicit domain balancing

SWAD uses a source-validation trace, but it does not optimize worst-domain source risk or fairness across source domains. A checkpoint can look good on average while already drifting toward a subset of source domains.

## Gap C: no explicit covariance control

Uniformly averaging dense neighboring checkpoints inside one trajectory may reduce variance, but many adjacent checkpoints are highly correlated and provide little additional variance reduction.

## Gap D: no explicit locality test

SWAD assumes averaging a contiguous window stays inside a good basin, but it does not verify linear connectivity or low interpolation barrier.

# Recommended method: D-COLA

`D-COLA` = `Domain-balanced Covariance- and Locality-Aware Averaging`

This is the method I would pursue first.

## Core idea

Use SWAD's dense checkpoint pool, but replace its uniform time-window rule with a post-hoc optimization that explicitly trades off:

1. source-domain balance,
2. prediction covariance reduction,
3. weight-space locality inside one connected valley.

The point is not to be flatter in a vague sense. The point is to minimize a controllable surrogate of target risk suggested by combining SWAD's robust-risk intuition with DiWA's variance-covariance-locality analysis.

## Candidate set construction

Let the dense checkpoint pool be `{\theta_t}_{t=1}^K`.

For each checkpoint, compute source-domain validation losses:

```tex
L_e(\theta_t), \qquad e \in \{1,\dots,E\}
```

Choose an anchor checkpoint by domain-balanced risk:

```tex
a = \arg\min_t \max_e L_e(\theta_t).
```

This is already different from SWAD's first local optimum rule. It centers the soup around the checkpoint that is best for the worst observed source domain.

Then keep only checkpoints in a connected low-loss valley around the anchor:

```tex
\mathcal{V} = \left\{ t :
\max_e L_e(\theta_t) \le \max_e L_e(\theta_a) + \epsilon
\text{ and }
B(t,a) \le \tau
\right\},
```

where `B(t,a)` is a linear interpolation barrier:

```tex
B(t,a) =
\max_{\alpha \in [0,1]}
\bar{L}\big((1-\alpha)\theta_a + \alpha \theta_t\big)
- \max\{\bar{L}(\theta_a), \bar{L}(\theta_t)\},
```

and `\bar{L}` is the average source validation loss.

This is the locality guardrail.

## Covariance term

For retained checkpoints, precompute logits or per-sample losses on each source-domain validation set and estimate a pairwise covariance matrix:

```tex
C_{ij}
=
\frac{1}{E}
\sum_{e=1}^{E}
\operatorname{Cov}_{x \in \mathcal{V}_e}
\left(
\ell_i^e(x),
\ell_j^e(x)
\right).
```

High `C_{ij}` means checkpoints `i` and `j` are redundant on source-domain validation behavior. D-COLA should avoid placing too much mass on mutually redundant checkpoints.

## Optimization objective

Let `w` be simplex weights over checkpoints in `\mathcal{V}` and define:

```tex
\bar{\theta}_w = \sum_{t \in \mathcal{V}} w_t \theta_t.
```

The proposed objective is:

```tex
\min_{w \in \Delta^{|\mathcal{V}|}}
\underbrace{\max_e L_e(\bar{\theta}_w)}_{\text{domain-balanced source risk}}
+ \lambda_{\text{cov}} \underbrace{w^\top C w}_{\text{prediction covariance}}
+ \lambda_{\text{loc}} \underbrace{\sum_{t \in \mathcal{V}} w_t B(t,a)}_{\text{locality / basin safety}}
+ \lambda_{\text{ent}} \underbrace{\sum_t w_t \log w_t}_{\text{stability regularizer}}.
```

Interpretation:

- first term: do not sacrifice the hardest source domain,
- second term: do not waste mass on highly correlated checkpoints,
- third term: do not break the WA approximately ENS assumption,
- fourth term: prevent degenerate one-checkpoint solutions when several checkpoints are similarly good.

## Practical selection trick

Directly evaluating `L_e(\bar{\theta}_w)` for many `w` values is expensive.

Use the DiWA lemma that `f_WA \approx f_ENS` inside one connected valley, and optimize first on ensemble predictions:

```tex
f_{\text{ENS},w}(x) = \sum_{t \in \mathcal{V}} w_t f(x,\theta_t).
```

Search for `w` using cached logits, then output the single-model weight average `\bar{\theta}_w`.

This keeps the method post-hoc and computationally realistic.

## Why this is stronger than SWAD

SWAD:

- contiguous interval,
- uniform weights,
- selected by average source validation loss dynamics,
- no explicit redundancy penalty,
- no explicit connectivity test.

D-COLA:

- non-uniform checkpoint soup,
- centered on worst-domain source risk,
- penalizes redundant checkpoints,
- enforces connected-valley averaging,
- still outputs one model.

## Why this is different from DiWA

DiWA mainly changes where members come from: different runs with diverse hyperparameters.

D-COLA changes how we select and weight members:

- it is explicitly post-hoc on checkpoint pools,
- it can work on one trajectory or many runs,
- it optimizes a domain-balanced covariance-locality objective rather than using uniform or greedy validation-only rules.

# Falsifiable hypotheses

## H1

Within one training trajectory, the best post-hoc DG soup is not the SWAD interval average but a non-uniform subset inside a connected valley.

## H2

On DomainBed, minimizing `max_e L_e` over the source domains yields better OOD performance than minimizing average validation loss alone.

## H3

Adding the covariance term improves OOD more than IID, because it mainly attacks variance under diversity shift.

## H4

Removing the locality barrier causes WA to diverge from ENS and hurts both IID and OOD.

## H5

A multi-run version of D-COLA beats DiWA-restricted by combining cross-run diversity with within-valley safety.

# Minimum experimental program

## Baselines

- ERM
- SWA with constant and cyclic schedules
- SWAD
- MA / EoA-style single-run moving average
- DiWA-uniform
- DiWA-restricted
- naive top-k checkpoint soup by validation score
- naive uniform average over the best contiguous window

## Main metrics

- OOD average accuracy on DomainBed
- IID accuracy on source-domain held-out splits
- per-domain OOD accuracy
- standard error across three data splits
- validation-test rank correlation across checkpoints

## Diagnostics

- average pairwise covariance `w^T C w`
- interpolation barrier distribution
- pairwise weight distance distribution
- correlation between `max_e L_e`, average validation loss, and OOD accuracy

## Required ablations

- remove covariance term
- remove locality term
- replace worst-domain risk with average validation loss
- use uniform weights on the same candidate set
- same-run only versus multi-run pool
- logits covariance versus loss covariance

# Publication bar

## Honest target

For a serious NeurIPS or ICLR submission in 2026, the method should at least:

- beat SWAD's `66.9` average,
- be competitive with or exceed the stronger `68.0` class set by DiWA and EoA,
- show consistent wins, not a single-dataset spike,
- explain why it works with more than "flatter is better."

## Honest venue assessment

NeurIPS or ICLR is realistic if the method wins clearly and the story is tight.

Nature is not a realistic primary target for an incremental DG algorithm paper unless the work becomes substantially broader than a benchmark improvement, for example by delivering a new widely applicable principle with unusually strong theoretical and empirical reach.

# The one-sentence thesis

The best successor to SWAD is not "find an even flatter window"; it is "optimize a connected checkpoint soup that balances worst-domain source risk, variance-reducing diversity, and weight-space locality."
