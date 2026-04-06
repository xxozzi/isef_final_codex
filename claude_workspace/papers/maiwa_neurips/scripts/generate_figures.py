#!/usr/bin/env python
"""Generate conceptual figures for the MAIWA paper."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"


def _save(fig: plt.Figure, name: str, close: bool = True) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    if close:
        plt.close(fig)


def _simplex_coords(p: np.ndarray) -> np.ndarray:
    """Map 3-simplex barycentric coordinates to 2D triangle coordinates."""
    verts = np.array([
        [-0.95, -0.75],
        [0.95, -0.75],
        [0.0, 0.95],
    ])
    return p @ verts


def figure_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(12.0, 3.7))
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
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16, lw=1.7, color="#333333"))

    box(0.02, 0.38, 0.14, 0.26, "Full checkpoint bank\nfrom one trajectory", "#4c78a8")
    box(0.20, 0.38, 0.16, 0.26, "Per-domain held-out\nloss matrix $L$", "#f58518")
    box(0.40, 0.38, 0.16, 0.26, "Domain Gibbs tilts\n$q_i^w(t)\\propto w_t e^{-\\beta \\ell_{i,t}}$", "#54a24b")
    box(0.60, 0.38, 0.16, 0.26, "Average adaptation\ninformation $\\frac{1}{I}\\sum_i \\mathrm{KL}(q_i^w\\|w)$", "#e45756")
    box(0.80, 0.38, 0.17, 0.26, "Projected gradient on\nfull simplex $\\Delta_\\varepsilon$", "#72b7b2")

    arrow(0.16, 0.51, 0.20, 0.51)
    arrow(0.36, 0.51, 0.40, 0.51)
    arrow(0.56, 0.51, 0.60, 0.51)
    arrow(0.76, 0.51, 0.80, 0.51)

    ax.text(0.22, 0.17, r"$\ell_{i,t} = |V_i|^{-1}\sum_{(x,y)\in V_i}\ell(f_{\theta_t}(x),y)$", fontsize=11, ha="center")
    ax.text(0.58, 0.17, r"$\mathcal{J}(w)=\langle w,\bar\ell\rangle+\lambda \mathcal{A}(w)+\tau \mathrm{KL}(w\|u_T)$", fontsize=12, ha="center")
    ax.text(0.50, 0.88, "MAIWA acts directly on the full checkpoint bank", fontsize=14, ha="center")
    _save(fig, "maiwa_pipeline.pdf")


def figure_simplex_2d() -> None:
    fig, ax = plt.subplots(figsize=(7.4, 6.0))
    ax.axis("off")

    verts = np.array([
        [-1.0, -0.78],
        [1.0, -0.78],
        [0.0, 0.98],
    ])
    tri = Polygon(verts, closed=True, facecolor="#d9eaf7", edgecolor="#4c78a8", alpha=0.25, lw=1.8)
    ax.add_patch(tri)

    w = np.array([0.36, 0.33, 0.31])
    q1 = np.array([0.70, 0.18, 0.12])
    q2 = np.array([0.16, 0.68, 0.16])
    q3 = np.array([0.12, 0.20, 0.68])
    pts = [_simplex_coords(p) for p in (w, q1, q2, q3)]

    ax.scatter(*pts[0], s=110, color="#111111", zorder=5)
    ax.text(pts[0][0] + 0.04, pts[0][1] - 0.02, r"$w$", fontsize=12)

    colors = ["#e45756", "#54a24b", "#b279a2"]
    labels = [r"$q_1^w$", r"$q_2^w$", r"$q_3^w$"]
    for p, color, label in zip(pts[1:], colors, labels):
        ax.scatter(*p, s=90, color=color, zorder=5)
        ax.annotate("", xy=p, xytext=pts[0], arrowprops=dict(arrowstyle="-|>", lw=2.0, color=color))
        ax.text(p[0] + 0.03, p[1] + 0.03, label, fontsize=11, color=color)

    ax.text(verts[0, 0] - 0.08, verts[0, 1] - 0.09, r"$\theta_1$", fontsize=11)
    ax.text(verts[1, 0] + 0.02, verts[1, 1] - 0.09, r"$\theta_2$", fontsize=11)
    ax.text(verts[2, 0], verts[2, 1] + 0.08, r"$\theta_3$", fontsize=11, ha="center")

    ax.text(-1.02, 1.18, "Each domain tilts the same shared prior", fontsize=13)
    ax.text(-1.02, 1.02, r"small $\mathrm{KL}(q_i^w\|w)$ means little specialization is needed", fontsize=11)
    ax.set_xlim(-1.18, 1.18)
    ax.set_ylim(-0.96, 1.28)
    _save(fig, "simplex_specialization_2d.pdf")


def figure_simplex_3d() -> None:
    fig = plt.figure(figsize=(8.3, 6.2))
    ax = fig.add_subplot(111, projection="3d")

    verts = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.5, np.sqrt(3) / 2, 0.0],
        [0.5, np.sqrt(3) / 6, np.sqrt(2 / 3)],
    ])
    faces = [
        [verts[0], verts[1], verts[2]],
        [verts[0], verts[1], verts[3]],
        [verts[0], verts[2], verts[3]],
        [verts[1], verts[2], verts[3]],
    ]
    poly = Poly3DCollection(faces, facecolors="#9ecae1", edgecolors="#4c78a8", linewidths=1.2, alpha=0.12)
    ax.add_collection3d(poly)

    w = np.array([0.28, 0.24, 0.20, 0.28])
    q1 = np.array([0.55, 0.20, 0.10, 0.15])
    q2 = np.array([0.12, 0.56, 0.18, 0.14])
    q3 = np.array([0.15, 0.16, 0.51, 0.18])

    def embed(p: np.ndarray) -> np.ndarray:
        return p @ verts

    w_xyz = embed(w)
    q_xyz = [embed(q) for q in (q1, q2, q3)]

    ax.scatter(*w_xyz, s=100, color="#1d1d1d")
    ax.text(*(w_xyz + np.array([0.02, 0.02, 0.02])), r"$w$", fontsize=12)

    colors = ["#e45756", "#54a24b", "#b279a2"]
    labels = [r"$q_1^w$", r"$q_2^w$", r"$q_3^w$"]
    for xyz, color, label in zip(q_xyz, colors, labels):
        ax.scatter(*xyz, s=90, color=color)
        ax.plot([w_xyz[0], xyz[0]], [w_xyz[1], xyz[1]], [w_xyz[2], xyz[2]], color=color, lw=2.0)
        ax.text(*(xyz + np.array([0.01, 0.01, 0.02])), label, fontsize=11, color=color)

    for i, v in enumerate(verts):
        ax.scatter(*v, color="#4c78a8", s=25)
        ax.text(*(v + np.array([0.01, 0.01, 0.01])), rf"$\theta_{i+1}$", fontsize=10)

    ax.set_axis_off()
    ax.view_init(elev=24, azim=38)
    ax.set_title("Full-bank simplex with domain-specific Gibbs tilts", pad=18)
    _save(fig, "maiwa_simplex_3d.pdf")
    fig2 = plt.figure(figsize=(8.3, 6.2))
    ax2 = fig2.add_subplot(111, projection="3d")
    poly2 = Poly3DCollection(faces, facecolors="#9ecae1", edgecolors="#4c78a8", linewidths=1.2, alpha=0.12)
    ax2.add_collection3d(poly2)
    ax2.scatter(*w_xyz, s=100, color="#1d1d1d")
    ax2.text(*(w_xyz + np.array([0.02, 0.02, 0.02])), r"$w$", fontsize=12)
    for xyz, color, label in zip(q_xyz, colors, labels):
        ax2.scatter(*xyz, s=90, color=color)
        ax2.plot([w_xyz[0], xyz[0]], [w_xyz[1], xyz[1]], [w_xyz[2], xyz[2]], color=color, lw=2.0)
        ax2.text(*(xyz + np.array([0.01, 0.01, 0.02])), label, fontsize=11, color=color)
    for i, v in enumerate(verts):
        ax2.scatter(*v, color="#4c78a8", s=25)
        ax2.text(*(v + np.array([0.01, 0.01, 0.01])), rf"$\theta_{i+1}$", fontsize=10)
    ax2.set_axis_off()
    ax2.view_init(elev=24, azim=38)
    ax2.set_title("Interior support becomes necessary when domains disagree", pad=18)
    _save(fig2, "simplex_specialization_3d.pdf")


def figure_objective_simplex() -> None:
    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    ax.axis("off")

    verts = np.array([
        [-0.95, -0.75],
        [0.95, -0.75],
        [0.0, 0.95],
    ])
    tri = Polygon(verts, closed=True, facecolor="#d9eaf7", edgecolor="#4c78a8", alpha=0.20, lw=1.6)
    ax.add_patch(tri)

    ell = np.array([
        [0.1, 0.9, 0.9],
        [0.9, 0.2, 0.8],
        [0.8, 0.9, 0.2],
    ])
    beta = 6.0

    def objective(p: np.ndarray) -> float:
        pooled = p @ ell.mean(axis=0)
        A = 0.0
        for i in range(3):
            a = np.exp(-beta * ell[i])
            z = p @ a
            q = p * a / z
            A += np.sum(q * (np.log(q + 1e-12) - np.log(p + 1e-12)))
        return pooled + 0.28 * A

    bary = []
    values = []
    step = 180
    for i in range(step + 1):
        for j in range(step + 1 - i):
            k = step - i - j
            p = np.array([i, j, k], dtype=float) / step
            bary.append(_simplex_coords(p))
            values.append(objective(p))
    bary = np.asarray(bary)
    values = np.asarray(values)

    tri_plot = ax.tricontourf(bary[:, 0], bary[:, 1], values, levels=18, cmap="Blues")
    best = bary[np.argmin(values)]
    ax.scatter(best[0], best[1], color="#111111", s=70, zorder=5)
    ax.text(best[0] + 0.05, best[1] + 0.03, "minimum", fontsize=10)

    ax.text(verts[0, 0] - 0.08, verts[0, 1] - 0.08, r"$\theta_1$", fontsize=11)
    ax.text(verts[1, 0] + 0.02, verts[1, 1] - 0.08, r"$\theta_2$", fontsize=11)
    ax.text(verts[2, 0], verts[2, 1] + 0.08, r"$\theta_3$", fontsize=11, ha="center")
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.95, 1.15)
    ax.set_title("MAIWA objective on a 3-checkpoint slice")
    cbar = fig.colorbar(tri_plot, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Objective value")
    _save(fig, "maiwa_objective_simplex.pdf", close=False)
    _save(fig, "simplex_objective_landscape.pdf")


def figure_regimes() -> None:
    betas = np.linspace(0.05, 10.0, 300)
    loss_flat = np.array([0.45, 0.47, 0.50, 0.48])
    loss_comp = np.array([0.10, 0.95, 0.92, 0.90])

    def adaptation(beta: float, losses: np.ndarray, w: np.ndarray) -> float:
        a = np.exp(-beta * losses)
        z = np.dot(w, a)
        q = w * a / z
        return np.sum(q * (np.log(q + 1e-12) - np.log(w + 1e-12)))

    uniform = np.ones(4) / 4
    spiky = np.array([0.82, 0.06, 0.06, 0.06])

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.1))

    axes[0].plot(betas, [adaptation(b, loss_flat, uniform) for b in betas], lw=2.3, color="#4c78a8", label="flat bank")
    axes[0].plot(betas, [adaptation(b, loss_comp, uniform) for b in betas], lw=2.3, color="#e45756", label="complementary bank")
    axes[0].set_title("Uniform shared posterior")
    axes[0].set_xlabel(r"Inverse temperature $\beta$")
    axes[0].set_ylabel(r"Adaptation information $\mathcal{A}_i(w)$")
    axes[0].grid(alpha=0.25)
    axes[0].legend(frameon=False, fontsize=9)

    axes[1].plot(betas, [adaptation(b, loss_comp, uniform) for b in betas], lw=2.3, color="#54a24b", label="coverage prior")
    axes[1].plot(betas, [adaptation(b, loss_comp, spiky) for b in betas], lw=2.3, color="#b279a2", label="collapsed prior")
    axes[1].set_title("Low-temperature coverage effect")
    axes[1].set_xlabel(r"Inverse temperature $\beta$")
    axes[1].set_ylabel(r"Adaptation information $\mathcal{A}_i(w)$")
    axes[1].grid(alpha=0.25)
    axes[1].legend(frameon=False, fontsize=9)

    fig.suptitle("The same objective transitions from variance control to support coverage", y=1.02, fontsize=13)
    _save(fig, "maiwa_regimes.pdf", close=False)
    _save(fig, "beta_regimes.pdf")


def figure_flatness_quadratic() -> None:
    x = np.linspace(-2.0, 2.0, 400)
    y = np.linspace(-2.0, 2.0, 400)
    xx, yy = np.meshgrid(x, y)

    sharp = 0.9 * xx**2 + 2.7 * yy**2
    flat = 0.55 * xx**2 + 0.85 * yy**2

    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))
    for ax, z, title in zip(axes, [sharp, flat], ["Sharp local basin", "Flat local basin"]):
        ax.contour(xx, yy, z, levels=10, colors="#4c78a8", linewidths=1.0)
        samples = np.array([
            [-0.8, -0.3],
            [-0.2, 0.5],
            [0.0, -0.2],
            [0.4, 0.3],
            [0.8, -0.1],
        ])
        ax.scatter(samples[:, 0], samples[:, 1], color="#e45756", s=30)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title)
        for spine in ax.spines.values():
            spine.set_visible(False)
    axes[0].text(-1.95, -1.85, r"large $\mathrm{Var}_w(\ell_i)$" "\n" r"$\Rightarrow$ larger $\mathcal{A}_i(w)$", fontsize=10)
    axes[1].text(-1.95, -1.85, r"small $\mathrm{Var}_w(\ell_i)$" "\n" r"$\Rightarrow$ smaller $\mathcal{A}_i(w)$", fontsize=10)
    fig.suptitle("Quadratic intuition: flatness appears as low loss variance across the bank", y=1.02, fontsize=13)
    _save(fig, "maiwa_flatness_quadratic.pdf")


def figure_soup_translation() -> None:
    fig, ax = plt.subplots(figsize=(10.8, 3.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x: float, y: float, w: float, h: float, text: str, color: str) -> None:
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.03",
            linewidth=1.4, edgecolor=color, facecolor=color, alpha=0.15,
        )
        ax.add_patch(patch)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    def arrow(x0: float, y0: float, x1: float, y1: float) -> None:
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=16, lw=1.8, color="#333333"))

    box(0.03, 0.34, 0.24, 0.30, "Bank-weighted predictive mixture\n$\\tilde f_w(x)=\\sum_t w_t f_{\\theta_t}(x)$", "#4c78a8")
    box(0.39, 0.34, 0.22, 0.30, "Local-linearity residual\n$\\|f_{\\theta(w)}(x)-\\tilde f_w(x)\\|\\le r_i(w,x)$", "#f58518")
    box(0.73, 0.34, 0.23, 0.30, "Deployable weighted soup\n$\\theta(w)=\\sum_t w_t\\theta_t$", "#54a24b")
    arrow(0.27, 0.49, 0.39, 0.49)
    arrow(0.61, 0.49, 0.73, 0.49)

    ax.text(0.50, 0.86, "Predictive mixture analysis transfers to one deployable soup under local linearity", ha="center", fontsize=13)
    ax.text(0.50, 0.12, r"$\ell(f_{\theta(w)}(x),y)\le \sum_t w_t \ell(f_{\theta_t}(x),y)+L_\ell r_i(w,x)$", ha="center", fontsize=12)
    _save(fig, "soup_translation.pdf")


def figure_support_coverage() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 3.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    domains = ["domain 1", "domain 2", "domain 3", "domain 4"]
    checkpoints = [f"$\\theta_{i}$" for i in range(1, 8)]
    pref = np.array([
        [0.10, 0.25, 0.90, 0.95, 0.95, 0.92, 0.94],
        [0.92, 0.12, 0.85, 0.90, 0.91, 0.95, 0.96],
        [0.88, 0.91, 0.13, 0.82, 0.90, 0.94, 0.96],
        [0.90, 0.93, 0.92, 0.15, 0.22, 0.91, 0.94],
    ])
    x0, y0, w, h = 1.2, 0.8, 0.9, 0.7
    for i, d in enumerate(domains):
        ax.text(0.2, 4.1 - i * 0.8, d, fontsize=10, va="center")
        for j, cp in enumerate(checkpoints):
            color = plt.cm.Blues_r(pref[i, j])
            rect = Rectangle((x0 + j * w, y0 + (3 - i) * h), 0.75, 0.55, facecolor=color, edgecolor="white")
            ax.add_patch(rect)
            if i == 0:
                ax.text(x0 + j * w + 0.38, 4.55, cp, fontsize=10, ha="center")

    ax.text(7.8, 4.4, "shared prior", fontsize=10)
    weights = np.array([0.18, 0.19, 0.18, 0.19, 0.14, 0.06, 0.06])
    for j, wt in enumerate(weights):
        ax.add_patch(Rectangle((7.8, 0.85 + j * 0.35), 1.6 * wt, 0.22, facecolor="#54a24b", edgecolor="none", alpha=0.85))
        ax.text(7.65, 0.96 + j * 0.35, checkpoints[j], ha="right", va="center", fontsize=9)
    ax.text(7.8, 0.35, "low-temperature optimum spreads mass across\ndomain-preferred checkpoints", fontsize=10)
    _save(fig, "maiwa_support_coverage.pdf")


def main() -> None:
    figure_pipeline()
    figure_simplex_2d()
    figure_simplex_3d()
    figure_objective_simplex()
    figure_regimes()
    figure_flatness_quadratic()
    figure_soup_translation()
    figure_support_coverage()


if __name__ == "__main__":
    main()
