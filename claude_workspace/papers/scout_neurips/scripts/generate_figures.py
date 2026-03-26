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


def scout_overview():
    fig, ax = plt.subplots(figsize=(10.5, 3.6))
    ax.axis("off")
    boxes = [
        (0.02, 0.25, 0.18, 0.5, "#dbeafe", "Dense trajectory\ncheckpoints"),
        (0.25, 0.25, 0.18, 0.5, "#dcfce7", "Low-loss +\nbarrier-filtered\ncandidate pool"),
        (0.48, 0.25, 0.22, 0.5, "#fef3c7", "KL-ball DRO over\nhard source-example\nreweightings"),
        (0.75, 0.25, 0.21, 0.5, "#fee2e2", "Single weighted soup\nin convex hull of\nuniform $M$-subsets"),
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
                lw=1.5,
            )
        )
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=12)
    for x1, x2 in [(0.20, 0.25), (0.43, 0.48), (0.70, 0.75)]:
        ax.annotate(
            "",
            xy=(x2, 0.5),
            xytext=(x1, 0.5),
            arrowprops=dict(arrowstyle="->", lw=2),
        )
    ax.text(
        0.5,
        0.08,
        "Theory object = algorithm object: robust coverage of hard examples inside a soup-safe trajectory region",
        ha="center",
        va="center",
        fontsize=12,
    )
    save(fig, "scout_overview.pdf")


def uncertainty_set():
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.set_title("Example-Reweighting Uncertainty Set", fontsize=13)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("$r_1$")
    ax.set_ylabel("$r_2$")
    tri = np.array([[0, 0], [1, 0], [0, 1], [0, 0]])
    ax.plot(tri[:, 0], tri[:, 1], color="black", lw=1.5)
    theta = np.linspace(0, 2 * np.pi, 400)
    x = 1 / 3 + 0.18 * np.cos(theta)
    y = 1 / 3 + 0.12 * np.sin(theta)
    ax.fill(x, y, color="#dbeafe", alpha=0.8, label="KL-ball around uniform")
    ax.scatter([1 / 3], [1 / 3], color="black", s=30, zorder=3)
    ax.text(0.36, 0.34, "$u_n$", fontsize=11)
    ax.text(0.62, 0.68, "hard-example\nreweightings", fontsize=11, ha="center")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "uncertainty_set.pdf")


def hypersimplex():
    fig, ax = plt.subplots(figsize=(6.0, 4.6))
    ax.set_title("Convex Hull of Uniform $M$-Subsets", fontsize=13)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlabel("$w_1$")
    ax.set_ylabel("$w_2$")
    tri = np.array([[0, 0], [1, 0], [0, 1], [0, 0]])
    ax.plot(tri[:, 0], tri[:, 1], color="black", lw=1.5)
    poly = np.array([[0.5, 0.0], [0.5, 0.5], [0.0, 0.5], [0.0, 0.0], [0.5, 0.0]])
    ax.fill(poly[:, 0], poly[:, 1], color="#dcfce7", alpha=0.85, label="$\\mathcal{W}_2$")
    verts = np.array([[0.5, 0.5], [0.5, 0.0], [0.0, 0.5]])
    ax.scatter(verts[:, 0], verts[:, 1], color="#1d4ed8", s=55, zorder=3)
    for x, y, t in [(0.5, 0.5, "$u_{\\{1,2\\}}$"), (0.5, 0.0, "$u_{\\{1,3\\}}$"), (0.0, 0.5, "$u_{\\{2,3\\}}$")]:
        ax.text(x + 0.03, y + 0.03, t, fontsize=10)
    ax.legend(frameon=False, loc="upper right")
    save(fig, "hypersimplex_uniform_subsets.pdf")


def diminishing_returns():
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.8))
    c = np.linspace(0.02, 1.5, 300)
    a_small = 0.12
    a_large = 0.55
    axes[0].plot(c, np.log(1 + a_small / c), lw=2.2, label="small unique gain")
    axes[0].plot(c, np.log(1 + a_large / c), lw=2.2, label="large unique gain")
    axes[0].set_title("Marginal Coverage Gain")
    axes[0].set_xlabel("current example coverage")
    axes[0].set_ylabel("$\\log(1 + a/c)$")
    axes[0].legend(frameon=False)

    overlap = np.linspace(0.0, 1.0, 300)
    penalty = 0.4 * overlap**2 + 0.15 * overlap
    axes[1].plot(overlap, penalty, color="#b91c1c", lw=2.2)
    axes[1].set_title("Second-Order Redundancy Penalty")
    axes[1].set_xlabel("overlap with already-covered examples")
    axes[1].set_ylabel("approximate penalty")
    save(fig, "diminishing_returns_vs_redundancy.pdf")


