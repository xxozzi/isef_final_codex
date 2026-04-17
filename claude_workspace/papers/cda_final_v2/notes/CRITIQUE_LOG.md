# CDA Final V2 Critique Log

## Imported Critique from Pre-Rewrite Review

### Scientific / Open-Ended Critique

- Preserve the source-fit plus source-mixture-sensitivity plus mergeability decomposition.
- Remove defensive voice and repeated self-protective caveats.
- Collapse repeated method explanations into one coherent story.
- Strengthen related work breadth and citation support.
- Stop framing experiments as reporting choices or internal persuasion.

### Rubric-Style Critique

- Experimental credibility was previously too narrow and too self-explained.
- Main-body theorem count was inflated by low-value statements.
- Abstract and introduction were too jargon-heavy and too busy.
- Baseline provenance was unclear for several internally named ideas.

### Visual Critique

- Existing figure system is inconsistent.
- `pipeline` is not paper-ready.
- Some figures are too slide-like or too argumentative.
- Figures should be used where they beat tables, not as redundant result mirrors.

## Completed Critique Passes

- [x] Adversarial scientific review on novelty and overclaiming.
- [x] Paper-editor review on flow, trustworthiness, and section logic.
- [x] Visual/editorial review on figure system, captions, and layout coherence.

## High-Severity Findings Addressed

- Removed manuscript-facing language such as "approved", "supplied", "draft", "expected", "pending", and "unresolved" from the main scientific prose, except for internal macro names and the submission-mode guard error text.
- Moderated the empirical claim around the small \(\diwa{}\) margin: the paper now says the gain is small and frames the result as top-tier competitiveness rather than broad superiority.
- Removed the reproduced ERM context row from the headline table and moved row-provenance policy into Appendix~\ref{app:reporting} in the manuscript.
- Made \(\Phi(w)\) and \(s_j\) explicit in the \(\piv{}\) method description.
- Added concrete protocol details for \(\gamma\), \(\varepsilon_{\rm vsc}\), \(\alpha\), \(\eta\), \(\lambda_{\rm ent}\), and the retained-family stopping rule.
- Revised figures so they are referenced in the prose, tied to equations, and regenerated from the checked-in Python source.
- Updated the VSC schematic so it no longer shows a hard-coded perfect disagreement-mask match.
- Updated the certificate schematic so it includes the \(\epsilon_{\rm app}\) term from Eq.~\eqref{eq:soup_certificate}.

## Remaining Known Limitations

- The figure assets were regenerated and compile, but they should still be visually inspected in the PDF before any serious external circulation.
- Red provisional content is intentionally still present and submission-mode compilation correctly fails until those spans are removed.
