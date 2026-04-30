# CDA Rewrite Narrative

This file pins down the implicit line of reasoning for the rewritten paper. It is not prose for the final manuscript. It is the argument the manuscript must make through structure, notation, results, and figures.

## Status

Yes, we now have an explicit narrative for the rewrite, but it must be anchored outside CDA's own mechanics:

> Source-only post-hoc deployment is an underidentified model-selection problem. A completed DG run can produce many plausible checkpoints or soups, target labels are unavailable, and scalar source validation averages collapse a domain-wise evidence vector into one number. CDA starts from this external bottleneck: when several candidates look comparable under the usual source aggregate, use the domain-wise source loss vector rather than discarding it. Source-composition robustness is CDA's conditional way of scalarizing that vector for mergeable checkpoint banks, not the reason the problem exists.

The current draft should not claim that CDA discovers the target domain. It should not claim that prior work ignores source mixtures. It should not imply that SWAD, DiWA, EoA, or model soups are deficient because they did not optimize CDA's criterion. It should claim something narrower: source-only checkpoint deployment is often decided by insufficient scalar evidence, and CDA evaluates whether a domain-wise source-risk criterion improves that decision.

## Core Narrative

1. **DG has become harder to claim convincingly.**
   DomainBed showed that many train-time DG algorithms weaken under controlled model selection, while ERM remains strong. SWAD, DiWA, EoA, and model soups shifted the practical baseline toward post-hoc or averaging-based deployment. A CDA paper must begin from this stricter baseline, not from a generic "DG is hard" paragraph.

2. **Deployment often starts after training has already happened.**
   A completed run produces a checkpoint bank
   \[
   \mathcal{B}=\{\theta_1,\ldots,\theta_K\}.
   \]
   The post-hoc decision is to choose a deployed model from this bank, usually by selecting or averaging checkpoints. This is narrower than train-time DG, but it is operationally meaningful.

3. **The external problem is source-only selection under scalar underidentification.**
   Standard source-only selection typically collapses validation evidence across domains into an aggregate score. That scalar is useful, but it can underidentify the deployment choice: two candidates can have similar source average while making different errors across the source domains, and those differences are invisible after averaging. This problem exists before CDA is introduced. DomainBed makes model selection central; QRM and DRO-style work emphasize that domain-wise risks contain information beyond a single average; DGSAM-style work shows that aggregate objectives can hide domain-wise fragility. The motivating question is therefore not "why did prior work not use CDA?" It is: when a fixed checkpoint bank contains candidates that are similar under source-average validation, can domain-wise source evidence improve source-only deployment selection?

4. **The general solution path is to preserve and use domain-wise source evidence.**
   The source-specific warrant is recorded in `misc/modern_literature_refresh.md`. Multi-source adaptation, QRM/EQRM, GroupDRO, VREx, WDRDG, MODE, DomainBed, SWAD, DiWA, EoA, and model soups each constrain the claim. The common lesson for CDA is not that these papers are missing source reweighting. The lesson is that source-domain risks, model-selection rules, and weight-space deployment objects must be treated explicitly. CDA narrows this to a fixed checkpoint bank, where the observable evidence is the vector \(L(\theta)\) rather than only its mean.

5. **Source-composition robustness is CDA's conditional criterion.**
   CDA chooses one way to scalarize the source-loss vector: evaluate local robustness to source-domain reweightings while accounting for soup mergeability. For a retained candidate family, the approximation is
   \[
   L_T(\theta)
   \le
   \alpha_T^\top L(\theta)+\epsilon_{\mathrm{app}},
   \qquad
   \alpha_T=\bar u+\delta,\quad
   \mathbf{1}^\top\delta=0,\quad
   \|\delta\|_2\le\rho .
   \]
   This is not an absolute guarantee about the target domain and not a claim that CDA estimates \(\alpha_T\). It is a conditional deployment model. If \(\epsilon_{\mathrm{app}}\) is large, the model is weak and the paper must show that failure.

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
   Define retained-family selection and weighting. Avoid empirical evidence inside the method section.

5. **Experiments**
   Report real, reproduced results only: DomainBed-style tables, PACS high-resolution tests, and baseline comparisons.

6. **Analysis and Ablations**
   Show selector-vs-weight ablations, source-average underidentification diagnostics, certificate-vs-OOD scatter, mergeability diagnostics, and failure cases.

7. **Limitations**
   Plainly state source-domain labels, local mixture support, residual size, compute cost, bank dependence, and the absence of unconditional target guarantees.

8. **Conclusion**
   One paragraph. No broad promises.

## Required Figures and Tables

- **Main results table:** reproduced methods only, all cells backed by raw artifacts, with mean \(\pm\) standard deviation.
- **PACS split table:** all four target domains, high-resolution seed count, and paired comparisons.
- **Component ablation table:** best singleton, late-window uniform, VSC+uniform, CDA-Piv, CDA-BD, no-sensitivity, no-entropy.
- **Source-average underidentification figure:** candidates with similar aggregate source validation but different domain-wise source vectors and OOD outcomes.
- **Selection-instability figure:** candidate rankings under the scalar source average versus domain-wise criteria derived from the same source evidence.
- **Certificate scatter:** \( \bar L+\rho\|P_\perp L\|_2 \) versus OOD accuracy across checkpoints and soups.
- **Mergeability diagnostic:** predicted endpoint loss vector \(z(w)\) versus actual soup loss vector \(L(\bar\theta(w))\).
- **Source-mixture residual figure:** fitted mixture residual \(\epsilon_{\mathrm{app}}\) per target split.
- **Failure-case figure:** a split where \(\epsilon_{\mathrm{app}}\) is large and CDA should not help.

## Claim Boundaries

- Say: CDA is a domain-wise source-risk criterion for source-only post-hoc checkpoint deployment.
- Say: CDA optimizes a conditional source-supported robustness proxy.
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
