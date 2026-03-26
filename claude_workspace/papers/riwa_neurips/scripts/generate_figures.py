#!/usr/bin/env python
"""Generate conceptual figures for the RIWA paper."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


def _save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def figure_concept() -> None:
    x = np.linspace(-1.8, 1.8, 400)
    y = np.linspace(-1.5, 1.5, 400)
    xx, yy = np.meshgrid(x, y)

    def pooled() -> np.ndarray:
        return 0.85 * xx**2 + 0.35 * yy**2

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    left = axes[0]
    left.contour(xx, yy, pooled(), levels=10, colors="#6f8fb7", linewidths=1.0)
    left.scatter([0.45], [0.10], s=70, color="#1d1d1d", zorder=5)
    left.text(0.53, 0.22, "checkpoint", fontsize=10)
    left.add_patch(FancyArrowPatch((0.45, 0.10), (1.15, 0.58), arrowstyle="->", mutation_scale=14, lw=2.0, color="#1f77b4"))
    left.add_patch(FancyArrowPatch((0.45, 0.10), (-0.15, 0.52), arrowstyle="->", mutation_scale=14, lw=2.0, color="#ff7f0e"))
    left.add_patch(FancyArrowPatch((0.45, 0.10), (0.95, -0.55), arrowstyle="->", mutation_scale=14, lw=1.8, ls="--", color="#444444"))
    left.text(1.20, 0.62, "weight perturbation", fontsize=9, color="#1f77b4")
    left.text(-1.55, -1.18, "flat pooled basin\nbut shift sensitivity is hidden", fontsize=10, ha="left")
    left.set_title("Parameter-space flatness", fontsize=12)

    right = axes[1]
    right.set_xlim(-1.4, 1.4)
    right.set_ylim(-1.25, 1.25)
    tri = np.array([[-1.05, -0.85], [1.05, -0.85], [0.0, 1.0]])
    right.add_patch(Polygon(tri, closed=True, facecolor="#9ecae1", edgecolor="#4c78a8", alpha=0.18, lw=1.6))
    center = np.array([0.0, -0.23])
    right.add_patch(Circle(center, 0.42, facecolor="#fdd0a2", edgecolor="#f58518", alpha=0.28, lw=1.6))
    right.scatter([center[0]], [center[1]], s=70, color="#1d1d1d", zorder=5)
    right.text(center[0] + 0.08, center[1] + 0.10, r"$u_m$", fontsize=11)
    for dx, dy, color in [(-0.62, -0.20, "#e45756"), (0.67, -0.08, "#54a24b"), (0.05, 0.72, "#b279a2")]:
        right.add_patch(FancyArrowPatch(tuple(center), (center[0] + dx, center[1] + dy), arrowstyle="->", mutation_scale=14, lw=2.0, color=color))
    right.text(-1.18, -0.98, "simplex of support weights", fontsize=10)
    right.text(-0.40, 0.95, "nearby redistributions", fontsize=9, color="#b279a2")
    right.text(-1.15, -1.18, "RIWA scores worst-case\nlocal weight redistributions", fontsize=10, ha="left")
    right.set_title("Distributional canalization", fontsize=12)

    fig.suptitle("RIWA replaces flatness in parameter space with stability in distribution space", fontsize=13, y=1.02)
    _save(fig, "distributional_canalization_vs_flatness.pdf")


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11.8, 3.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x: float, y: float, w: float, h: float, text: str, color: str) -> None:
        patch = FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            linewidth=1.4,
            edgecolor=color,
            facecolor=color,
            alpha=0.14,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    def arrow(x0: float, y0: float, x1: float, y1: float) -> None:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16, lw=1.7, color="#333333"))

    box(0.03, 0.38, 0.14, 0.25, "Single training run\nwith dense checkpoints", "#4c78a8")
    box(0.21, 0.38, 0.16, 0.25, "Support-example\nand validation gradients", "#f58518")
    box(0.42, 0.38, 0.16, 0.25, "Local ambiguity set\nin sample-weight space", "#54a24b")
    box(0.63, 0.38, 0.14, 0.25, "Worst-case one-step\nvalidation score", "#e45756")
    box(0.82, 0.38, 0.15, 0.25, "Low-score window\nand weight average", "#72b7b2")

    arrow(0.17, 0.50, 0.21, 0.50)
    arrow(0.37, 0.50, 0.42, 0.50)
    arrow(0.58, 0.50, 0.63, 0.50)
    arrow(0.77, 0.50, 0.82, 0.50)

    ax.text(0.29, 0.16, r"$g_i,\ \bar g,\ g_V$", fontsize=11, ha="center")
    ax.text(0.50, 0.16, r"$\alpha \in \mathcal{A}_\rho,\quad \theta(\alpha)=\theta-\eta P g_U(\alpha)$", fontsize=11, ha="center")
    ax.text(0.74, 0.16, r"$S^{\mathrm{ex}} = \max_{\alpha \in \mathcal{A}_\rho} L_V(\theta(\alpha))$", fontsize=11, ha="center")
    ax.text(0.50, 0.86, "RIWA pipeline", fontsize=14, ha="center")

    _save(fig, "riwa_pipeline.pdf")


def figure_tradeoff() -> None:
    variance = np.linspace(0.0, 1.8, 200)
    fig, ax = plt.subplots(figsize=(6.5, 4.1))
    for descent, color in [(1.2, "#4c78a8"), (0.95, "#f58518"), (0.7, "#54a24b")]:
        robust_score = -descent + 0.45 * np.sqrt(variance + 1e-9)
        ax.plot(variance, robust_score, lw=2.3, color=color, label=rf"mean descent $={descent:.2f}$")
    ax.axhline(0.0, color="#444444", lw=1.0, ls="--")
    ax.text(1.15, 0.05, "improvement boundary", fontsize=9, color="#444444")
    ax.set_xlabel(r"Projected support covariance $g_V^\top P C P g_V$")
    ax.set_ylabel(r"First-order robust objective offset")
    ax.set_title("RIWA penalizes projected shift sensitivity")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.25)
    _save(fig, "projected_covariance_tradeoff.pdf")


def figure_simplex() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.1))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.05, 1.15)
    ax.axis("off")

    tri = np.array([[-0.95, -0.78], [0.95, -0.78], [0.0, 0.95]])
    ax.add_patch(Polygon(tri, closed=True, facecolor="#d9eaf7", edgecolor="#4c78a8", alpha=0.22, lw=1.8))

    center = np.array([0.0, -0.20])
    ax.add_patch(Circle(center, 0.36, facecolor="#fdd0a2", edgecolor="#f58518", alpha=0.30, lw=1.6))
    ax.scatter([center[0]], [center[1]], s=80, color="#111111", zorder=5)
    ax.text(center[0] + 0.06, center[1] + 0.06, "uniform weights", fontsize=10)

    directions = [(-0.62, -0.10), (0.58, -0.18), (0.02, 0.62)]
    labels = ["style-heavy", "class-heavy", "latent subgroup"]
    colors = ["#e45756", "#54a24b", "#b279a2"]
    for (dx, dy), label, color in zip(directions, labels, colors):
        end = (center[0] + dx, center[1] + dy)
        ax.add_patch(FancyArrowPatch(tuple(center), end, arrowstyle="->", mutation_scale=15, lw=2.0, color=color))
        ax.text(end[0] + 0.02, end[1] + 0.02, label, fontsize=9, color=color)

    ax.text(-1.05, -0.95, "local ambiguity set\naround empirical source mixture", fontsize=10, ha="left")
    ax.text(-1.05, 1.02, "sample-weight simplex", fontsize=11, ha="left")
    ax.text(0.10, -0.56, r"$\max_{\alpha \in \mathcal{A}_\rho} L_V(\theta-\eta P g_U(\alpha))$", fontsize=11)

    _save(fig, "weight_simplex_ambiguity.pdf")


def figure_window() -> None:
    t = np.arange(0, 70)
    base = 0.95 + 0.0019 * (t - 36.0) ** 2
    wiggle = 0.05 * np.sin(t / 4.8) + 0.03 * np.cos(t / 7.0)
    score = base + wiggle
    score = score - score.min()
    threshold = score.min() + 0.22
    mask = score <= threshold

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.plot(t, score, color="#4c78a8", lw=2.4, label="RIWA score")
    ax.fill_between(t, score, threshold, where=mask, color="#72b7b2", alpha=0.35, label="selected window")
    ax.axhline(threshold, color="#e45756", lw=1.5, ls="--", label=r"sublevel width $\delta$")
    ax.scatter([t[np.argmin(score)]], [score.min()], color="#111111", s=40, zorder=5)
    ax.set_xlabel("Checkpoint index")
    ax.set_ylabel("Score")
    ax.set_title("Dense checkpointing and low-score window selection (schematic)")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(alpha=0.25)
    _save(fig, "dense_window_schematic.pdf")


def main() -> None:
    figure_concept()
    figure_pipeline()
    figure_tradeoff()
    figure_simplex()
    figure_window()


if __name__ == "__main__":
    main()
