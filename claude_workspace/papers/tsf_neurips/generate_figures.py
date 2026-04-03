#!/usr/bin/env python
"""Generate original figures for the TSF NeurIPS paper."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


ROOT = Path(__file__).resolve().parent
FIGDIR = ROOT / "figures"


def dct_matrix(n: int) -> np.ndarray:
    c = np.zeros((n, n), dtype=float)
    factor = np.pi / n
    for k in range(n):
        alpha = np.sqrt(1.0 / n) if k == 0 else np.sqrt(2.0 / n)
        for t in range(n):
            c[k, t] = alpha * np.cos((t + 0.5) * k * factor)
    return c


def tsf_filter_matrix(n: int, lam: float = 6.0, order: int = 2) -> tuple[np.ndarray, np.ndarray]:
    c = dct_matrix(n)
    omega = 2.0 * np.sin(np.pi * np.arange(n) / (2.0 * n))
    rho = omega ** (2 * order)
    h = 1.0 / (1.0 + lam * rho)
    t = c.T @ np.diag(h) @ c
    return t, h


def checkpoint_mean_update_kernel(n: int) -> np.ndarray:
    idx = np.arange(1, n + 1)
    return (n + 1 - idx) / (n + 1)


def update_to_checkpoint_coeffs(a: np.ndarray) -> np.ndarray:
    n = len(a)
    alpha = np.zeros(n + 1, dtype=float)
    alpha[0] = 1.0 - a[0]
    for t in range(1, n):
        alpha[t] = a[t - 1] - a[t]
    alpha[n] = a[n - 1]
    return alpha


def make_toy_updates(n: int = 24) -> tuple[np.ndarray, np.ndarray]:
    t = np.linspace(0.0, 1.0, n)
    drift_x = 0.18 + 0.09 * np.cos(1.3 * np.pi * t)
    drift_y = 0.04 + 0.03 * np.sin(1.2 * np.pi * t)
    osc_x = 0.05 * np.sin(10.0 * np.pi * t)
    osc_y = 0.11 * np.sin(8.0 * np.pi * t + 0.5)
    noise_x = 0.015 * np.sin(19.0 * np.pi * t + 0.2)
    noise_y = 0.012 * np.cos(17.0 * np.pi * t + 0.3)
    v = np.stack([drift_x + osc_x + noise_x, drift_y + osc_y + noise_y], axis=1)
    return t, v


def cumulative_path(v: np.ndarray, start: np.ndarray | None = None) -> np.ndarray:
    if start is None:
        start = np.zeros(v.shape[1], dtype=float)
    pts = [start]
    cur = start.astype(float).copy()
    for row in v:
        cur = cur + row
        pts.append(cur.copy())
    return np.asarray(pts)


def savefig(fig: plt.Figure, name: str) -> None:
    path = FIGDIR / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def generate_overview() -> None:
    fig, axes = plt.subplots(1, 5, figsize=(16, 3.4))
    titles = [
        "1. Dense checkpoints",
        "2. Group updates",
        "3. Checkpoint-axis DCT",
        "4. Spectral shrinkage",
        "5. Reconstruct one model",
    ]
    for ax, title in zip(axes, titles):
        ax.set_title(title, fontsize=11, pad=8)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)

    ax = axes[0]
    path_t = np.linspace(0, 1, 12)
    x = path_t
    y = 0.5 + 0.2 * np.sin(2.0 * np.pi * path_t) + 0.05 * np.sin(10.0 * np.pi * path_t)
    ax.plot(x, y, color="#4C78A8", lw=2.5)
    ax.scatter(x, y, color="#1F4E79", s=24, zorder=3)
    ax.text(0.04, 0.1, r"$\theta^{(1)},\ldots,\theta^{(N)}$", fontsize=12, transform=ax.transAxes)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0.0, 1.05)

    ax = axes[1]
    rng = np.linspace(-1.0, 1.0, 12)
    mat = np.outer(np.sin(2.0 * np.pi * np.linspace(0, 1, 11)), np.cos(2.5 * np.pi * rng))
    ax.imshow(mat, cmap="coolwarm", aspect="auto")
    ax.text(0.03, 0.08, r"$V_g \in \mathbb{R}^{(N-1)\times d_g}$", fontsize=12, transform=ax.transAxes, color="black")

    ax = axes[2]
    k = np.arange(1, 13)
    amps = np.array([1.9, 1.5, 1.1, 0.9, 0.85, 0.75, 0.55, 0.35, 0.22, 0.18, 0.12, 0.08])
    ax.bar(k, amps, color="#72B7B2")
    ax.set_xlim(0.2, 12.8)
    ax.set_ylim(0, 2.1)
    ax.set_xlabel("Temporal mode")
    ax.text(0.06, 0.08, r"$\widehat V_g = C V_g$", fontsize=12, transform=ax.transAxes)

    ax = axes[3]
    h = np.array([1.0, 0.98, 0.92, 0.82, 0.70, 0.58, 0.42, 0.28, 0.18, 0.12, 0.07, 0.04])
    ax.bar(k, amps * h, color="#54A24B")
    ax.plot(k, 2.0 * h, color="#E45756", marker="o", lw=2)
    ax.set_xlim(0.2, 12.8)
    ax.set_ylim(0, 2.1)
    ax.set_xlabel("Temporal mode")
    ax.text(0.04, 0.08, r"$\widetilde{\widehat V}_g = H_{\lambda,m}\widehat V_g$", fontsize=12, transform=ax.transAxes)

    ax = axes[4]
    losses = np.sort(np.array([0.12, 0.18, 0.21, 0.25, 0.27, 0.33, 0.40, 0.44, 0.55, 0.63, 0.78, 0.92]))[::-1]
    idx = np.arange(len(losses))
    alpha_n = 4
    colors = ["#E45756" if i < alpha_n else "#4C78A8" for i in idx]
    ax.bar(idx, losses, color=colors)
    ax.axvline(alpha_n - 0.5, color="black", ls="--", lw=1.2)
    ax.text(0.05, 0.9, r"$\theta^\star = \theta^{(1)} + \sum_t \widetilde v^{(t)}$", fontsize=11, transform=ax.transAxes)
    ax.text(0.05, 0.78, r"$\widehat R_\alpha(\theta^\star)=\mathrm{Top}_\alpha(\ell(\theta^\star))$", fontsize=11, transform=ax.transAxes)
    ax.set_xlabel("Support examples sorted by loss")
    ax.set_ylim(0, 1.05)

    for i in range(4):
        x0 = axes[i].get_position().x1
        y0 = 0.5 * (axes[i].get_position().y0 + axes[i].get_position().y1)
        x1 = axes[i + 1].get_position().x0
        fig.add_artist(
            patches.FancyArrowPatch(
                (x0 + 0.005, y0),
                (x1 - 0.005, y0),
                transform=fig.transFigure,
                arrowstyle="-|>",
                mutation_scale=18,
                lw=1.8,
                color="#666666",
            )
        )
    savefig(fig, "overview_pipeline.pdf")


def generate_trajectory_intuition() -> None:
    fig = plt.figure(figsize=(14, 5.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.15])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], projection="3d")

    n = 24
    _, v = make_toy_updates(n)
    tmat, _ = tsf_filter_matrix(n, lam=7.0, order=2)
    vf = tmat @ v
    p_raw = cumulative_path(v)
    p_flt = cumulative_path(vf)

    ax1.plot(p_raw[:, 0], p_raw[:, 1], color="#4C78A8", lw=2.2, label="raw checkpoint path")
    ax1.scatter(p_raw[:, 0], p_raw[:, 1], color="#4C78A8", s=14)
    ax1.plot(p_flt[:, 0], p_flt[:, 1], color="#E45756", lw=3.0, label="TSF filtered path")
    ax1.scatter(p_flt[0, 0], p_flt[0, 1], color="black", s=40, marker="s", label="start")
    ax1.scatter(p_raw[-1, 0], p_raw[-1, 1], color="#4C78A8", s=60, marker="X", label="raw endpoint")
    ax1.scatter(p_flt[-1, 0], p_flt[-1, 1], color="#E45756", s=60, marker="X", label="filtered endpoint")
    ax1.set_title("2D trajectory intuition", fontsize=12)
    ax1.set_xlabel("principal direction 1")
    ax1.set_ylabel("principal direction 2")
    ax1.legend(frameon=False, fontsize=9, loc="upper left")

    xx = np.linspace(-0.4, 4.9, 120)
    yy = np.linspace(-1.6, 1.6, 120)
    X, Y = np.meshgrid(xx, yy)
    Z = 0.06 * (X - 2.3) ** 2 + 0.20 * Y**2 + 0.05 * np.sin(1.4 * X) * np.cos(1.8 * Y)
    ax2.plot_surface(X, Y, Z, cmap="YlGnBu", alpha=0.65, linewidth=0, antialiased=True)
    z_raw = 0.06 * (p_raw[:, 0] - 2.3) ** 2 + 0.20 * p_raw[:, 1] ** 2 + 0.05 * np.sin(1.4 * p_raw[:, 0]) * np.cos(1.8 * p_raw[:, 1])
    z_flt = 0.06 * (p_flt[:, 0] - 2.3) ** 2 + 0.20 * p_flt[:, 1] ** 2 + 0.05 * np.sin(1.4 * p_flt[:, 0]) * np.cos(1.8 * p_flt[:, 1])
    ax2.plot(p_raw[:, 0], p_raw[:, 1], z_raw + 0.03, color="#4C78A8", lw=2.3)
    ax2.scatter(p_raw[:, 0], p_raw[:, 1], z_raw + 0.03, color="#4C78A8", s=10)
    ax2.plot(p_flt[:, 0], p_flt[:, 1], z_flt + 0.03, color="#E45756", lw=3.0)
    ax2.scatter([p_raw[-1, 0]], [p_raw[-1, 1]], [z_raw[-1] + 0.03], color="#4C78A8", s=55, marker="X")
    ax2.scatter([p_flt[-1, 0]], [p_flt[-1, 1]], [z_flt[-1] + 0.03], color="#E45756", s=55, marker="X")
    ax2.set_title("3D corner view on a toy loss surface", fontsize=12)
    ax2.set_xlabel("direction 1")
    ax2.set_ylabel("direction 2")
    ax2.set_zlabel("loss")
    ax2.view_init(elev=24, azim=-62)
    savefig(fig, "trajectory_intuition.pdf")


def generate_signal_spectrum() -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 8))
    n = 32
    t = np.arange(n)
    raw = 0.55 * np.sin(2 * np.pi * t / n) + 0.18 * np.sin(4 * np.pi * t / n) + 0.30 * np.sin(12 * np.pi * t / n) + 0.08 * np.cos(18 * np.pi * t / n)
    tmat, h = tsf_filter_matrix(n, lam=8.0, order=2)
    filt = tmat @ raw
    c = dct_matrix(n)
    spec_raw = c @ raw
    spec_filt = h * spec_raw

    axes[0, 0].plot(t, raw, color="#4C78A8", lw=2.0, label="raw updates")
    axes[0, 0].plot(t, filt, color="#E45756", lw=2.6, label="filtered updates")
    axes[0, 0].set_title("Update signal")
    axes[0, 0].set_xlabel("checkpoint index")
    axes[0, 0].legend(frameon=False)

    k = np.arange(1, n + 1)
    axes[0, 1].bar(k - 0.18, np.abs(spec_raw), width=0.35, color="#4C78A8", label="raw")
    axes[0, 1].bar(k + 0.18, np.abs(spec_filt), width=0.35, color="#E45756", label="filtered")
    axes[0, 1].set_title("DCT magnitudes")
    axes[0, 1].set_xlabel("temporal mode")
    axes[0, 1].legend(frameon=False)

    axes[1, 0].plot(k, h, color="#54A24B", lw=2.6)
    axes[1, 0].scatter(k, h, color="#54A24B", s=18)
    axes[1, 0].set_ylim(-0.02, 1.02)
    axes[1, 0].set_title("Spectral response")
    axes[1, 0].set_xlabel("temporal mode")
    axes[1, 0].set_ylabel(r"$h_j(\lambda,m)$")

    path_raw = np.cumsum(raw)
    path_filt = np.cumsum(filt)
    axes[1, 1].plot(t, path_raw, color="#4C78A8", lw=2.0, label="raw cumulative path")
    axes[1, 1].plot(t, path_filt, color="#E45756", lw=2.6, label="filtered cumulative path")
    axes[1, 1].set_title("Integrated endpoint path")
    axes[1, 1].set_xlabel("checkpoint index")
    axes[1, 1].legend(frameon=False)
    savefig(fig, "signal_spectrum.pdf")


def generate_kernel_comparison() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 3.8))
    n = 24
    tmat, _ = tsf_filter_matrix(n, lam=6.0, order=2)
    a_tsf = tmat.sum(axis=0)
    a_uni = checkpoint_mean_update_kernel(n)
    alpha_tsf = update_to_checkpoint_coeffs(a_tsf)
    alpha_uni = np.ones(n + 1) / (n + 1)

    idx_u = np.arange(1, n + 1)
    axes[0].plot(idx_u, a_uni, color="#4C78A8", lw=2.5, label="uniform checkpoint average")
    axes[0].plot(idx_u, a_tsf, color="#E45756", lw=2.5, label="TSF endpoint kernel")
    axes[0].set_title("Update-space endpoint kernel")
    axes[0].set_xlabel("update index")
    axes[0].legend(frameon=False, fontsize=9)

    idx_c = np.arange(1, n + 2)
    axes[1].bar(idx_c - 0.18, alpha_uni, width=0.35, color="#4C78A8", label="uniform soup coeffs")
    axes[1].bar(idx_c + 0.18, alpha_tsf, width=0.35, color="#E45756", label="TSF coeffs")
    axes[1].axhline(0.0, color="black", lw=1.0)
    axes[1].set_title("Induced checkpoint coefficients")
    axes[1].set_xlabel("checkpoint index")
    axes[1].legend(frameon=False, fontsize=9)

    im = axes[2].imshow(tmat, cmap="coolwarm", aspect="auto")
    axes[2].set_title(r"Linear smoother $C^\top H C$")
    axes[2].set_xlabel("input update index")
    axes[2].set_ylabel("output update index")
    fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)
    savefig(fig, "kernel_comparison.pdf")


def generate_hidden_shift_topalpha() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 4.2))
    losses = np.array([0.92, 0.81, 0.77, 0.69, 0.63, 0.55, 0.48, 0.41, 0.33, 0.27, 0.18, 0.11])
    n = len(losses)
    alpha = 1 / 3
    k = int(alpha * n)
    idx = np.arange(n)
    colors = ["#E45756" if i < k else "#72B7B2" for i in idx]

    axes[0].bar(idx + 1, losses, color=colors)
    axes[0].axvline(k + 0.5, color="black", ls="--", lw=1.1)
    axes[0].text(k / 2 + 0.5, 0.97, r"worst $\alpha$ fraction", ha="center", va="top", fontsize=11)
    axes[0].set_title(r"Top-$\alpha$ empirical risk")
    axes[0].set_xlabel("support examples sorted by loss")
    axes[0].set_ylabel("loss")

    q = np.zeros(n)
    q[:k] = 1.0 / k
    axes[1].bar(idx + 1, q, color=colors)
    axes[1].axhline(1.0 / k, color="#E45756", ls=":", lw=1.6, label=r"cap $1/(\alpha n)$")
    axes[1].set_title("Equivalent capped-simplex reweighting")
    axes[1].set_xlabel("support examples")
    axes[1].set_ylabel("weight")
    axes[1].legend(frameon=False)
    savefig(fig, "hidden_shift_topalpha.pdf")


def generate_filter_family_grid() -> None:
    fig, axes = plt.subplots(2, 3, figsize=(12.8, 7.0))
    n = 24
    _, v = make_toy_updates(n)
    base = cumulative_path(v)
    settings = [(1.0, 1), (2.0, 1), (6.0, 1), (1.0, 2), (3.0, 2), (8.0, 2)]
    for ax, (lam, order) in zip(axes.ravel(), settings):
        tmat, _ = tsf_filter_matrix(n, lam=lam, order=order)
        path = cumulative_path(tmat @ v)
        ax.plot(base[:, 0], base[:, 1], color="#BBBBBB", lw=1.8, label="raw")
        ax.plot(path[:, 0], path[:, 1], color="#E45756", lw=2.5, label="TSF")
        ax.scatter(path[-1, 0], path[-1, 1], color="#E45756", marker="X", s=45)
        ax.set_title(rf"$\lambda={lam:.1f},\ m={order}$")
        ax.set_xticks([])
        ax.set_yticks([])
        if ax is axes[0, 0]:
            ax.legend(frameon=False, fontsize=8, loc="upper left")
    savefig(fig, "filter_family_grid.pdf")


def main() -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 160,
        }
    )
    generate_overview()
    generate_trajectory_intuition()
    generate_signal_spectrum()
    generate_kernel_comparison()
    generate_hidden_shift_topalpha()
    generate_filter_family_grid()


if __name__ == "__main__":
    main()
