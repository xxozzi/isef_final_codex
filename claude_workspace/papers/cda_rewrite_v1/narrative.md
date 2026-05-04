# CDA Rewrite Narrative

This file pins down the implicit line of reasoning for the rewritten paper. It is not prose for the final manuscript. It is the argument the manuscript must make through structure, notation, results, and figures.

## Status

Yes, we now have an explicit narrative for the rewrite, but it must be anchored outside CDA's own mechanics:

> Source-only post-hoc deployment is an underidentified model-selection problem. A completed DG run can produce many plausible checkpoints or soups, target labels are unavailable, and scalar source validation averages collapse a domain-wise evidence vector into one number. CDA starts from this external bottleneck: when several candidates look comparable under the usual source aggregate, use the domain-wise source loss vector rather than discarding it. Source-composition robustness is CDA's conditional way of scalarizing that vector for mergeable checkpoint banks, not the reason the problem exists.

The current draft should not claim that CDA discovers the target domain. It should not claim that prior work ignores source mixtures. It should not imply that SWAD, DiWA, EoA, or model soups are deficient because they did not optimize CDA's criterion. It should claim something narrower: source-only checkpoint deployment is often decided by insufficient scalar evidence, and CDA evaluates whether a domain-wise source-risk criterion improves that decision.

## Final Method Decision

The paper-facing CDA method is frozen as:

\[
\text{CDA}=\text{VSC}+\text{CDA-BD}.
\]

The implementation mapping is recorded in `misc/method/final_method.md`. `CDA-Piv` may appear as an ablation, but the main method is `VSC + CDA-BD`.

## Core Narrative

1. **DG has become harder to claim convincingly.**
   DomainBed showed that many train-time DG algorithms weaken under controlled model selection, while ERM remains strong. SWAD shifted the single-run post-hoc DG baseline toward checkpoint averaging. Other single-run averaging neighbors exist, including EoA's single-run simple moving average component, DNA's single-run longitudinal averaging, and ERM++'s model-parameter averaging. DiWA, full EoA-as-ensemble, model soups, WiSE-FT, MonoSoup, data-free DG, and large-learning-rate flat-minima methods are important related deployment or averaging references, but they either use multiple trained models, assume a pretrained-and-finetuned pair, train separate source models, alter the optimizer/training procedure, or operate outside the standard multi-source DG setting. They should not count as peer single-run baselines for CDA unless the implementation is converted to the same one-run, source-only checkpoint-bank protocol. A CDA paper must begin from this stricter evaluation framing, not from a generic "DG is hard" paragraph.

2. **Deployment often starts after training has already happened.**
   A completed run produces a checkpoint bank
   \[
   \mathcal{B}=\{\theta_1,\ldots,\theta_K\}.
   \]
   The post-hoc decision is to choose a deployed model from this bank, usually by selecting or averaging checkpoints. This is narrower than train-time DG, but it is operationally meaningful.

3. **The external problem is source-only selection under scalar underidentification.**
   Standard source-only selection typically collapses validation evidence across domains into an aggregate score. That scalar is useful, but it can underidentify the deployment choice: two candidates can have similar source average while making different errors across the source domains, and those differences are invisible after averaging. This problem exists before CDA is introduced. DomainBed makes model selection central; QRM and DRO-style work emphasize that domain-wise risks contain information beyond a single average; DGSAM-style work shows that aggregate objectives can hide domain-wise fragility. The motivating question is therefore not "why did prior work not use CDA?" It is: when a fixed checkpoint bank contains candidates that are similar under source-average validation, can domain-wise source evidence improve source-only deployment selection?

4. **The general solution path is to preserve and use domain-wise source evidence.**
   The source-specific warrant is recorded in `misc/literature_notes/modern_literature_refresh.md`. Multi-source adaptation, QRM/EQRM, GroupDRO, VREx, WDRDG, MODE, DomainBed, SWAD, DiWA, EoA, and model soups each constrain the claim. The common lesson for CDA is not that these papers are missing source reweighting. The lesson is that source-domain risks, model-selection rules, and weight-space deployment objects must be treated explicitly. CDA narrows this to a fixed single-run checkpoint bank, where the observable evidence is the vector \(L(\theta)\) rather than only its mean.

5. **Source-composition robustness is CDA's conditional criterion, not a premise the reader has to accept on faith.**
   CDA chooses one way to scalarize the source-loss vector: evaluate local robustness to source-domain reweightings while accounting for soup mergeability. The paper must motivate this from three places: prior domain-wise risk literature, the observed source-risk geometry of the checkpoint bank, and post-hoc residual diagnostics. For a retained candidate family, the working condition is
   \[
   L_T(\theta)
   \le
   \alpha_T^\top L(\theta)+\epsilon_{\mathrm{app}},
   \qquad
   \alpha_T=\bar u+\delta,\quad
   \mathbf{1}^\top\delta=0,\quad
   \|\delta\|_2\le\rho .
   \]
   This is not an absolute guarantee about the target domain and not a claim that CDA estimates \(\alpha_T\). It is a conditional deployment model. The paper must justify it empirically by reporting \(\epsilon_{\mathrm{app}}\), showing when source-risk geometry has signal, and including at least one failure case where the residual is large and CDA should not help.

