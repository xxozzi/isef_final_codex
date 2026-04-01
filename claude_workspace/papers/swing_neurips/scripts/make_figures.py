from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


ROOT = Path(__file__).resolve().parent.parent
FIGDIR = ROOT / "figures"


def setup_style():
    mpl.rcParams.update(
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
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )


def save(fig, name):
    fig.savefig(FIGDIR / f"{name}.pdf")
    plt.close(fig)


def basin_height(x, y):
    return 0.35 * x**2 + 0.12 * y**2 + 0.08 * x * y + 0.08 * np.sin(1.2 * x) * np.cos(0.8 * y)


def plot_basin_surface(ax, alpha=0.75):
    xs = np.linspace(-2.6, 2.6, 100)
    ys = np.linspace(-2.4, 2.4, 100)
    X, Y = np.meshgrid(xs, ys)
    Z = basin_height(X, Y)
    ax.plot_surface(X, Y, Z, cmap="YlGnBu", linewidth=0, antialiased=True, alpha=alpha)
    ax.view_init(elev=27, azim=-62)
    ax.set_xlabel("dir. 1")
    ax.set_ylabel("dir. 2")
    ax.set_zlabel("loss")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


def fig_basin_3d_steps():
    fig = plt.figure(figsize=(13.4, 4.2))
    axs = [
        fig.add_subplot(1, 3, 1, projection="3d"),
        fig.add_subplot(1, 3, 2, projection="3d"),
        fig.add_subplot(1, 3, 3, projection="3d"),
    ]

    mu = np.array([0.0, 0.0])
    ref = np.array([1.9, 0.95])
    iso = np.array([1.2, 0.60])
    swing = np.array([1.45, 0.28])
    pool = np.array(
        [
            [-1.4, -0.5],
            [-1.0, 0.2],
            [-0.8, -0.2],
            [-0.3, 0.6],
            [0.2, -0.3],
            [0.6, 0.5],
            [0.9, -0.1],
            [1.3, 0.8],
            [1.7, 0.4],
        ]
    )

    titles = [
        "Step 1: Connected checkpoint basin",
        "Step 2: Fit-vs-fragility geometry",
        "Step 3: Directional basin edit",
    ]

    for ax, title in zip(axs, titles):
        plot_basin_surface(ax)
        ax.set_title(title, pad=10)

    z_pool = basin_height(pool[:, 0], pool[:, 1]) + 0.06
    axs[0].scatter(pool[:, 0], pool[:, 1], z_pool, color="#1b9e77", s=34, depthshade=False)
    axs[0].scatter(mu[0], mu[1], basin_height(*mu) + 0.1, color="#2c3e50", s=65, depthshade=False)
    axs[0].text(mu[0], mu[1], basin_height(*mu) + 0.28, r"$\mu$", color="#2c3e50")
    axs[0].scatter(ref[0], ref[1], basin_height(*ref) + 0.08, color="#d95f02", s=60, depthshade=False)
    axs[0].text(ref[0], ref[1], basin_height(*ref) + 0.28, r"$\theta_{\mathrm{ref}}$", color="#d95f02")

    plane_x = np.linspace(-1.9, 2.3, 15)
    plane_y = 0.42 * plane_x - 0.25
    plane_z = basin_height(plane_x, plane_y) + 0.02
    axs[1].plot(plane_x, plane_y, plane_z, color="#2c3e50", linewidth=2.8)
    axs[1].scatter(mu[0], mu[1], basin_height(*mu) + 0.1, color="#2c3e50", s=65, depthshade=False)
    axs[1].scatter(ref[0], ref[1], basin_height(*ref) + 0.08, color="#d95f02", s=60, depthshade=False)
    eig_a = np.array([1.05, 0.55])
    eig_b = np.array([1.35, 0.12])
    for vec, label, color in [(eig_a, r"$v_{\mathrm{fit}}$", "#7570b3"), (eig_b, r"$v_{\mathrm{frag}}$", "#e7298a")]:
        p = mu + vec
        axs[1].plot(
            [mu[0], p[0]],
            [mu[1], p[1]],
            [basin_height(*mu) + 0.1, basin_height(*p) + 0.18],
            color=color,
            linewidth=3,
        )
        axs[1].text(p[0], p[1], basin_height(*p) + 0.3, label, color=color)

    for pt, label, color in [(ref, r"$\theta_{\mathrm{ref}}$", "#d95f02"), (iso, r"isotropic", "#1f78b4"), (swing, r"SWING", "#1b9e77")]:
        axs[2].scatter(pt[0], pt[1], basin_height(*pt) + 0.08, color=color, s=62, depthshade=False)
        axs[2].text(pt[0], pt[1], basin_height(*pt) + 0.26, label, color=color)
    axs[2].scatter(mu[0], mu[1], basin_height(*mu) + 0.1, color="#2c3e50", s=65, depthshade=False)
    axs[2].plot(
        [mu[0], ref[0]],
        [mu[1], ref[1]],
        [basin_height(*mu) + 0.1, basin_height(*ref) + 0.08],
        color="#d95f02",
        linestyle="--",
        linewidth=2.5,
    )
    axs[2].plot(
        [mu[0], swing[0]],
        [mu[1], swing[1]],
        [basin_height(*mu) + 0.1, basin_height(*swing) + 0.08],
        color="#1b9e77",
        linewidth=3,
    )
    axs[2].plot(
        [mu[0], iso[0]],
        [mu[1], iso[1]],
        [basin_height(*mu) + 0.1, basin_height(*iso) + 0.08],
        color="#1f78b4",
        linewidth=2.5,
    )

    save(fig, "basin_3d_steps")


