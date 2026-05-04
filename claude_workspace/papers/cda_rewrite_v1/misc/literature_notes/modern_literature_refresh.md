# Modern Literature Refresh

Last checked: 2026-04-30.

This file is the source-specific matrix used to constrain the CDA rewrite. Its purpose is not to prove that CDA is important by assertion; its purpose is to prevent a fake gap.

The motivation must follow this chain:

1. **Problem in current literature:** source-only post-hoc deployment is often decided by scalar source validation, which can underidentify the choice among candidates with similar average source performance but different domain-wise behavior.
2. **General solution path:** preserve and use the domain-wise source-risk vector instead of collapsing it immediately to a single average, while preserving the mergeability required for weight-space soups.
3. **CDA-specific hypothesis:** for compatible checkpoint banks, source-domain composition robustness is one useful scalarization of that domain-wise vector, and the hypothesis is falsified when \(\epsilon_{\mathrm{app}}\) or \(M(w)\) is large.

The allowed CDA gap is narrow:

\[
\text{source-only weighting of a fixed, mergeable checkpoint bank using domain-wise source-risk evidence.}
\]

## Literature Matrix

| Source | Year / Status | Problem Setting | Core Mechanism or Assumption | Relation to Source Mixtures | Relation to Checkpoint Deployment | Constraint on CDA |
|---|---:|---|---|---|---|---|
| Mansour, Mohri, Rostamizadeh, *Domain Adaptation with Multiple Sources* | 2008 / NeurIPS | Multi-source adaptation with source distributions and target mixture | Distribution-weighted combining rules can guarantee small loss for target mixtures of sources under assumptions | Direct theoretical warrant for source-supported target mixtures | Not about neural checkpoint banks or post-hoc weight soups | CDA must cite source mixtures as old prior art; CDA may only use a local loss-vector analogue for deployment. |
| Sun et al., *A Two-Stage Weighting Framework for Multi-Source Domain Adaptation* | 2011 / NeurIPS | Multi-source domain adaptation with marginal and conditional shifts | Two-stage source weighting using target-domain data | Shows that source weighting must account for different shift types | Uses target data; not source-only checkpoint deployment | CDA must not borrow target-aware weighting language; it must show source-only selection. |
| DomainBed | 2021 / ICLR | Standardized DG evaluation and model selection | Training-domain validation and leave-one-domain-out protocols | Source validation is part of the DG problem | Not a post-hoc checkpoint-weighting method | CDA must obey source-only model selection and report the exact protocol and result files. |
| WILDS | 2021 / ICML | Real-world distribution-shift benchmarks | Dataset-level robustness with explicit split metadata | Shows that benchmark shift structure matters | Not about checkpoint soups | CDA should include failure cases and avoid overclaiming from synthetic or small benchmarks. |
| GroupDRO | 2020 / ICLR | Worst-group robustness | Minimax risk over predefined groups with regularization | Robustness over group weights is established prior art | Training-time objective, not post-hoc deployment | CDA cannot claim novelty in domain/group robustness; it can use group-risk logic only for fixed-bank selection. |
| VREx / risk extrapolation family | 2021 / ICML area | Domain-risk invariance | Penalizes variability of risk across environments | Source-domain risk vector variation is already a major object | Training-time objective | CDA must distinguish deployment-time weighting from training-time risk penalties. |
| QRM / EQRM | 2022 / NeurIPS | Probable DG | Domain risks are treated probabilistically; average and worst-case DG are both incomplete | Strong warrant that source-domain variation should inform probable target variation | Training-time objective and evaluation protocol, not weight-space checkpoint soups | CDA may cite QRM as motivation for source-risk distributions, not as a gap it supersedes. |
| WDRDG | 2024/2025 / IEEE JSTSP, arXiv 2022 | DG under class-conditional Wasserstein uncertainty | Worst-case risk over class-specific uncertainty sets | Establishes modern DRO-style uncertainty sets for DG | Training-time optimization, not fixed-bank deployment | CDA must not claim uncertainty-set novelty; its residual \(\epsilon_{\mathrm{app}}\) is an empirical boundary. |
| MODE | 2023 / ICML | Domain generation under uncertainty subsets | Explores a moderate uncertainty subset sharing semantic factors | Supports bounded uncertainty rather than arbitrary worst case | Training-time distribution exploration | CDA's local radius \(\rho\) should be presented as bounded deployment modeling, not universal robustness. |
| SWA | 2018 / UAI | Weight averaging for flat minima | Averages weights along SGD trajectory | No domain mixture model | Establishes weight averaging as a deployment object | CDA must measure whether its soups are mergeable; averaging alone is not CDA. |
| SWAD | 2021 / NeurIPS | DG through dense overfit-aware averaging | Flatness and late-trajectory averaging | Indirect: reduces sensitivity but not source-mixture certificate | Direct post-hoc trajectory averaging baseline | CDA must compare to SWAD or carefully limit claims. |
| Model Soups | 2022 / ICML | Post-hoc averaging of fine-tuned models | Greedy/uniform weight-space soups without inference overhead | No source-domain mixture certificate | Directly relevant to mergeable deployment objects | CDA must diagnose \(M(w)\), because loss-vector weighting only matters if the deployed soup behaves like its endpoints. |
| EoA | 2021 / arXiv / post-hoc ensemble averaging family | Moving-average and ensemble stabilization | Stabilizes selection/averaging | No source-mixture risk model | Direct deployment-time averaging neighbor | CDA must position as certificate-driven weighting, not generic ensembling. |
| DiWA | 2022 / ICML | Diverse weight averaging for DG | Averages diverse models; diversity improves robustness | No explicit local source-mixture ambiguity objective | Direct post-hoc DG baseline | CDA must not claim diversity is wrong; it measures a different axis and needs matched baselines. |
| MIRO | 2022 / ECCV | DG with pretrained representations | Mutual-information regularization toward pretrained features | No source-mixture certificate | Training-time plug-in method | CDA must state whether comparisons are training-time, post-hoc, or literature-only. |
| FAD | 2023 / ICCV | Flatness-aware minimization for DG | Optimizer-level flatness control with theory and experiments | No direct source-mixture certificate, but domain robustness is central | Training-time optimizer | CDA cannot claim flatness-aware DG is missing. Current extracted source is invalid for style; use PDF/official page for claims. |
| DGSAM | 2025 arXiv / ICLR 2026 submission | Per-domain sharpness for DG | Aggregated SAM can hide sharp individual-domain landscapes | Strong warrant for per-domain, not only aggregate, risk geometry | Training-time optimizer | Supports CDA's focus on source-domain loss vectors; also raises a baseline/related-work burden. |
| Large-scale pretraining DG critique | 2025 / ICLR | Foundation-model DG evaluation | DG gains may reflect pretraining alignment, especially on in-pretraining splits | Not a source-mixture theory | Not a checkpoint-soup method | CDA must avoid broad SOTA claims unless backbone/pretraining/protocol are controlled. |
| DG in-the-wild with CLIP/domain-aware representations | 2025 / NeurIPS submission | CLIP evaluation under possible benchmark coverage | Evaluates domain-aware representations and OOD severity | Not a source-mixture certificate | Not fixed-bank post-hoc deployment | CDA should cite as a current evaluation caveat, not as a direct baseline. |
| Distributionally robust multi-source UDA | 2025 NeurIPS / 2026 ICLR poster family | Multi-source UDA with unlabeled target data | Robust aggregation or uncertainty modeling using target samples | Source weighting is direct but target-aware | Not source-only DG; not fixed checkpoint bank | CDA must define boundary against target-data and UDA methods. |
| Domain-specific risk / test-time adaptation papers | 2023--2026 | Target/test-time adaptation | Use target samples, target descriptions, or adaptation at inference | May estimate target-side quantities | Not source-only post-hoc selection | CDA must not compare as if same setting; these define excluded target-aware settings. |

