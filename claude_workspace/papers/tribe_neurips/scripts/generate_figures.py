from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)


def tribe_overview():
    fig, ax = plt.subplots(figsize=(11.2, 3.9))
    ax.axis("off")
    boxes = [
        (0.02, 0.22, 0.16, 0.56, "#dbeafe", "Dense checkpoint\nbank"),
        (0.23, 0.22, 0.18, 0.56, "#dcfce7", "Fixed averaged\nanchor"),
        (0.46, 0.22, 0.18, 0.56, "#fef3c7", "Trajectory-basis\ndiscovery"),
        (0.69, 0.22, 0.17, 0.56, "#fee2e2", "Robust local\nhead repair"),
        (0.89, 0.22, 0.09, 0.56, "#e9d5ff", "One\nmodel"),
    ]
    for x, y, w, h, c, txt in boxes:
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.025",
                fc=c,
                ec="black",
                lw=1.4,
            )
        )
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=12)
    for x1, x2 in [(0.18, 0.23), (0.41, 0.46), (0.64, 0.69), (0.86, 0.89)]:
        ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(
        0.5,
        0.06,
        "Checkpoint selection remains post-hoc; the new ingredient is a local classifier-boundary repair driven by trajectory failure modes.",
        ha="center",
        fontsize=11.5,
    )
    save(fig, "tribe_overview.pdf")


def trajectory_basis_pipeline():
    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.6), gridspec_kw={"width_ratios": [1.2, 1.0, 1.0]})
    rng = np.random.default_rng(7)
    n, t, k = 26, 18, 3
    u = rng.normal(size=(n, k))
    v = rng.normal(size=(t, k))
    mat = u @ np.diag([2.2, 1.4, 0.9]) @ v.T + 0.35 * rng.normal(size=(n, t))
    im = axes[0].imshow(mat, cmap="RdBu_r", aspect="auto")
    axes[0].set_title("Centered trajectory matrix $\\widetilde R$")
    axes[0].set_xlabel("checkpoint index")
    axes[0].set_ylabel("source-holdout examples")
    plt.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

    _, s, vt = np.linalg.svd(mat, full_matrices=False)
    axes[1].bar(np.arange(1, 9), s[:8], color="#60a5fa", edgecolor="black")
    axes[1].set_title("Singular spectrum")
    axes[1].set_xlabel("mode")
    axes[1].set_ylabel("value")
    axes[1].axvline(3.5, color="#b91c1c", ls="--", lw=1.5)
    axes[1].text(3.65, 0.92 * s[0], "keep top-$k$", color="#b91c1c")

    scores = mat @ vt[:2].T
    axes[2].scatter(scores[:, 0], scores[:, 1], s=40, color="#34d399", edgecolor="black", alpha=0.9)
    axes[2].axhline(0, color="gray", lw=1)
    axes[2].axvline(0, color="gray", lw=1)
    axes[2].set_title("Example coordinates $z(x,y)$")
    axes[2].set_xlabel("basis coordinate 1")
    axes[2].set_ylabel("basis coordinate 2")
    save(fig, "trajectory_basis_pipeline.pdf")


def basis_uncertainty_geometry():
    fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.8))
    axes[0].set_title("Low-rank shift family in score space")
    theta = np.linspace(0, 2 * np.pi, 300)
    x = 0.35 * np.cos(theta)
    y = 0.18 * np.sin(theta)
    axes[0].fill(x, y, color="#fde68a", alpha=0.9)
    axes[0].plot(x, y, color="black", lw=1.3)
    axes[0].scatter([0], [0], s=35, color="black")
    axes[0].text(0.02, 0.02, "uniform source\nweights", fontsize=10)
    axes[0].set_xlabel("trajectory direction 1")
    axes[0].set_ylabel("trajectory direction 2")
    axes[0].set_aspect("equal")

    axes[1].set_title("Equivalent robust penalty")
    c = np.linspace(0.0, 1.0, 250)
    mean = 0.25 + 0.25 * c
    basis = 0.05 + 0.55 * np.sqrt(c)
    total = mean + basis
    axes[1].plot(c, mean, lw=2.2, label="mean loss")
    axes[1].plot(c, basis, lw=2.2, label="basis-aligned penalty")
    axes[1].plot(c, total, lw=2.6, color="#b91c1c", label="robust objective")
    axes[1].set_xlabel("repair progress")
    axes[1].set_ylabel("objective value")
    axes[1].legend(frameon=False)
    save(fig, "basis_uncertainty_geometry.pdf")


