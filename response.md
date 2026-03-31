# Paper Review Memo

I reviewed the paper drafts under [claude_workspace/papers](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers), checked them against the current empirical record in [claude_workspace/resume.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/resume.md), and cross-checked the main novelty claims against adjacent literature on predictive multiplicity / Rashomon sets, subgroup robustness without group labels, and distributionally robust optimization. I am scoring these as research bets, not as literal submissions in their current `TBD` state. If submitted today with the empirical sections still blank, all of their acceptance odds would be near zero. The `acceptance` score below means: **if the paper were fully executed well from here, how plausible would a NeurIPS/ICLR main-track acceptance be?**

Scale:
- `novelty`: `1-3` = incremental/repackaging, `4-7` = genuinely new but field-grounded, `8-10` = conceptually surprising and meaningfully different
- `success`: chance of becoming materially stronger than `SWAD` or otherwise clearly useful in this project
- `theory`: internal coherence, honesty of assumptions, and alignment between optimized object and deployed object
- `impact`: how much it would change the post-hoc DG conversation if it worked
- `acceptance`: realistic conference potential **if fully executed well**
- `evidence`: how much empirical support we actually have right now in repo/chat
- `project fit`: how well the method matches the actual project target of post-hoc + domain-label-free DG

Evidence caveat:
- the cleanest current evidence is the fresh `erm_replay_bank` seed-1 comparison and the 4-split PACS replay sweep
- the older local workspace snapshot is still useful, but it predates some later reruns
- the `erm_stawa` / other stale-bank historical results should be treated as supporting context, not as the main reason to choose a direction
- the `overall` ranking weights project fit and evidence together, which is why `PRISM` edges out `D-COLA` even though `D-COLA` remains the strongest raw empirical method

## Ranked Table

| Rank | Paper | Label-free | Novelty | Success | Theory | Impact | Acceptance | Evidence | Project fit | Overall |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `PRISM` | Yes | 7.5 | 7.0 | 8.0 | 7.5 | 7.2 | 7.0 | 9.0 | 7.5 |
| 2 | `D-COLA` | No | 6.0 | 8.5 | 6.5 | 7.5 | 6.5 | 9.0 | 3.0 | 7.2 |
| 3 | `TRIBE` | Yes | 8.5 | 6.0 | 7.0 | 8.5 | 5.5 | 2.5 | 9.0 | 6.5 |
| 4 | `CORA` | Yes | 7.0 | 5.5 | 6.5 | 7.0 | 5.5 | 4.5 | 8.0 | 5.9 |
| 5 | `ROAR` | Yes | 6.5 | 5.0 | 7.5 | 6.5 | 5.5 | 4.0 | 8.0 | 5.8 |
| 6 | `RIWA` | Yes | 6.5 | 5.0 | 7.5 | 6.5 | 5.5 | 2.0 | 8.0 | 5.8 |
| 7 | `SCOUT` | Yes | 7.5 | 3.5 | 6.0 | 7.0 | 4.5 | 5.0 | 8.5 | 5.7 |
| 8 | `ROWA` | No | 5.5 | 4.5 | 6.5 | 5.5 | 4.5 | 1.5 | 2.0 | 4.8 |
| 9 | `STAWA-New` | Yes | 5.5 | 4.0 | 6.5 | 5.5 | 4.0 | 5.5 | 8.0 | 4.7 |
| 10 | `STAWA` | Yes | 5.0 | 4.0 | 6.5 | 5.0 | 3.8 | 5.0 | 7.5 | 4.6 |
| 11 | `STAWA-Old` | Yes | 4.5 | 3.0 | 5.5 | 4.5 | 3.5 | 4.5 | 7.0 | 4.1 |

Notes:
- `stawa_neurips` and `stawa_new` are almost the same draft. The file diff is basically title framing plus a short abstract sentence, so I am treating them as the same method family with very similar scores.
- `D-COLA` is still the strongest raw empirical method in the project.
- `PRISM` ranks first here because this memo is trying to answer the actual project question, which is post-hoc + domain-label-free DG rather than unrestricted raw strength.
- If I ranked **strictly for domain-label-free follow-up**, the top three would be `PRISM`, `TRIBE`, and `CORA`, in that order.
- I did **not** score [d_cola_proposal.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/papers/d_cola/d_cola_proposal.md) separately because it is a proposal memo, not a full paper draft parallel to the `.tex` manuscripts.