## Gap-Boundary Proof

The matrix supports the following boundary:

1. Source mixtures are already established by multi-source adaptation and source-weighted target-mixture theory.
2. Source-domain risk distributions are already established by QRM/EQRM, GroupDRO, VREx, WDRDG, and related uncertainty-set work.
3. Flatness and domain-wise sharpness are already established by SWAD, FAD, DGSAM, and SAM-style DG.
4. Post-hoc weight averaging is already established by SWA, model soups, EoA, and DiWA.
5. What remains is not "mixtures," "robustness," "flatness," or "averaging." The remaining decision is how to select and weight a fixed checkpoint bank using only source-domain losses when scalar source validation underidentifies the choice and the deployed object is a mergeable weight-space soup.

This does not make source-domain composition robustness automatically superior to SWAD, DiWA, EoA, or model soups. It makes composition robustness one hypothesis for using domain-wise source evidence in a specific selection problem. This is why the local approximation

\[
L_T(\theta)\le \alpha_T^\top L(\theta)+\epsilon_{\mathrm{app}}
\]

is admissible only as a candidate-family deployment model. It is credible when \(\epsilon_{\mathrm{app}}\) is small on held-out target splits and weak when \(\epsilon_{\mathrm{app}}\) is large. The final paper must show both.

## Checked 2024--2026 Items

- **ICLR 2025 large-scale pretraining DG critique:** checked through OpenReview and ICLR proceedings; constrains CDA to control backbone and pretraining before making broad claims.
- **DGSAM / ICLR 2026 submission:** checked through OpenReview and arXiv source download; supports per-domain geometry and warns against aggregate-flatness claims.
- **WDRDG 2025 journal version:** checked through publisher metadata and arXiv download; confirms modern DG already uses distributionally robust uncertainty sets.
- **Distributionally robust multi-source UDA 2025/2026:** checked through NeurIPS/OpenReview pages; boundary case because it uses target-domain information.
- **CLIP DG in-the-wild 2025 submission:** checked through OpenReview; boundary/evaluation caveat, not a direct source-only checkpoint baseline.
- **Recent test-time/adaptive DG papers:** checked as boundary cases; excluded from direct comparison if they use target samples or adaptation.

## Novelty Constraint

CDA may claim:

- source-only post-hoc selection and weighting of a fixed checkpoint bank using domain-wise source-risk evidence;
- a local source-mixture certificate over source-domain loss vectors;
- mergeability diagnostics for translating endpoint loss arithmetic into a deployed weight-space soup;
- empirical validation or falsification through \(\epsilon_{\mathrm{app}}\) and \(M(w)\).

CDA may not claim:

- that target domains are generally source mixtures;
- that CDA estimates the target mixture;
- that prior work ignores source mixtures, domain robustness, flatness, or checkpoint averaging;
- that broad benchmark gains exist until reproduced result files prove them.
