#!/usr/bin/env python
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
from matplotlib.patches import ConnectionPatch, FancyArrowPatch, FancyBboxPatch, Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "figures"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "font.family": "serif",
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / name, bbox_inches="tight")
    plt.close(fig)


def draw_covariance_panel(ax, matrix, title, xlabel, ylabel):
    cmap = plt.get_cmap("magma")
    norm = Normalize(vmin=0.0, vmax=1.0)
    n = matrix.shape[0]
    for i in range(n):
        for j in range(n):
            value = matrix[i, j]
            face = cmap(norm(value))
            rect = Rectangle(
                (j, i),
                1.0,
                1.0,
                facecolor=face,
                edgecolor=(1.0, 1.0, 1.0, 0.9),
                linewidth=1.2,
            )
            ax.add_patch(rect)
    ax.set_xlim(0, n)
    ax.set_ylim(n, 0)
    ax.set_aspect("equal")
    ax.set_facecolor("#f6f1eb")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(np.arange(n) + 0.5)
    ax.set_yticks(np.arange(n) + 0.5)
    ax.set_xticklabels([rf"$c_{i}$" for i in range(1, n + 1)])
    ax.set_yticklabels([rf"$c_{i}$" for i in range(1, n + 1)])
    for spine in ax.spines.values():
        spine.set_linewidth(1.1)
        spine.set_color("#333333")
    for i in range(n):
        for j in range(n):
            value = matrix[i, j]
            text_color = "white" if value < 0.70 else "black"
            ax.text(j + 0.5, i + 0.5, f"{value:.2f}", ha="center", va="center", color=text_color, fontsize=8, fontweight="semibold")
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    return sm


def add_box(ax, xy, width, height, text, facecolor, edgecolor="#222222"):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=1.2,
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        wrap=True,
    )


def add_arrow(ax, start, end, color="#333333"):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.4,
        color=color,
    )
    ax.add_patch(arrow)


def make_overview() -> None:
    fig, ax = plt.subplots(figsize=(12, 3.2))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 2.4)
    ax.axis("off")

    boxes = [
        ((0.2, 0.8), 1.7, 0.9, "Dense checkpoint\npool", "#d8e6f2"),
        ((2.2, 0.8), 1.8, 0.9, "Worst-domain\nanchor", "#f6d8ae"),
        ((4.4, 0.8), 2.0, 0.9, "Connected-valley\nfilter", "#d9ead3"),
        ((6.9, 0.8), 2.1, 0.9, "Convex weight\nselection", "#ead1dc"),
        ((9.4, 0.8), 1.1, 0.9, "Single\nsoup", "#f4cccc"),
    ]
    for pos, w, h, text, color in boxes:
        add_box(ax, pos, w, h, text, color)

    for x0, x1 in [(1.9, 2.2), (4.0, 4.4), (6.4, 6.9), (9.0, 9.4)]:
        add_arrow(ax, (x0, 1.25), (x1, 1.25))

    ax.text(2.95, 0.35, r"$a=\arg\min_t \max_e \widehat{L}_e(\theta_t)$", ha="center")
    ax.text(5.4, 0.35, r"$\widehat{L}_{\max} \leq \widehat{L}_{\max}(\theta_a)+\epsilon,\; B(t,a)\leq \tau$", ha="center")
    ax.text(7.95, 0.35, r"$\min_{w\in\Delta} \max_e \widehat{L}^{\mathrm{ens}}_e(w)+\lambda_{\mathrm{cov}}w^\top Cw+\lambda_{\mathrm{loc}}b^\top w$", ha="center")
    save(fig, "dcola_overview.pdf")


