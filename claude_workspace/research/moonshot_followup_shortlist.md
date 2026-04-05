---
title: Moonshot Follow-Up Shortlist
description: Short comparative memo ranking the three post-moonshot follow-up proposals and recording the exact empirical signals that justify each one.
created: 2026-04-03 19:45
last_modified: 2026-04-03 19:45
last_modified_by: codex
status: active
related_files:
  - claude_workspace/research/spectral_subset_soup_proposal.md
  - claude_workspace/research/graph_diffusion_subset_soup_proposal.md
  - claude_workspace/research/gibbs_topk_subset_soup_proposal.md
  - claude_workspace/results/shotgun_painting_nuclear_v2/shotgun_summary.json
  - claude_workspace/results/moonshot_2_painting_nuclear_v1/moonshot_2_summary.json
key_functions:
  - Record the three live follow-up method directions after the shotgun and moonshot probe batteries
  - State the current ranking, empirical trigger, and recommended implementation order
  - Preserve the exact probe IDs that justified the shortlist
latest_change: Initial shortlist memo created after comparing the full shotgun, moonshot, and moonshot_2 frontiers.
---

# Moonshot Follow-Up Shortlist

## 1. Current Ranking

1. **Spectral Subset Soup**
2. **Graph Diffusion Subset Soup**
3. **Gibbs Top-K Subset Soup**

## 2. Why This Ranking

### 2.1 Spectral Subset Soup

Best live probe:

- `spectral_subset_cos_k024_r04 = 0.87109375` full / `0.8948655256723717` out

Why it ranks first:

- strongest new out point,
- sparse and deployable,
- clearly geometry-based,
- strongest balance of novelty and empirical signal.

### 2.2 Graph Diffusion Subset Soup

Best live probe:

- `diffuse_cos_bestmean_a06_s01_logit = 0.87451171875` full / `0.8899755501222494` out

Why it ranks second:

- best balanced new geometry-weighted family,
- attractive anchor-plus-neighborhood interpretation,
- but currently still probe-defined by a full-bank soft weight vector.

### 2.3 Gibbs Top-K Subset Soup

Best balanced live probe:

- `gibbs_uniform_supportmean_t0p02_prob = 0.87158203125` full / `0.8924205378973105` out

Best full live probe:

- `gibbs_recency_supporttail_t0p01_logit = 0.87841796875` full / `0.8753056234718827`

Why it ranks third:

- real signal,
- theory-friendly,
- but lower novelty and higher risk of collapsing to a smoothed quality subset.

## 3. Important Reference Baselines

Uniform-all:

- `0.8642578125` full / `0.882640586797066` out

Best balanced old point:

- `even_018_prob = 0.87158203125` full / `0.8924205378973105` out

Best full old point:

- `diverse_supporttail_k007_l10 = 0.8798828125` full / `0.8679706601466992` out

## 4. Practical Recommendation

Implementation order:

1. implement Spectral Subset Soup
2. implement Graph Diffusion Subset Soup
3. implement Gibbs Top-K Subset Soup

The required gate for all three:

> convert the live probe into the actual deployable weight-space soup and check whether the gain survives translation.

If that probe-to-soup translation fails, the family should be demoted regardless of how good the replay-only probe looked.
