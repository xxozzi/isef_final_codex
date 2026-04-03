---
title: Trajectory Spectral Filtering for Single-Run Post-Hoc Domain Generalization
description: Research proposal for a stripped-down spectral checkpoint-trajectory method that filters temporal oscillations in weight updates rather than selecting or averaging a subset of safe checkpoints.
created: 2026-04-02 15:30
last_modified: 2026-04-02 17:05
last_modified_by: codex
status: draft
related_files:
  - claude_workspace/results/results_ledger.md
  - claude_workspace/results/swing_lessons_learned.md
key_functions:
  - Define a non-SWAD post-hoc DG proposal based on checkpoint-axis spectral filtering
  - State assumptions, theorem targets, implementation plan, and failure modes
  - Record concessions and arguments against the proposal
latest_change: Revised after harsh review to narrow the novelty claim, strengthen theory wording, and add stronger baseline and failure criteria.
---

# Trajectory Spectral Filtering

## 1. Executive Summary

This memo proposes a new post-hoc method for single-run domain generalization:

> **Trajectory Spectral Filtering (TSF): treat the checkpoint trajectory as a time signal in weight-update space, remove temporally unstable components, and reconstruct one final model from the filtered update path.**

The proposal is intentionally **not** another subset-soup selector, another safe-basin center finder, or another continuous post-hoc weight optimizer. The project evidence now strongly suggests that those families collapse back toward the same effective mechanism as SWAD-like safe-basin averaging. TSF is an attempt to move to a different operator on the checkpoint trajectory:

- not "which checkpoints should we average?"
- but "which temporal components of the learning path should survive into the final model?"

The proposal is also intentionally **stripped down** from the more speculative "Spectral Trajectory Extrapolation" idea. The spectral filtering part is kept. The infinite-horizon extrapolation part is removed.

The core claim is modest:

- some checkpoint-to-checkpoint motion reflects persistent, low-complexity drift;
- some motion reflects oscillatory detours, minibatch noise, or unstable late fitting;
- filtering the oscillatory component of the *update path* can produce a final model that is better than the raw final checkpoint and meaningfully different from plain averaging.

This memo does **not** claim the method is already validated. It is a research proposal. The strongest positive case is conceptual and geometric. The strongest negative case is that checkpoint-axis frequency may not align with robust-vs-spurious structure in a useful enough way.

## 2. Why This Proposal Exists

The local project record now shows a pattern:

- safe checkpoint pools are real and useful;
- uniform averaging inside those pools is a very strong baseline;
- methods that add complicated geometry on top of that baseline have not clearly justified themselves.

The clearest statements are in:

- [results_ledger.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/results_ledger.md)
- [swing_lessons_learned.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/results/swing_lessons_learned.md)

In particular:

- `SWING` did not clearly and consistently beat `SWING-uniform`.
- `CHOIR` lost clearly to `CHOIR-uniform`.
- `PRISM` is competitive and interesting, but its gains are still small enough that the project keeps collapsing back toward "safe basin + uniform/central aggregation."

So the next idea should not merely be:

- "a better subset scorer,"
- "a better soup weighting rule,"
- or "a better safe-basin correction."

Instead, the next idea should change the operator applied to the post-hoc trajectory object rather than merely changing how checkpoints are averaged or scored.

TSF does that by operating on the **temporal structure of checkpoint updates**.

## 3. Position Relative to Existing Literature

### 3.1 What existing checkpoint methods do

Existing checkpoint-based post-hoc methods mostly do one of the following:

1. **Average trajectory points**
   - SWA averages checkpoints along a late trajectory and argues this finds broader optima.
   - Source: [Izmailov et al., UAI 2018](https://auai.org/uai2018/proceedings/papers/313.pdf).
   - SWAD extends this logic to domain generalization by seeking flatter minima: [SWAD OpenReview](https://openreview.net/forum?id=zkHlu_3sJYU).
   - EMA is another strong temporal smoothing baseline over iterates:
     [Exponential Moving Average of Weights in Deep Learning: Dynamics and Benefits](https://openreview.net/forum?id=2M9CUnYnBA).

2. **Average a selected set of checkpoints or models**
   - Model soups average selected models without extra inference cost: [Model Soups](https://proceedings.mlr.press/v162/wortsman22a.html).
   - DiWA averages diverse independently trained models for OOD generalization: [DiWA NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/file/46108d807b50ad4144eb353b5d0e8851-Paper-Conference.pdf).

3. **Approximate posterior structure over iterates**
   - SWAG fits first and second moments of SGD iterates: [SWAG OpenReview](https://openreview.net/forum?id=rkeMsHBlUS).

4. **Perform spectral or structured editing of a single update or merged models**
   - MonoSoup uses SVD of a single checkpoint update to rebalance ID/OOD behavior: [MonoSoup OpenReview](https://openreview.net/forum?id=ICANwnoGgN).
   - TIES resolves sign conflicts across task-specific models: [TIES OpenReview](https://openreview.net/forum?id=xtaX3WyCj1).

5. **Learn or search linear combinations of checkpoints**
   - LCSC combines saved checkpoints for diffusion/consistency models by search: [LCSC OpenReview](https://openreview.net/forum?id=QowsEic1sc).
   - Fast Geometric Ensembling and related methods also exploit multiple points on a training path:
     [FGE NeurIPS 2018](https://papers.neurips.cc/paper/8095-loss-surfaces-mode-connectivity-and-fast-ensembling-of-dnns).

6. **Use trajectory information as a structured diagnostic object**
   - Learning trajectories can predict generalization behavior:
     [Learning Trajectories are Generalization Indicators](https://openreview.net/forum?id=YdfcKb4Wif).
   - Learning trajectories can even be transferred or reused in other settings:
     [Transferring Learning Trajectories of Neural Networks](https://openreview.net/forum?id=bWNJFD1l8M).

### 3.2 What this proposal does differently

TSF should **not** be presented as leaving checkpoint-trajectory methods entirely. The honest claim is narrower:

> It applies an explicit spectral filter to the **groupwise checkpoint-to-checkpoint update sequence** and reconstructs one final model from the filtered path.

It does not:

- average a subset of checkpoints directly;
- fit a posterior over iterates;
- perform task-model merging;
- or search arbitrary coefficients over checkpoints.

Instead, for each parameter group, it considers the discrete update sequence
\[
v_g^{(t)} = w_g^{(t+1)} - w_g^{(t)}, \qquad t=1,\ldots,N-1
\]
and filters this sequence along the checkpoint axis before reconstructing the final weight.

This is the proposal's main novelty claim.

### 3.3 Honest novelty claim

As of **April 3, 2026**, I did **not** find a published paper that exactly matches the following construction:

- take one run's checkpoint-to-checkpoint update sequence,
- group parameters into architecture-aligned blocks,
- apply a fixed orthonormal transform along the checkpoint axis,
- attenuate selected temporal modes,
- and reconstruct a single final model from the filtered update path.

That is a **narrow constructional novelty claim**.

It is **not** a claim that:

- trajectory information is a new object,
- post-hoc use of iterates is new,
- or spectral editing in weight space is new.

### 3.4 Adjacent ideas that support the motivation but do not already implement this method

Several papers support parts of the motivation:

- Learning trajectories contain information about generalization:
  [Learning Trajectories are Generalization Indicators](https://openreview.net/forum?id=YdfcKb4Wif)
- Deep networks tend to learn simpler/low-frequency structure first:
  [A Closer Look at Memorization in Deep Networks](https://proceedings.mlr.press/v70/arpit17a)
  and [On the Spectral Bias of Deep Neural Networks](https://www.arisbar.org/publication/spectral-bias/)
- SGD iterate geometry can be useful beyond a single endpoint:
  [SWA in PyTorch](https://pytorch.org/blog/stochastic-weight-averaging-in-pytorch/)
  and [SWAG OpenReview](https://openreview.net/forum?id=rkeMsHBlUS)

But there is also an important constraint from the literature:

- harmful spurious features need not be late or hard; they can be easy and early:
  [Beyond Distribution Shift: Spurious Features Through the Lens of Training Dynamics](https://openreview.net/forum?id=Tkvmt9nDmB)

But none of these, as far as I found, defines the final deployed model by **low-pass filtering the checkpoint-update sequence of one run**.

That novelty claim should still be stated carefully:

> I did not find a published paper that exactly matches this construction, but the proposal lives near several adjacent families and therefore carries moderate novelty risk.

## 4. The Core Construction

### 4.1 Setup

Let the training run produce checkpoints
\[
\theta^{(1)}, \theta^{(2)}, \ldots, \theta^{(N)}.
\]

Partition the parameters into groups
\[
g \in \mathcal G.
\]

A group can be:

- a convolutional output channel,
- an attention head,
- an MLP block,
- a layer matrix,
- or another architecture-aligned tensor block.

This proposal deliberately avoids scalar-level filtering because scalar parameters are too sensitive to symmetries, rescalings, and noise.

For group \(g\), let
\[
w_g^{(t)} \in \mathbb R^{d_g}
\]
denote the flattened parameter vector of that group at checkpoint \(t\).

Define the checkpoint-to-checkpoint update sequence:
\[
v_g^{(t)} = w_g^{(t+1)} - w_g^{(t)}, \qquad t=1,\ldots,N-1.
\]

Stack these updates row-wise into a matrix
\[
V_g \in \mathbb R^{(N-1)\times d_g}.
\]

### 4.2 Spectral transform along the checkpoint axis

Let \(C \in \mathbb R^{(N-1)\times(N-1)}\) be an orthonormal transform on the checkpoint axis, such as a DCT matrix.

Transform the update sequence:
\[
\widehat V_g = C V_g.
\]

Each row of \(\widehat V_g\) corresponds to one temporal frequency band of the update path for group \(g\).

### 4.3 Low-pass filtering

Apply a diagonal spectral filter
\[
H_g = \operatorname{diag}(h_{g,1},\ldots,h_{g,N-1}), \qquad 0\le h_{g,j}\le 1.
\]

The filtered spectral coefficients are
\[
\widetilde{\widehat V}_g = H_g \widehat V_g.
\]

Then invert the transform:
\[
\widetilde V_g = C^\top \widetilde{\widehat V}_g.
\]

This yields a filtered update sequence
\[
\widetilde v_g^{(1)}, \ldots, \widetilde v_g^{(N-1)}.
\]

### 4.4 Final model reconstruction

The final filtered group is reconstructed by summing the filtered updates:
\[
w_g^\star
=
w_g^{(1)} + \sum_{t=1}^{N-1} \widetilde v_g^{(t)}.
\]

The final filtered model is
\[
\theta^\star = \{w_g^\star : g\in\mathcal G\}.
\]

This is important:

- the method uses the **entire observed trajectory**;
- it does **not** extrapolate beyond the final checkpoint;
- it does **not** require choosing a subset of checkpoints to average.

## 5. Why We Strip Out Extrapolation

The original spectral-trajectory idea also proposed fitting a smooth curve and taking its infinite-time limit.

That part is removed.

### 5.1 What is kept

- checkpoint trajectory as a signal
- temporal spectral decomposition
- suppression of unstable components
- one final reconstructed model

### 5.2 What is removed

- per-parameter exponential-asymptote fitting
- claims about recovering the "true" infinite-time resting state
- any step that requires leaving the observed trajectory support

### 5.3 Why it must be removed

1. **The asymptotic model is too strong.**
   There is no solid reason to believe a deep-network parameter group follows a simple exponential law toward a meaningful asymptote.

2. **Extrapolation leaves the observed region.**
   Filtering observed motion is one thing. Predicting a future point outside the observed checkpoint cloud is much riskier.

3. **The novelty does not depend on it.**
   The novel part is already the checkpoint-axis spectral filtering of update trajectories.

4. **The theorem target becomes cleaner without it.**
   We can analyze bias-variance tradeoffs of filtered observed trajectories. We do not need to justify infinite-horizon recovery.

## 6. The Research Hypothesis

The central hypothesis is:

> **For at least some parameter groups, the checkpoint-update sequence can be decomposed into a low-band drift component that carries stable task-relevant progress and a higher-band oscillatory component that reflects SGD noise, mini-batch conflict, or unstable late specialization.**

If that is true, then low-pass filtering the update sequence can improve the final model.

This is a hypothesis, not an established theorem.

The main motivational arguments are:

1. **Trajectory information matters.**
   Learning trajectories have predictive value for generalization: [Learning Trajectories are Generalization Indicators](https://openreview.net/forum?id=YdfcKb4Wif).

2. **Simple/shared structure is often learned before idiosyncratic fitting.**
   See [Arpit et al. 2017](https://proceedings.mlr.press/v70/arpit17a) and [spectral bias work](https://www.arisbar.org/publication/spectral-bias/).

3. **Averaging works in part because it suppresses noisy endpoint variation.**
   See [SWA](https://auai.org/uai2018/proceedings/papers/313.pdf), [SWAG](https://openreview.net/forum?id=rkeMsHBlUS), and [EMA of Weights](https://openreview.net/forum?id=2M9CUnYnBA).

What is **not** justified directly by the literature:

- that checkpoint-axis high frequency specifically equals "spurious features"
- that every oscillation is bad
- that low-pass filtering will always outperform plain averaging
- that early or low-band structure is automatically the structure that transfers best under shift

Those stronger claims should be avoided.

## 7. Assumptions

### Assumption A1: update decomposition as a toy signal model

For each group \(g\),
\[
v_g^{(t)} = s_g^{(t)} + \varepsilon_g^{(t)},
\]
where:

- \(s_g^{(t)}\) is a low-band signal component,
- \(\varepsilon_g^{(t)}\) is a higher-band oscillatory component with mean near zero over the checkpoint axis.

This should be read as a **toy stochastic-process model on the observed checkpoint sequence**, not as a literal semantic decomposition into "robust" and "spurious" features.

### Assumption A2: checkpoint density

The checkpoints are dense enough in training time that temporal oscillation is actually observable. If checkpoints are too sparse, the transform basis cannot meaningfully separate low- and high-band behavior.

### Assumption A3: local risk smoothness around a reference path or endpoint

There exists a reference endpoint
\[
w_g^\dagger = w_g^{(1)} + \sum_{t=1}^{N-1} s_g^{(t)}
\]
such that robust loss under source-supported shifts is locally smooth around the full parameter vector \(w^\dagger\).

### Assumption A4: architecture-aligned grouping

Grouping is chosen so that group trajectories are more stable and more semantically meaningful than raw scalar trajectories.

## 8. Why these assumptions are at least plausible

### 8.1 Why A1 is plausible as a signal model

It is not absurd to believe that the update path contains a smooth trend plus oscillation:

- SWA and SWAG both treat iterates as carrying structured information beyond the final endpoint.
- The SWAG paper explicitly models first and second moments of SGD iterates and argues they reflect stationary structure near good solutions: [SWAG OpenReview](https://openreview.net/forum?id=rkeMsHBlUS).
- The trajectory generalization paper shows that trajectory complexity carries generalization information: [Learning Trajectories are Generalization Indicators](https://openreview.net/forum?id=YdfcKb4Wif).

These papers do **not** prove A1, but they make it reasonable enough to study as a denoising model.

### 8.2 Why A2 is plausible

The project already operates in a dense-checkpoint regime for replay methods, so the infrastructure is compatible with this assumption.

### 8.3 Why A3 is plausible in a local perturbation sense

Most local post-hoc methods already rely on some version of local smoothness or basin structure. TSF does not require a stronger smoothness story than many existing post-hoc weight methods; it only needs a local excess-risk bound near the filtered endpoint.

### 8.4 Why A4 is plausible

Groupwise processing is standard practice when scalar parameters are too unstable or too symmetry-sensitive. This is already implicit in many model-merging and spectral-editing methods.

## 9. Theorem Targets

The proposal does **not** need a grand theorem like "TSF finds the true robust model."

It needs a modest, correct theorem.

### 9.1 Bias-variance decomposition for filtered trajectory reconstruction

Fix one group \(g\). Let the spectral coefficients of the signal and oscillatory parts be
\[
\widehat s_{g,j}, \qquad \widehat \varepsilon_{g,j}.
\]

For a hard low-pass filter keeping the first \(K_g\) modes, define the filtered reconstruction \(w_g^\star\).

Then a target theorem is:

\[
\mathbb E\|w_g^\star - w_g^\dagger\|^2
\le
\underbrace{\sum_{j>K_g}\|\widehat s_{g,j}\|^2}_{\text{truncation bias}}

+
\underbrace{\sum_{j\le K_g}\mathbb E\|\widehat\varepsilon_{g,j}\|^2}_{\text{retained variance}}.
\]

The raw final checkpoint keeps all frequency bands:
\[
\mathbb E\|w_g^{(N)} - w_g^\dagger\|^2
=
\sum_{j=1}^{N-1}\mathbb E\|\widehat\varepsilon_{g,j}\|^2
\]
under zero-bias signal reconstruction.

So if high-band oscillatory energy dominates high-band signal energy, some cutoff \(K_g < N-1\) improves the mean-squared reconstruction error to the latent smoothed path under this toy model.

### 9.2 Local loss transfer under smoothness

Suppose for every source-supported reweighting \(r\) in an allowed shift family \(\mathcal R\),
\[
L_r(\theta) - L_r(\theta^\dagger)
\le
G_r\|\theta-\theta^\dagger\|

+
\frac{\beta_r}{2}\|\theta-\theta^\dagger\|^2.
\]

Then:
\[
\sup_{r\in\mathcal R}\big(L_r(\theta^\star)-L_r(\theta^\dagger)\big)
\le
G_{\max}\|\theta^\star-\theta^\dagger\|

+
\frac{\beta_{\max}}{2}\|\theta^\star-\theta^\dagger\|^2.
\]

So if TSF reduces parameter error to a locally good reference endpoint \(\theta^\dagger\), it also improves a worst-case local robust-risk bound.

This is the correct level of claim only if it is presented as **conditional**.

### 9.3 A more defensible theorem target

The most defensible theorem is not a DG theorem. It is a **late-trajectory denoising theorem**:

- under a toy process model on the observed checkpoint sequence,
- TSF reduces reconstruction error to a latent smoothed path compared with the raw endpoint,
- and any downstream improvement in robust loss is then a conditional local-perturbation consequence.

That is weaker than the original ambition, but more rigorous.

### 9.4 What should not be claimed

The proposal should **not** claim:

- that low-frequency checkpoint motion is inherently causal or invariant;
- that TSF universally beats SWA/SWAD;
- that the checkpoint axis admits a universal physical frequency interpretation;
- that the filtered endpoint is the true optimum.

## 10. Practical Design Choices

### 10.1 Filtering object

The proposal should filter **updates**, not absolute weights.

This is preferable because:

- absolute checkpoint trajectories are dominated by global drift;
- update sequences make oscillation and drift more separable;
- reconstructing from filtered updates preserves path information while avoiding direct averaging of early poor checkpoints.

### 10.2 Grouping

Recommended grouping:

- CNNs: output channels or full convolution kernels
- Transformers: attention heads, MLP matrices, or full layer projections
- generic fallback: full tensor blocks

### 10.3 Transform

Default transform:

- DCT along the checkpoint axis

Reasons:

- orthonormal
- simple
- deterministic
- no learned decomposition required
- natural low-pass interpretation

### 10.4 Filter family

Three practical options:

1. Hard low-pass cutoff:
   \[
   h_{g,j} = \mathbf 1\{j\le K_g\}
   \]
2. Soft polynomial decay:
   \[
   h_{g,j} = \frac{1}{1+\lambda(j/(N-1))^p}
   \]
3. Energy-threshold truncation:
   choose \(K_g\) so that retained spectral energy exceeds a fraction \(\rho\)

### 10.5 Hyperparameter selection

Two variants are worth proposing:

- **TSF-DF**: fully data-free with a fixed energy threshold \(\rho\)
- **TSF-DG**: choose a small set of filtering strengths using a pooled source holdout split without domain labels

The second variant is more defensible for domain generalization benchmarking.

### 10.6 BatchNorm

If BatchNorm is present, refresh BN statistics after constructing the filtered model:

- PyTorch explicitly notes this for SWA:
  [PyTorch SWA blog](https://pytorch.org/blog/stochastic-weight-averaging-in-pytorch/)

## 11. Why This Could Help IID and OOD

### 11.1 IID case

If endpoint checkpoints contain accumulated oscillatory noise, filtering can reduce variance in the final weights while keeping the broad drift that defines the learned solution.

That is similar in spirit to why SWA can help, but the mechanism is different:

- SWA averages points;
- TSF removes unstable *trajectory frequencies*.

### 11.2 OOD case

The OOD argument is weaker and must be stated carefully.

The proposal is:

- if unstable late motion partly corresponds to narrow, nonpersistent fitting behavior,
- then suppressing that motion may help under shift.

This is supported only indirectly by:

- memorization/simple-patterns-first results,
- spectral bias literature,
- and trajectory/generalization literature.

It is not a proven consequence.

There is also a real counterargument from the literature:

- harmful spurious structure can be easy and early, not only late and unstable:
  [Murali et al. 2023](https://openreview.net/forum?id=Tkvmt9nDmB)

So the OOD case should be treated as an empirical question, not a theorem-level interpretation.

## 12. Why This Is Not Just SWAD Again

This is the main project-level question.

TSF is not:

- a safe-window average,
- a subset selector,
- a center finder inside a safe basin,
- or a small correction around a safe-basin mean.

It uses the **entire observed training trajectory** and constructs one model by filtering the temporal structure of its updates.

That is the strongest reason to study it now:

- it does not collapse back to the locally falsified template
  "safe basin + clever correction."

At the same time, this is also the proposal's most fragile choice.

- if the only successful variant ends up using a late safe window, then TSF has collapsed back toward ordinary smoothing on a local basin and should not be treated as a distinct headline method.

## 13. Experimental Plan

### 13.1 Baselines

At minimum:

- final checkpoint
- EMA over checkpoints or updates
- simple moving average over updates
- SWA / SWAD
- uniform average over a late window
- same-run safe-pool uniform average
- PRISM if using pooled-source holdout
- MonoSoup if adaptable

### 13.2 Core ablations

1. Filter updates vs filter absolute weights
2. Full trajectory vs late subsequence
3. Groupwise vs scalar
4. Hard low-pass vs soft shrinkage
5. Data-free vs pooled-source tuning
6. With and without BN refresh
7. TSF vs update EMA / moving-average smoothing

### 13.3 Diagnostics

The method should log:

- retained frequency energy by group
- spectral energy profile by layer/group
- distance from final checkpoint
- distance from plain full-trajectory mean
- held-out source loss before and after filtering
- BN refresh delta

### 13.4 Strong falsification tests

The proposal should be rejected quickly if any of the following occurs:

1. It collapses numerically to plain averaging.
2. It is highly sensitive to checkpoint density.
3. It consistently hurts held-out source loss while not helping OOD.
4. Any improvement disappears after comparing against a simple moving average over updates.
5. The only working version is a late safe-window variant that behaves like ordinary smoothing.

## 14. Main Risks

1. **Checkpoint-axis frequency may be the wrong object.**
   High temporal frequency in updates may not correspond to harmful fitting.

2. **Whole-trajectory filtering may reintroduce bad early behavior.**
   Even though the method filters updates rather than weights, this remains a real risk.

3. **Grouping may dominate the effect.**
   The apparent success may be due more to a good grouping heuristic than to the spectral idea itself.

4. **The method may collapse to a smoothed version of the final checkpoint with negligible gains.**

5. **Novelty risk is real.**
   The proposal is close enough to SWA/SWAG/MonoSoup/trajectory-merging ideas that reviewers may see it as a repackaging unless the actual construction and evidence are sharp.

6. **The nearest true baseline may be ordinary update smoothing, not a new DG method.**
   If TSF cannot beat EMA or moving-average smoothing, the spectral claim collapses.

## 15. Strongest Arguments Against the Proposal

These are the arguments a hostile reviewer should raise.

### 15.1 "The checkpoint axis has no principled frequency semantics."

This is the strongest theoretical objection.

Response:
- true in general;
- the proposal should not claim universal semantics;
- it should claim only that temporal filtering may separate smooth drift from oscillatory motion in some runs.

### 15.2 "This is just signal-processing style dressing on trajectory smoothing."

Response:
- partly true;
- the method must empirically show behavior different from plain moving averages and SWA-like averaging.

### 15.3 "The full trajectory includes checkpoints from incompatible regimes."

Response:
- valid;
- filtering updates rather than absolute weights helps, but does not fully eliminate the risk.

### 15.4 "You are borrowing motivation from input-frequency spectral bias, but filtering is done in checkpoint time."

Response:
- also true;
- this must be stated as an analogy/motivation, not a theorem.

### 15.5 "MonoSoup and related work already do spectral post-hoc editing."

Response:
- yes, and this is the closest prior-art family;
- the distinction is that MonoSoup performs a spectral decomposition of a **single update** or layer delta, whereas TSF filters the **entire sequence of checkpoint updates**.

### 15.6 "This may just be a complicated linear smoother."

Response:
- this is the most dangerous alternative explanation;
- the proposal should explicitly benchmark against EMA and moving-average update smoothing;
- if TSF does not beat them clearly, the proposal should be dropped.

## 16. Concessions

The proposal should explicitly concede the following.

1. **This is not yet a proven best-bet method.**
   It is a sharpened research hypothesis.

2. **The strongest support is conceptual, not empirical.**
   The project does not yet have evidence that checkpoint-axis high frequencies are a useful removal target.

3. **The OOD story is more speculative than the IID story.**
   The bias-variance denoising argument is cleaner than the domain-generalization argument.

4. **The method may fail precisely because the project has already shown that simple averaging is extremely strong.**
   If the key benefit of checkpoint methods is just broad interior averaging, TSF may not add enough.

5. **The closest comparison may be to ordinary smoothing, not to a new family.**
   If EMA or moving-average update smoothing matches TSF, then TSF is not a new practical method.

6. **A negative result would still be informative.**
   If TSF fails, that would be evidence that full-trajectory temporal filtering does not unlock a new signal beyond what safe-basin averaging already captures.

## 17. Bottom Line

TSF is worth studying because:

- it is outside the specific safe-basin-correction template that failed locally,
- it keeps one final deployable model,
- it uses a mathematically clean object,
- and it can be stripped down enough to avoid the worst speculative steps.

TSF is risky because:

- its key modeling assumption may simply be wrong,
- its OOD justification is only indirect,
- and it may end up being a fancy way to do something that plain averaging already does well enough.

That is the correct scientific position:

> **Trajectory Spectral Filtering is a plausible non-SWAD post-hoc DG direction, but it should be treated as a carefully bounded research proposal, not as a solved method.**