def fig_anisotropic_vs_scalar_2d():
    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    x = np.linspace(-2.5, 2.7, 401)
    y = np.linspace(-2.1, 2.2, 401)
    X, Y = np.meshgrid(x, y)

    zref = np.array([1.8, 1.15])
    A = np.array([[2.2, 0.4], [0.4, 1.0]])
    B = np.array([[0.35, 0.05], [0.05, 2.3]])
    rho = 0.55

    def quad(Zx, Zy):
        D = np.stack([Zx - zref[0], Zy - zref[1]], axis=-1)
        fit = 0.5 * np.einsum("...i,ij,...j->...", D, A, D)
        frag = rho * np.einsum("...i,ij,...j->...", np.stack([Zx, Zy], axis=-1), B, np.stack([Zx, Zy], axis=-1))
        return fit + frag

    J = quad(X, Y)
    ax.contour(X, Y, J, levels=12, cmap="viridis", linewidths=1.2)

    M = A + 2 * rho * B
    swing = np.linalg.solve(M, A @ zref)
    alpha = np.dot(zref, zref) / (np.dot(zref, zref) + 2 * rho * (zref @ B @ zref))
    iso = alpha * zref

    ax.scatter(*zref, color="#d95f02", s=70, zorder=5, label=r"$z_{\mathrm{ref}}$")
    ax.scatter(*iso, color="#1f78b4", s=70, zorder=5, label="best scalar shrink")
    ax.scatter(*swing, color="#1b9e77", s=70, zorder=5, label="SWING optimum")
    ax.scatter(0, 0, color="#2c3e50", s=65, zorder=5, label=r"$\mu$")
    ax.plot([0, zref[0]], [0, zref[1]], "--", color="#d95f02", linewidth=2)
    ax.plot([0, iso[0]], [0, iso[1]], color="#1f78b4", linewidth=2)
    ax.plot([0, swing[0]], [0, swing[1]], color="#1b9e77", linewidth=2.5)

    ax.annotate("high fit support", xy=(2.05, 1.65), xytext=(1.0, 1.9), arrowprops=dict(arrowstyle="->", color="#6a3d9a"), color="#6a3d9a")
    ax.annotate("high fragility", xy=(1.55, 0.25), xytext=(2.0, -0.8), arrowprops=dict(arrowstyle="->", color="#e7298a"), color="#e7298a")
    ax.set_xlabel("generalized coordinate 1")
    ax.set_ylabel("generalized coordinate 2")
    ax.set_title("2D analogue: anisotropic shrinkage beats scalar shrinkage")
    ax.legend(frameon=False, loc="upper left")
    ax.set_aspect("equal")
    save(fig, "anisotropic_vs_scalar_2d")


def fig_reweighting_simplex():
    fig, ax = plt.subplots(figsize=(6.5, 5.4))
    tri = np.array([[0.05, 0.05], [0.95, 0.08], [0.50, 0.92], [0.05, 0.05]])
    ax.plot(tri[:, 0], tri[:, 1], color="#2c3e50", linewidth=2.5)

    vertices = np.array([[0.05, 0.05], [0.95, 0.08], [0.50, 0.92]])
    labels = [r"$g_1$", r"$g_2$", r"$g_3$"]
    colors = ["#1b9e77", "#d95f02", "#7570b3"]
    for v, label, color in zip(vertices, labels, colors):
        ax.scatter(v[0], v[1], color=color, s=90, zorder=5)
        ax.text(v[0] + 0.015, v[1] + 0.02, label, color=color)

    center = vertices.mean(axis=0)
    ax.scatter(center[0], center[1], color="#2c3e50", s=70, zorder=5)
    ax.text(center[0] + 0.02, center[1] + 0.02, r"$\bar g$", color="#2c3e50")

    rays = np.array(
        [
            center + np.array([0.12, 0.20]),
            center + np.array([0.22, -0.03]),
            center + np.array([-0.20, 0.03]),
            center + np.array([0.06, -0.18]),
        ]
    )
    for r in rays:
        ax.arrow(center[0], center[1], r[0] - center[0], r[1] - center[1], width=0.002, head_width=0.025, color="#e7298a", length_includes_head=True, alpha=0.8)

    ax.add_patch(patches.Circle(center, 0.18, fill=False, linestyle="--", linewidth=2.0, edgecolor="#1f78b4"))
    ax.text(0.14, 0.83, r"local reweighting ball", color="#1f78b4")
    ax.text(0.14, 0.74, r"$\chi^2/\ell_2$ ambiguity around the pooled source support")
    ax.text(0.11, 0.18, "reweightings swing the update\nalong fragile directions", color="#e7298a")
    ax.set_title("Reweighting view: local shifts in source-support space")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    save(fig, "reweighting_simplex")


