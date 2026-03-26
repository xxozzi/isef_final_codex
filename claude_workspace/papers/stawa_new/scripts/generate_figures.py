#!/usr/bin/env python
"""Generate conceptual figures for the STAWA paper."""

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


def figure_concept() -> None:
    x = np.linspace(-1.9, 1.9, 400)
    y = np.linspace(-1.6, 1.6, 400)
    xx, yy = np.meshgrid(x, y)
    zz = 0.85 * xx**2 + 0.35 * yy**2

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    left = axes[0]
    left.contour(xx, yy, zz, levels=10, colors="#6f8fb7", linewidths=1.0)
    left.scatter([0.40], [0.10], s=70, color="#111111", zorder=5)
    left.text(0.50, 0.22, "checkpoint", fontsize=10)
    left.add_patch(FancyArrowPatch((0.40, 0.10), (1.10, 0.55), arrowstyle="->", mutation_scale=14, lw=2.0, color="#1f77b4"))
    left.add_patch(FancyArrowPatch((0.40, 0.10), (1.18, -0.35), arrowstyle="->", mutation_scale=14, lw=2.0, color="#e45756"))
    left.text(1.14, 0.61, "same flat region", fontsize=9, color="#1f77b4")
    left.text(0.98, -0.52, "but predictions still drift", fontsize=9, color="#e45756")
    left.text(-1.55, -1.22, "weight-space geometry alone\ncannot see ongoing function drift", fontsize=10, ha="left")
    left.set_title("Flatness view", fontsize=12)

    right = axes[1]
    t = np.arange(6)
    y1 = np.array([0.82, 0.80, 0.79, 0.79, 0.79, 0.79])
    y2 = np.array([0.18, 0.20, 0.21, 0.21, 0.21, 0.21])
    right.plot(t, y1, color="#4c78a8", lw=2.5, marker="o")
    right.plot(t, y2, color="#f58518", lw=2.5, marker="o")
    right.fill_between(t, 0.46, 0.54, color="#72b7b2", alpha=0.2)
    right.text(2.15, 0.58, "stable plateau", fontsize=10, color="#2f4f4f")
    right.text(0.05, 0.90, "semantic output", fontsize=9, color="#4c78a8")
    right.text(0.05, 0.08, "counterfactual output", fontsize=9, color="#f58518")
    right.set_xlim(-0.2, 5.2)
    right.set_ylim(0.0, 1.0)
    right.set_xticks(range(6))
    right.set_xlabel("Future checkpoints")
    right.set_ylabel("Prediction")
    right.grid(alpha=0.25)
    right.set_title("Functional stationarity view", fontsize=12)

    fig.suptitle("STAWA replaces weight-space flatness with function-space stationarity", fontsize=13, y=1.02)
    _save(fig, "flatness_vs_stationarity.pdf")


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(11.8, 3.4))
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

    box(0.02, 0.37, 0.14, 0.26, "Single training run\nwith dense checkpoints", "#4c78a8")
    box(0.20, 0.37, 0.17, 0.26, "Held-out support set\nfor future drift", "#f58518")
    box(0.41, 0.37, 0.15, 0.26, "Mean and spread of\npredictive drift", "#54a24b")
    box(0.61, 0.37, 0.14, 0.26, "Validation loss\nplus drift score", "#e45756")
    box(0.80, 0.37, 0.17, 0.26, "Low-score window\nand weight average", "#72b7b2")

    arrow(0.16, 0.50, 0.20, 0.50)
    arrow(0.37, 0.50, 0.41, 0.50)
    arrow(0.56, 0.50, 0.61, 0.50)
    arrow(0.75, 0.50, 0.80, 0.50)

    ax.text(0.29, 0.15, r"$\Delta_t(x)=\frac{1}{H}\sum_{h=1}^H d(p_t(x),p_{t+h}(x))$", fontsize=11, ha="center")
    ax.text(0.58, 0.15, r"$S_t = L_V(\theta_t) + \lambda_1 \mu_t + \lambda_2 \sigma_t$", fontsize=11, ha="center")
    ax.text(0.50, 0.86, "STAWA pipeline", fontsize=14, ha="center")

    _save(fig, "stawa_pipeline.pdf")


