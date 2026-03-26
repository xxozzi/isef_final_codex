---
title: Session Resume / Handoff
description: Full handoff for the single-run post-hoc domain generalization work in this repo, including implemented methods, papers, empirical findings, theory lessons, operational gotchas, and next-step guidance for restarting on a new machine with no chat history.
last_modified: 2026-03-26 15:23
last_modified_by: agent
status: active
key_functions:
  - Preserve current research/code context across chat sessions
  - Summarize verified repo state, local results, and important HPC-log findings
  - Provide a copy-paste prompt for restarting the project in a fresh chat
latest_change: Added a comprehensive restart handoff covering domaingen method implementations, current leaderboard, D-COLA ablations, SCOUT/PRISM status, theory caveats, and exact next-chat instructions.
---

# Resume

This file is the single handoff document for restarting work on this project from a fresh chat or a different machine.

It is meant to preserve:
- the current code/research state,
- the main empirical findings,
- the theory lessons learned so far,
- the open problems,
- and the exact context a new chat should recover before continuing.

## 1. Repository / Environment Snapshot

Current local repo root:

```text
/Users/jaydenjeong/Work/projects/ml/isef_final_codex
```

Important note:
- The current execution environment in this session is `zsh` on a Unix-like machine.
- `AGENTS.md` contains older PowerShell/Windows assumptions, but the actual environment used in this session was Unix/zsh.
- The HPC commands used for real experiments target:

```text
/project/jje239_dgxpublicai25/jwje228/work
```

High-level repo structure:
- `domaingen/`: main codebase for training, replay, post-hoc methods, configs, and SLURM scripts
- `claude_workspace/research/`: research memos and method proposals
- `claude_workspace/papers/`: paper drafts and NeurIPS-style manuscripts
- `claude_workspace/results/`: local copies of important result summaries and diagnostics
- `literature/`: source paper material, including SWAD, DiWA, and MIRO TeX source / PDFs

## 2. What Is Implemented in `domaingen`

The following post-hoc methods have been integrated into `domaingen`:
- `STAWA-new`
- `STAWA-old`
- `D-COLA`
- `CORA`
- `ROAR`
- `SCOUT`
- `PRISM`

Core implementation files:
- `domaingen/posthoc/stawa.py`
- `domaingen/posthoc/dcola.py`
- `domaingen/posthoc/cora.py`
- `domaingen/posthoc/roar.py`
- `domaingen/posthoc/scout.py`
- `domaingen/posthoc/prism.py`
- `domaingen/train.py`
- `domaingen/replay_methods.py`

Related configs:
- `domaingen/configs/erm_stawa_new.yaml`
- `domaingen/configs/erm_stawa_old.yaml`
- `domaingen/configs/erm_dcola.yaml`
- `domaingen/configs/erm_cora.yaml`
- `domaingen/configs/erm_roar.yaml`
- `domaingen/configs/erm_scout.yaml`
- `domaingen/configs/erm_prism.yaml`
- `domaingen/configs/coda_*.yaml` variants for several methods

Submission / replay scripts:
- `domaingen/scripts/submit.sh`
- `domaingen/scripts/template.sh`
- `domaingen/scripts/submit_replay.sh`
- `domaingen/scripts/replay_template.sh`

The repo README has been updated to describe training and replay for these methods:
- `domaingen/README.md`

## 3. Backbone / Training Facts

Verified from current configs:
- `erm_dcola.yaml`, `erm_cora.yaml`, `erm_prism.yaml`, and `erm_scout.yaml` all use:
  - `resnet18: false`
  - `clip_backbone: false`
- That means those configs use the ImageNet-pretrained ResNet-50 path, not CLIP.

Important training-path fact:
- `STAWA`, `D-COLA`, `CORA`, `ROAR`, `SCOUT`, and `PRISM` are post-hoc selectors/soupers on top of a base training run.
- `SWAD` is different: it has a training-time mechanism in this repo.

Also implemented:
- training metrics logging to `train_steps.jsonl`
- checkpoint/full-eval summaries in `results.jsonl`
- `run_manifest.json`
- per-method diagnostics JSON files

## 4. Main Papers / Memos in the Workspace

Full paper drafts exist for:
- `claude_workspace/papers/stawa_neurips/`
- `claude_workspace/papers/stawa_new/`
- `claude_workspace/papers/stawa_old/`
- `claude_workspace/papers/d_cola/`
- `claude_workspace/papers/cora_neurips/`
- `claude_workspace/papers/roar_neurips/`
- `claude_workspace/papers/scout_neurips/`