## Method-by-Method Critique

### 1. D-COLA

The best case for `D-COLA` is simple: it is the strongest empirical object in the project so far. On the older verified local workspace snapshot, it led the replay leaderboard, and on the fresh canonical seed-1 bank it again beat `SWAD` and `PRISM`. The ablations in [claude_workspace/resume.md](/Users/jaydenjeong/Work/projects/ml/isef_final_codex/claude_workspace/resume.md) are unusually informative: `uniform` staying near baseline says exact final weights are not the main sauce, while `no_cov` and `contiguous` dropping hard says complementarity and noncontiguity really matter. That is a strong scientific signal, not just a benchmark win.

The case against `D-COLA` is also clear. The theory is not as clean as the empirical story. The objective is partly heuristic, the predictive-mixture-to-weight-soup bridge is an approximation, and the method uses explicit source-domain structure, which violates the stricter domain-label-free target. From a conference perspective, this looks more like a strong empirical paper than a major theory paper. If your north star is domain-label-free post-hoc DG, `D-COLA` is more of an empirical scaffold than the final destination.

Why these scores: moderate novelty because it combines known ingredients rather than inventing a new principle; high success and evidence because it actually works; middling theory because the mixture/soup bridge and domain-label dependence weaken the cleanliness.

### 2. PRISM

The best case for `PRISM` is that it is the cleanest domain-label-free method that has already shown real empirical life. On the fresh four-split PACS replay sweep, it slightly beat `SWAD` on average and won clearly on `photo` and `sketch`. Conceptually, it fixes a real problem that showed up in `SCOUT`: the action scored by the objective is the actual deployed soup, not a predictive-mixture surrogate. That improves theory/deployment alignment, which is usually a meaningful advantage in review.

The case against `PRISM` is that the win is still narrow. On the fresh canonical seed-1 bank, `D-COLA` stayed ahead. The cross-pool ablation was the big warning sign: `D-COLA`’s objective transferred well across pools, while `PRISM`’s objective degraded substantially on the `D-COLA` pool. That suggests the remaining weakness is more likely in the `PRISM` objective than in candidate-pool construction alone. The theory is cleaner than `D-COLA`, but the empirical margin over `SWAD` is not yet strong enough to sell as a field-changing idea.

Why these scores: novelty is high but not outrageous because minimax regret, hidden subpopulation robustness, and soup locality all already exist; theory is strong because object/deployment alignment is good; success and evidence are real but not dominant.

### 3. TRIBE

The best case for `TRIBE` is upside. This is the clearest draft in the folder that moves beyond checkpoint selection/averaging into post-hoc model repair. It says: first get a strong fixed anchor, then use checkpoint trajectories to discover hidden failure directions, then do a local last-layer repair. That is a meaningful conceptual jump. It is also well connected to adjacent literature: predictive multiplicity / Rashomon work says there can be many equally good models, and recent subgroup-robust work without group labels shows that last-layer retraining can matter a lot. The project’s own results also motivate it: pure selection/averaging seems to be getting close to a ceiling. The novelty is not last-layer retraining by itself, but the use of checkpoint-trajectory geometry to define the repair directions.

The case against `TRIBE` is that its critical assumption is much heavier than the selector papers. It needs the remaining DG gap to be mostly a head-level problem, and it needs trajectory residuals to contain a stable low-rank signal that is actually relevant to the target shift. The paper is honest about that, which helps the theory score, but it is still unproven territory. There is also very little direct evidence yet. As a submission bet, it is high-upside and high-risk.

Why these scores: very high novelty because the trajectory-basis-plus-repair combination is genuinely unusual; theory is coherent but intentionally conditional; evidence is minimal; impact would be huge if it works because it opens a new post-hoc DG regime beyond soups.

### 4. CORA

