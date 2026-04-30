# CDA Rewrite Fixes and Writing Notes

This file records concrete fixes to apply while rewriting the CDA paper. It is a working memory file, not manuscript prose.

## High-Level Fix

The current paper is too verbose because it explains the author’s reasoning instead of presenting a research argument. The rewrite must make claims through structure, equations, algorithms, tables, and ablations.

Bad pattern:

> Corollary 3.3 matters because...

Professional pattern:

> For the tangent ambiguity set,
> \[
> \sup_{\alpha}\alpha^\top L(\theta)
> =
> \bar L(\theta)+\rho\|P_\perp L(\theta)\|_2 .
> \]

No explanation of why the reader should care unless the next sentence changes the method or experimental design.

## Current Draft Problems

- The introduction starts with too much narrative setup and too many examples.
- The paper repeatedly says what CDA is not.
- The method section contains empirical-analysis material.
- The theory section contains commentary that belongs in proofs, appendix notes, or not at all.
- The current result tables contain provisional values and must not be trusted.
- Several current figures are generated illustrations, not evidence.
- The related work is underdeveloped for 2026 and does not adequately address QRM, DRO, recent pretraining-era DG, flatness-aware DG, and model-soup literature.
- The source-mixture assumption is asserted before the upstream scalar source-selection bottleneck is motivated or stress-tested.

## Style Rules From Strong Papers

### SWAD

SWAD’s structure is direct: distribution shift problem, DomainBed result that ERM is strong, flatness motivation, SWAD method, empirical evidence. It does not spend paragraphs apologizing for what SWAD is not. The rewrite should imitate this sequence but not its older claim scope.

Useful pattern:

- State the evaluation pressure.
- Introduce one mechanism.
- Show the mechanism is measurable.
- Report tables and ablations.

Avoid copying:

- Overclaiming “first” unless provable.
- ImageNet robustness expansion before core DG results are stable.

### DiWA

DiWA is useful because it ties a simple method to a decomposition and then uses experiments to support the mechanism. Its lesson for CDA is to keep the mechanism compact: source-loss-vector sensitivity plus mergeability residual.

Use:

- A decomposition that justifies what gets measured.
- Clear distinction between weight averaging and ensembling.
- Tables that specify reproduced versus literature numbers.

Avoid:

- Claiming diversity is insufficient in general. Say CDA measures a different robustness axis.

### MIRO

MIRO motivates a modern DG method through pretrained representations and the failure of naive fine-tuning. It speaks in a current DG context, not only the early DomainBed era.

Use:

- Pretraining-era context.
- Direct experimental protocol description.
- Careful distinction between fair DomainBed comparisons and large-backbone exploratory comparisons.

### QRM

QRM is crucial because it rejects pure average and pure worst-case DG and formulates risk over a distribution of domains. CDA must cite this because it supports the broader claim that domain-wise source risks contain information a single source average discards.

Use:

- The idea that domain-wise source risks contain information beyond a single source average.
- Quantile/tail-risk framing as related work, not as CDA novelty.

Avoid:

- Claiming CDA is the first to connect source risks to target risk.

### DomainBed

DomainBed’s professional lesson is evaluation discipline. It explicitly treats model selection as part of the learning problem.

Use:

- Training-domain validation discipline.
- Leave-one-domain-out reporting.
- Standard errors and hyperparameter protocol clarity.

### Model Soups and EoA

These papers make post-hoc deployment credible by showing that averaged weights can be practical deployment objects. CDA must speak to compatibility and mergeability because source-loss-vector weighting is meaningless if the soup is not locally connected.

Use:

- Weight-space soup as the deployed object.
- Mergeability diagnostics.
- No-inference-overhead framing.

### GroupDRO, WDRDG, FAD, DGSAM

These papers prevent a fake gap. CDA is not introducing robustness over environments or domains from scratch. It uses source-domain reweighting as one way to exploit domain-wise source evidence after scalar source validation underidentifies source-only post-hoc selection.

Use:

- GroupDRO for worst-group/group-shift motivation.
- WDRDG for explicit uncertainty sets around source/target shifts.
- FAD/DGSAM for the point that global flatness can be insufficient under domain-wise risk.

## Literature Coverage Checklist