Key research memos:
- `claude_workspace/research/stationarity_aware_weight_averaging.md`
- `claude_workspace/research/cora_consensus_of_rashomon_averaging.md`
- `claude_workspace/research/scout_submodular_coverage_uniform_trajectory_soups.md`
- `claude_workspace/research/prism_posthoc_regret_implicit_subpopulations.md`
- `claude_workspace/research/circe_causal_invariance_via_reweighted_checkpoint_environments.md`
- `claude_workspace/research/adjacent_posthoc_literature_sweep.md`

Most recent memo in the markdown scanner:
- `PRISM` (`claude_workspace/research/prism_posthoc_regret_implicit_subpopulations.md`)

## 5. Verified Local Results

Primary local results file:
- `claude_workspace/results/results.jsonl`

Using that file as the local source of truth, the current leaderboard on the `erm_cora` replay bank is:

| Method | Art full | In | Out | Delta vs ERM (Art) |
|---|---:|---:|---:|---:|
| `ERM-replay` | `0.7676` | `0.7627` | `0.7873` | `+0.0000` |
| `SWAD-replay` | `0.8584` | `0.8609` | `0.8484` | `+0.0908` |
| `STAWA-new` | `0.8643` | `0.8658` | `0.8582` | `+0.0967` |
| `STAWA-old` | `0.8022` | `0.7999` | `0.8117` | `+0.0347` |
| `D-COLA` | `0.8726` | `0.8737` | `0.8680` | `+0.1050` |
| `CORA` | `0.8413` | `0.8401` | `0.8460` | `+0.0737` |
| `ROAR` | `0.8633` | `0.8639` | `0.8606` | `+0.0957` |

Current local conclusion:
- `D-COLA` is still the best recorded main method in the workspace.

Important caveat:
- These local workspace results do **not** include all later HPC-log experiments discussed in chat, especially later `SCOUT` runs and any future `PRISM` runs.
- When there is a conflict between chat snippets and local workspace files, the local file should be treated as the current verified local artifact unless the HPC run output is explicitly re-imported.

## 6. Verified Local D-COLA Ablations

Primary local ablation file:
- `claude_workspace/results/ablation_results_dcola.json`

This file is newline-delimited JSON despite the `.json` suffix.

Current ablation ranking on art accuracy:

| D-COLA variant | Art full |
|---|---:|
| `baseline` | `0.8750` |
| `uniform` | `0.8745` |
| `early` | `0.8687` |
| `no_loc` | `0.8667` |
| `pooled_anchor` | `0.8638` |
| `contiguous` | `0.8613` |
| `no_cov` | `0.8594` |

Main interpretation from the ablations:
- Exact optimized weights matter very little.
  - `uniform` is almost tied with full `D-COLA`.
- Covariance / nonredundancy matters a lot.
  - `no_cov` is the worst ablation.
- Noncontiguity matters.
  - `contiguous` is materially worse than baseline.
- Locality and anchoring help, but less than covariance.

This pushed the research direction away from fancy weight optimization and toward:
- better subset selection,
- safe complementarity,
- and more principled uniform or near-uniform soups.

## 7. Important Additional Findings From HPC Logs Discussed in Chat

These findings were observed in chat via HPC log snippets. They are important context, but they are not all currently mirrored into `claude_workspace/results/`.

### 7.1 D-COLA on the `erm_stawa` checkpoint bank

Observed log result:
- `art_painting_full_acc: 0.8745`
- `test_env0_in_acc: 0.8749`
- `test_env0_out_acc: 0.8729`

This beat:
- `SWAD` on that trajectory
- `STAWA-old`
- `STAWA-new`
- `CORA`

### 7.2 CORA on the `erm_stawa` checkpoint bank

Observed log result:
- `art_painting_full_acc: 0.8701`
- `test_env0_in_acc: 0.8749`
- `test_env0_out_acc: 0.8509`

Interpretation:
- `CORA` clearly beat both STAWA variants
- `CORA` was close to `SWAD`
- `CORA` did not cleanly beat `D-COLA`

### 7.3 SCOUT on the `erm_cora` checkpoint bank: two important runs

Observed log result A, default tighter candidate pool:
- candidates `[400, 3050, 8750]`
- uniform weights because the feasible set collapsed
- `art_painting_full_acc: 0.8706`
- `test_env0_in_acc: 0.8707`
- `test_env0_out_acc: 0.8704`

Interpretation:
- Strong result
- But mostly evidence that SCOUT candidate-pool construction was good
- Not strong evidence that the SCOUT optimizer itself was doing useful work, because the feasible set had effectively collapsed to one uniform solution