def make_timeline() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(11, 3.6), sharex=True)
    times = np.arange(1, 15)

    for ax in axes:
        ax.set_xlim(0.5, 14.5)
        ax.set_ylim(0, 1.2)
        ax.spines[["left", "right", "top"]].set_visible(False)
        ax.set_yticks([])
        ax.grid(axis="x", alpha=0.15)

    axes[0].set_title("SWAD: contiguous uniform averaging")
    axes[1].set_title("D-COLA: filtered nonuniform soup around worst-domain anchor")

    axes[0].hlines(0.5, 1, 14, color="#999999", linewidth=1.2)
    axes[1].hlines(0.5, 1, 14, color="#999999", linewidth=1.2)

    axes[0].scatter(times, np.full_like(times, 0.5), s=25, color="#88aacc", zorder=3)
    window = np.arange(5, 11)
    axes[0].scatter(window, np.full_like(window, 0.5), s=95, color="#1f77b4", zorder=4)
    axes[0].text(7.5, 0.92, "uniform interval", ha="center", color="#1f77b4")
    axes[0].text(5, 0.13, r"$t_s$", ha="center")
    axes[0].text(10, 0.13, r"$t_e$", ha="center")

    weights = np.array([0.0, 0.0, 0.07, 0.0, 0.16, 0.21, 0.0, 0.18, 0.0, 0.14, 0.1, 0.0, 0.14, 0.0])
    mask = weights > 0
    sizes = 30 + 420 * weights[mask]
    axes[1].scatter(times, np.full_like(times, 0.5), s=25, color="#b7b7b7", zorder=3)
    axes[1].scatter(times[mask], np.full(mask.sum(), 0.5), s=sizes, color="#d62728", zorder=4)
    axes[1].scatter([6], [0.5], s=180, marker="*", color="#ffbf00", edgecolor="#444444", zorder=5)
    axes[1].text(6, 0.92, "anchor", ha="center", color="#7f6000")
    axes[1].text(10.7, 0.92, "nonuniform weights after filtering", ha="center", color="#d62728")
    axes[1].set_xlabel("Checkpoint index")
    save(fig, "swad_vs_dcola_timeline.pdf")


def synthetic_loss(x, y):
    valley1 = 0.35 * ((x + 1.0) ** 2 + 1.8 * (y - 0.1) ** 2)
    valley2 = 0.48 * ((x - 1.1) ** 2 + 1.3 * (y + 0.2) ** 2)
    ridge = 1.6 * np.exp(-2.4 * (x ** 2 + (y + 0.1) ** 2))
    return np.minimum(valley1, valley2 + 0.25) + ridge


def method_heatmap_data():
    losses = np.array(
        [
            [1.08, 0.96, 0.82, 0.71, 0.60, 0.50, 0.46, 0.49, 0.53, 0.57, 0.65, 0.72, 0.80, 0.92],
            [0.88, 0.79, 0.67, 0.58, 0.54, 0.50, 0.47, 0.48, 0.52, 0.59, 0.66, 0.70, 0.76, 0.84],
            [1.22, 1.00, 0.87, 0.74, 0.61, 0.53, 0.45, 0.46, 0.49, 0.56, 0.63, 0.70, 0.83, 1.05],
            [0.95, 0.82, 0.76, 0.67, 0.59, 0.55, 0.51, 0.50, 0.54, 0.60, 0.64, 0.69, 0.75, 0.83],
        ]
    )
    return losses, losses.max(axis=0), int(np.argmin(losses.max(axis=0)))


def candidate_weights():
    return np.array([0.00, 0.00, 0.05, 0.00, 0.16, 0.21, 0.18, 0.00, 0.14, 0.00, 0.11, 0.15, 0.00, 0.00])


def make_valley_geometry() -> None:
    fig, ax = plt.subplots(figsize=(5.2, 4.1))
    xs = np.linspace(-2.4, 2.4, 300)
    ys = np.linspace(-2.0, 2.0, 300)
    xx, yy = np.meshgrid(xs, ys)
    zz = synthetic_loss(xx, yy)
    levels = np.linspace(0.15, 2.6, 14)
    cs = ax.contourf(xx, yy, zz, levels=levels, cmap="YlGnBu")
    fig.colorbar(cs, ax=ax, fraction=0.046, pad=0.04)

    candidates = np.array(
        [
            [-1.52, 0.15],
            [-1.26, 0.09],
            [-1.05, 0.06],
            [-0.88, 0.03],
            [-0.68, 0.00],
        ]
    )
    anchor = np.array([-1.03, 0.06])
    soup = np.average(candidates, axis=0, weights=np.array([0.27, 0.46, 0.27, 0.00, 0.00]))

    ax.plot(candidates[:, 0], candidates[:, 1], "o", color="#d62728", label="candidate checkpoints")
    ax.plot(anchor[0], anchor[1], marker="*", markersize=14, color="#ffbf00", markeredgecolor="#222222", label="anchor")
    ax.plot(soup[0], soup[1], marker="D", markersize=7, color="white", markeredgecolor="#222222", label="D-COLA soup")
    for point in candidates:
        ax.plot([anchor[0], point[0]], [anchor[1], point[1]], color="white", alpha=0.55, linewidth=1.3)
    ax.text(0.62, 1.55, "high barrier", color="black")
    ax.annotate("", xy=(0.12, 0.75), xytext=(0.82, 1.38), arrowprops={"arrowstyle": "->", "lw": 1.2})
    ax.set_xlabel("Weight-space direction 1")
    ax.set_ylabel("Weight-space direction 2")
    ax.legend(loc="lower left", fontsize=8, frameon=True)
    save(fig, "valley_geometry.pdf")


