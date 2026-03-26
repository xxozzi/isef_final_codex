---
title: Consensus overlap weight averaging for single-run domain generalization
description: Research memo proposing a new first-principles single-run post-hoc method that extends beyond SWAD by selecting checkpoints with large per-domain consensus volume.
created: 2026-03-16 00:45
last_modified: 2026-03-16 01:11
last_modified_by: agent
status: superseded
related_files: claude_workspace/workspace_index.md, claude_workspace/research/minimum_adaptation_information_weight_averaging.md, literature/swad_tex_source/main.tex, literature/diwa_tex_source/main.tex, literature/tawa.tex
key_functions: N/A
latest_change: Marked this memo as a precursor after finding a stronger adaptation-information formulation.
change_log:
  - 2026-03-16 01:11: Marked this memo as a precursor after finding a stronger adaptation-information formulation.
  - 2026-03-16 00:53: Normalized the memo to ASCII and kept the COWA proposal, theory sketch, and experiment plan intact.
  - 2026-03-16 00:45: Added the literature synthesis, new consensus-volume hypothesis, COWA algorithm, theory sketch, and experiment plan.
---

# Bottom Line

This memo is now a precursor. After checking newer DG and posterior-aggregation literature, I no longer think `COWA` is the strongest candidate for a field-shaping post-hoc DG method. The current main recommendation is the adaptation-information memo at [minimum_adaptation_information_weight_averaging.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/research/minimum_adaptation_information_weight_averaging.md).

The strongest candidate I found is not "better flatness" and not "generic weighted averaging." It is a different principle:

> **Domain generalization should optimize the overlap of per-domain low-loss neighborhoods in parameter space, not merely the flatness of the pooled loss.**

This gives a concrete single-run post-hoc method:

- **`COWA` = Consensus Overlap Weight Averaging**
- It scores checkpoints by:
  - low average source-domain loss,
  - low source-domain gradient disagreement,
  - large shared basin volume,
  - low mismatch between per-domain local curvatures.
- It then averages only a contiguous high-consensus window.

This is the cleanest route I found to a genuinely new post-hoc DG idea that is:

- still single-run,
- still weight-averaging-based,
- directly motivated by first principles,
- and not reducible to "ERM + augmentations" or a generic quality-weighted soup.

I cannot honestly claim this is already a NeurIPS/Nature/ICLR breakthrough. I can claim it is the strongest defensible research direction I found after checking the local SWAD/DiWA material and broader adjacent literatures.

# What I Verified

## 1. SWAD is strong, but its theory is pooled-flatness-only

From the local SWAD source in [`literature/swad_tex_source/2.theoretical_analysis.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex), the core bound is:

```tex
\mathcal{E}_{\mathcal{T}}(\theta) < \hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\theta)
+\frac{1}{2I}\sum_{i=1}^{I}\mathbf{Div}(\mathcal{D}_{i},\mathcal{T})
+ \max_{k\in[1,N]} \sqrt{\frac{v_{k}\ln\left(m/v_{k}\right)+\ln(N/\delta)}{m}}
```

and the optimal robust-risk solution satisfies:

```tex
\mathcal{E}_{\mathcal{T}}(\hat{\theta}^{\gamma}) - \min_{\theta'}\mathcal{E}_{\mathcal{T}}\left(\theta'\right)
\leq
\hat{\mathcal{E}}_{\mathcal{D}}^{\gamma}(\hat{\theta}^{\gamma}) - \min_{\theta''}\hat{\mathcal{E}}_{\mathcal{D}}(\theta'')
+ \frac{1}{I}\sum_{i=1}^{I}\mathbf{Div}(\mathcal{D}_{i},\mathcal{T})
+ \text{confidence terms.}
```

The algorithmic side of SWAD is dense sampling plus validation-loss-based start/end detection. Empirically, the local table in [`literature/swad_tex_source/tables/besttable.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/tables/besttable.tex) reports:

- ERM average: `63.3`
- Best SOTA competitor average before SWAD: `65.3`
- SWAD average: `66.9`
- `CORAL + SWAD`: `67.3`

The SWAD discussion section explicitly admits two important limitations:

- the theorem's confidence term behaves poorly as `gamma -> 0`,
- **SWAD does not strongly use domain-specific information**.

That second limitation is the opening.

## 2. DiWA says diversity matters, but it currently needs multiple runs

From the local DiWA source in [`literature/diwa_tex_source/sections/02_theory.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/02_theory.tex) and [`literature/diwa_tex_source/sections/appendix/01_app_proof.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/appendix/01_app_proof.tex), the central decomposition is:

