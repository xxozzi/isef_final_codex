# CDA Paper Skeleton

Date created: 2026-04-30

This is the intended structure for the rewritten paper. The paper should argue from a practical source-only deployment problem to a specific checkpoint-selection and weighting rule:

\[
\text{fixed source validation can underidentify deployment choices}
\rightarrow
\text{domain-wise source-risk vectors carry useful evidence}
\rightarrow
\text{CDA uses that evidence to choose and weight a mergeable checkpoint family}.
\]

The paper should not claim that CDA estimates the target distribution unconditionally. The claim is conditional: when source-domain risk structure is informative for the target shift and checkpoint averaging remains locally mergeable, CDA gives a source-only rule for deployment-time checkpoint averaging. This condition must be justified with literature, geometry, residual diagnostics, and failure cases.

## Main Section Order

1. Introduction.
   State the deployment problem. We have a trained checkpoint bank and no target validation labels. A scalar source-validation mean can rank two candidates the same even when their source-domain risk vectors differ. CDA uses the vector \(L(\theta)\), not only \(\bar L(\theta)\), to make a deployment choice.

2. Related Work.
   Position CDA next to DomainBed-style model selection, SWAD, model soups, DiWA, EoA, QRM/EQRM, DRO/GroupDRO/VREx, MIRO, DGSAM, WDRDG, FAD, WILDS, WiSE-FT, MonoSoup, data-free DG, and recent pretraining-era DG work. The goal is not to say these methods miss CDA. The goal is to show that source risks, deployment-time averaging, and robustness criteria are already central concerns, while CDA studies a narrower single-run checkpoint-bank decision. SWAD, EoA's single-run SMA/MA component, DNA, and ERM++'s MPA are the closest single-run averaging neighbors. DiWA, full EoA-as-ensemble, model soups, WiSE-FT, MonoSoup, data-free DG, and large-learning-rate flat-minima work should be treated as adjacent references unless a strictly single-run, source-only, same-setting variant is reproduced.

3. Problem Setup.
   Define source domains, target domain, checkpoint bank, source-risk matrix, source average, centered source-risk vector, and deployed soup. Introduce:
   \[
   L(\theta)=(L_1(\theta),\ldots,L_m(\theta)),\qquad
   \bar L(\theta)=\frac{1}{m}\sum_{d=1}^m L_d(\theta).
   \]

4. Method.
   Present CDA as two steps:
   \[
   \mathrm{CDA}=\mathrm{VSC}+\mathrm{CDA\text{-}BD}.
   \]
   VSC keeps a checkpoint family that is accurate enough by source validation and stable enough under source-domain composition changes. CDA-BD then computes source-only weights over that family using the domain-wise risk vectors. Keep this section procedural and short.

5. Theory.
   State the robust source-risk objective and the conditions under which it is meaningful. The theory should be presented as a conditional source-risk certificate, not as a target-domain guarantee. Proofs go to the appendix unless a short statement is needed to understand the method.

6. Experiments.
   Lead with a broad benchmark table whose final rows are CDA variants. The accepted same-seed PACS result is important evidence, but it is not the whole story:
   \[
   \mathrm{SWAD}=0.8719,\qquad
   \mathrm{CDA}=0.8842,\qquad
   \Delta=0.0123.
   \]
   Then show ablations and diagnostics that explain why the result is not just a random soup win.

7. Limitations.
   Say plainly when CDA should fail: weak source-domain coverage, non-mergeable checkpoint families, misleading source risk vectors, unstable BN refresh, or target shifts not reflected in source-domain factors.

## Planned Figure Set

Rule: do not use bar charts, slope charts, line charts, or any other graph to compare benchmark accuracy rows. Benchmark accuracy and ablation accuracy belong in tables. Figures should show mechanism, geometry, selection behavior, or assumption checks that a table cannot communicate efficiently. The main paper should keep exactly five figure roles unless a result genuinely breaks the narrative.

1. Figure 1, source-evidence underidentification.
   Use this before introducing CDA. Panel A shows two candidate checkpoints or soups with similar \(\bar L\) but different \(L(\theta)\). Panel B plots candidates by source mean and source disagreement, with contour lines for:
   \[
   \bar L+\rho\|P_\perp L\|_2.
   \]
   Job: establish that scalar source validation can discard useful domain-wise evidence.

2. Figure 2, CDA selection geometry.
   Use this after the method definition. Project centered source-risk vectors \(P_\perp L(\theta)\) into the two-dimensional source-risk plane for one PACS split. Highlight the VSC-retained family, size retained points by CDA-BD weight, and mark the final averaged model. Add a small checkpoint-step inset showing CDA-BD weight mass over the trajectory.
   Job: show how CDA moves from a checkpoint bank to a concrete weighted deployment.

3. Figure 3, domain-risk cancellation.
   Show the centered source-risk vectors of checkpoints receiving nontrivial CDA-BD weight, then show their weighted sum. This can be a small vector diagram or a compact matrix-plus-result panel.
   Job: make the nonuniform weighting behavior interpretable and CDA-specific.