def make_landscape_3d() -> None:
    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    xs = np.linspace(-2.2, 2.2, 120)
    ys = np.linspace(-1.9, 1.9, 120)
    xx, yy = np.meshgrid(xs, ys)
    zz = synthetic_loss(xx, yy)

    ax.plot_surface(xx, yy, zz, cmap="YlGnBu", alpha=0.82, linewidth=0, antialiased=True)
    ax.contour(xx, yy, zz, zdir="z", offset=0.0, levels=12, colors="white", alpha=0.45, linewidths=0.6)

    candidates = np.array(
        [
            [-1.55, 0.15],
            [-1.24, 0.10],
            [-1.02, 0.06],
            [-0.82, 0.02],
            [-0.52, -0.02],
            [-0.18, -0.05],
        ]
    )
    vals = synthetic_loss(candidates[:, 0], candidates[:, 1])
    dcola = np.average(candidates, axis=0, weights=np.array([0.30, 0.40, 0.18, 0.08, 0.04, 0.00]))
    swad = candidates.mean(axis=0)
    marker_lift = 0.08
    vals_lifted = vals + marker_lift
    dcola_z = synthetic_loss(dcola[0], dcola[1]) + marker_lift
    swad_z = synthetic_loss(swad[0], swad[1]) + marker_lift
    ax.plot(candidates[:, 0], candidates[:, 1], vals_lifted, "-o", color="#d62728", linewidth=2.2, markersize=5.5, label="candidate valley")
    ax.scatter([candidates[2, 0]], [candidates[2, 1]], [vals[2] + 0.12], marker="*", s=260, color="#ffbf00", edgecolor="#333333", depthshade=False, label="anchor")
    ax.scatter([dcola[0]], [dcola[1]], [dcola_z], marker="D", s=92, color="white", edgecolor="#111111", depthshade=False, label="D-COLA soup")
    ax.scatter([swad[0]], [swad[1]], [swad_z], marker="s", s=92, color="#1f77b4", edgecolor="#111111", depthshade=False, label="uniform interval soup")
    ax.text(dcola[0] + 0.16, dcola[1] - 0.12, dcola_z + 0.18, "D-COLA", color="#111111")
    ax.text(swad[0] + 0.20, swad[1] + 0.06, swad_z + 0.28, "uniform soup", color="#1f77b4")
    ax.set_xlabel("Direction 1")
    ax.set_ylabel("Direction 2")
    ax.set_zlabel("Validation loss")
    ax.set_zlim(0.0, 2.5)
    ax.set_box_aspect((1.2, 1.0, 0.55))
    ax.view_init(elev=55, azim=-148)
    ax.set_title("Illustrative corner-view loss landscape")
    ax.legend(loc="upper left", fontsize=8)
    save(fig, "loss_landscape_3d.pdf")