```tex
\mathbb{E}_{L_S^M}\mathcal{E}_T(\theta_{\text{WA}}(L_S^M))
=
\mathbb{E}_{(x,y)\sim p_T}\Big[\biasb^2(x, y)+\frac{1}{M} \varb(x)+\frac{M-1}{M} \covb(x)\Big] + O(\Deltab^2).
```

DiWA's key message is:

- weight averaging helps when diversity shift dominates,
- diversity reduces covariance,
- but weights must remain local enough to be averageable.

Empirically, the local table in [`literature/diwa_tex_source/tables/domainbed/db_main_results.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/tables/domainbed/db_main_results.tex) shows:

- SWAD average: `66.9`
- DiWA with random init, uniform `M=60`: `67.1`
- DiWA with LP init, uniform `M=60`: `68.0`

So the concrete gap is:

- multi-run diversity still beats SWAD,
- but single-run post-hoc DG has not cleanly closed that gap.

## 3. Fishr points to the missing object: cross-domain local geometry

The Fishr paper argues for **invariant gradient variances across domains**, and the ICML abstract states that Fishr "matches gradient variances across domains while provably inducing an invariance of the training dynamics" and empirically "yields a loss landscape that generalizes better to out-of-distribution domains."

Primary source:

- [Fishr: Invariant Gradient Variances for Out-of-distribution Generalization](https://proceedings.mlr.press/v162/rame22a.html)

This is training-time, not post-hoc, but it matters because it suggests the real object is not pooled flatness. It is **agreement of local geometry across domains**.

## 4. Model soups and later averaging work say selection matters

Relevant primary sources:

- [Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time](https://proceedings.mlr.press/v162/wortsman22a.html)
- [Not All Weights Are Worth Averaging](https://arxiv.org/abs/2410.22311)
- [A Simple Baseline for Bayesian Uncertainty in Deep Learning](https://papers.neurips.cc/paper_files/paper/2019/hash/118921efba23fc329e6560b27861f0c2-Abstract.html)
- [Loss Surfaces, Mode Connectivity, and Fast Ensembling of DNNs](https://papers.nips.cc/paper_files/paper/2018/hash/be3087e74e9100d4bc4c6268cdbe8456-Abstract.html)

These works support three facts:

- not all checkpoints or models should be averaged,
- low-barrier connectivity matters,
- posterior-style or trajectory-style averaging can outperform single checkpoints.

But these methods are mostly **domain-agnostic**. They do not solve the DG-specific question: which checkpoints are jointly stable for all source domains?

## 5. The local `TAWA` draft is not enough

The existing local draft at [`literature/tawa.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/tawa.tex) proposes a "quality-weighted" single-trajectory average. Its problem is not style; it is theory.

Its main theorem assumes a quality metric `q(theta_t)` such that OOD accuracy is already a strictly increasing convex function of `q`. That makes the "proof" of superiority circular:

- if the quality metric already tracks OOD accuracy, weighted averaging helps,
- but the hard problem is defining a non-circular metric.

So the real gap remains open.

# The New Principle

## Consensus-Volume Hypothesis

For source domains `1..I`, define the per-domain low-loss neighborhood around checkpoint `theta`:

```text
B_i(theta, eps) = {delta : L_i(theta + delta) <= L_i(theta) + eps }.
```

Define the **consensus volume**:

```text
V_cons(theta, eps) = Vol( intersection_{i=1}^I B_i(theta, eps) ).
```

My claim is:

> **OOD generalization depends more directly on `V_cons(theta, eps)` than on the volume of the pooled-loss basin.**

SWAD implicitly looks for large low-loss neighborhoods of the pooled risk. But pooled flatness can still hide domain-specific sharp directions.

The DG object should be the **intersection** of per-domain stable regions.

## Why pooled flatness is insufficient

Take a simple quadratic local model:

```text
L_i(theta + delta) = L_i(theta) + (lambda/2) (u_i^T delta)^2
```

with orthonormal `u_i`, one sharp direction per domain.

Then:

- each domain is sharp, but in a different direction;
- the pooled risk spreads that sharpness across directions;
- the pooled basin can look broad even though the region that is simultaneously good for all domains is much smaller.

In `I` effective sharp dimensions, the pooled stable radius scales like `sqrt(I)`, so pooled-volume estimates inflate by roughly `I^(I/2)` up to constants.