- [ ] DomainBed and source-domain validation.
- [ ] WILDS and in-the-wild distribution shifts.
- [ ] SWA and flat minima.
- [ ] SWAD and dense overfit-aware averaging.
- [ ] DiWA and diversity in weight averaging.
- [ ] Model soups and weight-space averaging.
- [ ] EoA and moving-average/ensemble stability.
- [ ] GroupDRO and worst-group robustness.
- [ ] VREx and risk invariance.
- [ ] QRM/EQRM and probable DG.
- [ ] WDRDG and distributionally robust DG.
- [ ] FAD/DGSAM and domain-wise sharpness.
- [ ] MIRO and pretrained representation regularization.
- [ ] ICLR 2025 large-scale pretraining critique.
- [ ] ICLR 2026/NeurIPS 2025 foundation-model DG submissions, marked by publication status.
- [ ] Robust DG under simultaneous marginal and conditional shifts.
- [ ] Linear mode connectivity and soup mergeability.

## Reviewer-2 Traps

- Do not write target-estimation language. CDA does not infer the target mixture \( \alpha_T \); it optimizes a source-only robustness proxy and reports residual diagnostics.
- Do not write "first," "only," or "the first method" unless a separate literature matrix proves the claim.
- Do not imply prior work ignores mixtures. Multi-source adaptation, QRM, DRO, GroupDRO, and WDRDG all make related mixture or uncertainty-set assumptions.
- Do not imply SWAD, DiWA, EoA, or model soups are worse because they did not pursue source-domain composition robustness. Motivate the project from scalar source-selection underidentification, then introduce composition robustness only as CDA's conditional criterion.
- Do not motivate CDA with "existing signals do not ask our question." That is circular unless the paper first establishes why the question matters.
- Do not imply prior work ignores flatness. SWAD, FAD, DGSAM, SAM variants, and related work already own that territory.
- Do not imply prior work ignores post-hoc averaging. SWA, model soups, EoA, and DiWA are central prior art.
- Do not motivate CDA with a gap that only appears after knowing CDA. The motivation must be readable before the method name appears.
- Do not use stale benchmark framing. Since pretraining-era DG now questions whether classic benchmark gains are really algorithmic, any broad claim must control for backbone, pretraining, and protocol.
- Do not report five-benchmark averages without complete lineage.
- Do not let polished notes, `.tex` tables, or hard-coded plot arrays serve as evidence.
- Do not treat `FAD` or `WILDS` as style sources from the current audit until usable paper prose is extracted; their current source extractions are partial or invalid for style analysis.

## Concrete Writing Mechanics

**Introduction paragraphs.**

- Paragraph 1: name the modern evaluation pressure in one direct claim, with DomainBed and pretraining-era DG as anchors.
- Paragraph 2: define the deployment object \( \mathcal{B}=\{\theta_1,\ldots,\theta_K\} \) and the source-only post-hoc decision.
- Paragraph 3: state the non-CDA problem: scalar source validation can underidentify the choice among checkpoint candidates.
- Paragraph 4: motivate domain-wise source-risk vectors from DomainBed, QRM, DRO/WDRDG, DGSAM-style domain-wise analysis, and post-hoc deployment practice before naming CDA.
- Paragraph 5: state source-domain composition robustness as one conditional scalarization of that vector, then introduce the certificate and mergeability problem.
- Paragraph 6: state CDA and contributions.
- Avoid long examples unless a single example is needed to define a variable.

**Related-work paragraphs.**

- Start each paragraph with the mechanism, not a history lesson.
- Spend most of the paragraph on what the prior literature actually contributes.
- End with a narrow boundary statement: CDA uses that idea for source-only weighting of fixed checkpoint banks.
- Never end by saying the prior work "fails to" do CDA.

**Theorem text.**

- Introduce an assumption only when it changes the theorem or algorithm.
- State the result, then give one operational consequence.
- Move derivations, geometric intuition, and edge cases to the appendix.
- Never write "this theorem matters because"; the next algorithm step or diagnostic should make the relevance visible.

**Captions.**

- Captions should say what was measured, on which artifact-backed scope, and what visual encoding means.
- Captions should not argue that the method is good.
- A strong caption reads like a compact audit trail, not like a slide subtitle.