def local_repair_geometry():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.0))
    axes[0].set_title("Local head neighborhood")
    circle = plt.Circle((0, 0), 1.0, fc="#e0f2fe", ec="black", lw=1.5)
    axes[0].add_patch(circle)
    axes[0].scatter([0], [0], s=70, color="#1d4ed8", label="anchor head")
    axes[0].scatter([0.45], [0.25], s=70, color="#dc2626", label="repaired head")
    axes[0].arrow(0, 0, 0.38, 0.22, width=0.02, color="#374151", length_includes_head=True)
    axes[0].text(-0.95, 0.88, "allowed local\nrepair set", fontsize=11)
    axes[0].set_xlim(-1.2, 1.2)
    axes[0].set_ylim(-1.2, 1.2)
    axes[0].set_aspect("equal")
    axes[0].legend(frameon=False, loc="lower right")

    axes[1].set_title("Decision-boundary correction")
    xs = np.linspace(-3, 3, 300)
    ys1 = 0.45 * xs + 0.35
    ys2 = 0.45 * xs - 0.1
    axes[1].fill_between(xs, ys1, 3.2, color="#dbeafe", alpha=0.6)
    axes[1].fill_between(xs, -3.2, ys1, color="#fde68a", alpha=0.6)
    axes[1].plot(xs, ys1, color="#1d4ed8", lw=2.4, label="anchor boundary")
    axes[1].plot(xs, ys2, color="#dc2626", lw=2.4, label="repaired boundary")
    hard = np.array([[-1.4, -1.0], [-0.8, -0.3], [0.2, 0.1], [1.0, 0.45]])
    axes[1].scatter(hard[:, 0], hard[:, 1], s=60, color="black", marker="x", label="hard latent mode")
    axes[1].legend(frameon=False, loc="upper left")
    axes[1].set_xlim(-3, 3)
    axes[1].set_ylim(-2.2, 2.2)
    axes[1].set_xlabel("feature 1")
    axes[1].set_ylabel("feature 2")
    save(fig, "local_repair_geometry.pdf")


def crossfit_protocol():
    fig, ax = plt.subplots(figsize=(10.5, 2.8))
    ax.axis("off")
    widths = [0.22, 0.22, 0.22, 0.22]
    labels = [
        ("selection", "#dbeafe"),
        ("basis discovery", "#fde68a"),
        ("head repair", "#dcfce7"),
        ("validation", "#fee2e2"),
    ]
    x = 0.04
    for (label, color), w in zip(labels, widths):
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, 0.3),
                w,
                0.4,
                boxstyle="round,pad=0.02,rounding_size=0.02",
                fc=color,
                ec="black",
                lw=1.3,
            )
        )
        ax.text(x + w / 2, 0.5, label, ha="center", va="center", fontsize=12)
        x += w + 0.02
    ax.text(0.5, 0.12, "One source holdout, four disjoint roles, no adaptive recycling of the same examples.", ha="center", fontsize=11.5)
    save(fig, "crossfit_protocol.pdf")


def risk_certificate():
    fig, ax = plt.subplots(figsize=(8.8, 3.6))
    ax.axis("off")
    boxes = [
        (0.04, 0.25, 0.24, 0.5, "#dbeafe", "source-supported\ntarget shift"),
        (0.38, 0.25, 0.26, 0.5, "#fde68a", "trajectory-basis\nuncertainty family"),
        (0.74, 0.25, 0.22, 0.5, "#dcfce7", "local robust\nhead repair"),
    ]
    for x, y, w, h, c, txt in boxes:
        ax.add_patch(
            patches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.03",
                fc=c,
                ec="black",
                lw=1.4,
            )
        )
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=12)
    ax.annotate("", xy=(0.38, 0.5), xytext=(0.28, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(0.74, 0.5), xytext=(0.64, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(
        0.5,
        0.07,
        "target risk <= best robust local repair + generalization error + basis recovery error",
        ha="center",
        fontsize=12.5,
    )
    save(fig, "risk_certificate.pdf")


def main():
    tribe_overview()
    trajectory_basis_pipeline()
    basis_uncertainty_geometry()
    local_repair_geometry()
    crossfit_protocol()
    risk_certificate()


if __name__ == "__main__":
    main()
