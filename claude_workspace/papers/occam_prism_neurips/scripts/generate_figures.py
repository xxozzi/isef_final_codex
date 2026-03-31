#!/usr/bin/env python
"""Generate original figures for the Occam-PRISM NeurIPS paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


BG = "#f6f3ed"
INK = "#202531"
TEAL = "#2d8f85"
ORANGE = "#e07a5f"
GOLD = "#e9c46a"
BLUE = "#4b6cb7"
SLATE = "#7c8da6"
SAND = "#d9d2c1"
MOSS = "#7a9d54"


def _setup() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(14, 4.3))
    ax.set_xlim(0, 16.5)
    ax.set_ylim(0, 4.5)
    ax.axis("off")

    boxes = [
        (0.4, "Dense trajectory", "one source-pooled run\nmany checkpoints"),
        (3.5, "Validation families", "multiple $(\\varepsilon,\\tau,M)$\nfamily definitions"),
        (6.6, "Admissible set", "keep only tractable\nexact-search families"),
        (9.7, "Support regret", "exact top-$\\alpha$ regret\non actual soups"),
        (12.8, "Occam choice", "empirical regret\nplus family penalty"),
    ]
    for x0, title, subtitle in boxes:
        patch = FancyBboxPatch(
            (x0, 1.0),
            2.55,
            2.2,
            boxstyle="round,pad=0.18,rounding_size=0.15",
            facecolor="white",
            edgecolor=INK,
            linewidth=1.3,
        )
        ax.add_patch(patch)
        ax.text(x0 + 1.275, 2.45, title, ha="center", va="center", fontsize=12, fontweight="bold")
        ax.text(x0 + 1.275, 1.65, subtitle, ha="center", va="center", fontsize=10)

    for x in [2.95, 6.05, 9.15, 12.25]:
        ax.add_patch(FancyArrowPatch((x, 2.1), (x + 0.55, 2.1), arrowstyle="-|>", mutation_scale=15, lw=1.5, color=INK))

    xs = np.linspace(0.8, 2.55, 10)
    ys = 2.2 + 0.45 * np.sin(np.linspace(0, 3.4, 10))
    ax.plot(xs, ys, color=TEAL, lw=2.5)
    ax.scatter(xs, ys, c=TEAL, s=25, zorder=4)

    grid_x = np.array([3.95, 4.45, 4.95, 5.45])
    grid_y = np.array([1.45, 2.05, 2.65])
    for i, gx in enumerate(grid_x):
        for j, gy in enumerate(grid_y):
            fc = SAND if (i + j) % 2 == 0 else GOLD
            ax.add_patch(Rectangle((gx - 0.18, gy - 0.18), 0.36, 0.36, facecolor=fc, edgecolor="white"))
    ax.text(4.7, 1.15, r"family grid", ha="center", fontsize=9)

    admissible = [(7.0, 2.55), (7.55, 1.7), (8.05, 2.2), (8.55, 1.45)]
    rejected = [(6.95, 1.25), (8.6, 2.8)]
    for x0, y0 in admissible:
        ax.scatter([x0], [y0], s=120, color=BLUE, edgecolor="white", linewidth=1.0, zorder=4)
    for x0, y0 in rejected:
        ax.scatter([x0], [y0], s=120, color=SAND, edgecolor=ORANGE, linewidth=1.5, marker="X", zorder=4)
    ax.text(7.75, 1.05, r"|A_gamma| <= Kmax", ha="center", fontsize=9)

    support_x = np.arange(10.2, 11.95, 0.22)
    vals = np.array([0.15, 0.35, 0.25, 0.6, 0.55, 0.8, 0.3, 0.7])
    ax.bar(support_x, vals, width=0.16, bottom=1.15, color=SLATE)
    ax.add_patch(Rectangle((11.2, 1.15), 0.62, 1.05, facecolor=ORANGE, alpha=0.22, edgecolor=ORANGE, linewidth=1.2))
    ax.text(11.5, 2.35, r"top-$\alpha$", ha="center", fontsize=9, color=ORANGE)

    ax.text(14.0, 2.3, r"regret(gamma,S) + pen(gamma)", ha="center", fontsize=13)
    ax.text(14.0, 1.55, "select one family-action pair", ha="center", fontsize=10)
    _save(fig, "prism_pipeline.pdf")


def figure_family_frontier() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 5.1))
    families = ["A", "B", "C", "D", "E", "F", "G"]
    empirical = np.array([0.19, 0.16, 0.12, 0.11, 0.09, 0.085, 0.082])
    penalty = np.array([0.01, 0.025, 0.045, 0.06, 0.09, 0.13, 0.18])
    total = empirical + penalty
    idx = int(np.argmin(total))

    ax.scatter(empirical, penalty, s=170, c=[TEAL if i != idx else ORANGE for i in range(len(families))], zorder=4)
    for i, name in enumerate(families):
        ax.text(empirical[i] + 0.002, penalty[i] + 0.003, name, fontsize=10)

    ax.plot(empirical, penalty, color=SLATE, lw=1.2, alpha=0.5)
    ax.scatter([empirical[idx]], [penalty[idx]], s=270, facecolors="none", edgecolors=ORANGE, linewidths=2.0, zorder=5)
    ax.annotate(
        "chosen by PRISM",
        xy=(empirical[idx], penalty[idx]),
        xytext=(0.16, 0.145),
        arrowprops=dict(arrowstyle="->", color=INK, lw=1.3),
        fontsize=10,
    )
    ax.set_xlabel("empirical hidden-subpopulation regret")
    ax.set_ylabel("Occam penalty")
    ax.set_title("PRISM searches over families on a regret-penalty frontier")
    _save(fig, "family_frontier.pdf")


def figure_budget_frontier() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8), sharey=True)
    eps = [0.02, 0.03, 0.05]
    taus = [0.02, 0.03, 0.05]
    mats = [
        np.array([[6, 9, 14], [8, 13, 22], [11, 21, 37]]),
        np.array([[18, 31, 57], [27, 44, 83], [40, 78, 129]]),
        np.array([[55, 97, 180], [73, 146, 263], [111, 221, 405]]),
    ]
    titles = [r"$M=1$", r"$M=2$", r"$M=3$"]
    for ax, mat, title in zip(axes, mats, titles):
        im = ax.imshow(mat, cmap="YlGnBu")
        ax.set_xticks(range(3), labels=[str(t) for t in taus])
        ax.set_yticks(range(3), labels=[str(e) for e in eps])
        ax.set_xlabel(r"$\tau$")
        ax.set_title(title)
        for i in range(3):
            for j in range(3):
                val = mat[i, j]
                color = "white" if val > mat.max() * 0.45 else INK
                ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=10, fontweight="bold")
    axes[0].set_ylabel(r"$\varepsilon$")
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.82)
    cbar.set_label("action count")
    fig.suptitle("Admissible family size changes sharply across validation thresholds and soup size")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "search_budget_frontier.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "family_grid_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)


def figure_tail_geometry() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.7))
    vals = np.array([-0.35, -0.1, 0.05, 0.18, 0.35, 0.62, 0.88, 1.15, 1.62, 2.05])
    order = np.argsort(vals)
    vals = vals[order]
    x = np.arange(len(vals))
    tail = 4
    colors = [SAND] * len(vals)
    for i in range(len(vals) - tail, len(vals)):
        colors[i] = ORANGE
    ax.bar(x, vals, color=colors, edgecolor="white")
    ax.axvline(len(vals) - tail - 0.5, color=INK, ls="--", lw=1.2)
    ax.annotate(
        r"capped adversary q in Q_alpha^n",
        xy=(len(vals) - 2, 1.5),
        xytext=(1.0, 1.85),
        arrowprops=dict(arrowstyle="->", lw=1.3, color=INK),
        fontsize=10,
    )
    ax.text(len(vals) - tail + 0.2, 2.18, r"selected top-$\alpha$ tail", color=ORANGE, fontsize=10)
    ax.set_xticks([])
    ax.set_ylabel("pairwise gap")
    ax.set_title("Worst-case hidden-subpopulation regret is a top-alpha mean of pairwise soup gaps")
    _save(fig, "tail_regret_geometry.pdf")


def figure_interval_domination() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 4.9))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    outer = FancyBboxPatch((0.7, 0.9), 8.6, 4.6, boxstyle="round,pad=0.2,rounding_size=0.2", facecolor="#fffdf8", edgecolor=INK, linewidth=1.4)
    mid = FancyBboxPatch((2.0, 1.7), 5.9, 3.0, boxstyle="round,pad=0.2,rounding_size=0.16", facecolor="#eef7f4", edgecolor=TEAL, linewidth=1.4)
    inner = FancyBboxPatch((3.2, 2.35), 3.5, 1.7, boxstyle="round,pad=0.2,rounding_size=0.14", facecolor="#fff4df", edgecolor=GOLD, linewidth=1.4)
    ax.add_patch(outer)
    ax.add_patch(mid)
    ax.add_patch(inner)
    ax.text(5.0, 5.1, r"all admissible families across gamma in Gamma_adm", ha="center", fontsize=12, fontweight="bold")
    ax.text(5.0, 4.0, r"subset soups searched by PRISM", ha="center", fontsize=11, color=TEAL)
    ax.text(5.0, 3.05, r"interval-only subfamilies", ha="center", fontsize=11, color=INK)
    ax.add_patch(FancyArrowPatch((7.2, 3.0), (8.9, 3.0), arrowstyle="-|>", mutation_scale=16, color=ORANGE, lw=1.6))
    ax.text(9.15, 3.0, "certificate\ndomination", va="center", fontsize=10, color=ORANGE)
    _save(fig, "interval_domination.pdf")


def figure_alpha_curve() -> None:
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    alpha = np.linspace(0.08, 1.0, 220)
    curve_a = 0.1 + 0.42 / (1 + np.exp(6.5 * (alpha - 0.33)))
    curve_b = 0.08 + 0.33 / (1 + np.exp(8.0 * (alpha - 0.45)))
    threshold = 0.24
    idx = np.where(curve_b <= threshold)[0][0]
    alpha_star = alpha[idx]

    ax.plot(alpha, curve_a, color=SLATE, lw=2.0, label="candidate soup A")
    ax.plot(alpha, curve_b, color=TEAL, lw=2.6, label="selected soup")
    ax.axhline(threshold, color=ORANGE, ls="--", lw=1.4)
    ax.axvline(alpha_star, color=ORANGE, ls="--", lw=1.4)
    ax.scatter([alpha_star], [threshold], s=85, color=ORANGE, zorder=4)
    ax.text(alpha_star + 0.015, threshold + 0.012, r"$\alpha^\star_\tau$", color=ORANGE, fontsize=11)
    ax.set_xlabel(r"hidden-subpopulation mass lower bound $\alpha$")
    ax.set_ylabel(r"worst-case regret $\Psi_\alpha$")
    ax.set_title("PRISM produces monotone hidden-subpopulation certificates")
    ax.legend(frameon=False)
    _save(fig, "alpha_certificate_curve.pdf")


def main() -> None:
    _setup()
    figure_pipeline()
    figure_family_frontier()
    figure_budget_frontier()
    figure_tail_geometry()
    figure_interval_domination()
    figure_alpha_curve()


if __name__ == "__main__":
    main()