4. Figure 4, local deployment geometry.
   Pair a source-loss contour plot with flatness-versus-radius curves. The contour plane should include representative single-run deployed models by role: ERM++ or final checkpoint, a strong single-run training-time DG method such as CORAL or SAM if available, SWAD or EoA-SMA/MPA as single-run averaging references, VSC+uniform, CDA-Piv, and VSC+CDA-BD. The flatness curve should use a statistic such as:
   \[
   \Delta_r(\theta)=\mathbb{E}_{\|\delta\|=r}\left[L(\theta+\delta)-L(\theta)\right].
   \]
   Job: test whether CDA lands in a stable, mergeable region rather than merely finding a lucky high-accuracy soup.

5. Figure 5, assumption audit.
   Combine predicted-versus-real source-risk mixture and source-mixture residual. Compare
   \[
   z(w)=\sum_i w_i L(\theta_i)
   \]
   against \(L(\bar\theta(w))\), and report
   \[
   M(w)=\|L(\bar\theta(w))-z(w)\|_2,\qquad \epsilon_{\mathrm{app}}.
   \]
   Job: show when the assumptions behind CDA are plausible and when CDA should fail.

## Optional Appendix Figures

1. Source-risk heatmap, if Figure 2 is too abstract.
2. Accuracy-versus-compute frontier, to justify the final-only CDA runner and document why DomainNet is paused. This belongs in the appendix or protocol discussion, not as main evidence for CDA's scientific claim.
3. \(K\)-sensitivity curve, plotting accuracy, source-heldout risk, and
   \[
   K_{\mathrm{eff}}=\frac{1}{\sum_i w_i^2}
   \]
   as the retained family size changes.
4. Support-size sensitivity curve, if multiple support sizes \(S\) are run.
5. Checkpoint timeline and selected-family behavior, if the Figure 2 checkpoint-step inset is too compressed.
6. Raw weight distribution and entropy,
   \[
   H(w)=-\sum_i w_i\log w_i,
   \]
   if reviewers need evidence that CDA-BD is not secretly selecting one checkpoint.
7. Selected-family overlap across seeds, if extra seeds are available.
8. Prediction-diversity map, if it reveals a difference not already visible in Figure 2 or Figure 3.
9. BN refresh sensitivity plot, if both BN refresh modes are run.
10. Per-seed uncertainty plots, if extra seeds exist.

## Planned Tables

1. Main benchmark table.
   A broad single-run table with standard DG and single-run post-hoc/averaging baselines first, and CDA variants as the final bold rows. Candidate rows: ERM, ERM++, IRM, GroupDRO, Mixup, MLDG, CORAL, MMD, DANN, CDANN, VREx, RSC, SagNet, Fish/Fishr where available, SAM/DGSAM where available, SWAD, EoA-SMA/MA if reproduced as a single-run moving-average baseline, DNA if reproducible under the same one-run budget, ERM++-MPA if separated from the full ERM++ recipe, then CDA+ERM, CDA+CORAL, and CDA+SAM/ERM++ if those runs exist. DiWA, full EoA-as-ensemble, model soups, WiSE-FT, MonoSoup, DFDG/DEKAN, and large-learning-rate Lookahead-style DG should be excluded from the main peer table unless a strictly same-budget single-run variant is reproduced.

2. PACS split table.
   Per-target and mean accuracy for the strongest reproduced baselines and CDA variants. The accepted same-seed SWAD versus CDA result lives here, but the table should not be only SWAD and CDA.

3. CDA-on-base-method table.
   Show whether CDA is useful on top of multiple checkpoint-bank producers. Rows should include ERM++, CORAL, SAM/DGSAM if available, and any other stable base method. Columns should include final checkpoint, source-selected checkpoint, VSC+uniform, and VSC+CDA-BD.

4. Ablation table.
   Rows: best source-validation singleton, VSC+uniform, VSC+CDA-Piv, VSC+CDA-BD, CDA-BD without entropy, VSC tolerance variants, and BN refresh variants. This table explains which part of CDA matters.

5. Appendix evidence/protocol table.
   List dataset, target domain, seed count, checkpoint-bank construction, source-only selection fields, result path, and Slurm log path. This is not a main-paper table.

6. Extended benchmark table.
   The paper target is the full DomainBed image benchmark package: PACS, VLCS, OfficeHome, TerraIncognita, and DomainNet. These runs are required for publication-ready status, not optional decoration. Do not create a five-benchmark grand average from partial evidence.

7. Appendix related averaging table.
   Discuss DiWA, full EoA-as-ensemble, model soups, WiSE-FT, MonoSoup, data-free DG, and large-learning-rate flat-minima methods as broader averaging/editing/deployment references. Do not present them as directly comparable peer baselines to single-run CDA unless the training-run budget and task setting are matched.

8. Appendix raw-result table.
   Per-target, per-seed, per-method rows. This is the source for generated main tables.

## What Each Piece Must Contribute

- The motivation figure explains why a scalar source average can be too little information.
- The main benchmark table gives the empirical claim.
- The PACS split table shows where the accepted same-seed result comes from.
- The ablation table tests whether VSC and CDA-BD each matter.
- The selection-geometry figure explains what CDA actually does.
- The domain-risk cancellation figure shows why nonuniform weighting is doing something interpretable.
- The local deployment geometry figure tests whether CDA lands in a stable region.
- The assumption-audit figure shows when the source-risk and averaging assumptions are plausible.

Anything that does not support one of these jobs should be cut or moved to the appendix.