def make_anchor_heatmap() -> None:
    losses, worst, anchor = method_heatmap_data()
    domains = ["Dom 1", "Dom 2", "Dom 3", "Dom 4"]
    checkpoints = np.arange(1, losses.shape[1] + 1)

    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(8.4, 5.0), gridspec_kw={"height_ratios": [2.2, 1.1]}, sharex=True)
    im = ax0.imshow(losses, aspect="auto", cmap="YlOrRd")
    fig.colorbar(im, ax=ax0, fraction=0.03, pad=0.02)
    ax0.set_yticks(np.arange(len(domains)))
    ax0.set_yticklabels(domains)
    ax0.set_title("Worst-domain anchor selection")
    ax0.scatter([anchor], [2], marker="*", s=250, color="#1f77b4", edgecolor="white")
    ax0.text(anchor + 0.2, 2.35, "anchor checkpoint", color="#1f77b4")

    ax1.plot(checkpoints, worst, "-o", color="#444444", linewidth=1.8)
    ax1.scatter([checkpoints[anchor]], [worst[anchor]], s=110, color="#1f77b4", zorder=4)
    ax1.set_ylabel(r"$\max_e \widehat{L}_e$")
    ax1.set_xlabel("Checkpoint index")
    ax1.grid(alpha=0.2)
    ax1.annotate("min worst-domain loss", xy=(checkpoints[anchor], worst[anchor]), xytext=(checkpoints[anchor] + 1.1, worst[anchor] + 0.16), arrowprops={"arrowstyle": "->"})
    save(fig, "anchor_heatmap.pdf")


def make_barrier_weights() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6), gridspec_kw={"width_ratios": [1.2, 1.0, 1.0]})
    alpha = np.linspace(0, 1, 100)
    pass_curve = 0.42 + 0.06 * np.sin(np.pi * alpha) ** 2
    fail_curve = 0.44 + 0.32 * np.sin(np.pi * alpha) ** 2

    axes[0].plot(alpha, pass_curve, color="#2ca02c", linewidth=2.0, label="passes barrier")
    axes[0].plot(alpha, fail_curve, color="#d62728", linewidth=2.0, label="fails barrier")
    axes[0].axhline(0.56, linestyle="--", color="#555555", linewidth=1.2)
    axes[0].text(0.02, 0.575, r"threshold $\tau$", color="#555555")
    axes[0].set_xlabel(r"Interpolation coefficient $\alpha$")
    axes[0].set_ylabel("Average validation loss")
    axes[0].set_title("Barrier screening")
    axes[0].legend(fontsize=8, frameon=True)
    axes[0].grid(alpha=0.2)

    cov = np.array(
        [
            [1.00, 0.82, 0.75, 0.15, 0.10],
            [0.82, 1.00, 0.78, 0.17, 0.13],
            [0.75, 0.78, 1.00, 0.20, 0.14],
            [0.15, 0.17, 0.20, 1.00, 0.62],
            [0.10, 0.13, 0.14, 0.62, 1.00],
        ]
    )
    im = draw_covariance_panel(
        axes[1],
        cov,
        "Loss covariance",
        "Candidate checkpoint $j$",
        "Candidate checkpoint $i$",
    )
    fig.colorbar(im, ax=axes[1], fraction=0.048, pad=0.04)

    w = np.array([0.02, 0.04, 0.08, 0.26, 0.19, 0.15, 0.11, 0.09, 0.06])
    axes[2].bar(np.arange(1, len(w) + 1), w, color="#d62728", edgecolor="#333333")
    axes[2].set_ylim(0, 0.32)
    axes[2].set_title("Final simplex weights")
    axes[2].set_xlabel("Candidate index")
    axes[2].set_ylabel(r"$w_t$")
    axes[2].grid(axis="y", alpha=0.2)
    save(fig, "barrier_covariance_weights.pdf")


