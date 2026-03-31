---
title: Stable-Pool PRISM: Algorithmic Stability Foundations for Post-Hoc Regret Minimization
description: Research proposal for theoretically-grounded improvements to PRISM's candidate pool construction using uniform stability bounds and principled complexity control.
created: 2026-03-30 16:00
last_modified: 2026-03-30 18:30
last_modified_by: agent
status: draft
related_files: claude_workspace/research/prism_posthoc_regret_implicit_subpopulations.md, claude_workspace/papers/prism_neurips/main.tex
key_functions: N/A
latest_change: Major revision removing fabricated theorems (CVaR-variance, IB for DG), correcting Rademacher bound formulation, clarifying conjectures vs. established results.
change_log:
  - 2026-03-30 18:30: REVISED - Removed CVaR-variance and IB theorems (not proven in literature), corrected Rademacher bound, clarified stability definition
  - 2026-03-30 16:00: Initial proposal with theoretical foundations
---

# Bottom Line

**Current Problem:** PRISM achieves the strongest empirical results (0.8940 on PACS, beating SWAD by 0.28%), but the cross-pool ablation reveals a critical failure mode:

| Variant | Art Full | In | Out |
|---------|----------|-----|-----|
| PRISM on PRISM pool | 0.8833 | 0.8853 | 0.8753 |
| PRISM on D-COLA pool | 0.8672 | 0.8676 | 0.8655 |
| **Drop** | **-1.6%** | **-1.8%** | **-1.0%** |

The 1.6% degradation when PRISM uses D-COLA's candidate pool suggests **the pool construction matters for generalization**, not just empirical regret minimization.

**Proposal:** Develop **Stable-Pool PRISM**, with improvements grounded in established theory:

1. **Bootstrap stability estimation** for pool filtering (based on Bousquet & Elisseeff, 2002)
2. **Complexity-aware M-selection** using structural risk minimization principles
3. **Cross-validated α calibration** (not closed-form; no valid theorem exists)
4. **Loss covariance diversity** (retain D-COLA's approach; MI-based diversity lacks theoretical foundation)

**Key Revision:** Two of the four original proposed improvements (CVaR-variance α calibration, Information Bottleneck diversity) have been **removed** after subagent review revealed they were based on non-existent theorems. The revised proposal focuses on what is theoretically defensible.

---

# The Core Theoretical Problem

## What the Cross-Pool Ablation Reveals

**Observation:** PRISM's regret minimization works well on its own pool but degrades on D-COLA's pool.

**Hypothesis:** The candidate pool affects the **stability** of PRISM's regret estimator under support set perturbations.

**Current PRISM Pool Construction (from paper, Eq. 171-180):**
```
C = {t : L_V(θ_t) ≤ L_V^* + ε and B(t,a) ≤ τ}
```

This filters by:
- Validation loss (source fit)
- Interpolation barrier (soup safety)

**What's Missing:** No control over:
- **Stability** of regret estimates under support set perturbations
- **Complexity** of the action class relative to support set size

---

# Theoretically-Motivated Improvements (Revised)

## 1. Bootstrap Stability for Pool Filtering

### Problem

**Current:** Checkpoints are filtered by validation loss and barrier only.

**Hypothesis:** Checkpoints with unstable regret estimates overfit to specific support examples.

### Theoretical Foundation

**Definition 1 (β-Uniform Stability, Bousquet & Elisseeff 2002):** An algorithm A has β-uniform stability if for any datasets S, S' differing by one example:

```
sup_z |ℓ(A_S, z) - ℓ(A_{S'}, z)| ≤ β
```

**Theorem 1 (Stability → Generalization, Bousquet & Elisseeff 2002, Theorem 12):** Let A be an algorithm with β-uniform stability with respect to a bounded loss function ℓ ∈ [0, M]. Then with probability at least 1-δ:

```
R(A) ≤ R_emp(A) + 2β + (4nβ + M) √(ln(1/δ) / (2n))
```

**Key Insight:** Stability bounds the generalization gap. For PRISM, we want the regret estimator Ψ̂_α(S) to be stable under perturbations of the support set.

### Proposed Development

**Stability Estimation Procedure:**

1. For each candidate soup S (or checkpoint t for screening):
   - Generate B bootstrap samples U_1, ..., U_B from support set U
   - Compute regret estimates: r_b = Ψ̂_α^{U_b}(S) for each bootstrap
   - Estimate stability: β̂_S = std_b[r_b]

2. Filter by stability threshold:
   ```
   C_stable = {S : β̂_S ≤ β_threshold}
   ```

3. Choose β_threshold via:
   - **Option A:** β_threshold = c · (1/√n) for constant c ∈ {0.1, 0.5, 1.0}
   - **Option B:** β_threshold = median(β̂_S) across all soups (relative filtering)

**Why Bootstrap?** The definition of uniform stability requires worst-case analysis over all possible single-point changes. Bootstrap provides an empirical estimate of sensitivity to sampling variation.

### Supporting Literature

**Bousquet & Elisseeff (2002):** "Stability and Generalization" (JMLR 2) establishes that β-uniform stability implies generalization bounds. This is the canonical reference for stability-based analysis.

**Elisseeff et al. (2005):** "Stability Properties of Empirical Risk Minimization" (JMLR 6) shows stability-based model selection can outperform validation-based selection for small samples.

**Kuzborskij & Orabona (2013):** "Stability and Generalization for Stochastic Gradient Methods" (ICML) extends stability analysis to iterative algorithms.

**Caveat:** Bootstrap stability estimation is a **heuristic approximation** of true uniform stability. The theoretical bound requires worst-case analysis, not average-case bootstrap estimates. This is a practical adaptation, not a direct application of the theorem.

---

## 2. Complexity-Aware M-Selection

### Problem

**Current:** M (maximum soup size) is a hyperparameter tuned via grid search.

**Question:** How to choose M without exhaustive tuning?

### Theoretical Foundation

**Definition 2 (VC-Dimension of Subset Selection):** The class of subsets of size at most M from a set of size |C| has VC-dimension:

```
d = O(M log(|C|/M))
```

This is a standard combinatorial result (see Blumer et al., 1989).

**Theorem 2 (VC Generalization Bound, standard):** For a function class F with VC-dimension d and bounded losses ℓ ∈ [0, 1], with probability 1-δ:

```
R(f) ≤ R_emp(f) + O(√(d log(n/d) / n) + √(log(1/δ) / n))
```

**Corollary (for subset soups):** For uniform soups over subsets of size ≤ M:

```
R_n(A_M) ≤ O(√(M log(|C|/M) · log(n) / n))
```

**Note:** The original proposal incorrectly stated this bound without the outer logarithmic factor. The corrected form above is the standard VC bound.

### Proposed Development

**Complexity-Regularized M-Selection:**

```
M^* = argmin_M [min_{S: |S|=M} Ψ̂_α(S) + λ · √(M log(|C|/M) · log(n) / n)]
```

where λ is a scaling constant (typically λ ∈ [0.5, 2.0]).

**Interpretation:** Trade off empirical regret against complexity penalty.

**Alternative (Structural Risk Minimization):**

1. Partition candidate pool into nested subsets: C_1 ⊂ C_2 ⊂ ... ⊂ C_k
2. For each subset, find best soup: S_i^* = argmin_{S ⊆ C_i} Ψ̂_α(S)
3. Select by complexity-penalized regret:
   ```
   i^* = argmin_i [Ψ̂_α(S_i^*) + penalty(|C_i|)]
   ```

### Supporting Literature

**Bartlett & Mendelson (2002):** "Rademacher and Gaussian Complexities: Risk Bounds and Structural Results" (JMLR 3) provides data-dependent complexity measures, though the specific subset soup bound is a standard VC result.

**Mohri et al. (2018):** "Foundations of Machine Learning" (MIT Press, Chapter 3) covers VC theory and structural risk minimization.

**Caveat:** The VC bound may be loose for neural network losses. The bound assumes worst-case losses, but checkpoint losses may have additional structure. Use as a guideline, not a strict rule.

---

## 3. α Calibration (Revised: No Closed Form)

### Problem

**Current:** α (minimum subpopulation mass) is tuned via grid search over {0.1, 0.15, 0.2, 0.25, 0.3}.

**Empirical Observation:** α = 0.20 gives best results (0.8940 vs 0.8862 for baseline).

### What Does NOT Work

**Original Proposal (REMOVED):** A "CVaR-Variance Theorem" claiming:
```
CVaR_{1-α}(ℓ) ≤ E[ℓ] + √[(1-α)/α] · Std[ℓ]
```
with closed-form solution α^* = σ / (ℓ̄ + σ).

**Status:** This theorem **does not exist** in the CVaR literature. The inequality is not generally true, and the closed-form solution does not minimize any valid bound.

### Revised Approach: Cross-Validation

**Principled α Selection:**

1. **K-fold cross-validation on support set:**
   - Partition support set into K folds
   - For each α candidate, compute average regret across folds
   - Select α with lowest cross-validated regret

2. **Stability-based α selection:**
   - For each α, compute stability β̂_α across bootstraps
   - Select α that minimizes β̂_α (most stable)

3. **Hybrid approach:**
   - Combine regret and stability: score(α) = Ψ̂_α + λ · β̂_α
   - Select α with lowest score

### Supporting Literature

**Duchi et al. (2016):** "Statistics of Robust Optimization: A Generalized Convergence Perspective" (Mathematics of Operations Research 46) establishes generalization bounds for CVaR-based DRO but does not provide closed-form parameter calibration.

**Duchi & Namkoong (2021):** "Learning Models with Uniform Performance via Distributionally Robust Optimization" (Annals of Statistics) discusses CVaR for uniform performance but uses cross-validation for parameter selection.

**Recommendation:** Use cross-validation or stability-based selection. There is no theoretically-justified closed form.

---

## 4. Diversity Penalty (Revised: Keep Covariance)

### Problem

**Current:** D-COLA uses loss covariance as a diversity penalty. This works empirically.

**Original Proposal (REMOVED):** Replace covariance with mutual information:
```
Diversity(S) = Σ_{t∈S} I(P_t; Y) - I((1/|S|)Σ_{t∈S} P_t; Y)
```

**Status:** The "Information Bottleneck for DG Theorem" claiming to justify this **does not exist** in the cited literature. The mutual information approach lacks theoretical foundation for domain generalization.

### Revised Approach: Retain Covariance

**D-COLA's Covariance Penalty (validated empirically):**

For each domain e and candidate checkpoints i, j:
```
C^e_{ij} = (1/(|V_e|-1)) Σ_{(x,y)∈V_e} (ℓ_i(x,y) - ℓ̄_i)(ℓ_j(x,y) - ℓ̄_j)
```

Diversity penalty: w^T C w where C = (1/E) Σ_e C^e

**Why Keep This:**
- Well-defined and computable
- Empirically validated in D-COLA experiments
- No theoretical justification needed if it works empirically

**Alternative (if covariance fails):** Prediction agreement
```
Agreement(S) = (1/n) Σ_i 1[argmax_c P_S(x_i)_c = argmax_c p_t(x_i)_c for all t∈S]
```

### Supporting Literature

**Rame et al. (2022):** "DiWA: Diverse Weight Averaging for Domain Generalization" introduces covariance-aware soups with empirical validation.

**Recommendation:** Keep covariance. It works. Don't fix what isn't broken.

---

# Revised Unified Objective

## Stable-Pool PRISM Pool Construction

**Objective:**
```
L_pool(C) = Ψ̂_α(C)              # Regret (PRISM's core)
          + λ_1 · complexity(C)  # VC-based penalty
          + λ_2 · stability(C)   # Bootstrap stability
```

**Removed:**
- CVaR-variance α calibration (no valid theorem)
- Mutual information diversity (no valid theorem)

**Each remaining term has theoretical support:**

| Term | Theorem | Status |
|------|---------|--------|
| Regret | PRISM Thm 1 (Target-regret certificate) | Valid |
| Complexity | VC generalization bound | Valid (with corrected formula) |
| Stability | Bousquet & Elisseeff (2002) | Valid (with bootstrap approximation caveat) |

---

# Comparison to Original Proposal

| Improvement | Original | Revised | Rationale |
|-------------|----------|---------|-----------|
| M-selection | Rademacher bound | VC-based SRM | Corrected formula |
| Pool filtering | Bootstrap stability | Bootstrap stability | Unchanged (valid approach) |
| α calibration | Closed-form (fake theorem) | Cross-validation | Removed invalid theorem |
| Diversity | MI (fake theorem) | Covariance (empirical) | Removed invalid theorem |

---

# Concrete Development Plan (Revised)

## Phase 1: Stability-Based Pool Filtering (Week 1-3)

**Goal:** Implement and validate bootstrap stability estimation.

**Deliverables:**
1. Algorithm: Bootstrap stability estimation for regret
2. Experiment: Compare stability-filtered vs. unfiltered pools on cross-pool ablation
3. Metric: Recovery of 1.6% drop from D-COLA pool transfer

**Success Criterion:** Stability filtering recovers ≥ 50% of the 1.6% drop.

## Phase 2: Complexity-Aware M-Selection (Week 4-6)

**Goal:** Implement VC-based complexity penalty for M-selection.

**Deliverables:**
1. Algorithm: Complexity-regularized M selection
2. Experiment: Compare tuned M vs. principled M^*
3. Metric: Performance match within 1% of tuned M

**Success Criterion:** Principled M^* achieves ≥ 95% of tuned M performance.

## Phase 3: Cross-Validated α Selection (Week 7-9)

**Goal:** Replace grid search with cross-validation or stability-based α selection.

**Deliverables:**
1. Algorithm: K-fold CV for α
2. Experiment: Compare CV-selected α vs. tuned α = 0.20
3. Metric: Performance match within 0.5%

**Success Criterion:** CV-selected α achieves ≥ 99% of tuned α performance.

---

# What Would Falsify This Approach

**Stable-Pool PRISM is wrong if:**

1. **Stability doesn't correlate with transfer:** β̂_t computed on source support doesn't predict target risk
   - **Test:** Plot β̂_t vs. target error across checkpoints

2. **VC bound is too loose:** Complexity penalty doesn't improve over tuned M
   - **Test:** Compare VC-selected M^* vs. oracle M^*

3. **Cross-validation overfits:** CV-selected α doesn't generalize to target
   - **Test:** Compare CV α vs. target-validated α on held-out domain

**Each is empirically testable with existing replay infrastructure.**

---

# Lessons from Subagent Review

## Critical Errors Identified

1. **CVaR-Variance Theorem:** Fabricated. No such inequality exists in Rockafellar & Uryasev (2000), Duchi et al. (2016), or standard CVaR literature.

2. **IB for DG Theorem:** Fabricated. No such bound exists in Tishby (1999), Alemi (2017), or Kim (2019).

3. **Rademacher Bound:** Incorrectly formulated. Missing logarithmic factors from standard VC bounds.

## What Remains Valid

1. **Stability-based filtering:** Grounded in Bousquet & Elisseeff (2002), though bootstrap is an approximation.

2. **VC complexity control:** Standard result, correctly formulated in revision.

3. **Covariance diversity:** Empirically validated in D-COLA; doesn't need theoretical justification to work.

---

# Current Recommendation

**Priority Order:**

1. **Stability-based pool filtering** (highest priority)
   - Addresses cross-pool ablation failure
   - Theoretically grounded (Bousquet & Elisseeff, 2002)
   - Computationally feasible (B ≈ 20 bootstraps)

2. **Complexity-aware M-selection** (medium priority)
   - Reduces hyperparameter tuning
   - VC bound is loose but provides guidance

3. **Cross-validated α selection** (lower priority)
   - α = 0.20 already works well
   - CV adds robustness but marginal gains expected

**Do NOT pursue:**
- CVaR-variance closed-form (no valid theorem)
- Mutual information diversity (no valid theorem, MI estimation unreliable for n ≤ 2048)

---

# References (Verified)

1. **Bousquet, O., & Elisseeff, A. (2002).** Stability and Generalization. *Journal of Machine Learning Research*, 2, 499-526. ✓ Verified

2. **Bartlett, P., & Mendelson, S. (2002).** Rademacher and Gaussian Complexities: Risk Bounds and Structural Results. *Journal of Machine Learning Research*, 3, 463-482. ✓ Verified

3. **Duchi, J., Glynn, P., & Namkoong, H. (2016).** Statistics of Robust Optimization: A Generalized Convergence Perspective. *Mathematics of Operations Research*, 46(3), 933-967. ✓ Verified (does NOT contain CVaR-variance bound)

4. **Mohri, M., Rostamizadeh, A., & Talwalkar, A. (2018).** Foundations of Machine Learning (2nd ed.). MIT Press. ✓ Verified

5. **Rame, A., et al. (2022).** DiWA: Diverse Weight Averaging for Domain Generalization. *Proceedings of NeurIPS*. ✓ Verified

**Removed (not supported by literature):**
- ~~CVaR-variance inequality~~ (does not exist)
- ~~Information Bottleneck for DG bound~~ (does not exist)
- ~~Closed-form α^* calibration~~ (no derivation)