def noncontiguous_toy():
    fig, ax = plt.subplots(figsize=(9.0, 3.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel("training time")
    steps = [0.8, 1.8, 3.0, 4.1, 5.2, 6.3, 7.5, 8.7]
    colors = ["#93c5fd", "#93c5fd", "#cbd5e1", "#cbd5e1", "#cbd5e1", "#fca5a5", "#fca5a5", "#cbd5e1"]
    labels = ["covers A", "covers A", "redundant", "redundant", "redundant", "covers B", "covers B", "late redundant"]
    for s, c, l in zip(steps, colors, labels):
        ax.scatter([s], [0.5], s=180, color=c, edgecolor="black", zorder=3)
        ax.text(s, 0.68, l, ha="center", fontsize=9)
    ax.plot([steps[0], steps[5]], [0.5, 0.5], color="#16a34a", lw=3, label="SCOUT-style complementary pair")
    ax.plot([steps[2], steps[4]], [0.32, 0.32], color="#ef4444", lw=3, label="contiguous valley-only choice")
    ax.legend(frameon=False, loc="upper center", ncol=2)
    ax.set_title("Why Noncontiguous Complementarity Can Beat a Contiguous Window", fontsize=13)
    save(fig, "noncontiguous_complementarity_toy.pdf")


def soup_transfer():
    fig, ax = plt.subplots(figsize=(8.6, 3.4))
    ax.axis("off")
    items = [
        (0.03, 0.2, 0.23, 0.58, "#dbeafe", "candidate set\n$\\mathcal{C}$"),
        (0.39, 0.2, 0.23, 0.58, "#fde68a", "predictive mixture\ncertificate"),
        (0.75, 0.2, 0.22, 0.58, "#dcfce7", "single weight soup\n$\\theta_{\\mathrm{SCOUT}}$"),
    ]
    for x, y, w, h, c, txt in items:
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
    ax.annotate("", xy=(0.39, 0.5), xytext=(0.26, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(0.75, 0.5), xytext=(0.62, 0.5), arrowprops=dict(arrowstyle="->", lw=2))
    ax.text(0.505, 0.78, "locality assumption", ha="center", fontsize=11)
    ax.text(0.505, 0.1, "$R_T(\\theta_{\\mathrm{SCOUT}}) \\leq U_\\rho(w^\\star) + \\delta_{\\mathrm{loc}}$", ha="center", fontsize=12)
    save(fig, "soup_transfer_bridge.pdf")


def surrogate_link():
    fig, ax = plt.subplots(figsize=(8.6, 3.6))
    ax.axis("off")
    ax.text(0.5, 0.88, "SCOUT objective around current coverage state $c_i(S)$", ha="center", fontsize=13)
    ax.text(
        0.5,
        0.58,
        r"$\Delta_t(S)=\sum_i r_i \log\!\left(1+\frac{a_{it}}{c_i(S)}\right)"
        r"\approx \sum_i r_i \frac{a_{it}}{c_i(S)} - \frac{1}{2}\sum_i r_i \frac{a_{it}^2}{c_i(S)^2}$",
        ha="center",
        fontsize=14,
    )
    ax.text(0.27, 0.28, "reward unique gain\non hard examples", ha="center", fontsize=12)
    ax.text(0.73, 0.28, "penalize redundant overlap\nwith already-covered examples", ha="center", fontsize=12)
    ax.annotate("", xy=(0.36, 0.43), xytext=(0.27, 0.33), arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.annotate("", xy=(0.64, 0.43), xytext=(0.73, 0.33), arrowprops=dict(arrowstyle="->", lw=1.8))
    save(fig, "surrogate_link_to_dcola.pdf")


def main():
    scout_overview()
    uncertainty_set()
    hypersimplex()
    diminishing_returns()
    noncontiguous_toy()
    soup_transfer()
    surrogate_link()


if __name__ == "__main__":
    main()