def make_detailed_methodology() -> None:
    losses, worst, anchor = method_heatmap_data()
    weights = candidate_weights()
    fig = plt.figure(figsize=(8.2, 14.0))
    gs = fig.add_gridspec(4, 1, hspace=1.05)
    ax_heat = fig.add_subplot(gs[0, 0])
    ax_barrier = fig.add_subplot(gs[1, 0])
    ax_cov = fig.add_subplot(gs[2, 0])
    ax_weight = fig.add_subplot(gs[3, 0])
    fig.subplots_adjust(left=0.12, right=0.88, top=0.96, bottom=0.05)

    im = ax_heat.imshow(losses, aspect="auto", cmap="YlOrRd")
    ax_heat.set_title(r"Step 1. Score checkpoints and choose $a=\arg\min_t \max_e \widehat{L}_e(\theta_t)$", pad=12)
    ax_heat.set_xlabel("Checkpoint index")
    ax_heat.set_ylabel("Source domain")
    ax_heat.set_xticks(np.arange(losses.shape[1]))
    ax_heat.set_xticklabels(np.arange(1, losses.shape[1] + 1))
    ax_heat.set_yticks(range(4))
    ax_heat.set_yticklabels(["$e_1$", "$e_2$", "$e_3$", "$e_4$"])
    ax_heat.scatter([anchor], [2], marker="*", s=240, color="#1f77b4", edgecolor="white", linewidth=1.3, zorder=4)
    ax_heat.annotate("worst-domain anchor", xy=(anchor, 2), xytext=(anchor + 2.0, 3.25), color="#1f77b4", arrowprops={"arrowstyle": "->", "lw": 1.2})
    fig.colorbar(im, ax=ax_heat, fraction=0.03, pad=0.02, label="Validation loss")

    alpha = np.linspace(0, 1, 100)
    curves = [
        (0.46 + 0.04 * np.sin(np.pi * alpha) ** 2, "#2ca02c", "candidate A: keep"),
        (0.47 + 0.09 * np.sin(np.pi * alpha) ** 2, "#98df8a", "candidate B: keep"),
        (0.49 + 0.28 * np.sin(np.pi * alpha) ** 2, "#d62728", "candidate C: reject"),
    ]
    for curve, color, label in curves:
        ax_barrier.plot(alpha, curve, color=color, linewidth=2.4, label=label)
    ax_barrier.axhline(0.58, linestyle="--", color="#555555", linewidth=1.3)
    ax_barrier.text(0.02, 0.595, r"threshold $\tau$", color="#555555")
    ax_barrier.set_title(r"Step 2. Filter by interpolation barrier $B(t,a)$", pad=12)
    ax_barrier.set_xlabel(r"Interpolation coefficient $\alpha$")
    ax_barrier.set_ylabel("Average validation loss")
    ax_barrier.set_xlim(0, 1)
    ax_barrier.grid(alpha=0.22)
    ax_barrier.legend(loc="upper right", fontsize=9, frameon=True)

    cov = np.array(
        [
            [1.00, 0.86, 0.80, 0.20, 0.10, 0.08],
            [0.86, 1.00, 0.83, 0.18, 0.12, 0.09],
            [0.80, 0.83, 1.00, 0.16, 0.11, 0.10],
            [0.20, 0.18, 0.16, 1.00, 0.66, 0.58],
            [0.10, 0.12, 0.11, 0.66, 1.00, 0.72],
            [0.08, 0.09, 0.10, 0.58, 0.72, 1.00],
        ]
    )
    im2 = draw_covariance_panel(
        ax_cov,
        cov,
        r"Step 3. Estimate the covariance proxy $C$",
        "Candidate checkpoint $j$",
        "Candidate checkpoint $i$",
    )
    fig.colorbar(im2, ax=ax_cov, fraction=0.03, pad=0.02, label="Empirical covariance")

    keep_idx = np.arange(1, len(weights) + 1)
    ax_weight.bar(keep_idx, weights, color="#d62728", edgecolor="#333333")
    ax_weight.set_title(r"Step 4. Optimize $J(w)$ and form the final soup", pad=12)
    ax_weight.set_xlabel("Retained candidate checkpoint")
    ax_weight.set_ylabel(r"Weight $w_t$")
    ax_weight.set_ylim(0, 0.25)
    ax_weight.grid(axis="y", alpha=0.22)
    ax_weight.text(
        0.02,
        0.97,
        "Convex objective:\nworst-domain fit + covariance\n+ locality + entropy",
        transform=ax_weight.transAxes,
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#bbbbbb", "boxstyle": "round,pad=0.25", "alpha": 0.92},
    )

    arrow_kw = {"arrowstyle": "-|>", "mutation_scale": 20, "linewidth": 1.6, "color": "#444444"}
    fig.add_artist(ConnectionPatch((0.5, -0.18), (0.5, 1.12), "axes fraction", "axes fraction", axesA=ax_heat, axesB=ax_barrier, **arrow_kw))
    fig.add_artist(ConnectionPatch((0.5, -0.18), (0.5, 1.12), "axes fraction", "axes fraction", axesA=ax_barrier, axesB=ax_cov, **arrow_kw))
    fig.add_artist(ConnectionPatch((0.5, -0.18), (0.5, 1.12), "axes fraction", "axes fraction", axesA=ax_cov, axesB=ax_weight, **arrow_kw))
    save(fig, "dcola_detailed_methodology.pdf")