6. **The certificate gives one measurable version of the criterion.**
   For the local tangent ambiguity set,
   \[
   \sup_{\alpha}\alpha^\top L(\theta)
   =
   \bar L(\theta)+\rho\|P_\perp L(\theta)\|_2 .
   \]
   This defines a source-only score that keeps the source mean and the centered domain-wise sensitivity visible. It is a criterion to test, not a universal truth.

7. **Checkpoint averaging adds a mergeability condition.**
   If \(w\in\Delta^K\), the paper can reason about the endpoint source-loss mixture
   \[
   z(w)=\sum_j w_jL(\theta_j),
   \]
   but the deployed object is the weight-space soup
   \[
   \bar\theta(w)=\sum_j w_j\theta_j .
   \]
   The bridge is the mergeability residual
   \[
   M(w)=\|L(\bar\theta(w))-z(w)\|_2 .
   \]
   CDA is credible only when \(M(w)\) is measured and small enough to make source-loss-vector arithmetic meaningful.

8. **The experiments must test the full causal chain.**
   The paper must show: first, source-average selection underidentifies or misranks meaningful candidates in the available checkpoint banks; second, domain-wise source evidence can distinguish those candidates; third, CDA's source-composition robustness criterion improves or matches deployment accuracy against strong post-hoc baselines; fourth, \(\epsilon_{\mathrm{app}}\) and \(M(w)\) explain when the criterion fails. Without all four pieces, the motivation is circular.

## Final Paper Shape

1. **Introduction**
   Establish strict DG evaluation, post-hoc deployment, source-only selection under scalar underidentification, domain-wise source evidence as the general solution path, and CDA as one conditional criterion. End with concise contributions.

2. **Related Work**
   Organize by mechanism: DG evaluation and source validation; domain-wise risk and distributional robustness; flatness and sharpness in DG; weight averaging and soups; pretraining-era DG.

3. **Problem Setup and Source-Mixture Certificate**
   State notation, the source-supported hidden-shift approximation, the robust value, and the mergeability residual. Put proofs in the appendix.

4. **CDA Method**
   Define VSC retained-family selection and CDA-BD weighting. Avoid empirical evidence inside the method section.

5. **Experiments**
   Report real, reproduced results only: a broad DomainBed-style main table, PACS high-resolution tests, CDA applied on top of multiple training methods, and baseline comparisons.

6. **Analysis and Ablations**
   Show selector-vs-weight ablations, source-evidence underidentification, CDA selection geometry, domain-risk cancellation, local deployment geometry, mergeability diagnostics, and failure cases.

7. **Limitations**
   Plainly state source-domain labels, local mixture support, residual size, compute cost, bank dependence, and the absence of unconditional target guarantees.

8. **Conclusion**
   One paragraph. No broad promises.

## Required Figures and Tables

Performance comparisons belong in tables, not benchmark plots. The figures must show mechanism, geometry, and diagnostics that tables cannot show.

- **Table 1, main benchmark table:** a broad single-run benchmark table, with standard DG baselines and single-run post-hoc/averaging baselines first and CDA rows last. Candidate rows include ERM, ERM++, IRM, GroupDRO, Mixup, MLDG, CORAL, MMD, DANN, CDANN, VREx, RSC, SagNet, Fish/Fishr when available, SAM/DGSAM when available, SWAD, EoA-SMA/MA if reproduced as a single-run moving-average baseline, DNA if reproducible under the same one-run budget, ERM++-MPA if separated from the full ERM++ recipe, then **CDA+ERM**, **CDA+CORAL**, and **CDA+SAM/ERM++** in the final bold rows if those runs exist. DiWA, full EoA-as-ensemble, model soups, WiSE-FT, MonoSoup, DFDG/DEKAN, and large-learning-rate Lookahead-style DG should not be mixed into this main table as peer baselines unless a strictly single-run, source-only, same-setting variant is reproduced; otherwise they belong in related work or a separate appendix note.
- **Table 2, PACS split table:** PACS per-target results for the strongest reproduced baselines and CDA variants. The accepted same-seed SWAD/CDA comparison belongs here as one row pair, not as the whole empirical story:
  \[
  \mathrm{SWAD}=0.8719,\qquad
  \mathrm{CDA}=0.8842,\qquad
  \Delta=0.0123.
  \]