That is the exact failure mode SWAD's pooled-flatness viewpoint cannot distinguish.

# The Proposed Method: COWA

## Name

**`COWA` = Consensus Overlap Weight Averaging**

This is a single-run, post-hoc method. It assumes you already have a dense checkpoint trajectory, exactly in the operational regime where SWAD lives.

## Core objects at checkpoint `theta_t`

For each source domain `i` and checkpoint `t`, compute on a held-out split:

- domain loss: `L_{i,t}`
- domain gradient: `g_{i,t} = grad_theta L_i(theta_t)`
- domain empirical Fisher or Gauss-Newton approximation: `F_{i,t}`

Then define:

```text
Lbar_t = (1/I) sum_i L_{i,t}
gbar_t = (1/I) sum_i g_{i,t}
Fbar_t = (1/I) sum_i F_{i,t}
```

Domain-gradient disagreement:

```text
G_t = (1/I) sum_i || g_{i,t} - gbar_t ||^2_{(Fbar_t + lambda I)^(-1)}
```

Curvature-dispersion Jensen gap:

```text
J_t = log det(Fbar_t + lambda I) - (1/I) sum_i log det(F_{i,t} + lambda I) >= 0
```

Interpretation:

- `Lbar_t` measures source fit.
- `G_t` measures whether domains agree on the local descent direction.
- `log det(Fbar_t + lambda I)` measures overall sharpness or inverse shared volume.
- `J_t` measures whether each domain has similar local geometry, not just similar average curvature.

## Checkpoint score

Use:

```text
S_t = - Lbar_t - beta G_t - (tau/2) log det(Fbar_t + lambda I) - eta J_t
```

where:

- `beta` penalizes domain-gradient conflict,
- `tau` rewards broad shared volume,
- `eta` penalizes mismatch between domainwise local basins.

This is not a generic quality score. Each term comes from a DG-specific argument:

- low pooled risk,
- low domain conflict,
- large shared stable volume,
- small cross-domain curvature mismatch.

## Window selection and averaging

Let `t* = arg max_t S_t`.

Define a candidate contiguous window around `t*`:

```text
W = { t : S_t >= S_{t_star} - delta }
```

Then optionally enforce a low-barrier filter with source validation loss:

```text
Barrier(t, t*) =
max_{alpha in [0,1]} Lbar( alpha theta_t + (1-alpha) theta_{t_star} )
- max{ Lbar_t, Lbar_{t_star} }.
```

Keep only checkpoints with `Barrier(t, t*) <= b`.

Finally average:

```text
w_t proportional to exp(kappa S_t), t in W
theta_COWA = sum_{t in W} w_t theta_t.
```

This keeps the "post-hoc weight average" spirit of SWAD, but replaces validation-loss gating with a source-domain-consensus principle.

## Practical implementation

To keep it feasible:

- only score the last `K` checkpoints, for example the final `100-300`;
- estimate Fisher on the classifier plus last block first;
- use low-rank Lanczos or Hutchinson approximations for `log det`;
- use fixed held-out batches per domain for stable estimates;
- if compute is tight, replace full Fisher with diagonal Fisher plus top-`r` eigens.

# Theory Sketch

## Assumption A: local convex-hull shift

Assume that around a good checkpoint `theta_t`, the unseen target domain has local loss:

```text
L_T(theta_t + delta) = sum_i alpha_i L_i(theta_t + delta) + xi_t(delta),
```

where:

- `alpha` lies in the simplex,
- `|xi_t(delta)| <= eps_shift` for `||delta|| <= r`.

This is not "all DG is solved." It says only that the target's local geometry is approximately inside the hull of the source local geometries. If this is false, no post-hoc source-only method can fully guarantee success.

## Proposition 1: consensus volume gives a target-stable region

If `delta` belongs to every source-domain low-loss neighborhood:

```text
delta in intersection_i B_i(theta_t, eps),
```

then under Assumption A:

```text
L_T(theta_t + delta) <= sum_i alpha_i [L_i(theta_t) + eps] + eps_shift
```

and therefore `delta` is also target-stable up to `eps_shift`.

So `V_cons(theta_t, eps)` directly lower-bounds the size of a region provably stable for the target.

This is the conceptual jump beyond SWAD.

## Proposition 2: quadratic lower bound on consensus volume

Assume local second-order expansions:

```text
L_i(theta_t + delta) ~= L_i(theta_t) + g_i^T delta + (1/2) delta^T H_i delta.
```

Let:

```text
gbar = (1/I) sum_i g_i
Hbar = (1/I) sum_i H_i
kappa = max_i || g_i - gbar ||
rho = max_i || H_i - Hbar ||_op.
```

Then for every `i`:

```text
L_i(theta_t + delta)
<=
L_i(theta_t)
+ gbar^T delta
+ kappa ||delta||
+ (1/2) delta^T (Hbar + rho I) delta.
```

Therefore:

```text
{ delta :
gbar^T delta + kappa ||delta|| + (1/2) delta^T (Hbar + rho I) delta <= eps }
subseteq
intersection_i B_i(theta_t, eps).
```

So a lower bound on consensus volume is controlled by the **effective consensus precision**:

```text
H_eff = Hbar + rho I.
```

This immediately yields the first-principles takeaway:

> **Good DG checkpoints minimize not only pooled curvature `Hbar`, but also cross-domain curvature dispersion `rho`.**

Replacing `H_i` with empirical Fisher `F_i` gives the practical score used by COWA.

## Corollary: SWAD is the aligned-domain special case

If:

- `g_i = g_j` for all domains,
- `H_i = H_j` for all domains,

then `kappa = 0` and `rho = 0`, and the effective object collapses to pooled flatness.

So COWA strictly generalizes the SWAD intuition:

- **SWAD is right when all source domains already share local geometry.**
- **COWA matters when they do not.**

## Posterior interpretation

Using the local Gaussian approximation:

```text
q_{i,t}(delta) proportional to exp( -L_i(theta_t) - g_{i,t}^T delta - (1/2) delta^T F_{i,t} delta )
```

the product of domain posteriors has precision roughly `sum_i F_{i,t}` and mean shift driven by `sum_i g_{i,t}`.

Then:

- `log det(Fbar_t + lambda I)` acts like an inverse shared volume term,
- `G_t` penalizes domain disagreement in the local mean shift,
- `J_t` penalizes mismatch between the individual posteriors and their barycenter.

This is the Bayesian or Laplace-style interpretation of the same method.

# Why This Is Actually New

## Relative to SWAD

SWAD:

- optimizes pooled flatness,
- finds dense overfit-aware windows,
- uses no explicit per-domain local geometry.

COWA:

- optimizes per-domain basin overlap,
- explicitly measures domain-gradient and domain-curvature agreement,
- should distinguish "flat on average" from "simultaneously stable for all domains."

## Relative to DiWA

DiWA:

- reduces covariance by using multiple diverse runs,
- relies on cross-run diversity.

COWA:

- stays single-run,
- tries to recover the missing diversity signal from **cross-domain geometry along the trajectory** rather than from multiple independent runs.

## Relative to Fishr

Fishr:

- is a training-time regularizer,
- aligns gradient variances while training.

COWA:

- is fully post-hoc,
- scores checkpoints by where such alignment naturally emerges,
- can be layered on top of ERM, SWAD-style training, or other DG backbones.

## Relative to model soups and generic checkpoint selection

Model soups and later averaging papers say:

- selection matters,
- connectivity matters.

But they are not DG-specific. COWA adds the DG-specific ingredient:

- **the object to select for is source-domain consensus volume.**

## Relative to the existing local `TAWA` draft

`TAWA` uses:

- flatness,
- diversity,
- validation accuracy,

but without a non-circular DG-specific derivation.

COWA replaces the generic quality score with a concrete target:

- per-domain overlap of low-loss neighborhoods.

# Why This Could Beat SWAD on Both IID and OOD

The expected mechanism is:

1. SWAD finds flat pooled basins.
2. Some of those basins are still anisotropic in domain-specific directions.
3. COWA prefers checkpoints where source domains agree on which directions are safe.
4. Averaging inside that window yields:
   - better IID because the basin is still broad,
   - better OOD because the breadth is shared across domains, not just pooled.

This is also consistent with the empirical clue from the local sources:

- `CORAL + SWAD` beats plain SWAD,
- Fishr improves DG by matching domainwise gradient statistics,
- DiWA beats SWAD by injecting diversity across runs.

COWA tries to recover the missing piece in single-run form.

# Failure Modes

This is not magic. The main failure modes are:

## 1. Correlation shift dominates

DiWA explicitly argues that weight averaging helps under diversity shift but not correlation shift. If the target label mechanism is outside the source-domain hull, consensus-volume methods can still fail.

## 2. Fisher estimates are too noisy

On very small per-domain validation splits, the score may be unstable. The remedy is:

