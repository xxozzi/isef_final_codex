#!/usr/bin/env python
"""Generate original figures for the CHOIR NeurIPS paper."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig-choir")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"

BG = "#f6f2ea"
INK = "#1d2433"
TEAL = "#2a9d8f"
BLUE = "#4c78a8"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
PLUM = "#8b6f9b"
GREEN = "#6b8e23"
GRAY = "#d5cfbf"
LIGHT = "#fffdf8"


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "figure.facecolor": BG,
            "axes.facecolor": BG,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def _draw_box(ax, x0: float, y0: float, w: float, h: float, title: str, subtitle: str, color: str) -> None:
    box = FancyBboxPatch(
        (x0, y0),
        w,
        h,
        boxstyle="round,pad=0.18,rounding_size=0.16",
        facecolor=LIGHT,
        edgecolor=color,
        linewidth=1.8,
    )
    ax.add_patch(box)
    ax.text(x0 + 0.5 * w, y0 + 0.68 * h, title, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(x0 + 0.5 * w, y0 + 0.33 * h, subtitle, ha="center", va="center", fontsize=9.8, wrap=True)


def figure_overview() -> None:
    fig, ax = plt.subplots(figsize=(14.5, 4.8))
    ax.set_xlim(0, 18.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    stages = [
        (0.5, "One trajectory", "dense checkpoints from a single training run", BLUE),
        (4.0, "Safe family", "retain only near-optimal and barrier-safe checkpoints", TEAL),
        (7.5, "Hidden shifts", "top-alpha adversaries over pooled support examples", PLUM),
        (11.0, "Witness optima", "each hidden shift picks its preferred safe model", ORANGE),
        (14.5, "CHOIR center", "deploy the center of that optimum cloud", GREEN),
    ]
    for x0, title, subtitle, color in stages:
        _draw_box(ax, x0, 1.55, 2.85, 2.0, title, subtitle, color)

    for x in [3.4, 6.9, 10.4, 13.9]:
        arrow = FancyArrowPatch((x, 2.55), (x + 0.45, 2.55), arrowstyle="-|>", mutation_scale=18, lw=1.7, color=INK)
        ax.add_patch(arrow)

    xs = np.linspace(0.9, 2.8, 9)
    ys = 2.55 + 0.42 * np.sin(np.linspace(-0.7, 2.8, xs.size))
    ax.plot(xs, ys, color=BLUE, lw=2.3)
    ax.scatter(xs, ys, s=30, color=BLUE, edgecolor=LIGHT, linewidth=0.8, zorder=3)

    ax.add_patch(Ellipse((5.43, 2.55), 1.85, 1.2, angle=18, facecolor=TEAL, alpha=0.12, edgecolor=TEAL, lw=1.5))
    safe_pts = np.array([[4.7, 2.2], [5.0, 2.95], [5.35, 2.4], [5.8, 2.85], [6.1, 2.1]])
    ax.scatter(safe_pts[:, 0], safe_pts[:, 1], s=46, color=TEAL, edgecolor=LIGHT, linewidth=0.8)
    ax.scatter([5.35], [2.55], s=70, color=INK, zorder=4)

    bars = np.array([0.28, 0.41, 0.38, 0.82, 0.51, 0.94, 0.56, 0.72])
    support_x = np.linspace(7.85, 9.25, bars.size)
    colors = [GRAY, GRAY, GRAY, PLUM, GRAY, PLUM, GRAY, PLUM]
    ax.bar(support_x, bars, width=0.14, bottom=1.85, color=colors, edgecolor=LIGHT, linewidth=0.8)
    ax.text(8.55, 3.45, "top-alpha", ha="center", va="bottom", fontsize=10, color=PLUM)
    ax.add_patch(Rectangle((8.37, 1.83), 0.96, 1.18, fill=False, edgecolor=PLUM, linewidth=1.5, linestyle="--"))

    witness_pts = np.array([[11.5, 2.95], [11.95, 2.1], [12.45, 3.15], [12.75, 2.4], [13.1, 2.8]])
    ax.scatter(witness_pts[:, 0], witness_pts[:, 1], s=60, color=ORANGE, edgecolor=LIGHT, linewidth=0.9, zorder=3)
    for i in range(len(witness_pts)):
        for j in range(i + 1, len(witness_pts)):
            if np.linalg.norm(witness_pts[i] - witness_pts[j]) < 1.0:
                ax.plot(
                    [witness_pts[i, 0], witness_pts[j, 0]],
                    [witness_pts[i, 1], witness_pts[j, 1]],
                    color=ORANGE,
                    alpha=0.25,
                    lw=1.3,
                )

    center = np.array([15.95, 2.62])
    ax.add_patch(Circle(center, 0.92, facecolor=GREEN, alpha=0.12, edgecolor=GREEN, linewidth=1.6))
    ax.scatter([15.6, 16.15, 16.35, 15.85], [2.18, 2.22, 3.0, 3.05], s=42, color=ORANGE, alpha=0.55)
    ax.scatter([center[0]], [center[1]], s=105, color=GREEN, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    ax.text(center[0], 1.42, r"$\theta_{\mathrm{CHOIR}}$", ha="center", fontsize=11, color=GREEN)

    ax.text(9.05, 0.55, r"$q \mapsto \theta_q^\star$ yields a witness cloud", fontsize=12, ha="center")
    ax.text(15.95, 0.18, r"$\min_{\theta \in \mathcal{F}_{\mathrm{safe}}}\max_q \|\theta-\theta_q^\star\|_H^2$", fontsize=13, ha="center")
    save(fig, "choir_overview.pdf")


def figure_2d_geometry() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12.8, 5.2))

    ax = axs[0]
    ax.set_title("Safe family and hidden-shift optima")
    poly = np.array(
        [
            [-2.4, -1.0],
            [-1.7, 0.9],
            [-0.4, 1.7],
            [1.5, 1.35],
            [2.1, 0.2],
            [1.4, -1.55],
            [-0.7, -1.85],
        ]
    )
    ax.add_patch(Polygon(poly, closed=True, facecolor=TEAL, alpha=0.12, edgecolor=TEAL, linewidth=2.0))

    checkpoints = np.array(
        [
            [-2.0, -0.75],
            [-1.55, 0.45],
            [-0.9, 1.15],
            [-0.15, 1.35],
            [0.55, 1.1],
            [1.25, 0.6],
            [1.55, -0.2],
            [1.05, -1.1],
            [0.0, -1.45],
            [-1.0, -1.15],
        ]
    )
    ax.plot(checkpoints[:, 0], checkpoints[:, 1], color=BLUE, lw=2.0, alpha=0.85)
    ax.scatter(checkpoints[:, 0], checkpoints[:, 1], s=36, color=BLUE, edgecolor=LIGHT, linewidth=0.8, zorder=3)

    witnesses = np.array([[-1.35, 0.7], [-0.55, 1.0], [0.25, 0.9], [1.0, 0.1], [0.35, -0.95], [-0.65, -0.8]])
    baseline = np.array([0.18, 0.05])
    choir = np.array([-0.05, 0.15])

    ax.scatter(witnesses[:, 0], witnesses[:, 1], s=72, color=ORANGE, edgecolor=LIGHT, linewidth=1.0, zorder=4, label="witness optima")
    ax.scatter(*baseline, s=115, color=GOLD, edgecolor=LIGHT, linewidth=1.0, zorder=5, label="uniform safe soup")
    ax.scatter(*choir, s=130, color=GREEN, edgecolor=LIGHT, linewidth=1.0, zorder=6, label="CHOIR center")
    ax.add_patch(Ellipse(choir, 2.7, 2.05, angle=10, fill=False, edgecolor=GREEN, linewidth=1.7, linestyle="--"))
    for point in witnesses:
        ax.plot([choir[0], point[0]], [choir[1], point[1]], color=GREEN, alpha=0.35, lw=1.1)

    ax.annotate("safe soup family", xy=(-1.8, 1.1), xytext=(-2.3, 2.0), arrowprops=dict(arrowstyle="->", lw=1.2, color=INK), fontsize=10)
    ax.annotate("enclosing radius", xy=(1.1, 0.92), xytext=(1.75, 1.75), arrowprops=dict(arrowstyle="->", lw=1.2, color=GREEN), fontsize=10, color=GREEN)
    ax.set_xlabel("basin direction 1")
    ax.set_ylabel("basin direction 2")
    ax.set_aspect("equal")
    ax.legend(frameon=False, loc="lower left")

    ax = axs[1]
    ax.set_title("Top-alpha adversaries from pooled support")
    losses = np.array([0.22, 0.44, 0.35, 0.63, 0.56, 0.91, 0.84, 1.14, 0.68, 1.02, 0.38, 0.79])
    order = np.argsort(losses)
    losses = losses[order]
    xs = np.arange(losses.size)
    top_k = 4
    colors = [GRAY] * losses.size
    for idx in range(losses.size - top_k, losses.size):
        colors[idx] = PLUM
    ax.bar(xs, losses, color=colors, edgecolor=LIGHT, linewidth=0.8)
    ax.axvline(losses.size - top_k - 0.5, color=INK, linestyle="--", lw=1.3)
    ax.text(losses.size - 2.0, 1.22, "selected top-alpha subset", color=PLUM, ha="center", fontsize=10)
    ax.annotate(
        "uniform mass over this subset\nis the worst capped reweighting",
        xy=(losses.size - 2, 1.02),
        xytext=(2.1, 1.14),
        arrowprops=dict(arrowstyle="->", lw=1.2, color=INK),
        fontsize=10,
    )
    ax.text(1.9, 0.22, r"$\max_{q \in \mathcal{Q}_\alpha^n} \widehat{L}_q(\theta)$", fontsize=12)
    ax.set_xlabel("support examples sorted by loss")
    ax.set_ylabel("per-example loss")
    ax.set_xticks([])
    save(fig, "choir_2d_geometry.pdf")


def basin_height(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return 0.17 * x**2 + 0.11 * y**2 + 0.045 * x * y + 0.18 * np.sin(1.25 * x) * np.cos(0.82 * y) + 0.15


def figure_3d_cloud() -> None:
    fig = plt.figure(figsize=(12.6, 5.3))
    ax = fig.add_subplot(1, 1, 1, projection="3d")

    xs = np.linspace(-2.8, 2.8, 120)
    ys = np.linspace(-2.5, 2.5, 120)
    X, Y = np.meshgrid(xs, ys)
    Z = basin_height(X, Y)
    ax.plot_surface(X, Y, Z, cmap="YlGnBu", linewidth=0, antialiased=True, alpha=0.82)

    traj = np.array(
        [
            [-2.2, -1.0],
            [-1.75, -0.15],
            [-1.25, 0.6],
            [-0.75, 1.05],
            [-0.05, 0.9],
            [0.6, 0.45],
            [1.15, 0.0],
            [1.55, -0.55],
            [1.9, -0.95],
        ]
    )
    tz = basin_height(traj[:, 0], traj[:, 1]) + 0.05
    ax.plot(traj[:, 0], traj[:, 1], tz, color=BLUE, lw=2.8)
    ax.scatter(traj[:, 0], traj[:, 1], tz, color=BLUE, s=34, depthshade=False)

    safe = traj[2:7]
    sz = basin_height(safe[:, 0], safe[:, 1]) + 0.07
    ax.scatter(safe[:, 0], safe[:, 1], sz, color=TEAL, s=58, depthshade=False, label="safe checkpoints")

    witnesses = np.array(
        [
            [-1.25, 0.52],
            [-0.55, 0.88],
            [0.05, 0.72],
            [0.82, 0.18],
            [0.45, -0.58],
            [-0.3, -0.45],
        ]
    )
    wz = basin_height(witnesses[:, 0], witnesses[:, 1]) + 0.12
    ax.scatter(witnesses[:, 0], witnesses[:, 1], wz, color=ORANGE, s=74, depthshade=False, label="witness optima")

    choir = np.array([0.0, 0.2])
    cz = basin_height(choir[0], choir[1]) + 0.16
    ax.scatter([choir[0]], [choir[1]], [cz], color=GREEN, s=110, depthshade=False, label="CHOIR center")
    for wx, wy, wz_i in zip(witnesses[:, 0], witnesses[:, 1], wz):
        ax.plot([choir[0], wx], [choir[1], wy], [cz, wz_i], color=GREEN, alpha=0.35, lw=1.4)

    ax.text(-2.28, -1.12, tz[0] + 0.15, "trajectory", color=BLUE)
    ax.text(-1.35, 0.7, wz[0] + 0.18, "shift-specific optima", color=ORANGE)
    ax.text(0.12, 0.22, cz + 0.18, r"$\theta_{\mathrm{CHOIR}}$", color=GREEN)

    ax.view_init(elev=27, azim=-58)
    ax.set_xlabel("basin direction 1")
    ax.set_ylabel("basin direction 2")
    ax.set_zlabel("loss")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title("Corner view: CHOIR centers the hidden-shift optimum cloud inside one safe basin")
    save(fig, "choir_3d_cloud.pdf")


def figure_step_panels() -> None:
    fig, axs = plt.subplots(1, 4, figsize=(14.6, 3.8))
    titles = [
        "1. Safe-pool construction",
        "2. Probe-induced adversaries",
        "3. Hidden-shift witnesses",
        "4. Centered deployment",
    ]

    for ax, title in zip(axs, titles):
        ax.set_title(title)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")

    ax = axs[0]
    xs = np.linspace(1.2, 8.8, 10)
    ys = 3.15 + 1.05 * np.sin(np.linspace(-0.5, 2.6, xs.size))
    ax.plot(xs, ys, color=BLUE, lw=2.3)
    ax.scatter(xs, ys, s=40, color=BLUE, edgecolor=LIGHT, linewidth=0.8)
    ax.add_patch(Rectangle((2.9, 1.1), 3.4, 3.65, fill=False, edgecolor=TEAL, linewidth=1.6, linestyle="--"))
    ax.text(4.6, 0.55, "near-optimal and barrier-safe", ha="center", color=TEAL, fontsize=10)

    ax = axs[1]
    bars = np.array([0.3, 0.55, 0.42, 0.75, 0.6, 0.95, 0.48, 1.05])
    for offset, color in zip([0.0, 0.38, 0.76], [BLUE, GOLD, PLUM]):
        ax.bar(np.arange(8) + 1.0 + offset, bars * (0.85 + 0.12 * offset), width=0.28, bottom=1.0, color=GRAY, edgecolor=LIGHT, linewidth=0.7)
        ax.add_patch(Rectangle((5.8 + offset, 0.95), 1.55, 1.4, fill=False, edgecolor=color, linewidth=1.4))
    ax.text(5.25, 3.1, "each probe selects its top-alpha tail", ha="center", fontsize=10)

    ax = axs[2]
    basin = np.array([[1.1, 1.3], [2.0, 4.4], [4.0, 5.0], [6.7, 4.2], [8.2, 2.4], [7.0, 1.0], [3.2, 0.8]])
    ax.add_patch(Polygon(basin, closed=True, facecolor=TEAL, alpha=0.12, edgecolor=TEAL, linewidth=1.8))
    witnesses = np.array([[2.2, 3.8], [3.8, 4.25], [5.6, 3.7], [6.2, 2.35], [4.1, 1.7]])
    ax.scatter(witnesses[:, 0], witnesses[:, 1], s=66, color=ORANGE, edgecolor=LIGHT, linewidth=0.9)
    ax.text(4.5, 0.45, "optimum preferred by each hidden shift", ha="center", fontsize=10)

    ax = axs[3]
    witnesses = np.array([[2.0, 4.1], [3.2, 4.5], [5.0, 3.8], [5.65, 2.35], [3.85, 1.9]])
    choir = np.array([4.0, 3.05])
    ax.add_patch(Circle(choir, 2.05, fill=False, edgecolor=GREEN, linewidth=1.6, linestyle="--"))
    ax.scatter(witnesses[:, 0], witnesses[:, 1], s=58, color=ORANGE, edgecolor=LIGHT, linewidth=0.9)
    ax.scatter([choir[0]], [choir[1]], s=120, color=GREEN, edgecolor=LIGHT, linewidth=1.0)
    for w in witnesses:
        ax.plot([choir[0], w[0]], [choir[1], w[1]], color=GREEN, alpha=0.35, lw=1.2)
    ax.text(4.0, 0.45, "minimize the worst witness distance", ha="center", fontsize=10)

    save(fig, "choir_step_panels.pdf")


def _simplex_xy(q: np.ndarray) -> np.ndarray:
    v1 = np.array([0.5, 0.92])
    v2 = np.array([0.08, 0.08])
    v3 = np.array([0.92, 0.08])
    return q[0] * v1 + q[1] * v2 + q[2] * v3


def figure_active_set() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12.6, 5.0))

    ax = axs[0]
    ax.set_title("Active shifts in reweighting space")
    tri = np.array([[0.5, 0.92], [0.08, 0.08], [0.92, 0.08], [0.5, 0.92]])
    ax.plot(tri[:, 0], tri[:, 1], color=INK, lw=2.1)
    ax.text(0.5, 0.96, r"$q^{(1)}$", ha="center")
    ax.text(0.05, 0.04, r"$q^{(2)}$", ha="left")
    ax.text(0.95, 0.04, r"$q^{(3)}$", ha="right")

    probes = np.array(
        [
            [0.56, 0.24, 0.20],
            [0.22, 0.58, 0.20],
            [0.28, 0.20, 0.52],
            [0.46, 0.15, 0.39],
        ]
    )
    probe_xy = np.array([_simplex_xy(q) for q in probes])
    ax.scatter(probe_xy[:, 0], probe_xy[:, 1], s=68, color=PLUM, edgecolor=LIGHT, linewidth=0.9, label="probe-induced shifts")
    center = probe_xy.mean(axis=0)
    ax.scatter([center[0]], [center[1]], s=80, color=INK, label="pooled support")
    for pt in probe_xy:
        ax.plot([center[0], pt[0]], [center[1], pt[1]], color=PLUM, alpha=0.35, lw=1.2)
    ax.add_patch(Circle(center, 0.19, fill=False, edgecolor=PLUM, linewidth=1.4, linestyle="--"))
    ax.text(0.5, -0.02, r"capped simplex $\mathcal{Q}_\alpha^n$", ha="center", fontsize=11)
    ax.legend(frameon=False, loc="upper right")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax = axs[1]
    ax.set_title("Mapped witness cloud in model space")
    ax.set_xlim(-2.6, 2.8)
    ax.set_ylim(-2.2, 2.4)
    ax.add_patch(Ellipse((0.0, 0.05), 4.6, 3.25, angle=12, facecolor=TEAL, alpha=0.1, edgecolor=TEAL, linewidth=1.7))

    cloud = np.array([[-1.2, 0.6], [-0.4, 1.25], [0.75, 0.95], [1.45, -0.1], [0.35, -1.0], [-0.75, -0.7]])
    choir = np.array([0.0, 0.15])
    ax.scatter(cloud[:, 0], cloud[:, 1], s=70, color=ORANGE, edgecolor=LIGHT, linewidth=0.9, label=r"$\theta_q^\star$")
    ax.scatter([choir[0]], [choir[1]], s=125, color=GREEN, edgecolor=LIGHT, linewidth=1.0, label=r"$\theta_{\mathrm{CHOIR}}$")
    ax.add_patch(Ellipse(choir, 2.9, 2.25, angle=8, fill=False, edgecolor=GREEN, linewidth=1.5, linestyle="--"))
    for pt in cloud:
        ax.plot([choir[0], pt[0]], [choir[1], pt[1]], color=GREEN, alpha=0.35, lw=1.2)
    ax.text(0.02, -1.7, "same hidden shifts, now viewed as preferred safe optima", ha="center", fontsize=10)
    ax.legend(frameon=False, loc="upper left")
    ax.set_xlabel("model-space direction 1")
    ax.set_ylabel("model-space direction 2")
    ax.set_aspect("equal")
    save(fig, "choir_active_set.pdf")


def main() -> None:
    setup()
    figure_overview()
    figure_2d_geometry()
    figure_3d_cloud()
    figure_step_panels()
    figure_active_set()


if __name__ == "__main__":
    main()
