#!/usr/bin/env python
"""Generate transparent-background figures for the CDA paper."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig-cda")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"

INK = "#0f172a"
BLUE = "#2563eb"
TEAL = "#14b8a6"
GOLD = "#f59e0b"
MAGENTA = "#d946ef"
GREEN = "#84cc16"
CORAL = "#f97316"
GRAY = "#64748b"
LIGHT = "#e2e8f0"


def setup() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 11,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "text.color": INK,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.edgecolor": INK,
            "savefig.transparent": True,
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def save(fig: plt.Figure, name: str) -> None:
    path = FIG_DIR / name
    stem = path.with_suffix("")
    fig.savefig(stem.with_suffix(".png"), transparent=True, bbox_inches="tight", pad_inches=0.02, dpi=320)
    fig.savefig(stem.with_suffix(".pdf"), transparent=True, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def capsule(ax, xy, w, h, text, color, fontsize=16, subtext=None):
    patch = FancyBboxPatch(
        xy,
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.2",
        linewidth=2.4,
        edgecolor=color,
        facecolor=(1, 1, 1, 0.0),
    )
    ax.add_patch(patch)
    ax.text(xy[0] + w / 2, xy[1] + 0.58 * h, text, ha="center", va="center", fontsize=fontsize, fontweight="bold")
    if subtext:
        ax.text(xy[0] + w / 2, xy[1] + 0.26 * h, subtext, ha="center", va="center", fontsize=10, linespacing=1.1, color=GRAY)


def figure_overview() -> None:
    fig, ax = plt.subplots(figsize=(14.2, 3.2))
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 3.2)
    ax.axis("off")

    capsule(ax, (0.55, 0.78), 3.35, 1.35, "Model Criterion", BLUE, subtext="low source-mixture sensitivity")
    capsule(ax, (5.15, 0.78), 4.15, 1.35, "Theory", TEAL, subtext="target risk controlled by canalization")
    capsule(ax, (10.65, 0.78), 3.25, 1.35, "Practical CDA", GOLD, subtext="robust fit + interactions + mergeability")

    for x0, x1, color in [(3.95, 1.45, INK), (9.45, 1.45, INK)]:
        ax.add_patch(FancyArrowPatch((x0, x1), (x0 + 1.0, x1), arrowstyle="-|>", mutation_scale=22, linewidth=2.2, color=color))

    ax.plot([10.0, 10.0], [0.45, 2.75], color=CORAL, linewidth=2.0, linestyle="--")
    ax.text(10.0, 2.92, "surrogate boundary", color=CORAL, ha="center", fontsize=11)
    save(fig, "cda_overview.pdf")


def figure_surrogate_panels() -> None:
    fig, axs = plt.subplots(1, 3, figsize=(13.2, 3.85))

    # Panel 1: simplex + tangent ball
    ax = axs[0]
    tri = np.array([[0.10, 0.10], [0.90, 0.10], [0.50, 0.86]])
    ax.add_patch(Polygon(tri, closed=True, fill=False, edgecolor=INK, linewidth=2.2))
    center = np.array([0.50, 0.35])
    ax.add_patch(Circle(center, 0.17, fill=False, edgecolor=TEAL, linewidth=2.4))
    ax.scatter([center[0]], [center[1]], s=70, color=TEAL, zorder=3)
    for vec, color in zip([np.array([0.13, 0.05]), np.array([-0.10, 0.10]), np.array([-0.09, -0.08])], [BLUE, MAGENTA, CORAL]):
        ax.add_patch(FancyArrowPatch(center, center + vec, arrowstyle="-|>", mutation_scale=16, linewidth=2.0, color=color))
    ax.text(0.50, 0.91, "local hidden shift", ha="center", fontsize=12.5, fontweight="bold")
    ax.text(0.50, -0.04, r"$\alpha=u_E+\delta,\ \mathbf{1}^\top\delta=0,\ \|\delta\|_2\leq\rho$", ha="center", fontsize=10.5, color=GRAY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Panel 2: theorem decomposition
    ax = axs[1]
    ax.text(0.50, 0.86, "theorem", ha="center", fontsize=12.5, fontweight="bold")
    ax.text(0.50, 0.58, r"$L_T(\theta)\ \leq\ \bar L(\theta)\ +\ \rho\|P_\perp L(\theta)\|_2\ +\ \epsilon_{\mathrm{app}}$", ha="center", fontsize=13.5)
    ax.plot([0.15, 0.29], [0.43, 0.43], color=BLUE, linewidth=3.0, solid_capstyle="round")
    ax.text(0.22, 0.33, "target risk", ha="center", fontsize=10.2, color=BLUE, fontweight="bold")
    ax.plot([0.42, 0.54], [0.43, 0.43], color=GRAY, linewidth=3.0, solid_capstyle="round")
    ax.text(0.48, 0.33, "source fit", ha="center", fontsize=10.2, color=GRAY, fontweight="bold")
    ax.plot([0.66, 0.84], [0.43, 0.43], color=TEAL, linewidth=3.0, solid_capstyle="round")
    ax.text(0.75, 0.33, "canalization", ha="center", fontsize=10.2, color=TEAL, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Panel 3: interaction matrix
    ax = axs[2]
    M = np.array([
        [0.95, 0.40, -0.25, -0.10],
        [0.40, 0.80, -0.35, -0.18],
        [-0.25, -0.35, 0.75, 0.28],
        [-0.10, -0.18, 0.28, 0.65],
    ])
    im = ax.imshow(M, cmap="coolwarm", vmin=-1.0, vmax=1.0)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i,j]:+.2f}", ha="center", va="center", fontsize=9, color=INK, fontweight="bold")
    ax.text(1.5, -0.85, "expanded interactions", ha="center", va="bottom", fontsize=12.5, fontweight="bold", transform=ax.transData)
    ax.set_xticks(range(4), ["1", "2", "3", "4"])
    ax.set_yticks(range(4), ["1", "2", "3", "4"])
    ax.set_xlabel("checkpoint")
    ax.set_ylabel("checkpoint")
    for spine in ax.spines.values():
        spine.set_visible(False)
    save(fig, "cda_surrogate_panels.pdf")


def figure_flatness_vs_canalization() -> None:
    fig, axs = plt.subplots(1, 2, figsize=(12.2, 4.6))

    ax = axs[0]
    xs = np.linspace(-2.2, 2.2, 220)
    ys = np.linspace(-2.2, 2.2, 220)
    X, Y = np.meshgrid(xs, ys)
    Z = 0.22 * X**2 + 0.16 * Y**2
    ax.contour(X, Y, Z, levels=8, colors=GRAY, linewidths=1.4)
    A = np.array([-0.7, 0.2])
    B = np.array([0.9, -0.15])
    ax.scatter([A[0], B[0]], [A[1], B[1]], s=[80, 80], color=[TEAL, CORAL], zorder=3)
    ax.text(A[0] - 0.1, A[1] + 0.18, "A", color=TEAL, fontsize=14, fontweight="bold")
    ax.text(B[0] + 0.08, B[1] + 0.18, "B", color=CORAL, fontsize=14, fontweight="bold")
    ax.text(0.0, 2.35, "same pooled flatness", ha="center", fontsize=12.5, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    ax = axs[1]
    ax.axhline(0, color=LIGHT, linewidth=1.2)
    ax.axvline(0, color=LIGHT, linewidth=1.2)
    a_vecs = [np.array([0.02, 0.02]), np.array([-0.02, -0.02])]
    b_vecs = [np.array([0.24, -0.06]), np.array([-0.24, 0.06])]
    for vec in a_vecs:
        ax.add_patch(FancyArrowPatch((0, 0), vec, arrowstyle="-|>", mutation_scale=14, linewidth=2.0, color=TEAL))
    for vec in b_vecs:
        ax.add_patch(FancyArrowPatch((0, 0), vec, arrowstyle="-|>", mutation_scale=14, linewidth=2.0, color=CORAL))
    ax.add_patch(Circle((0, 0), 0.08, fill=False, edgecolor=TEAL, linewidth=2.2))
    ax.add_patch(Circle((0, 0), 0.26, fill=False, edgecolor=CORAL, linewidth=2.2, linestyle="--"))
    ax.text(0.06, 0.09, "A", color=TEAL, fontsize=14, fontweight="bold")
    ax.text(0.29, -0.13, "B", color=CORAL, fontsize=14, fontweight="bold")
    ax.text(0.0, 0.38, "different canalization", ha="center", fontsize=12.5, fontweight="bold")
    ax.set_xlim(-0.42, 0.42)
    ax.set_ylim(-0.42, 0.42)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    save(fig, "cda_flatness_vs_canalization.pdf")


def figure_hidden_shift_simplex() -> None:
    fig, ax = plt.subplots(figsize=(5.8, 4.8))
    tri = np.array([[0.10, 0.10], [0.90, 0.10], [0.50, 0.88]])
    ax.add_patch(Polygon(tri, closed=True, fill=False, edgecolor=INK, linewidth=2.4))
    center = np.array([0.50, 0.37])
    ax.add_patch(Circle(center, 0.18, fill=False, edgecolor=TEAL, linewidth=2.4))
    ax.scatter([center[0]], [center[1]], s=65, color=TEAL, zorder=3)
    target = np.array([0.62, 0.48])
    ax.scatter([target[0]], [target[1]], s=70, color=GOLD, zorder=3)
    ax.add_patch(FancyArrowPatch(center, target, arrowstyle="-|>", mutation_scale=18, linewidth=2.2, color=GOLD))
    ax.text(center[0], center[1] - 0.08, r"$u_E$", ha="center", fontsize=11.5)
    ax.text(target[0] + 0.03, target[1], r"$\alpha_T$", color=GOLD, fontsize=12)
    ax.text(0.50, 0.95, "source-mixture geometry", ha="center", fontsize=13, fontweight="bold")
    ax.text(0.50, 0.02, "Theorem 1 applies when the target stays near the source mixture.", ha="center", fontsize=10.2, color=GRAY)
    ax.axis("off")
    save(fig, "cda_hidden_shift_simplex.pdf")


def figure_method_panels() -> None:
    fig, axs = plt.subplots(1, 5, figsize=(14.8, 3.3))
    for ax in axs:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

    titles = ["bank", "family", "domain losses", "objective", "deploy"]
    for ax, title in zip(axs, titles):
        ax.text(0.5, 0.93, title, ha="center", fontsize=12.5, fontweight="bold")

    # bank
    ax = axs[0]
    xs = np.linspace(0.10, 0.88, 8)
    ys = 0.40 + 0.18 * np.sin(np.linspace(-1.0, 1.7, 8))
    ax.plot(xs, ys, color=BLUE, linewidth=2.6)
    ax.scatter(xs, ys, s=55, color=BLUE, edgecolors="white", linewidths=0.8, zorder=3)

    # family
    ax = axs[1]
    ax.add_patch(FancyBboxPatch((0.18, 0.20), 0.52, 0.55, boxstyle="round,pad=0.02,rounding_size=0.08", fill=False, edgecolor=TEAL, linewidth=2.4, linestyle="--"))
    family = np.array([[0.26, 0.35], [0.38, 0.52], [0.52, 0.58], [0.62, 0.46]])
    ax.scatter(family[:, 0], family[:, 1], s=70, color=TEAL, edgecolors="white", linewidths=0.8)

    # losses
    ax = axs[2]
    ax.plot([0.22, 0.22], [0.18, 0.74], color=LIGHT, linewidth=1.2)
    ax.plot([0.22, 0.80], [0.18, 0.18], color=LIGHT, linewidth=1.2)
    lines = [(0.70, BLUE), (0.58, MAGENTA), (0.46, CORAL)]
    for h, col in lines:
        ax.plot([0.26, 0.74], [h, 0.28 + 0.15 * np.random.RandomState(int(h*100)).rand()], color=col, linewidth=2.3)
    ax.text(0.50, 0.07, "held-out source losses", ha="center", fontsize=10.2, color=GRAY)

    # surrogate
    ax = axs[3]
    M = np.array([[0.85, -0.35], [-0.35, 0.72]])
    ax.imshow(M, cmap="coolwarm", vmin=-1, vmax=1, extent=(0.20, 0.80, 0.22, 0.82))
    ax.text(0.50, 0.12, r"$\max_e \widehat L_e + \lambda_{\mathrm{can}} w^\top C w + \lambda_{\mathrm{mg}} m^\top w$", ha="center", fontsize=9.8)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # deploy
    ax = axs[4]
    pts = np.array([[0.28, 0.36], [0.40, 0.60], [0.58, 0.62], [0.68, 0.42]])
    center = np.array([0.50, 0.46])
    for pt in pts:
        ax.plot([center[0], pt[0]], [center[1], pt[1]], color=GOLD, linewidth=1.8)
    ax.scatter(pts[:, 0], pts[:, 1], s=70, color=GOLD, edgecolors="white", linewidths=0.8)
    ax.scatter([center[0]], [center[1]], s=170, color=GREEN, edgecolors="white", linewidths=1.0)
    ax.text(0.50, 0.07, "one final soup", ha="center", fontsize=10.2, color=GRAY)

    for i in range(4):
        bbox0 = axs[i].get_position()
        bbox1 = axs[i + 1].get_position()
        start = (bbox0.x1 - 0.01, 0.53 * (bbox0.y0 + bbox0.y1))
        end = (bbox1.x0 + 0.01, 0.53 * (bbox1.y0 + bbox1.y1))
        fig.add_artist(FancyArrowPatch(start, end, transform=fig.transFigure, arrowstyle="-|>", mutation_scale=18, linewidth=2.0, color=INK))
    save(fig, "cda_method_panels.pdf")


def bowl_z(x, y):
    return 0.16 * x**2 + 0.12 * y**2 + 0.04 * x * y


def project(points):
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]
    u = x - 0.85 * y
    v = 0.48 * (x + y) - 1.25 * z
    return np.column_stack([u, v])


def figure_3d_basin() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    ax.axis("off")

    # wireframe bowl
    xs = np.linspace(-2.3, 2.3, 21)
    ys = np.linspace(-2.1, 2.1, 21)
    for x in xs:
        pts = np.array([[x, y, bowl_z(x, y)] for y in ys])
        uv = project(pts)
        ax.plot(uv[:, 0], uv[:, 1], color="#cbd5e1", linewidth=1.15, alpha=1.0, zorder=1)
    for y in ys:
        pts = np.array([[x, y, bowl_z(x, y)] for x in xs])
        uv = project(pts)
        ax.plot(uv[:, 0], uv[:, 1], color="#cbd5e1", linewidth=1.15, alpha=1.0, zorder=1)

    # trajectory and soup points
    traj_xy = np.array([
        [-1.8, -0.8],
        [-1.4, -0.2],
        [-1.0, 0.35],
        [-0.55, 0.70],
        [-0.05, 0.66],
        [0.40, 0.34],
        [0.82, -0.02],
        [1.12, -0.34],
        [1.38, -0.62],
    ])
    traj = np.column_stack([traj_xy, bowl_z(traj_xy[:, 0], traj_xy[:, 1])])
    kept = traj[[2, 3, 4, 5, 6]]
    soup = np.array([[0.12, 0.22, bowl_z(0.12, 0.22)]])

    traj_uv = project(traj)
    kept_uv = project(kept)
    soup_uv = project(soup)

    ax.plot(traj_uv[:, 0], traj_uv[:, 1], color=BLUE, linewidth=3.2, zorder=3)
    ax.scatter(traj_uv[:, 0], traj_uv[:, 1], s=82, color=BLUE, edgecolors="white", linewidths=1.6, zorder=4)
    ax.scatter(kept_uv[:, 0], kept_uv[:, 1], s=280, color=GOLD, edgecolors=INK, linewidths=1.8, zorder=5)
    ax.scatter(soup_uv[:, 0], soup_uv[:, 1], s=420, color=GREEN, edgecolors="white", linewidths=2.0, zorder=6)
    for pt in kept_uv:
        ax.plot([soup_uv[0, 0], pt[0]], [soup_uv[0, 1], pt[1]], color=MAGENTA, linewidth=2.6, alpha=1.0, zorder=4)

    # axes
    origin = np.array([[-2.8, -2.2, 0.0], [2.7, -2.2, 0.0], [-2.8, 2.3, 0.0], [-2.8, -2.2, 1.8]])
    uv = project(origin)
    base = uv[0]
    ax.plot([base[0], uv[1, 0]], [base[1], uv[1, 1]], color=INK, linewidth=2.3)
    ax.plot([base[0], uv[2, 0]], [base[1], uv[2, 1]], color=INK, linewidth=2.3)
    ax.plot([base[0], uv[3, 0]], [base[1], uv[3, 1]], color=INK, linewidth=2.3)

    ax.text(base[0] + 2.35, base[1] + 0.30, "basin dir. 1", color=GRAY, fontsize=15, rotation=-15)
    ax.text(base[0] - 1.75, base[1] + 0.62, "basin dir. 2", color=GRAY, fontsize=15, rotation=27)
    ax.text(uv[3, 0] + 0.22, uv[3, 1] + 0.02, "loss", color=GRAY, fontsize=15)

    ax.annotate("trajectory", xy=traj_uv[2], xytext=(-4.8, 2.0), textcoords="data",
                fontsize=14, color=BLUE,
                arrowprops=dict(arrowstyle="-", color=BLUE, lw=2.0))
    ax.annotate("retained checkpoints", xy=kept_uv[2], xytext=(-0.2, 2.45), textcoords="data",
                fontsize=14, color=GOLD,
                arrowprops=dict(arrowstyle="-", color=GOLD, lw=2.0))
    ax.annotate("final soup", xy=soup_uv[0], xytext=(2.45, 1.95), textcoords="data",
                fontsize=14, color=GREEN,
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=2.0))

    ax.set_aspect("equal")
    save(fig, "cda_3d_basin.pdf")


def figure_simplex_face() -> None:
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    tri = np.array([[0.12, 0.12], [0.88, 0.12], [0.50, 0.86]])
    ax.add_patch(Polygon(tri, closed=True, fill=False, edgecolor=INK, linewidth=2.4))
    face = np.array([[0.28, 0.22], [0.70, 0.24], [0.56, 0.58]])
    ax.add_patch(Polygon(face, closed=True, fill=False, edgecolor=TEAL, linewidth=2.6))
    path = np.array([[0.34, 0.28], [0.43, 0.35], [0.51, 0.39], [0.60, 0.37]])
    ax.plot(path[:, 0], path[:, 1], color=GOLD, linewidth=2.6)
    ax.scatter(path[:, 0], path[:, 1], s=60, color=GOLD, edgecolors="white", linewidths=0.8, zorder=3)
    ax.scatter([0.51], [0.39], s=150, color=GREEN, edgecolors="white", linewidths=1.0, zorder=4)
    for pt, lab in zip(tri, ["ckpt 1", "ckpt 2", "ckpt 3"]):
        ax.text(pt[0], pt[1] + 0.05, lab, ha="center", fontsize=10.5)
    ax.text(0.50, 0.64, "low-curvature face", ha="center", fontsize=12.5, fontweight="bold")
    ax.text(0.50, 0.05, "support can matter more than exact weights", ha="center", fontsize=10.2, color=GRAY)
    ax.axis("off")
    save(fig, "cda_simplex_face.pdf")


def main() -> None:
    setup()
    figure_overview()
    figure_surrogate_panels()
    figure_flatness_vs_canalization()
    figure_hidden_shift_simplex()
    figure_method_panels()
    figure_3d_basin()
    figure_simplex_face()


if __name__ == "__main__":
    main()