- fixed held-out batches,
- smoothing over nearby checkpoints,
- diagonal plus low-rank Fisher approximations.

## 3. The single run never visits a high-consensus region

Then multi-run diversity may still be necessary, and DiWA can remain stronger.

## 4. Locality is violated inside the selected set

Then weighted averaging can still break. This is why the low-barrier filter is included.

# Falsifiable Predictions

If this idea is real, the following should happen:

1. Across checkpoints in one run, `S_t` should correlate with held-out OOD accuracy better than SWAD's validation-loss heuristic.
2. COWA-selected windows should have:
   - smaller `G_t`,
   - smaller `J_t`,
   - lower interpolation barriers,
   than SWAD-selected windows.
3. Gains should be largest on diversity-shift-heavy datasets such as PACS, OfficeHome, and DomainNet.
4. Gains should shrink on correlation-shift-heavy benchmarks such as ColoredMNIST.
5. The best COWA checkpoints should appear near, but not necessarily exactly at, SWAD's start-end interval.

If these predictions fail, abandon the method quickly.

# Experiment Plan

## Baselines

- ERM last checkpoint
- SWA
- SWAD
- DiWA if compute permits
- domain-agnostic weighted checkpoint averaging
- local `TAWA` draft if you want a direct negative control

## Datasets

- PACS
- VLCS
- OfficeHome
- TerraIncognita
- DomainNet
- ColoredMNIST as a stress test for correlation shift

## Main ablations

1. `risk only`:
   - `S_t = -Lbar_t`
2. `risk + flatness`:
   - `S_t = -Lbar_t - (tau/2) log det(Fbar_t + lambda I)`
3. `risk + flatness + gradient consensus`
4. `risk + flatness + curvature Jensen gap`
5. full `COWA`

## Diagnostics

- Spearman correlation between checkpoint score and OOD accuracy
- visualization of `G_t`, `J_t`, and OOD over time
- interpolation barrier plots between selected checkpoints
- principal-angle alignment of top Fisher eigenspaces across domains

## Minimal success bar

To count as serious:

- average OOD should beat SWAD by at least `0.5-1.0` points on the main DomainBed suites,
- IID should be flat or improved,
- the score should predict OOD better than SWAD's window heuristic.

If it only matches SWAD or only works on one dataset, it is not the breakthrough you want.

# Recommended Next Step

The fastest serious next step is not a full paper draft. It is:

1. implement the checkpoint scorer,
2. test checkpoint-score correlation on one existing trajectory,
3. compare the best COWA checkpoint/window against the SWAD window on PACS and OfficeHome,
4. only then scale to full DomainBed.

That will tell you quickly whether the principle is real.

# Sources

Local primary sources used:

- [`literature/swad_tex_source/main.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/main.tex)
- [`literature/swad_tex_source/2.theoretical_analysis.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/2.theoretical_analysis.tex)
- [`literature/swad_tex_source/3.method.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/3.method.tex)
- [`literature/swad_tex_source/4.empirical_results.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/4.empirical_results.tex)
- [`literature/swad_tex_source/5.discussion.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/5.discussion.tex)
- [`literature/swad_tex_source/tables/besttable.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/swad_tex_source/tables/besttable.tex)
- [`literature/diwa_tex_source/sections/02_theory.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/02_theory.tex)
- [`literature/diwa_tex_source/sections/03_approach.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/03_approach.tex)
- [`literature/diwa_tex_source/sections/04_analysis.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/sections/04_analysis.tex)
- [`literature/diwa_tex_source/tables/domainbed/db_main_results.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/diwa_tex_source/tables/domainbed/db_main_results.tex)
- [`literature/tawa.tex`](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/literature/tawa.tex)

Web primary sources checked:

- [SWAD arXiv page](https://arxiv.org/abs/2102.08604)
- [Fishr at PMLR](https://proceedings.mlr.press/v162/rame22a.html)
- [Model soups at PMLR](https://proceedings.mlr.press/v162/wortsman22a.html)
- [Not All Weights Are Worth Averaging](https://arxiv.org/abs/2410.22311)
- [SWAG NeurIPS page](https://papers.neurips.cc/paper_files/paper/2019/hash/118921efba23fc329e6560b27861f0c2-Abstract.html)
- [Mode connectivity NeurIPS page](https://papers.nips.cc/paper_files/paper/2018/hash/be3087e74e9100d4bc4c6268cdbe8456-Abstract.html)
- [Diverse Weight Averaging arXiv page](https://arxiv.org/abs/2206.08394)
