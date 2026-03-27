#!/usr/bin/env python
"""Generate original figures for the PRISM NeurIPS paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


BG = "#f7f4ee"
INK = "#1f2430"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
BLUE = "#457b9d"
PLUM = "#7b6d8d"
GRAY = "#d6d1c4"


def _setup():
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


def figure_overview() -> None:
    fig, ax = plt.subplots(figsize=(14, 3.8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 4)
    ax.axis("off")

    stages = [
        (0.5, "Dense trajectory", "Single run with frequent checkpoints"),
        (3.6, "Barrier screen", "Near-optimal and averageable candidates"),
        (6.7, "Deployable actions", "Uniform soups over feasible subsets"),
        (9.8, "Hidden subpopulations", "Top-alpha adversary over source support"),
        (12.9, "PRISM selector", "Minimize worst-case regret to best feasible soup"),
    ]

    for x0, title, subtitle in stages:
        box = FancyBboxPatch(
            (x0, 1.0),
            2.4,
            2.0,
            boxstyle="round,pad=0.18,rounding_size=0.14",
            facecolor="white",
            edgecolor=INK,
            linewidth=1.3,
        )
        ax.add_patch(box)
        ax.text(x0 + 1.2, 2.45, title, ha="center", va="center", fontsize=12, fontweight="bold")
        ax.text(x0 + 1.2, 1.7, subtitle, ha="center", va="center", fontsize=10, wrap=True)

    for x in [2.95, 6.05, 9.15, 12.25]:
        arrow = FancyArrowPatch((x, 2.0), (x + 0.5, 2.0), arrowstyle="-|>", mutation_scale=15, lw=1.5, color=INK)
        ax.add_patch(arrow)

    xs = np.linspace(0.9, 2.5, 9)
    ys = 2.1 + 0.35 * np.sin(np.linspace(0, 3.1, 9))
    ax.plot(xs, ys, color=TEAL, lw=2.5)
    ax.scatter(xs, ys, c=[TEAL] * 9, s=22, zorder=3)

    bars_x = np.array([4.0, 4.28, 4.56, 4.84, 5.12, 5.40])
    vals = np.array([1.6, 1.4, 1.1, 0.9, 0.85, 0.88])
    ax.bar(bars_x, vals, width=0.18, color=[GRAY, GRAY, TEAL, TEAL, TEAL, GRAY], bottom=1.0)

    soup_points = [(7.2, 2.55), (7.9, 1.5), (8.5, 2.35), (8.85, 1.7)]
    for xp, yp in soup_points:
        ax.scatter([xp], [yp], s=110, color=BLUE, edgecolor="white", linewidth=1.0, zorder=4)
    for i, (x1, y1) in enumerate(soup_points):
        for x2, y2 in soup_points[i + 1 :]:
            ax.plot([x1, x2], [y1, y2], color=BLUE, alpha=0.25, lw=1.5)

    support_x = np.linspace(10.2, 11.8, 8)
    heights = [0.35, 0.5, 0.3, 0.7, 0.45, 0.9, 0.4, 0.55]
    ax.bar(support_x, heights, width=0.16, bottom=1.1, color=PLUM, alpha=0.75)
    ax.add_patch(Rectangle((11.3, 1.1), 0.55, 1.2, facecolor=ORANGE, alpha=0.25, edgecolor=ORANGE, lw=1.2))
    ax.text(11.57, 2.45, "top-alpha", ha="center", va="bottom", fontsize=9, color=ORANGE)

    ax.text(14.1, 2.25, r"$\min_S \max_q$", fontsize=22, ha="center", va="center")
    ax.text(14.1, 1.55, "actual deployed soup", fontsize=10, ha="center")
    _save(fig, "prism_overview.pdf")


def figure_noise_vs_regret() -> None:
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    subgroups = np.arange(5)
    irreducible = np.array([0.08, 0.22, 0.16, 0.31, 0.11])
    soup_a = np.array([0.10, 0.20, 0.14, 0.26, 0.12])
    soup_b = np.array([0.14, 0.24, 0.17, 0.35, 0.16])
    oracle = np.array([0.07, 0.18, 0.12, 0.24, 0.09])

    width = 0.26
    ax.bar(subgroups - width, irreducible + soup_a, width=width, color=TEAL, label="raw risk: soup A")
    ax.bar(subgroups, irreducible + soup_b, width=width, color=BLUE, label="raw risk: soup B")
    ax.scatter(subgroups - width, soup_a - oracle, color=ORANGE, s=60, zorder=4, label="regret: soup A")
    ax.scatter(subgroups, soup_b - oracle, color=PLUM, s=60, zorder=4, label="regret: soup B")
    ax.plot(subgroups + width, irreducible + oracle, color=INK, lw=2.2, marker="o", label="oracle frontier")

    ax.set_xticks(subgroups)
    ax.set_xticklabels([f"group {i+1}" for i in subgroups])
    ax.set_ylabel("loss scale")
    ax.set_title("Raw risk mixes subgroup difficulty with excess loss; regret removes the subgroup-specific floor")
    ax.legend(loc="upper left", ncol=2, frameon=False)
    _save(fig, "risk_vs_regret_noise.pdf")


def figure_action_family() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    trajectory_steps = np.array([1, 2, 3, 4, 5, 6, 7])
    ax.scatter(trajectory_steps, np.zeros_like(trajectory_steps), s=70, color=BLUE, zorder=3)
    for step in trajectory_steps:
        ax.text(step, -0.18, str(step), ha="center", va="top", fontsize=10)

    safe_subsets = {
        1: [(1,), (3,), (4,), (6,), (7,)],
        2: [(1, 3), (1, 4), (3, 4), (4, 6), (6, 7)],
        3: [(1, 3, 4), (3, 4, 6), (4, 6, 7)],
    }
    interval_subsets = {(3,), (4,), (6,), (3, 4), (4, 6), (6, 7), (3, 4, 6), (4, 6, 7)}

    y_levels = {1: 0.9, 2: 1.9, 3: 2.9}
    for size, subsets in safe_subsets.items():
        y = y_levels[size]
        for subset in subsets:
            xs = np.array(subset, dtype=float)
            ax.scatter(xs, np.full_like(xs, y), s=55, color=TEAL if tuple(subset) not in interval_subsets else GOLD, zorder=3)
            ax.plot([xs.min(), xs.max()], [y, y], color=TEAL if tuple(subset) not in interval_subsets else GOLD, lw=5, alpha=0.7)

    ax.text(7.45, 2.95, "feasible subset soups", color=TEAL, va="center", fontsize=11)
    ax.text(7.45, 2.55, "interval-restricted family", color=GOLD, va="center", fontsize=11)
    ax.text(7.45, 2.15, "nodes outside the band are noncontiguous", color=INK, va="center", fontsize=10)
    ax.set_xlim(0.5, 9.4)
    ax.set_ylim(-0.5, 3.5)
    ax.set_yticks([0, 0.9, 1.9, 2.9])
    ax.set_yticklabels(["trajectory", "size 1", "size 2", "size 3"])
    ax.set_xlabel("checkpoint order")
    ax.set_title("The PRISM action family contains interval soups but is not restricted to them")
    _save(fig, "action_family_vs_interval_band.pdf")


def figure_top_alpha() -> None:
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    values = np.array([-0.4, 0.1, 0.2, 0.45, 0.7, 1.0, 1.2, 1.8, 2.2, 3.0])
    order = np.argsort(values)
    values = values[order]
    x = np.arange(values.size)
    cutoff = 3

    colors = [GRAY] * values.size
    for idx in range(values.size - cutoff, values.size):
        colors[idx] = ORANGE

    ax.bar(x, values, color=colors, edgecolor="white", linewidth=0.8)
    ax.axvline(values.size - cutoff - 0.5, color=INK, ls="--", lw=1.4)
    ax.text(values.size - cutoff + 0.1, 3.15, "selected adversarial tail", color=ORANGE, fontsize=10)
    ax.annotate(
        "top-alpha mean = exact hidden-subpopulation adversary",
        xy=(values.size - 2, 2.1),
        xytext=(2.0, 2.75),
        arrowprops=dict(arrowstyle="->", color=INK, lw=1.3),
        fontsize=10,
    )
    ax.set_xticks([])
    ax.set_ylabel("pairwise regret gap")
    ax.set_title("The capped adversary reduces to a top-alpha mean of pointwise regret gaps")
    _save(fig, "top_alpha_regret_geometry.pdf")


def figure_certificate_curve() -> None:
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    alpha = np.linspace(0.1, 1.0, 200)
    psi = 0.12 + 0.38 / (1 + np.exp(7 * (alpha - 0.42))) + 0.03 * np.sin(8 * alpha)
    threshold = 0.28
    idx = np.where(psi <= threshold)[0][0]
    alpha_star = alpha[idx]

    ax.plot(alpha, psi, color=TEAL, lw=2.8)
    ax.fill_between(alpha, psi, threshold, where=psi <= threshold, color=TEAL, alpha=0.18)
    ax.axhline(threshold, color=ORANGE, lw=1.5, ls="--")
    ax.axvline(alpha_star, color=ORANGE, lw=1.5, ls="--")
    ax.scatter([alpha_star], [threshold], s=80, color=ORANGE, zorder=4)
    ax.text(alpha_star + 0.02, threshold + 0.015, r"$\alpha^\star_\tau$", color=ORANGE, fontsize=12)
    ax.set_xlabel(r"subpopulation mass lower bound $\alpha$")
    ax.set_ylabel(r"worst-case regret $\Psi_\alpha(S)$")
    ax.set_title("A PRISM certificate records the smallest protected subpopulation size at a given regret tolerance")
    _save(fig, "certificate_curve_alpha_star.pdf")


def figure_noncontiguous() -> None:
    fig, ax = plt.subplots(figsize=(9.2, 4.4))
    ax.set_xlim(0.5, 8.5)
    ax.set_ylim(-0.8, 3.2)
    ax.axis("off")

    timeline_x = np.arange(1, 8)
    ax.plot([1, 7], [0, 0], color=INK, lw=1.8)
    ax.scatter(timeline_x, np.zeros_like(timeline_x), s=65, color=BLUE, zorder=3)
    for xi in timeline_x:
        ax.text(xi, -0.22, str(xi), ha="center", va="top")

    ax.text(1.0, 0.4, "trajectory order", fontsize=11, fontweight="bold")
    ax.plot([2, 6], [1.2, 1.2], color=GOLD, lw=8, alpha=0.9)
    ax.text(4.0, 1.45, "best interval family candidate", ha="center", color=INK)

    ax.plot([1, 1], [2.2, 2.2], marker="o", color=TEAL, markersize=8)
    ax.plot([7, 7], [2.2, 2.2], marker="o", color=TEAL, markersize=8)
    ax.plot([1, 7], [2.2, 2.2], color=TEAL, lw=4)
    ax.text(4.0, 2.45, "noncontiguous complementary pair", ha="center", color=INK)

    ax.text(7.6, 2.2, "low regret on hidden group A and B", va="center", fontsize=10)
    ax.text(7.6, 1.2, "interval misses one extreme specialization", va="center", fontsize=10)
    ax.add_patch(FancyArrowPatch((4.0, 1.45), (4.0, 2.05), arrowstyle="simple", mutation_scale=20, color=ORANGE, alpha=0.7))
    ax.set_title("Noncontiguous checkpoint complementarity can dominate every contiguous interval")
    _save(fig, "noncontiguous_complementarity.pdf")


def main() -> None:
    _setup()
    figure_overview()
    figure_noise_vs_regret()
    figure_action_family()
    figure_top_alpha()
    figure_certificate_curve()
    figure_noncontiguous()


if __name__ == "__main__":
    main()