def figure_mean_variance() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 3.8))

    drift_a = np.array([0.06, 0.08, 0.09, 0.10, 0.08, 0.09, 0.07, 0.09])
    drift_b = np.array([0.00, 0.01, 0.01, 0.02, 0.00, 0.01, 0.39, 0.37])

    axes[0].bar(np.arange(len(drift_a)), drift_a, color="#4c78a8", alpha=0.85)
    axes[0].set_ylim(0, 0.45)
    axes[0].set_title("Low mean, low variance")
    axes[0].set_xlabel("Support example")
    axes[0].set_ylabel("Per-example drift")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].text(0.1, 0.40, r"$\mu \approx 0.08,\ \sigma \approx 0.01$", fontsize=10)

    axes[1].bar(np.arange(len(drift_b)), drift_b, color="#e45756", alpha=0.85)
    axes[1].set_ylim(0, 0.45)
    axes[1].set_title("Low mean, high variance")
    axes[1].set_xlabel("Support example")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].text(0.1, 0.40, r"$\mu \approx 0.10,\ \sigma \approx 0.16$", fontsize=10)
    axes[1].text(5.7, 0.31, "hidden unstable pocket", fontsize=9, color="#7f1d1d")

    fig.suptitle("The variance term detects target-relevant pockets of instability", fontsize=13, y=1.03)
    _save(fig, "mean_variance_hidden_subset.pdf")


def figure_separation() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 5.7), sharex=True, sharey=True)
    titles = ["Checkpoint A on labeled point a", "Checkpoint A on hidden point c", "Checkpoint B on labeled point a", "Checkpoint B on hidden point c"]
    series = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
        [0, 1, 1],
    ]
    colors = ["#4c78a8", "#4c78a8", "#e45756", "#e45756"]

    for ax, title, ys, color in zip(axes.ravel(), titles, series, colors):
        ax.plot([0, 1, 2], ys, marker="o", lw=2.4, color=color)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([0, 1, 2], ["t", "t+1", "t+2"])
        ax.set_yticks([0, 1])
        ax.set_ylim(-0.1, 1.1)
        ax.grid(alpha=0.25)

    axes[0, 0].set_ylabel("Prediction")
    axes[1, 0].set_ylabel("Prediction")
    fig.suptitle("Separation theorem: same validation loss and flatness, different future drift", fontsize=13, y=1.02)
    _save(fig, "separation_toy_timeline.pdf")


def figure_window() -> None:
    t = np.arange(0, 70)
    val = 0.95 + 0.0012 * (t - 39.0) ** 2 + 0.03 * np.sin(t / 5.5)
    drift = 0.18 + 0.12 * np.exp(-((t - 20) / 9.0) ** 2) + 0.02 * np.cos(t / 7.0)
    drift += 0.10 * np.exp(-((t - 55) / 6.0) ** 2)
    score = val + 0.8 * drift
    score = score - score.min()
    threshold = score.min() + 0.22
    mask = score <= threshold

    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.8), sharex=True, gridspec_kw={"height_ratios": [1, 1.15]})

    axes[0].plot(t, val - val.min(), lw=2.2, color="#4c78a8", label="validation loss")
    axes[0].plot(t, drift - drift.min(), lw=2.2, color="#f58518", label="drift term")
    axes[0].set_ylabel("Normalized value")
    axes[0].set_title("Validation loss and future drift evolve differently")
    axes[0].legend(frameon=False, loc="upper right")
    axes[0].grid(alpha=0.25)

    axes[1].plot(t, score, lw=2.4, color="#2f4f4f", label="STAWA score")
    axes[1].fill_between(t, score, threshold, where=mask, color="#72b7b2", alpha=0.35, label="selected window")
    axes[1].axhline(threshold, lw=1.5, ls="--", color="#e45756", label=r"sublevel width $\delta$")
    axes[1].scatter([t[np.argmin(score)]], [score.min()], s=40, color="#111111", zorder=5)
    axes[1].set_xlabel("Checkpoint index")
    axes[1].set_ylabel("Score")
    axes[1].legend(frameon=False, loc="upper right")
    axes[1].grid(alpha=0.25)

    fig.suptitle("STAWA selects low-loss checkpoints that also lie in a stationarity plateau", fontsize=13, y=0.98)
    _save(fig, "drift_window_schematic.pdf")


def main() -> None:
    figure_concept()
    figure_pipeline()
    figure_mean_variance()
    figure_separation()
    figure_window()


if __name__ == "__main__":
    main()