def fig_operator_views():
    rng = np.random.default_rng(3)
    fig, axs = plt.subplots(1, 4, figsize=(13.3, 3.3))
    A = np.array(
        [
            [2.4, 0.3, 0.1, 0.0],
            [0.3, 1.7, 0.2, 0.1],
            [0.1, 0.2, 1.2, 0.2],
            [0.0, 0.1, 0.2, 0.8],
        ]
    )
    B = np.array(
        [
            [0.4, 0.1, 0.0, 0.0],
            [0.1, 0.9, 0.2, 0.0],
            [0.0, 0.2, 1.5, 0.2],
            [0.0, 0.0, 0.2, 2.1],
        ]
    )
    evals, evecs = np.linalg.eig(np.linalg.solve(A, B))
    order = np.argsort(evals)
    evals = np.real(evals[order])
    betas = 1 / (1 + 0.55 * evals)

    heatmaps = [(A, r"fit operator $\hat A$"), (B, r"fragility operator $\hat B$"), (np.linalg.solve(A, B), r"$\hat A^{-1}\hat B$")]
    for ax, (mat, title) in zip(axs[:3], heatmaps):
        im = ax.imshow(mat, cmap="YlGnBu")
        ax.set_title(title)
        ax.set_xticks(range(mat.shape[0]))
        ax.set_yticks(range(mat.shape[0]))
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center", color="black", fontsize=8)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax = axs[3]
    x = np.arange(len(evals))
    ax.bar(x - 0.18, evals, width=0.36, color="#7570b3", label=r"$\lambda_j$")
    ax.bar(x + 0.18, betas, width=0.36, color="#1b9e77", label=r"$\beta_j$")
    ax.set_xticks(x)
    ax.set_xticklabels([rf"$j={i+1}$" for i in x])
    ax.set_title("Generalized eigenvalues and shrinkage")
    ax.legend(frameon=False)
    save(fig, "operator_views")


def fig_method_overview():
    fig, ax = plt.subplots(figsize=(13.5, 3.8))
    ax.axis("off")

    boxes = [
        (0.03, 0.18, 0.18, 0.62, "#d9f0d3", "Dense checkpoint bank\nconnected low-loss pool"),
        (0.28, 0.18, 0.18, 0.62, "#ccebc5", "Reference model\nand basin center\n$\\theta_{\\mathrm{ref}},\\mu$"),
        (0.53, 0.18, 0.18, 0.62, "#cbd5e8", "Estimate operators\n$\\hat A$ from fit split\n$\\hat B$ from shift split"),
        (0.78, 0.18, 0.18, 0.62, "#fddbc7", "Generalized shrinkage\n$\\theta_{\\mathrm{SWING}}$\n(single deployable model)"),
    ]
    for x, y, w, h, color, text in boxes:
        ax.add_patch(patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015,rounding_size=0.02", facecolor=color, edgecolor="#2c3e50", linewidth=1.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=12)

    arrows = [(0.21, 0.49, 0.07), (0.46, 0.49, 0.07), (0.71, 0.49, 0.07)]
    for x, y, dx in arrows:
        ax.arrow(x, y, dx, 0, width=0.007, head_width=0.04, head_length=0.02, length_includes_head=True, color="#4a6fa5")

    ax.text(0.335, 0.1, "safe averaging stage", ha="center", color="#225ea8", fontsize=11)
    ax.text(0.74, 0.1, "new basin-edit stage", ha="center", color="#b35806", fontsize=11)
    ax.set_title("SWING pipeline: from a safe checkpoint basin to a directional post-hoc weight edit", pad=10)
    save(fig, "method_overview")


def fig_shrinkage_curve():
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    lam = np.linspace(0, 6, 400)
    for rho, color in [(0.25, "#1b9e77"), (0.5, "#7570b3"), (0.9, "#d95f02")]:
        beta = 1 / (1 + rho * lam)
        ax.plot(lam, beta, color=color, linewidth=2.8, label=rf"$\rho={rho}$")
    ax.set_xlabel(r"generalized fragility eigenvalue $\lambda_j$")
    ax.set_ylabel(r"shrinkage factor $\beta_j$")
    ax.set_title("High-fragility directions are attenuated smoothly")
    ax.legend(frameon=False)
    ax.set_ylim(0, 1.02)
    save(fig, "shrinkage_curve")


def main():
    FIGDIR.mkdir(parents=True, exist_ok=True)
    setup_style()
    fig_method_overview()
    fig_basin_3d_steps()
    fig_anisotropic_vs_scalar_2d()
    fig_reweighting_simplex()
    fig_operator_views()
    fig_shrinkage_curve()


if __name__ == "__main__":
    main()
