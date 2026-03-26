from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "figure.dpi": 200,
    }
)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def add_box(ax, xy, wh, text, fc="#f6f8fb", ec="#223b5a"):
    x, y = xy
    w, h = wh
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        linewidth=1.8,
        edgecolor=ec,
        facecolor=fc,
    )
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", wrap=True)


def add_arrow(ax, p0, p1, color="#223b5a"):
    arrow = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=16, lw=1.8, color=color)
    ax.add_patch(arrow)


def overview():
    fig, ax = plt.subplots(figsize=(13, 3.8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis("off")

    add_box(ax, (0.2, 1.25), (2.1, 1.4), "Dense single-run\ncheckpoints")
    add_box(ax, (2.9, 1.25), (2.4, 1.4), "Near-optimal +\nbarrier-safe set")
    add_box(ax, (5.9, 1.25), (2.6, 1.4), "Cached true-class\nprobabilities")
    add_box(ax, (9.1, 1.25), (2.5, 1.4), "KL-ball robust\nrisk objective")
    add_box(ax, (12.1, 1.25), (1.5, 1.4), "Single\nweight soup", fc="#eef6ef", ec="#1d5f3a")

    add_arrow(ax, (2.3, 1.95), (2.9, 1.95))
    add_arrow(ax, (5.3, 1.95), (5.9, 1.95))
    add_arrow(ax, (8.5, 1.95), (9.1, 1.95))
    add_arrow(ax, (11.6, 1.95), (12.1, 1.95))

    ax.text(1.25, 3.2, "trajectory", ha="center", color="#223b5a", fontweight="bold")
    ax.text(4.1, 3.2, "averageable candidate set", ha="center", color="#223b5a", fontweight="bold")
    ax.text(7.2, 3.2, "direct bound optimization", ha="center", color="#223b5a", fontweight="bold")
    ax.text(12.9, 3.2, "deploy", ha="center", color="#1d5f3a", fontweight="bold")

    save(fig, "roar_overview.pdf")


def selector_family():
    fig, ax = plt.subplots(figsize=(12.5, 3.8))
    xs = np.linspace(0, 100, 101)
    curve = 0.25 + 0.08 * np.sin(xs / 9.0) + 0.0018 * (xs - 68) ** 2 / 5
    ax.plot(xs, curve, color="#4c6272", lw=2.2)

    ax.axvspan(60, 88, alpha=0.16, color="#7ba6d8", label="SWAD interval")
    ax.scatter([73], [curve[73]], s=95, color="#d97b66", label="ERM / best checkpoint", zorder=4)

    dcola_x = np.array([8, 15, 22, 38, 48, 60, 73, 88])
    dcola_y = curve[dcola_x] + np.array([0.02, -0.005, 0.004, -0.01, 0.006, -0.008, 0.003, 0.01])
    sizes = np.array([80, 70, 65, 92, 78, 72, 86, 74])
    ax.scatter(dcola_x, dcola_y, s=sizes, color="#2a7a4b", alpha=0.8, label="D-COLA soup support", zorder=4)

    roar_x = np.array([12, 23, 40, 61, 77, 86])
    roar_y = curve[roar_x] + np.array([0.008, -0.004, -0.008, -0.012, 0.002, 0.004])
    ax.scatter(roar_x, roar_y, s=105, marker="D", color="#7b4ab3", alpha=0.85, label="ROAR feasible simplex", zorder=5)

    ax.set_xlabel("Checkpoint time")
    ax.set_ylabel("Source validation loss")
    ax.set_title("Selector Families on One Trajectory")
    ax.legend(loc="upper left", ncol=2, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)

    save(fig, "selector_family.pdf")


def robust_vs_mean():
    fig, ax = plt.subplots(figsize=(6.7, 4.6))
    rho = np.linspace(0.0, 1.2, 200)
    mean_loss = 0.25 + 0 * rho
    entropic = 0.25 + np.sqrt(2 * np.maximum(rho, 1e-8)) * 0.12
    entropic = np.clip(entropic, None, 0.62)
    worst = 0.62 + 0 * rho

    ax.plot(rho, mean_loss, label="mean validation loss", lw=2.4, color="#46627f")
    ax.plot(rho, entropic, label="ROAR robust risk", lw=2.6, color="#7b4ab3")
    ax.plot(rho, worst, label="hardest-example limit", lw=2.2, color="#c65b4b", linestyle="--")

    ax.annotate("small-$\\rho$ expansion:\nmean + dispersion penalty", xy=(0.22, 0.34), xytext=(0.42, 0.46),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#444"), fontsize=10)

    ax.set_xlabel("Robustness radius $\\rho$")
    ax.set_ylabel("Objective value")
    ax.set_title("ROAR Interpolates Between Mean Risk and Hard-Subset Protection")
    ax.legend(frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)

    save(fig, "robust_vs_mean.pdf")


def complementarity():
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.1))

    groups = ["Subset A", "Subset B"]
    ckpt1 = [0.10, 2.30]
    ckpt2 = [2.30, 0.10]
    mix = [0.69, 0.69]
    x = np.arange(len(groups))
    w = 0.22

    axes[0].bar(x - w, ckpt1, width=w, label="checkpoint 1", color="#557da0")
    axes[0].bar(x, ckpt2, width=w, label="checkpoint 2", color="#cf7a5d")
    axes[0].bar(x + w, mix, width=w, label="mixture", color="#6b9d6e")
    axes[0].set_xticks(x, groups)
    axes[0].set_ylabel("Clipped log loss")
    axes[0].set_title("Useful Complementarity")
    axes[0].legend(frameon=False)
    axes[0].spines[["top", "right"]].set_visible(False)

    rho = np.linspace(0, 1.0, 150)
    single_curve = 1.20 + 0.55 * (1 - np.exp(-2.8 * rho))
    mix_curve = 0.69 + 0 * rho
    axes[1].plot(rho, single_curve, lw=2.5, color="#557da0", label="best singleton")
    axes[1].plot(rho, mix_curve, lw=2.5, color="#6b9d6e", label="ROAR mixture")
    axes[1].fill_between(rho, mix_curve, single_curve, color="#cfe7cf", alpha=0.45)
    axes[1].set_xlabel("Robustness radius $\\rho$")
    axes[1].set_ylabel("Robust risk")
    axes[1].set_title("The robust objective favors mixtures that cover hard subsets")
    axes[1].legend(frameon=False)
    axes[1].spines[["top", "right"]].set_visible(False)

    save(fig, "safe_complementarity.pdf")


def uncertainty_set():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.1))

    base = np.ones(8) / 8
    worst = np.array([0.05, 0.05, 0.06, 0.08, 0.09, 0.12, 0.20, 0.35])
    idx = np.arange(8)
    axes[0].bar(idx, base, color="#4f7cac", label="uniform source weights")
    axes[0].bar(idx, worst - base, bottom=base, color="#d97b66", alpha=0.85, label="adversarial tilt")
    axes[0].set_xlabel("Validation examples")
    axes[0].set_ylabel("Example weights")
    axes[0].set_title("KL-ball reweightings over source support")
    axes[0].legend(frameon=False)
    axes[0].spines[["top", "right"]].set_visible(False)

    triangle = np.array([[0.08, 0.08], [0.92, 0.08], [0.5, 0.92]])
    poly = Polygon(triangle, closed=True, facecolor="#eef2f7", edgecolor="#3c5974", lw=1.8)
    axes[1].add_patch(poly)
    center = np.array([0.5, 0.36])
    circ = Circle(center, 0.18, facecolor="#e6d9f6", edgecolor="#7b4ab3", alpha=0.8, lw=1.8)
    axes[1].add_patch(circ)
    axes[1].text(0.5, 0.36, "KL ball", ha="center", va="center", color="#4d2f7b")
    axes[1].text(0.5, 0.98, "$r_3$", ha="center")
    axes[1].text(0.01, 0.02, "$r_1$", ha="left")
    axes[1].text(0.99, 0.02, "$r_2$", ha="right")
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_aspect("equal")
    axes[1].axis("off")
    axes[1].set_title("Ambiguity set in probability space")

    save(fig, "uncertainty_set.pdf")