**Limitations.**

- Each limitation should name the condition under which CDA can fail: large \(\epsilon_{\mathrm{app}}\), large \(M(w)\), missing domain labels, incomplete checkpoint bank, or expensive replay.
- Do not apologize and do not speculate about future breakthroughs.

**Negative framing.**

- Mature papers rarely spend prose saying what the method is not. Use positive definitions for the main text and reserve scope exclusions for limitations or related work boundaries.

## Sentence-Level Fixes

- Replace “CDA does not compete with training-time DG methods...” with “CDA selects and weights checkpoints after training using source-domain loss geometry.”
- Replace “Corollary X matters because...” with the mathematical consequence.
- Replace “This is why...” with either a theorem, algorithm step, or experimental hypothesis.
- Replace “not merely” and “not just” with a positive definition.
- Replace rhetorical questions with declarative setup.
- Replace “the primitive object is...” with “We optimize...”
- Replace “coherent reason” with the actual criterion.
- Replace “defensible” with measured evidence.

## Theorem Rules

- Main body gets assumptions, theorem statements, and one compact consequence.
- Appendix gets proofs and boundary cases.
- If a theorem does not affect the algorithm or a measured diagnostic, move it out of the main body.
- No theorem commentary should explain why the theorem deserves attention.
- The robust source-mixture value may stay in the main body:
  \[
  \sup_{\alpha}\alpha^\top L(\theta)
  =
  \bar L(\theta)+\rho\|P_\perp L(\theta)\|_2 .
  \]
- The soup certificate may stay only if it directly motivates \(M(w)\):
  \[
  M(w)=\|L(\bar\theta(w))-z(w)\|_2 .
  \]

## Experimental Fixes

- Delete every fake result.
- Treat every `\prov{}` span as non-evidence.
- Do not report a five-benchmark average until every component cell has raw artifact lineage.
- Do not compare against DiWA as reproduced unless it is actually rerun under the same protocol.
- Do not present diagnostic figures if values are hard-coded.
- Report mean \(\pm\) standard deviation.
- Report target-domain averages before grand averages.
- Include paired split-level comparisons where possible.
- Use failure cases to define the method’s scope.

## Figure Fixes

Good figures should answer one empirical question.

- Source-average underidentification: Do candidates with similar aggregate source validation have meaningfully different domain-wise source-risk vectors and OOD outcomes?
- Certificate scatter: Does \( \bar L+\rho\|P_\perp L\|_2 \) track OOD performance?
- Mergeability plot: Does \(z(w)\) predict \(L(\bar\theta(w))\)?
- Residual plot: Is the source-mixture approximation plausible for the split?
- Ablation heatmap: Which selector/weight pair actually helps?

Bad figures:

- Pipeline cartoons that repeat text.
- Slide-like conceptual diagrams in the main paper.
- Any plot with hard-coded values.
- Any figure that argues rather than measures.

## LaTeX Organization Fixes

- Keep `main.tex` short.
- Use `packages.tex`, `macros.tex`, and `theorems.tex`.
- Put each main section in its own file.
- Put proofs, protocol, additional results, and hyperparameters in separate appendix files.
- Keep final tables and figures generated by scripts, not handwritten.
- Keep all generated result tables traceable to raw CSV/JSON artifacts.
- Remove provisional macros entirely from the rewrite.

## Phrases to Ban From the Manuscript

- “matters because”
- “this is why”
- “why diversity”
- “does not compete”
- “not merely”
- “not just”
- “the claim is”
- “coherent reason”
- “defensible”
- “should be read”
- “primitive object”
- “story”
- “fake results”
- “approved values”
- “provisional”

## Final Tone Target

The paper should sound like:

> We study source-only post-hoc deployment from a fixed checkpoint bank. Scalar source validation can underidentify the choice among candidates with similar average source performance but different domain-wise behavior. CDA uses the domain-wise source-loss vector to define a conditional source-composition criterion for mergeable checkpoint soups. We evaluate the method with reproduced post-hoc baselines and diagnostics that test underidentification, mergeability, and the approximation residual.

It should not sound like:

> Here is why our idea is coherent, why it is not something else, why the theorem matters, and why the reader should interpret it kindly.