- **Table 3, CDA-on-base-method table:** compare each base training method before and after CDA-style deployment. Rows should include ERM++, CORAL, SAM/DGSAM if available, and possibly other stable checkpoint-bank producers. Columns should include final checkpoint, source-selected checkpoint, VSC+uniform, and VSC+CDA-BD.
- **Table 4, component ablation:** best source-validation singleton, VSC+uniform, VSC+CDA-Piv, VSC+CDA-BD, CDA-BD without entropy, VSC tolerance variants, and BN refresh variants. This tests which part of CDA matters.
- **Appendix/internal evidence table:** dataset, target domain, seed, checkpoint bank, result location, Slurm log directory, source-only selection fields, and artifact status. This is not a main-paper table.
- **Figure 1, source-evidence underidentification:** a compact two-panel motivation figure. Panel A shows two candidates with similar \(\bar L\) but different source-risk vectors \(L(\theta)\). Panel B plots \(\bar L(\theta)\) against \(\|P_\perp L(\theta)\|_2\) with contours of
  \[
  \bar L+\rho\|P_\perp L\|_2 .
  \]
  This figure establishes the problem and the source-only score before the method is introduced.
- **Figure 2, CDA selection geometry:** a method-analysis figure, not a benchmark chart. Plot centered source-risk vectors \(P_\perp L(\theta)\) in the two-dimensional source-risk plane for a PACS split, highlight the VSC-retained family, size retained points by CDA-BD weight, and mark the final soup. Add a small inset showing CDA-BD weight mass over checkpoint step. This shows how CDA moves from a checkpoint bank to a weighted deployment.
- **Figure 3, domain-risk cancellation:** show the centered source-risk vectors of checkpoints with nontrivial CDA-BD weight and their weighted sum. This is the most CDA-specific figure: it visualizes the balancing behavior that uniform averaging cannot show.
- **Figure 4, local deployment geometry:** source-loss contour plot around representative single-run deployed models, paired with flatness-versus-radius curves:
  \[
  \Delta_r(\theta)=\mathbb{E}_{\|\delta\|=r}\left[L(\theta+\delta)-L(\theta)\right].
  \]
  The compared models should be chosen by role, not by SWAD fixation: ERM++/final checkpoint, a strong single-run training-time DG method such as CORAL or SAM if available, SWAD or EoA-SMA/MPA as single-run averaging references, VSC+uniform, CDA-Piv, and VSC+CDA-BD. This tests whether CDA lands in a flat, mergeable region rather than merely selecting a high-accuracy endpoint.
- **Figure 5, assumption audit:** predicted source-risk mixture \(z(w)=\sum_i w_iL(\theta_i)\) versus measured soup risk \(L(\bar\theta(w))\), together with \(\epsilon_{\mathrm{app}}\) by target split. Compare VSC+uniform, CDA-Piv, VSC+CDA-BD, and CDA-on-base-method variants such as CDA+ERM++, CDA+CORAL, and CDA+SAM if available. This figure tells the reader when the CDA working condition is plausible and when the method should fail.
- **Appendix figure, prediction-diversity map:** DiWA-style diversity-versus-accuracy map only if it adds nonredundant information about the retained CDA family. It should be omitted if it merely repeats Figure 2.

## Claim Boundaries

- Say: CDA is a domain-wise source-risk criterion for source-only post-hoc checkpoint deployment.
- Say: CDA is evaluated primarily in the single-run post-hoc deployment setting.
- Say: CDA optimizes a conditional source-risk robustness proxy and audits the condition with residual diagnostics.
- Say: CDA is motivated by source-only model-selection underidentification, QRM-style domain-risk reasoning, DRO, flatness-aware DG, and model-soup literature.
- Do not say: CDA estimates the target domain.
- Do not say: prior work ignores source mixtures.
- Do not say: SWAD, DiWA, EoA, or model soups are inferior because they do not optimize source-domain composition robustness.
- Do not say: CDA provides absolute target-domain guarantees.
- Do not say: CDA is SOTA unless real, reproduced, uncertainty-aware results prove it.
- Do not say: the current provisional five-benchmark table is real.

## Reviewer-2 Motivation Test

Before writing the introduction, the narrative must pass this test:

- Can the paper state the upstream problem without CDA: scalar source validation can underidentify source-only checkpoint selection?
- Can the paper state the general solution path before CDA: preserve and use domain-wise source evidence?
- Can the paper introduce source-domain reweighting only after the broader domain-wise evidence problem is established?
- Can the paper name the exact decision not handled by those literatures: source-only weighting of a fixed, mergeable checkpoint bank under a measured local mixture certificate?
- Can the paper state at least one expected failure case, such as a target whose risk cannot be fitted by a nearby source mixture or a soup with large \(M(w)\)?
- Can the paper avoid the words "first," "only," "target estimation," and "prior work ignores mixtures"?

If any answer is no, the narrative is not frozen.