Observed log result B, looser pool (`scout_epsilon=0.03`, `scout_tau=0.03`, `scout_M=4`):
- candidates `[250, 400, 450, 1200, 1250, 2150, 2700, 2950, 3100, 4150]`
- nonuniform learned weights
- `art_painting_full_acc: 0.8477`
- `test_env0_in_acc: 0.8487`
- `test_env0_out_acc: 0.8435`

Interpretation:
- Once the SCOUT optimizer actually had room to move, performance dropped
- This suggested the current SCOUT optimizer/objective was not yet aligned tightly enough with actual soup behavior
- Specifically, there was concern about predictive-mixture improvement not transferring tightly enough to the deployed weight soup

### 7.4 PRISM status

`PRISM` was implemented as the latest theory-first method proposal, but no stable recorded PRISM leaderboard has been captured into the local workspace files yet.

## 8. Current Theory Lessons

### 8.1 What seems empirically true so far

The current strongest empirical pattern is:

> Selective, noncontiguous, soup-safe checkpoint sets matter more than exact final convex weight optimization.

Corollaries:
- simple flatness alone is not enough
- scalar checkpoint calmness / stationarity alone is not enough
- consensus alone is not enough
- exact weight optimization is secondary once a good set is identified

### 8.2 Why D-COLA currently wins

Current best explanation:
- `D-COLA` implicitly captures the right trio:
  - hard-case robustness,
  - checkpoint complementarity / nonredundancy,
  - and soup safety / locality

Even though `D-COLA` is partly heuristic, the ablations suggest it discovered something real:
- covariance matters,
- noncontiguous selection matters,
- candidate-set quality matters more than final weight refinement.

### 8.3 Why STAWA underperformed

Observed failure mode:
- `STAWA-old` and `STAWA-new` often collapsed to a single checkpoint or tiny window
- that means they often behaved more like checkpoint selection than true averaging

Interpretation:
- global or plateau-restricted stationarity alone was too coarse a signal

### 8.4 Why SCOUT was promising but not yet solved

SCOUT was designed to be more principled by directly optimizing a robust coverage objective over subsets/soups.

But the critique that emerged later was important:
- the theory/paper was not fully airtight
- the strongest result came in a degenerate case where the optimizer did almost nothing
- when the optimizer became active, performance fell

So SCOUT is useful as a research step, but not currently the champion.

### 8.5 Why PRISM became the next proposal

PRISM was proposed to fix the main criticism:
- the deployed object should be the actual soup
- the objective should directly reason about hidden subpopulation regret of that actual soup
- the method should be domain-label-free, not reliant on explicit source-domain labels

PRISM framing:
- actual action = averageable uniform soup over a candidate subset
- objective = worst-case regret over capped hidden subpopulations
- theory inspiration = minimax regret + hidden-subpopulation robustness + DORO-style capped adversary + DiWA/model-soup locality

Status:
- implemented
- not yet empirically validated enough to replace D-COLA

## 9. Important Theory Caveats / Corrections Learned So Far

These are important for future papers and new method proposals.

### 9.1 Avoid overclaiming “label-free”

The honest phrase for most of these methods is:
- `domain-label-free`

not:
- fully label-free

Reason:
- the methods still use labeled source holdout/support data
- they just do not require domain IDs

### 9.2 Avoid saying a method “directly optimizes the exact certified bound” unless it truly does

This became a major issue in the SCOUT discussion.

General rule:
- if the certificate contains a term not actually optimized, do not claim exact bound minimization
- if the theoretical object is a predictive mixture but the deployed model is a single weight soup, call that bridge an assumption / approximation, not an identity

### 9.3 Avoid circular theory

The user’s goal is explicitly:
- not to build another heuristic and then write theory around it afterward

So future methods should satisfy:
- the theoretical object is clear,
- the deployed object is the same object or a rigorously controlled approximation,
- the optimization procedure targets that object directly,
- and the assumptions are stated plainly.

## 10. Operational Gotchas

### 10.1 `__pycache__` files are tracked in `domaingen`

This caused `git pull` conflicts on HPC.

When that happens, the workaround used in chat was:

```bash
cd /project/jje239_dgxpublicai25/jwje228/work/domaingen
git restore methods/__pycache__ utils/__pycache__ posthoc/__pycache__ __pycache__
git pull
```

### 10.2 Replay directory bugs were fixed during the session

There was a replay bug where cleanup assumed the replay directory already existed.

That was fixed in the repo during the session, but if a future environment is stale, first replay runs may fail unless the updated `replay_methods.py` is present.

### 10.3 SWAD replay is approximate

The repo README explicitly notes:
- `SWAD` replay is checkpoint-based and cannot perfectly reconstruct original training-time segment averages unless every step was saved.