The best case for `CORA` is that it reframes post-hoc DG around predictive multiplicity rather than flatness or simple disagreement. That is a smart move: the broader literature on Rashomon sets and predictive multiplicity is active, which makes the idea feel timely rather than random. Among the label-free selector papers, this is one of the most intellectually distinctive. The novelty is not predictive multiplicity itself, which is already an active literature, but its conversion into a post-hoc DG soup-selection object. The paper also has a decent self-critique: it explicitly admits the consensus-fringe decomposition is a real modeling assumption, not a truth of nature.

The case against `CORA` is that the core mathematical object may be too indirect. You still have a predictive-mixture-to-weight-soup transfer gap, and the consensus-core framing may collapse to “plain soup plus uncertainty heuristic” if multiplicity structure is not strongly informative on real trajectories. Empirically, the current evidence is not exciting enough to rescue that risk. Compared with `PRISM`, it feels more original but less anchored by actual success.

Why these scores: high novelty, moderate theory, weak-to-moderate current evidence, and middling success odds until it shows that the consensus-core object tracks OOD better than simpler selectors.

### 5. ROAR

The best case for `ROAR` is theory-to-object alignment. Of the pure selector papers, it is one of the cleanest in spirit: directly optimize a robust objective over averageable soups, rather than motivate one thing and deploy another. That is a real strength. It also benefits from a huge amount of adjacent literature on DRO, KL ambiguity sets, and model averaging. If you want a paper that reviewers can understand quickly, `ROAR` has that advantage.

The case against `ROAR` is that it may be too close to existing robust-optimization language to feel truly surprising. It also still relies on a soup-transfer/locality story, and the current project evidence weakens the case that pure robust raw-risk selection is the most promising remaining direction. The older local `ROAR` result was respectable, but not enough to elevate it above the stronger branches.

Why these scores: theory is relatively good, novelty is moderate, evidence is real but not standout, and acceptance potential is decent if experiments surprise positively.

### 6. RIWA

The best case for `RIWA` is that it takes a very classical robustness idea, local sample reweighting, and applies it at the checkpoint-selection level in a clean way. The chi-square / local DRO interpretation gives it serious theoretical backbone. This is the kind of paper that can read as elegant: one new score, one clean duality story, one plausible reason flatness can miss the right object.

The case against `RIWA` is that the novelty ceiling is limited. Local reweighting invariance, influence-style reasoning, and chi-square DRO are already established literatures, so reviewers may see the method as “smart adaptation” rather than “new principle.” It also still ends in contiguous window averaging, which risks collapsing back toward a safer variant of `SWAD` rather than a new class of behavior. And right now it has no empirical support in this project.

Why these scores: good theory, decent novelty, low current evidence, and only moderate chance of a substantial empirical jump over `SWAD`.

### 7. SCOUT

The best case for `SCOUT` is that it was the first paper in this set that really demanded a direct objective over actual subset actions rather than another selection heuristic. The submodular-coverage framing is genuinely attractive, and the theory package is ambitious in a good way. On paper, this looked like one of the most principled moves in the whole project.

The case against `SCOUT` is the empirical story we now have. The strongest `SCOUT` result came in a degenerate setting where the optimizer effectively collapsed to a uniform soup. Once the optimizer had real room to move, performance dropped substantially. That is the worst possible pattern for a theory-first optimizer paper: it suggests the candidate pool was doing the useful work while the objective was misaligned with the deployed soup. Because of that, `SCOUT` now looks like a valuable research stepping stone rather than the method to keep pushing.

Why these scores: novelty remains high, but success is now clearly lower than it looked on paper; theory has to be discounted because the empirical failure mode hit the exact point the paper was trying to improve.

### 8. ROWA

The best case for `ROWA` is simplicity. Of the earlier papers, this is one of the cleanest “one new idea” drafts: a checkpoint is good if one-step cross-domain recovery is good. That gives it a nice bridge to meta-learning and transfer thinking, and it is easy to understand operationally. If it worked, it would be easy to adopt.

The case against `ROWA` is that it is not label-free, so it is misaligned with the stricter target that drove most of the later work. It is also close in spirit to leave-one-domain-out meta-learning and transfer-based DG ideas, which lowers the novelty score: this looks more like a sharp post-hoc translation of that literature than a new principle. With no project evidence behind it and a weaker fit to the core constraint, it is hard to rank highly now.

