#!/usr/bin/env python
"""Generate conceptual figures for the ROWA paper."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


def _save(fig: plt.Figure, name: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def figure_geometry() -> None:
    x = np.linspace(-1.8, 1.8, 400)
    y = np.linspace(-1.6, 1.6, 400)
    xx, yy = np.meshgrid(x, y)

    def pooled(x0: float, y0: float) -> np.ndarray:
        return 0.9 * (xx - x0) ** 2 + 0.5 * (yy - y0) ** 2

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.6, 1.6)
        for spine in ax.spines.values():
            spine.set_visible(False)

    left = axes[0]
    z_left = pooled(0.0, 0.0)
    left.contour(xx, yy, z_left, levels=10, colors="#7b9acc", linewidths=1.0)
    left.scatter([0.55], [0.15], s=70, color="#1f1f1f", zorder=5)
    left.text(0.62, 0.28, "checkpoint", fontsize=10)
    left.add_patch(FancyArrowPatch((0.55, 0.15), (1.25, 0.55), arrowstyle="->", mutation_scale=14, lw=2.0, color="#1f77b4"))
    left.add_patch(FancyArrowPatch((0.55, 0.15), (-0.10, 0.65), arrowstyle="->", mutation_scale=14, lw=2.0, color="#ff7f0e"))
    left.text(1.28, 0.58, r"$g_1$", color="#1f77b4", fontsize=11)
    left.text(-0.22, 0.72, r"$g_2$", color="#ff7f0e", fontsize=11)
    left.add_patch(FancyArrowPatch((0.55, 0.15), (0.08, -0.35), arrowstyle="->", mutation_scale=14, lw=2.0, ls="--", color="#444444"))
    left.text(-1.35, -1.30, "same pooled basin,\nconflicting domain updates", fontsize=10, ha="left")
    left.set_title("Flat but not recoverable", fontsize=12)

    right = axes[1]
    z_right = pooled(-0.05, 0.02)
    right.contour(xx, yy, z_right, levels=10, colors="#7b9acc", linewidths=1.0)
    right.scatter([0.55], [0.15], s=70, color="#1f1f1f", zorder=5)
    right.text(0.62, 0.28, "checkpoint", fontsize=10)
    right.add_patch(FancyArrowPatch((0.55, 0.15), (1.18, 0.52), arrowstyle="->", mutation_scale=14, lw=2.0, color="#1f77b4"))
    right.add_patch(FancyArrowPatch((0.55, 0.15), (1.05, 0.34), arrowstyle="->", mutation_scale=14, lw=2.0, color="#ff7f0e"))
    right.text(1.22, 0.56, r"$g_1$", color="#1f77b4", fontsize=11)
    right.text(1.08, 0.22, r"$g_2$", color="#ff7f0e", fontsize=11)
    right.add_patch(FancyArrowPatch((0.55, 0.15), (0.02, -0.18), arrowstyle="->", mutation_scale=14, lw=2.0, ls="--", color="#2f4f4f"))
    right.text(-1.35, -1.30, "shared update direction,\nheld-out domains recover", fontsize=10, ha="left")
    right.set_title("Recoverable checkpoint", fontsize=12)

    fig.suptitle("ROWA distinguishes cross-domain recoverability from pooled flatness", fontsize=13, y=1.02)
    _save(fig, "geometry_recoverability_vs_flatness.pdf")


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 3.2))
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
            alpha=0.15,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    def arrow(x0: float, y0: float, x1: float, y1: float) -> None:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=15, lw=1.6, color="#333333"))

    box(0.03, 0.38, 0.15, 0.24, "Single training run\nwith dense checkpoints", "#4c78a8")
    box(0.23, 0.38, 0.15, 0.24, "Per-domain held-out\nlosses and gradients", "#f58518")
    box(0.43, 0.38, 0.15, 0.24, "Leave-one-domain-out\nvirtual updates", "#54a24b")
    box(0.63, 0.38, 0.14, 0.24, "ROWA score\nper checkpoint", "#e45756")
    box(0.82, 0.38, 0.15, 0.24, "Low-score window\nand weight average", "#72b7b2")

    arrow(0.18, 0.50, 0.23, 0.50)
    arrow(0.38, 0.50, 0.43, 0.50)
    arrow(0.58, 0.50, 0.63, 0.50)
    arrow(0.77, 0.50, 0.82, 0.50)

    ax.text(0.30, 0.17, r"$g_{-i,t} = \nabla_\theta \frac{1}{I-1}\sum_{j \neq i} L_j(\theta_t)$", fontsize=11, ha="center")
    ax.text(0.71, 0.17, r"$R_t = \frac{1}{I}\sum_i L_i(\theta_t - \eta P_t g_{-i,t}) + \lambda\,\mathrm{Gap}_t$", fontsize=11, ha="center")
    ax.text(0.50, 0.86, "ROWA pipeline", fontsize=14, ha="center")

    _save(fig, "rowa_pipeline.pdf")


def figure_tradeoff() -> None:
    cov = np.linspace(0.0, 2.4, 200)
    shared = 1.25
    fig, ax = plt.subplots(figsize=(6.4, 4.1))
    for I, color in [(3, "#4c78a8"), (4, "#f58518"), (6, "#54a24b")]:
        score = shared - cov / (I - 1)
        ax.plot(cov, score, lw=2.3, color=color, label=rf"$I={I}$")
    ax.axhline(0.0, color="#444444", lw=1.0, ls="--")
    ax.text(1.53, 0.08, "positive transfer", fontsize=10, color="#444444")
    ax.set_xlabel(r"Domain-gradient covariance penalty $\mathrm{tr}(P C)$")
    ax.set_ylabel(r"Alignment term $A_P = \|\bar g\|_P^2 - \mathrm{tr}(P C)/(I-1)$")
    ax.set_title("Analytical effect of domain conflict on ROWA")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)
    _save(fig, "alignment_covariance_tradeoff.pdf")


def figure_window() -> None:
    t = np.arange(0, 60)
    score = 1.25 + 0.0022 * (t - 31.0) ** 2 + 0.05 * np.sin(t / 5.0)
    score = score - score.min()
    threshold = score.min() + 0.22
    mask = score <= threshold

    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.plot(t, score, color="#4c78a8", lw=2.3, label="ROWA score")
    ax.fill_between(t, score, threshold, where=mask, color="#72b7b2", alpha=0.35, label="selected window")
    ax.axhline(threshold, color="#e45756", lw=1.4, ls="--", label=r"sublevel threshold $\delta$")
    ax.set_xlabel("Checkpoint index")
    ax.set_ylabel("Score")
    ax.set_title("Dense checkpointing and sublevel window selection (schematic)")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(alpha=0.25)
    _save(fig, "dense_window_schematic.pdf")


def main() -> None:
    figure_geometry()
    figure_pipeline()
    figure_tradeoff()
    figure_window()


if __name__ == "__main__":
    main()