So:
- SWAD replay is useful and informative,
- but it is not a perfect reconstruction of native training-time SWAD.

## 11. Best Current “State of the World” Summary

If a new chat needs the shortest honest summary possible, it is this:

1. `D-COLA` is the current empirical champion in the local workspace.
2. The D-COLA ablations suggest that:
   - candidate-set quality matters more than exact weights,
   - covariance/nonredundancy matters a lot,
   - and noncontiguity matters a lot.
3. `STAWA` was an informative failure.
4. `CORA` and `ROAR` improved on some weaker ideas but did not beat `D-COLA`.
5. `SCOUT` was the strongest attempt at a more principled subset-selection theory, but its active optimizer underperformed once it had real flexibility.
6. `PRISM` is the latest attempt to align theory and deployed object more cleanly, but it still needs real experiments.

## 12. Good Next Steps

If starting fresh from this repo, the most sensible next steps are:

1. Re-run or import a clean `PRISM` replay on the same checkpoint bank as `D-COLA`.
2. If needed, assemble one single master comparison table that includes:
   - `ERM`
   - `SWAD`
   - `STAWA-old`
   - `STAWA-new`
   - `D-COLA`
   - `CORA`
   - `ROAR`
   - `SCOUT`
   - `PRISM`
3. Decide whether the next method should be:
   - a more principled subset-selection method building on the D-COLA ablation lessons, or
   - a refinement/repair of PRISM once real results come in.

## 13. Useful Commands

### 13.1 Replay the full leaderboard on one checkpoint bank

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
bash domaingen/scripts/submit_replay.sh \
  /project/jje239_dgxpublicai25/jwje228/work/results/erm_cora \
  --methods erm swad stawa_new stawa_old dcola cora roar scout prism
```

### 13.2 Replay only PRISM

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
bash domaingen/scripts/submit_replay.sh \
  /project/jje239_dgxpublicai25/jwje228/work/results/erm_cora \
  --methods prism
```

### 13.3 Run the D-COLA ablation suite

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
bash domaingen/scripts/submit_replay.sh \
  /project/jje239_dgxpublicai25/jwje228/work/results/erm_cora \
  --methods dcola_ablate
```

### 13.4 Train a new PRISM run

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
bash domaingen/scripts/submit.sh domaingen/configs/erm_prism.yaml
```

### 13.5 Train a new D-COLA run

```bash
cd /project/jje239_dgxpublicai25/jwje228/work
bash domaingen/scripts/submit.sh domaingen/configs/erm_dcola.yaml
```

## 14. Key Files a New Chat Should Read First

If there is time to read only a few files:
- `resume.md`
- `AGENTS.md`
- `domaingen/README.md`
- `claude_workspace/results/results.jsonl`
- `claude_workspace/results/ablation_results_dcola.json`
- `claude_workspace/research/prism_posthoc_regret_implicit_subpopulations.md`
- `claude_workspace/research/scout_submodular_coverage_uniform_trajectory_soups.md`
- `domaingen/replay_methods.py`
- `domaingen/posthoc/dcola.py`
- `domaingen/posthoc/prism.py`

If there is time for paper-level context too:
- `claude_workspace/papers/d_cola/d_cola_neurips.tex`
- `claude_workspace/papers/scout_neurips/main.tex`
- `literature/swad_tex_source/2.theoretical_analysis.tex`
- `literature/diwa_tex_source/sections/theory/theory_bvc.tex`
- `literature/diwa_tex_source/sections/theory/theory_locality_linearity.tex`

## 15. Copy-Paste Prompt for the Next Chat

Use this as the first prompt in the next chat:

```text
We’re continuing the post-hoc domain generalization project in this repo. Please get up to speed from the local files instead of asking me to re-explain things.

Start by reading:
1. resume.md
2. AGENTS.md
3. domaingen/README.md
4. claude_workspace/results/results.jsonl
5. claude_workspace/results/ablation_results_dcola.json

Then read the most relevant method/theory files referenced in resume.md, especially the current leading code paths and the latest proposal/memo.

After that:
- summarize the current empirical state,
- summarize the current theory state,
- call out any important inconsistencies or open risks,
- and recommend the single best next step.

Do not ask me to summarize prior chat history. Use the repo files as the source of truth, and explicitly distinguish between facts verified from files versus anything that appears to come only from prior discussion.
```

## 16. Final Note

This file is intentionally opinionated in a few places, but it tries to separate:
- verified local artifact facts,
- HPC-log observations seen in chat,
- and higher-level interpretations.

If a future chat finds a conflict:
- prefer the actual code and local result files first,
- then prefer fresh HPC artifacts,
- then treat this file’s interpretations as working hypotheses rather than immutable truth.