def make_certificate_terms() -> None:
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.axis("off")
    add_box(ax, (0.15, 2.55), 1.9, 0.7, "Worst-domain\npredictive fit", "#f6d8ae")
    add_box(ax, (2.4, 2.55), 1.7, 0.7, "Covariance\npenalty", "#ead1dc")
    add_box(ax, (4.45, 2.55), 1.4, 0.7, "Locality\npenalty", "#d9ead3")
    add_box(ax, (2.1, 1.3), 2.0, 0.75, "D-COLA objective\n$J(w)$", "#d8e6f2")
    add_box(ax, (2.05, 0.2), 2.1, 0.75, "Target-risk\ncertificate", "#f4cccc")
    add_arrow(ax, (1.1, 2.55), (2.75, 2.05))
    add_arrow(ax, (3.25, 2.55), (3.1, 2.05))
    add_arrow(ax, (5.05, 2.55), (3.45, 2.05))
    add_arrow(ax, (3.1, 1.3), (3.1, 0.95))
    ax.text(0.35, 3.55, r"$J(w)=\max_e \widehat{L}^{\mathrm{ens}}_e(w)+\lambda_{\mathrm{cov}}w^\top Cw+\lambda_{\mathrm{loc}}b^\top w+\lambda_{\mathrm{ent}}\Omega(w)$")
    ax.text(1.2, -0.1, r"$R_T(\bar{\theta}_w)\leq J(w)+\Xi$ under Assumption 4", color="#7a0000")
    ax.set_xlim(0, 6.1)
    ax.set_ylim(-0.3, 3.9)
    save(fig, "certificate_terms.pdf")


def make_prior_results() -> None:
    labels = ["ERM", "SWAD", "MA", "ENS", "DiWA", "DiWA LP"]
    values = [63.3, 66.9, 66.5, 67.1, 67.0, 68.0]
    colors = ["#999999", "#1f77b4", "#4c78a8", "#72b7b2", "#e45756", "#f58518"]
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    bars = ax.bar(labels, values, color=colors, edgecolor="#333333", linewidth=0.8)
    ax.set_ylim(60, 69)
    ax.set_ylabel("Average DomainBed accuracy (%)")
    ax.set_title("Published post-hoc DG baselines")
    ax.grid(axis="y", alpha=0.2)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.12, f"{value:.1f}", ha="center", va="bottom")
    ax.axhline(66.9, linestyle="--", linewidth=1.2, color="#1f77b4")
    ax.text(5.15, 67.08, "SWAD bar", color="#1f77b4", va="bottom")
    save(fig, "prior_published_results.pdf")


def make_tradeoff() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    locality = np.array([0.12, 0.18, 0.23, 0.28, 0.34, 0.42, 0.51, 0.61, 0.74, 0.88])
    covariance = np.array([0.92, 0.75, 0.63, 0.56, 0.48, 0.43, 0.38, 0.36, 0.34, 0.33])
    ax.plot(locality, covariance, "-o", color="#444444", alpha=0.7)
    pick = 4
    ax.scatter(locality[pick], covariance[pick], s=130, color="#d62728", label="D-COLA operating point", zorder=5)
    ax.annotate("too local,\nhigh redundancy", xy=(0.14, 0.89), xytext=(0.03, 0.97), arrowprops={"arrowstyle": "->"})
    ax.annotate("too diverse,\nhigh barrier", xy=(0.85, 0.34), xytext=(0.88, 0.54), arrowprops={"arrowstyle": "->"})
    ax.set_xlabel("Locality penalty / barrier surrogate")
    ax.set_ylabel("Covariance surrogate")
    ax.set_title("Covariance-locality trade-off")
    ax.grid(alpha=0.2)
    ax.legend(frameon=True)
    save(fig, "covariance_tradeoff.pdf")


def main() -> None:
    setup_style()
    make_overview()
    make_timeline()
    make_valley_geometry()
    make_landscape_3d()
    make_anchor_heatmap()
    make_barrier_weights()
    make_detailed_methodology()
    make_certificate_terms()
    make_prior_results()
    make_tradeoff()


if __name__ == "__main__":
    main()
