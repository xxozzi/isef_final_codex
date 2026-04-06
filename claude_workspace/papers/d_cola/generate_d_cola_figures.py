#!/usr/bin/env python
"""Generate original figures for the D-COLA paper."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig-dcola")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"

BG = "#f6f2ea"
LIGHT = "#fffdf8"
INK = "#1d2433"
BLUE = "#4c78a8"
TEAL = "#2a9d8f"
ORANGE = "#e76f51"
GOLD = "#e9c46a"
PLUM = "#8b6f9b"
GREEN = "#6b8e23"
GRAY = "#d5cfbf"
RED = "#b0413e"


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.dpi": 220,
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


def arrow(ax, start, end, color=INK, lw=1.6, ms=18, alpha=1.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=ms,
            lw=lw,
            color=color,
            alpha=alpha,
        )
    )


def box(ax, xy, wh, title: str, subtitle: str, color: str) -> None:
    x0, y0 = xy
    w, h = wh
    ax.add_patch(
        FancyBboxPatch(
            (x0, y0),
            w,
            h,
            boxstyle="round,pad=0.18,rounding_size=0.16",
            facecolor=LIGHT,
            edgecolor=color,
            linewidth=1.8,
        )
    )
    ax.text(x0 + 0.5 * w, y0 + 0.67 * h, title, ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(x0 + 0.5 * w, y0 + 0.30 * h, subtitle, ha="center", va="center", fontsize=9.5, wrap=True)


def surface_height(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    valley = 0.08 * x**2 + 0.06 * y**2 + 0.020 * x * y
    wrinkle = 0.11 * np.sin(1.1 * x) * np.cos(0.85 * y)
    ridge = 0.22 * np.exp(-1.8 * ((x - 1.2) ** 2 + 0.7 * (y + 0.1) ** 2))
    return valley + wrinkle + ridge + 0.12


def figure_overview() -> None:
    fig, ax = plt.subplots(figsize=(15.2, 5.2))
    ax.set_xlim(0, 19.2)
    ax.set_ylim(0, 5.5)
    ax.axis("off")

    stages = [
        (0.45, "Failure profiles", "checkpoints disagree on which source slices they miss", BLUE),
        (4.7, "Conflict structure", "redundant failures stay aligned; complementary ones cancel", ORANGE),
        (8.95, "Mergeable region", "only averages that stay faithful to one model are admissible", TEAL),
        (13.2, "Final soup", "solve one convex weighting problem on the retained family", GREEN),
    ]
    for x0, title, subtitle, color in stages:
        box(ax, (x0, 1.55), (3.3, 2.0), title, subtitle, color)
    for x in [4.15, 8.4, 12.65]:
        arrow(ax, (x, 2.55), (x + 0.35, 2.55))

    xs = np.linspace(0.95, 3.25, 12)
    prof1 = 2.55 + 0.48 * np.sin(np.linspace(0.1, 2.8, 12))
    prof2 = 2.35 + 0.32 * np.sin(np.linspace(0.35, 3.05, 12))
    prof3 = 2.75 - 0.42 * np.sin(np.linspace(0.2, 2.9, 12))
    for yy, color in [(prof1, RED), (prof2, ORANGE), (prof3, TEAL)]:
        ax.plot(xs, yy, color=color, lw=2.0)

    cluster_x = np.array([5.35, 5.95, 6.55, 7.15, 7.75])
    cluster_y = np.array([2.95, 2.45, 2.8, 2.2, 2.65])
    ax.scatter(cluster_x[:2], cluster_y[:2], s=70, color=RED, edgecolor=LIGHT, linewidth=0.9)
    ax.scatter(cluster_x[2:], cluster_y[2:], s=70, color=TEAL, edgecolor=LIGHT, linewidth=0.9)
    ax.add_patch(Ellipse((5.68, 2.68), 1.05, 0.9, angle=10, facecolor=RED, alpha=0.10, edgecolor=RED, linewidth=1.5))
    ax.add_patch(Ellipse((7.15, 2.55), 1.45, 1.05, angle=-5, facecolor=TEAL, alpha=0.10, edgecolor=TEAL, linewidth=1.5))
    ax.text(6.6, 1.25, "covariance penalizes overlap", ha="center", fontsize=10, color=ORANGE)

    region = Ellipse((10.65, 2.55), 2.75, 1.45, angle=8, facecolor=TEAL, alpha=0.10, edgecolor=TEAL, linewidth=1.8)
    ax.add_patch(region)
    safe_pts = np.array([[9.7, 2.15], [10.1, 3.0], [10.65, 2.45], [11.2, 2.95], [11.7, 2.2]])
    ax.scatter(safe_pts[:, 0], safe_pts[:, 1], s=44, color=TEAL, edgecolor=LIGHT, linewidth=0.8)
    ax.plot([9.55, 10.0, 10.55, 11.1, 11.65], [2.05, 2.75, 3.0, 2.65, 2.15], color=BLUE, lw=2.0, alpha=0.8)
    ax.text(10.65, 4.38, "flatness is the low-conflict limit", ha="center", fontsize=10, color=PLUM)

    sel = np.array([[13.85, 2.1], [14.75, 3.05], [15.65, 2.25]])
    ax.scatter(sel[:, 0], sel[:, 1], s=74, color=ORANGE, edgecolor=LIGHT, linewidth=0.8)
    soup = np.array([14.78, 2.45])
    ax.scatter([soup[0]], [soup[1]], s=150, color=GREEN, edgecolor=LIGHT, linewidth=1.0)
    for pt in sel:
        ax.plot([soup[0], pt[0]], [soup[1], pt[1]], color=GREEN, alpha=0.4, lw=1.2)
    ax.text(14.9, 1.18, "one deployable soup", ha="center", fontsize=10, color=GREEN)

    ax.text(9.6, 0.45, "mergeable complementarity", fontsize=14, ha="center")
    save(fig, "dcola_overview.pdf")


def figure_surrogate_panels() -> None:
    fig, axs = plt.subplots(1, 4, figsize=(15.0, 4.2))
    for ax in axs:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis("off")

    axs[0].set_title("1. Robust source-domain fit")
    simplex = Polygon([[1.3, 1.4], [8.4, 1.4], [4.85, 5.0]], closed=True, facecolor=LIGHT, edgecolor=PLUM, linewidth=1.6)
    axs[0].add_patch(simplex)
    for pt, label in [((1.3, 1.4), r"$\pi_1$"), ((8.4, 1.4), r"$\pi_2$"), ((4.85, 5.0), r"$\pi_3$")]:
        axs[0].scatter([pt[0]], [pt[1]], s=54, color=PLUM, edgecolor=LIGHT, linewidth=0.7)
        axs[0].text(pt[0], pt[1] - 0.42, label, ha="center", fontsize=10)
    axs[0].scatter([4.85], [4.25], s=120, marker="*", color=GOLD, edgecolor=INK, linewidth=0.8)
    axs[0].text(4.85, 0.58, r"$\sup_{\pi\in\Delta^E}\sum_e \pi_e \widehat L_e^{\mathrm{ens}}(w)=\max_e \widehat L_e^{\mathrm{ens}}(w)$", ha="center", fontsize=10)

    axs[1].set_title("2. Hidden-shift conflict")
    x = np.arange(1, 11)
    y1 = np.array([2.0, 2.4, 3.0, 3.4, 3.1, 2.5, 1.9, 1.5, 1.8, 2.3])
    y2 = np.array([1.8, 2.2, 2.8, 3.25, 3.0, 2.4, 1.85, 1.55, 1.75, 2.15])
    y3 = np.array([2.7, 2.3, 1.8, 1.35, 1.55, 2.15, 2.9, 3.35, 3.1, 2.75])
    for yy, color in [(y1, RED), (y2, ORANGE), (y3, TEAL)]:
        axs[1].plot(x, yy, color=color, lw=2.0)
    axs[1].axhline(2.35, color=INK, lw=0.9, alpha=0.35)
    axs[1].text(5.5, 0.58, r"$\sup_{\delta^\top \mathbf{1}=0,\;\|\delta\|\leq \rho}\delta^\top L_e w = \rho\|P_\perp L_e w\|_2$", ha="center", fontsize=10)

    axs[2].set_title("3. Mergeability remainder")
    axs[2].add_patch(Ellipse((4.5, 3.1), 4.2, 2.3, angle=10, facecolor=TEAL, alpha=0.10, edgecolor=TEAL, linewidth=1.6))
    pts = np.array([[2.7, 2.5], [3.6, 3.6], [4.7, 3.05], [5.6, 3.55], [6.25, 2.45]])
    axs[2].scatter(pts[:, 0], pts[:, 1], s=50, color=TEAL, edgecolor=LIGHT, linewidth=0.8)
    mix = np.array([4.3, 3.0])
    soup = np.array([5.2, 2.65])
    axs[2].scatter([mix[0]], [mix[1]], s=115, color=BLUE, edgecolor=LIGHT, linewidth=0.9)
    axs[2].scatter([soup[0]], [soup[1]], s=115, color=GREEN, edgecolor=LIGHT, linewidth=0.9)
    arrow(axs[2], mix, soup, color=INK, lw=1.4, ms=16)
    axs[2].text(4.3, 4.45, "predictive mixture", color=BLUE, ha="center")
    axs[2].text(5.2, 1.75, "single soup", color=GREEN, ha="center")
    axs[2].text(5.0, 0.58, r"$M(w)=\max_e |\widehat L_e(\bar\theta(w))-\widehat L_e^{\mathrm{ens}}(w)|$", ha="center", fontsize=10)

    axs[3].set_title("4. Convex surrogate on a face")
    tri = Polygon([[1.5, 1.3], [8.2, 1.3], [4.85, 5.0]], closed=True, facecolor=LIGHT, edgecolor=GREEN, linewidth=1.6)
    axs[3].add_patch(tri)
    levels = [
        np.array([[2.2, 1.75], [7.4, 1.75], [4.85, 4.35]]),
        np.array([[2.8, 2.05], [6.8, 2.05], [4.85, 3.85]]),
        np.array([[3.35, 2.35], [6.3, 2.35], [4.85, 3.45]]),
    ]
    for poly, alpha in zip(levels, [0.10, 0.15, 0.22]):
        axs[3].add_patch(Polygon(poly, closed=True, facecolor=GREEN, alpha=alpha, edgecolor=GREEN, linewidth=1.0))
    axs[3].scatter([4.85], [2.8], s=125, color=GREEN, edgecolor=LIGHT, linewidth=1.0)
    axs[3].text(4.85, 0.58, r"$\max_e \widehat L_e^{\mathrm{ens}} + \lambda_{\mathrm{cov}} w^\top Cw + \lambda_{\mathrm{loc}} b^\top w$", ha="center", fontsize=10)
    save(fig, "dcola_surrogate_panels.pdf")


def figure_2d_principle() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(13.2, 5.2))

    ax = axs[0]
    ax.set_title("Flat, conflict-free regime")
    ax.add_patch(Ellipse((0.0, 0.0), 5.8, 3.4, angle=10, facecolor=TEAL, alpha=0.10, edgecolor=TEAL, linewidth=1.8))
    path = np.array([[-2.0, -0.7], [-1.35, 0.0], [-0.75, 0.6], [-0.1, 0.95], [0.55, 0.88], [1.2, 0.42], [1.8, -0.18]])
    ax.plot(path[:, 0], path[:, 1], color=BLUE, lw=2.2)
    ax.scatter(path[:, 0], path[:, 1], s=44, color=BLUE, edgecolor=LIGHT, linewidth=0.8)
    soup = path.mean(axis=0)
    ax.scatter([soup[0]], [soup[1]], s=135, color=GOLD, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    ax.text(0.0, -1.78, "low conflict + low remainder: width alone is enough", ha="center", fontsize=10)
    ax.set_xlabel("mergeable direction 1")
    ax.set_ylabel("mergeable direction 2")
    ax.set_aspect("equal")

    ax = axs[1]
    ax.set_title("Mergeable complementarity regime")
    ax.add_patch(Ellipse((0.0, 0.0), 5.8, 3.5, angle=10, facecolor=TEAL, alpha=0.10, edgecolor=TEAL, linewidth=1.8))
    bank = np.array([[-2.1, -0.75], [-1.55, 0.03], [-0.95, 0.6], [-0.2, 0.98], [0.6, 0.88], [1.1, 0.28], [1.75, -0.33]])
    ax.plot(bank[:, 0], bank[:, 1], color=GRAY, lw=1.8, alpha=0.8)
    ax.scatter(bank[:, 0], bank[:, 1], s=36, color=GRAY, edgecolor=LIGHT, linewidth=0.8)
    sel = bank[[1, 3, 6]]
    ax.scatter(sel[:, 0], sel[:, 1], s=74, color=ORANGE, edgecolor=LIGHT, linewidth=0.8, zorder=4)
    final = np.average(sel, axis=0, weights=np.array([0.28, 0.42, 0.30]))
    ax.scatter([final[0]], [final[1]], s=135, color=GREEN, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    dirs = [(-0.40, 0.38), (0.36, 0.10), (-0.32, -0.35)]
    for pt, direction, color in zip(sel, dirs, [RED, BLUE, PLUM]):
        ax.arrow(pt[0], pt[1], direction[0], direction[1], width=0.010, head_width=0.12, head_length=0.14, color=color, alpha=0.75, length_includes_head=True)
    ax.text(0.0, -1.82, "same mergeable region, but the best soup is determined by conflict cancellation", ha="center", fontsize=10)
    ax.set_xlabel("mergeable direction 1")
    ax.set_ylabel("mergeable direction 2")
    ax.set_aspect("equal")
    save(fig, "dcola_2d_principle.pdf")


def figure_hidden_shift() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(13.8, 4.6))

    ax = axs[0]
    ax.set_title("Centered loss profiles reveal hidden-slice conflict")
    xs = np.arange(1, 13)
    r1 = np.array([0.42, 0.38, 0.30, 0.16, -0.05, -0.24, -0.33, -0.28, -0.08, 0.10, 0.25, 0.34])
    r2 = np.array([0.40, 0.36, 0.28, 0.14, -0.04, -0.20, -0.30, -0.25, -0.06, 0.08, 0.21, 0.31])
    c1 = np.array([-0.26, -0.18, -0.07, 0.07, 0.22, 0.30, 0.35, 0.22, 0.06, -0.08, -0.18, -0.27])
    for yy, color, label in [(r1, RED, r"$c_1$"), (r2, ORANGE, r"$c_2$"), (c1, TEAL, r"$c_3$")]:
        ax.plot(xs, yy, color=color, lw=2.0, label=label)
    ax.axhline(0.0, color=INK, lw=1.0, alpha=0.4)
    ax.set_xlabel("validation slice index")
    ax.set_ylabel("centered negative log-probability")
    ax.legend(frameon=False, loc="upper right")

    ax = axs[1]
    ax.set_title("Block structure: redundancy vs complementarity")
    block = np.array(
        [
            [1.0, 0.92, 0.22, 0.18, 0.20],
            [0.92, 1.0, 0.24, 0.20, 0.18],
            [0.22, 0.24, 1.0, 0.66, 0.62],
            [0.18, 0.20, 0.66, 1.0, 0.74],
            [0.20, 0.18, 0.62, 0.74, 1.0],
        ]
    )
    n = block.shape[0]
    for i in range(n):
        for j in range(n):
            val = block[i, j]
            color = plt.cm.magma(0.22 + 0.68 * val)
            ax.add_patch(Rectangle((j, n - 1 - i), 1, 1, facecolor=color, edgecolor=LIGHT, linewidth=1.2))
    ax.add_patch(Rectangle((0, 3), 2, 2, fill=False, edgecolor=RED, linewidth=2.0))
    ax.add_patch(Rectangle((2, 0), 3, 3, fill=False, edgecolor=TEAL, linewidth=2.0))
    ax.text(1.0, 5.35, "redundant block", ha="center", color=RED)
    ax.text(3.5, -0.45, "complementary block", ha="center", color=TEAL)
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect("equal")
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels([rf"$c_{k}$" for k in range(1, n + 1)])
    ax.set_yticklabels([rf"$c_{k}$" for k in range(n, 0, -1)])
    ax.set_xlabel("checkpoint index")
    ax.set_ylabel("checkpoint index")
    save(fig, "dcola_hidden_shift.pdf")


def figure_noncontiguity() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(13.8, 4.8))
    bank_x = np.linspace(0.8, 9.2, 12)
    bank_y = 2.8 + 0.85 * np.sin(np.linspace(-0.9, 2.8, 12))

    ax = axs[0]
    ax.set_title("Contiguous window can stay redundant")
    ax.plot(bank_x, bank_y, color=BLUE, lw=2.1)
    ax.scatter(bank_x, bank_y, s=38, color=GRAY, edgecolor=LIGHT, linewidth=0.8)
    contig = np.arange(4, 8)
    colors = [RED, RED, ORANGE, ORANGE]
    for idx, color in zip(contig, colors):
        ax.scatter([bank_x[idx]], [bank_y[idx]], s=88, color=color, edgecolor=LIGHT, linewidth=0.8, zorder=4)
    ax.add_patch(Rectangle((3.6, 1.25), 3.0, 3.0, fill=False, edgecolor=RED, linewidth=1.8, linestyle="--"))
    ax.text(5.1, 0.55, "time adjacency can keep the same failure mode", ha="center", fontsize=10)
    ax.set_xlim(0.3, 9.7)
    ax.set_ylim(0.5, 5.2)
    ax.set_xlabel("checkpoint time")
    ax.set_ylabel("trajectory coordinate")

    ax = axs[1]
    ax.set_title("Noncontiguous support can cover different failures")
    ax.plot(bank_x, bank_y, color=BLUE, lw=2.1, alpha=0.8)
    ax.scatter(bank_x, bank_y, s=38, color=GRAY, edgecolor=LIGHT, linewidth=0.8)
    chosen = [1, 5, 10]
    chosen_colors = [RED, ORANGE, TEAL]
    for idx, color in zip(chosen, chosen_colors):
        ax.scatter([bank_x[idx]], [bank_y[idx]], s=92, color=color, edgecolor=LIGHT, linewidth=0.8, zorder=4)
    soup = np.average(np.column_stack([bank_x[chosen], bank_y[chosen]]), axis=0, weights=np.array([0.32, 0.36, 0.32]))
    ax.scatter([soup[0]], [soup[1]], s=145, color=GREEN, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    for idx in chosen:
        ax.plot([soup[0], bank_x[idx]], [soup[1], bank_y[idx]], color=GREEN, alpha=0.35, lw=1.2)
    ax.text(5.25, 0.55, "error-structure coverage, not time adjacency, determines the useful face", ha="center", fontsize=10)
    ax.set_xlim(0.3, 9.7)
    ax.set_ylim(0.5, 5.2)
    ax.set_xlabel("checkpoint time")
    ax.set_ylabel("trajectory coordinate")
    save(fig, "dcola_noncontiguity.pdf")


def figure_3d_basin() -> None:
    fig = plt.figure(figsize=(11.2, 6.1))
    ax = fig.add_subplot(111, projection="3d")

    xs = np.linspace(-2.7, 2.7, 140)
    ys = np.linspace(-2.3, 2.5, 140)
    X, Y = np.meshgrid(xs, ys)
    Z = surface_height(X, Y)
    ax.plot_surface(X, Y, Z, cmap="YlGnBu", linewidth=0, antialiased=True, alpha=0.86)
    ax.contour(X, Y, Z, zdir="z", offset=0.0, levels=11, colors="white", linewidths=0.7, alpha=0.45)

    traj = np.array([[-2.0, -0.8], [-1.45, -0.05], [-0.95, 0.6], [-0.25, 0.98], [0.55, 0.86], [1.05, 0.32], [1.62, -0.28], [2.0, -0.9]])
    traj_z = surface_height(traj[:, 0], traj[:, 1]) + 0.06
    ax.plot(traj[:, 0], traj[:, 1], traj_z, color=BLUE, lw=2.6)
    ax.scatter(traj[:, 0], traj[:, 1], traj_z, color=BLUE, s=34, depthshade=False)

    selected = traj[[1, 3, 6]]
    sel_z = surface_height(selected[:, 0], selected[:, 1]) + 0.08
    soup = np.average(selected, axis=0, weights=np.array([0.28, 0.42, 0.30]))
    soup_z = surface_height(soup[0], soup[1]) + 0.12
    bad = np.array([1.65, 1.45])
    bad_z = surface_height(bad[0], bad[1]) + 0.12

    ax.scatter(selected[:, 0], selected[:, 1], sel_z, color=ORANGE, s=80, depthshade=False)
    ax.scatter([soup[0]], [soup[1]], [soup_z], color=GREEN, s=125, depthshade=False)
    ax.scatter([bad[0]], [bad[1]], [bad_z], color=RED, s=105, depthshade=False)
    for pt, pz in zip(selected, sel_z):
        ax.plot([soup[0], pt[0]], [soup[1], pt[1]], [soup_z, pz], color=GREEN, alpha=0.38, lw=1.3)

    ax.text(-1.8, -1.15, traj_z[0] + 0.18, "trajectory bank", color=BLUE)
    ax.text(0.2, -0.25, surface_height(0.2, -0.25) + 0.32, "mergeable face", color=TEAL)
    ax.text(soup[0] + 0.08, soup[1] - 0.10, soup_z + 0.18, "final soup", color=GREEN)
    ax.text(bad[0] + 0.08, bad[1] + 0.08, bad_z + 0.18, "invalid cross-ridge average", color=RED)

    ax.view_init(elev=28, azim=-61)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel("mergeable direction 1")
    ax.set_ylabel("mergeable direction 2")
    ax.set_zlabel("loss")
    save(fig, "dcola_3d_basin.pdf")


def figure_simplex_face() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    ax.set_xlim(-0.08, 1.08)
    ax.set_ylim(-0.08, 0.98)
    ax.axis("off")

    A = np.array([0.0, 0.0])
    B = np.array([1.0, 0.0])
    C = np.array([0.5, 0.866])
    tri = Polygon([A, B, C], closed=True, facecolor=LIGHT, edgecolor=PLUM, linewidth=1.8)
    ax.add_patch(tri)

    def bary_to_xy(w1: float, w2: float, w3: float) -> np.ndarray:
        return w1 * A + w2 * B + w3 * C

    samples = []
    values = []
    for i in range(41):
        for j in range(41 - i):
            w1 = i / 40
            w2 = j / 40
            w3 = 1 - w1 - w2
            xy = bary_to_xy(w1, w2, w3)
            val = 0.18 * (w1 - 0.28) ** 2 + 0.14 * (w2 - 0.34) ** 2 + 0.06 * (w3 - 0.38) ** 2
            val += 0.02 * (w1 - w2) * (w2 - w3)
            samples.append(xy)
            values.append(val)
    samples = np.array(samples)
    values = np.array(values)
    levels = np.linspace(values.min(), values.max(), 7)
    tcf = ax.tricontourf(samples[:, 0], samples[:, 1], values, levels=levels, cmap="YlGn", alpha=0.75)
    for coll in tcf.collections:
        coll.set_edgecolor("face")

    active_face = np.array([bary_to_xy(0.55, 0.0, 0.45), bary_to_xy(0.0, 0.58, 0.42)])
    ax.plot(active_face[:, 0], active_face[:, 1], color=BLUE, lw=3.0)
    opt = bary_to_xy(0.28, 0.34, 0.38)
    uni = bary_to_xy(1 / 3, 1 / 3, 1 / 3)
    ax.scatter([opt[0]], [opt[1]], s=140, color=GREEN, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    ax.scatter([uni[0]], [uni[1]], s=120, color=GOLD, edgecolor=LIGHT, linewidth=1.0, zorder=5)
    ax.text(opt[0] + 0.05, opt[1] + 0.03, r"$w_S^\star$", color=GREEN)
    ax.text(uni[0] - 0.11, uni[1] - 0.08, r"$u_S$", color=GOLD)
    ax.text(0.5, 0.93, "low-curvature face", ha="center", color=BLUE)
    ax.text(A[0] - 0.02, A[1] - 0.06, r"$c_1$", ha="center")
    ax.text(B[0] + 0.02, B[1] - 0.06, r"$c_2$", ha="center")
    ax.text(C[0], C[1] + 0.05, r"$c_3$", ha="center")
    ax.text(0.5, -0.05, "uniform and optimal weights can be close once the correct face is found", ha="center", fontsize=10)
    save(fig, "dcola_simplex_face.pdf")


def main() -> None:
    setup()
    figure_overview()
    figure_surrogate_panels()
    figure_2d_principle()
    figure_hidden_shift()
    figure_noncontiguity()
    figure_3d_basin()
    figure_simplex_face()


if __name__ == "__main__":
    main()