def soup_transfer():
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    xs = np.linspace(-2.2, 2.2, 300)
    ys = np.linspace(-2.0, 2.0, 260)
    X, Y = np.meshgrid(xs, ys)
    Z = 0.25 * (X ** 2 + 1.6 * Y ** 2) + 0.15 * np.sin(1.7 * X) + 0.05 * np.cos(2.2 * Y)
    ax.contour(X, Y, Z, levels=10, colors="#71869d", linewidths=1.0)

    pts = np.array([[-0.9, 0.35], [-0.35, 0.12], [0.15, -0.05], [0.62, -0.14]])
    ax.plot(pts[:, 0], pts[:, 1], "o", color="#2a7a4b", ms=8, label="candidate checkpoints")
    soup = np.average(pts, axis=0, weights=[0.15, 0.2, 0.35, 0.3])
    ax.plot(soup[0], soup[1], marker="D", color="#7b4ab3", ms=9, label="ROAR soup")
    ax.annotate("", xy=tuple(soup), xytext=tuple(pts[0]), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.annotate("", xy=tuple(soup), xytext=tuple(pts[-1]), arrowprops=dict(arrowstyle="->", lw=1.6))
    ax.text(-1.95, 1.65, "same connected low-loss basin", color="#445d74")
    ax.set_xlabel("weight-space direction 1")
    ax.set_ylabel("weight-space direction 2")
    ax.set_title("Locality supports predictive-mixture to weight-soup transfer")
    ax.legend(frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)

    save(fig, "soup_transfer.pdf")


def main():
    overview()
    selector_family()
    robust_vs_mean()
    complementarity()
    uncertainty_set()
    soup_transfer()


if __name__ == "__main__":
    main()