Why these scores: moderate theory and feasibility, but low evidence, moderate novelty, and weak fit to the actual project goal.

### 9. STAWA-New

The best case for `STAWA-New` is that the underlying intuition is reasonable: if a checkpoint’s predictions are still changing a lot under ongoing training dynamics, maybe that checkpoint is not ready to be trusted under shift. The plateau-constrained revision is also meaningfully better than the old global version. In terms of paper quality, it is one of the more honest drafts about its own risks.

The case against `STAWA-New` is that the main hostile-review explanation is still alive: this may mostly be a smarter late-phase timing rule. The project’s own results did not show a decisive jump over `SWAD`, and later work suggested noncontiguous complementarity mattered more than scalar stationarity. So even if the theory is coherent, the central signal may simply be too coarse. There is also a packaging problem now: having two near-duplicate STAWA drafts in the folder makes the line look less crisp and less mature to a reviewer.

Why these scores: moderate novelty, okay theory, decent implementation feasibility, but middling evidence and modest upside.

### 10. STAWA

`STAWA` as drafted in `stawa_neurips` is basically the same plateau-constrained family as `STAWA-New`, just packaged less explicitly. Because the files are nearly identical, I do not think there is a real scientific difference between them. The only reason I score it slightly lower is that the naming and packaging are less clean, and the near-duplicate status itself becomes a review liability.

Why these scores: same idea family as `STAWA-New`, same strengths, same weaknesses, slightly worse framing hygiene.

### 11. STAWA-Old

The best case for `STAWA-Old` is historical: it was a useful precursor that pushed the project away from flatness-only thinking and toward function-space dynamics. It also helped expose the failure mode that the global score could collapse into a coarse selector.

The case against `STAWA-Old` is straightforward. It is empirically weaker than the plateau-constrained revision, and the global score is less defensible both mathematically and operationally. At this point it reads more like an archived intermediate step than a paper to invest in.

Why these scores: the idea mattered for project learning, but as a stand-alone paper bet it is now the weakest of the major drafts.

## External Novelty Calibration

These external references matter for how I scored novelty:
- Predictive multiplicity and Rashomon sets are already active topics, which raises the bar for `CORA` novelty. See [Rashomon Capacity](https://arxiv.org/abs/2206.01295) and the newer ICLR 2024 multiplicity work at [ICLR Proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/file/8cd1ce03ea58b3d7dfd809e4d42f08ea-Paper-Conference.pdf).
- Last-layer retraining without group labels already exists, which means `TRIBE` is novel because of the trajectory-basis repair mechanism, not because “last-layer repair” itself is new. See [SELF / Towards Last-layer Retraining for Group Robustness with Fewer Annotations](https://proceedings.neurips.cc/paper_files/paper/2023/hash/265bee74aee86df77e8e36d25e786ab5-Abstract-Conference.html).
- Local chi-square DRO is classical enough that `RIWA` gets theory credibility but not maximal novelty. See [Sample Complexity for Distributionally Robust Learning under chi-square divergence](https://www.jmlr.org/papers/v24/22-0881.html).

## If I Had to Pick One to Develop Further

If the question is **which single method should we actually push next given the results we already have**, I would pick `PRISM`.

Why:
- it is the strongest domain-label-free method with real empirical signal right now
- it already slightly beat `SWAD` on the four-split PACS sweep
- it has much better theory/deployment alignment than `SCOUT`
- it is far lower risk than `TRIBE`, which still has zero direct evidence
- the cross-pool result gave a concrete target for improvement: the `PRISM` objective is the weak point, not just the pool

If domain labels were allowed, I would still pick `D-COLA` as the strongest raw empirical branch.

If the goal is a moonshot rather than the safest next step, then `TRIBE` is the best high-upside research bet after `PRISM`, because it is the only proposal here that plausibly escapes the selector/soup ceiling entirely.

## Bottom Line

My blunt ranking is:
- best empirical paper: `D-COLA`
- best label-free paper with actual evidence: `PRISM`
- highest-upside untested idea: `TRIBE`
- most elegant but empirically weakened theory-first selector: `SCOUT`
- most likely archived stepping stones rather than final bets: the `STAWA` family and `ROWA`
