from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def save(fig, name: str) -> None:
    fig.savefig(FIG_DIR / name, bbox_inches="tight")
    plt.close(fig)


def cora_overview() -> None:
    fig, ax = plt.subplots(figsize=(11.5, 3.8))
    ax.axis("off")
    colors = {
        "traj": "#4c78a8",
        "set": "#f58518",
        "bary": "#54a24b",
        "opt": "#e45756",
        "out": "#72b7b2",
    }

    boxes = [
        (0.02, 0.25, 0.17, 0.5, "Dense\ntrajectory", colors["traj"]),
        (0.23, 0.25, 0.19, 0.5, "Connected near-optimal\nRashomon set", colors["set"]),
        (0.47, 0.25, 0.18, 0.5, "Barycenter +\nmultiplicity core", colors["bary"]),
        (0.70, 0.25, 0.16, 0.5, "Convex simplex\noptimization", colors["opt"]),
        (0.90, 0.25, 0.08, 0.5, "Single\nsoup", colors["out"]),
    ]
    for x, y, w, h, txt, c in boxes:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.02,rounding_size=0.03",
                linewidth=1.5,
                edgecolor=c,
                facecolor=c,
                alpha=0.17,
            )
        )
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=13)

    for i in range(len(boxes) - 1):
        x1 = boxes[i][0] + boxes[i][2]
        x2 = boxes[i + 1][0]
        ax.annotate(
            "",
            xy=(x2 - 0.01, 0.5),
            xytext=(x1 + 0.01, 0.5),
            arrowprops=dict(arrowstyle="->", lw=2),
        )

    ax.text(
        0.5,
        0.93,
        "CORA changes the object from flatness/window choice to consensus structure inside the connected good-model set",
        ha="center",
        va="center",
        fontsize=14,
    )
    ax.text(0.02, 0.05, "No domain labels. One training run. One post-hoc pass. One test-time model.", fontsize=12)
    save(fig, "cora_overview.pdf")


def connected_rashomon_set() -> None:
    t = np.arange(0, 61)
    val = 0.45 - 0.28 * np.exp(-((t - 14) / 9) ** 2) - 0.24 * np.exp(-((t - 45) / 12) ** 2) + 0.03 * np.sin(t / 3)
    val = val - val.min() + 0.08
    barrier = 0.015 + 0.03 * np.exp(-((t - 25) / 6) ** 2) + 0.02 * np.exp(-((t - 57) / 4) ** 2)

    feasible = (val <= val.min() + 0.09) & (barrier <= 0.028)
    swad_mask = (t >= 38) & (t <= 52)
    anchor = int(np.argmin(val))

    fig, ax1 = plt.subplots(figsize=(11, 4.2))
    ax2 = ax1.twinx()
    ax1.plot(t, val, color="#4c78a8", lw=2.5, label=r"$L_{\mathcal{V}}(\theta_t)$")
    ax2.plot(t, barrier, color="#e45756", lw=2.0, ls="--", label=r"$B(t,a)$")

    ax1.scatter(t[feasible], val[feasible], color="#f58518", s=46, label=r"$t \in \mathcal{C}$", zorder=5)
    ax1.scatter([anchor], [val[anchor]], color="#54a24b", s=90, marker="*", label="anchor", zorder=6)
    ax1.fill_between(t, val.min() - 0.02, val.max() + 0.02, where=swad_mask, color="#72b7b2", alpha=0.12, label="typical SWAD interval")

    ax1.set_xlabel("Checkpoint index")
    ax1.set_ylabel("Pooled validation loss")
    ax2.set_ylabel("Interpolation barrier")
    ax1.set_title("Connected near-optimal checkpoints need not form one contiguous late window")

    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper right", fontsize=10)
    save(fig, "connected_rashomon_set.pdf")


def consensus_core_heatmap() -> None:
    rng = np.random.default_rng(0)
    n_ckpts = 12
    n_ex = 32
    heat = np.zeros((n_ckpts, n_ex))

    for j in range(n_ex):
        if j < 18:
            base = 0.86 + 0.03 * rng.standard_normal()
            heat[:, j] = np.clip(base + 0.015 * rng.standard_normal(n_ckpts), 0.02, 0.98)
        else:
            pattern = np.linspace(0.1, 0.9, n_ckpts)
            rng.shuffle(pattern)
            heat[:, j] = np.clip(pattern + 0.04 * rng.standard_normal(n_ckpts), 0.02, 0.98)

    rho = np.array([0.08, 0.10, 0.09, 0.11, 0.12, 0.08, 0.07, 0.10, 0.08, 0.06, 0.05, 0.06])
    rho /= rho.sum()
    multiplicity = np.concatenate([np.linspace(0.01, 0.08, 18), np.linspace(0.14, 0.42, 14)])

    fig = plt.figure(figsize=(11, 5))
    gs = fig.add_gridspec(2, 2, width_ratios=[18, 1.2], height_ratios=[1.5, 6], hspace=0.15, wspace=0.08)

    ax_top = fig.add_subplot(gs[0, 0])
    ax = fig.add_subplot(gs[1, 0])
    ax_side = fig.add_subplot(gs[1, 1])

    ax_top.plot(np.arange(n_ex), multiplicity, color="#e45756", lw=2.2)
    ax_top.axvspan(-0.5, 17.5, color="#54a24b", alpha=0.10)
    ax_top.axvspan(17.5, n_ex - 0.5, color="#f58518", alpha=0.10)
    ax_top.text(6, multiplicity.max() * 0.92, "consensus core", color="#2f6f44", fontsize=11)
    ax_top.text(23, multiplicity.max() * 0.92, "disagreement fringe", color="#a85b00", fontsize=11)
    ax_top.set_ylabel(r"$M(x)$")
    ax_top.set_xticks([])
    ax_top.set_xlim(-0.5, n_ex - 0.5)

    im = ax.imshow(heat, aspect="auto", cmap="viridis", vmin=0.0, vmax=1.0)
    ax.set_xlabel("Support examples sorted by multiplicity")
    ax.set_ylabel("Candidate checkpoints")
    ax.set_title("Near-optimal checkpoints agree on a core and disagree on a fringe")

    ax_side.barh(np.arange(n_ckpts), rho, color="#4c78a8")
    ax_side.set_title(r"$\rho_t$", fontsize=10)
    ax_side.set_xticks([])
    ax_side.set_yticks([])

    cbar = fig.colorbar(im, ax=[ax, ax_side], fraction=0.025, pad=0.02)
    cbar.set_label("Predicted probability for one reference class")
    save(fig, "consensus_core_heatmap.pdf")


def barycenter_geometry() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Core example
    core = np.array([[0.88, 0.08], [0.86, 0.09], [0.89, 0.07], [0.87, 0.08], [0.90, 0.06]])
    q_core = core.mean(axis=0)
    cora_core = q_core + np.array([0.005, -0.005])
    swad_core = np.array([0.84, 0.10])
    stawa_core = np.array([0.91, 0.05])

    axes[0].scatter(core[:, 0], core[:, 1], color="#4c78a8", s=60, label="candidate checkpoints")
    axes[0].scatter(*q_core, color="#54a24b", marker="*", s=180, label="barycenter $q(x)$")
    axes[0].scatter(*cora_core, color="#f58518", marker="D", s=90, label="CORA soup")
    axes[0].scatter(*swad_core, color="#72b7b2", marker="s", s=70, label="SWAD-like soup")
    axes[0].scatter(*stawa_core, color="#e45756", marker="^", s=70, label="STAWA-like point")
    axes[0].set_title("Low-multiplicity core example")
    axes[0].set_xlabel(r"$p(y=1 \mid x)$")
    axes[0].set_ylabel(r"$p(y=2 \mid x)$")
    axes[0].set_xlim(0.75, 0.95)
    axes[0].set_ylim(0.0, 0.18)

    # Fringe example
    fringe = np.array([[0.94, 0.03], [0.73, 0.21], [0.18, 0.72], [0.08, 0.88], [0.52, 0.38]])
    q_fringe = fringe.mean(axis=0)
    cora_fringe = np.array([0.48, 0.42])
    swad_fringe = np.array([0.80, 0.13])
    stawa_fringe = np.array([0.95, 0.02])

    axes[1].scatter(fringe[:, 0], fringe[:, 1], color="#4c78a8", s=60)
    axes[1].scatter(*q_fringe, color="#54a24b", marker="*", s=180)
    axes[1].scatter(*cora_fringe, color="#f58518", marker="D", s=90)
    axes[1].scatter(*swad_fringe, color="#72b7b2", marker="s", s=70)
    axes[1].scatter(*stawa_fringe, color="#e45756", marker="^", s=70)
    axes[1].set_title("High-multiplicity fringe example")
    axes[1].set_xlabel(r"$p(y=1 \mid x)$")
    axes[1].set_ylabel(r"$p(y=2 \mid x)$")
    axes[1].set_xlim(0.0, 1.0)
    axes[1].set_ylim(0.0, 1.0)
    axes[1].legend(loc="lower left", fontsize=9)

    fig.suptitle("CORA targets the predictive center of the connected good-model set")
    save(fig, "barycenter_geometry.pdf")


def objective_decomposition() -> None:
    m = np.linspace(0.0, 0.45, 200)
    c = np.exp(-7.0 * m)
    core = c * (0.08 + 0.9 * m)
    amb = (1 - c) * (0.55 - 0.30 * np.exp(-8 * m))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    axes[0].plot(m, c, color="#54a24b", lw=2.4, label=r"$c(x)=e^{-\kappa M(x)}$")
    axes[0].plot(m, 1 - c, color="#e45756", lw=2.4, label=r"$1-c(x)$")
    axes[0].set_xlabel(r"Multiplicity $M(x)$")
    axes[0].set_ylabel("Weight")
    axes[0].set_title("Core and fringe weights")
    axes[0].legend()

    axes[1].fill_between(m, 0, core, color="#54a24b", alpha=0.25, label="core matching term")
    axes[1].fill_between(m, core, core + amb, color="#f58518", alpha=0.25, label="fringe ambiguity term")
    axes[1].plot(m, core, color="#2f6f44", lw=2.2)
    axes[1].plot(m, core + amb, color="#a85b00", lw=2.2)
    axes[1].set_xlabel(r"Multiplicity $M(x)$")
    axes[1].set_ylabel("Per-example objective contribution")
    axes[1].set_title("CORA matches the core and hedges on the fringe")
    axes[1].legend()

    save(fig, "objective_decomposition.pdf")


def method_contrast() -> None:
    t = np.arange(0, 50)
    loss = 0.32 - 0.18 * np.exp(-((t - 14) / 8) ** 2) - 0.14 * np.exp(-((t - 35) / 9) ** 2)
    loss = loss - loss.min() + 0.08
    drift = 0.09 + 0.04 * np.sin(t / 4) + 0.08 * np.exp(-((t - 10) / 6) ** 2)
    cov = 0.18 + 0.05 * np.cos(t / 7) + 0.02 * np.exp(-((t - 34) / 5) ** 2)
    mult = 0.10 + 0.08 * np.exp(-((t - 20) / 6) ** 2) + 0.03 * np.exp(-((t - 38) / 4) ** 2)

    fig, axes = plt.subplots(4, 1, figsize=(10.5, 8.5), sharex=True)
    axes[0].plot(t, loss, color="#4c78a8", lw=2.2)
    axes[0].axvspan(28, 42, color="#72b7b2", alpha=0.18)
    axes[0].set_ylabel("loss")
    axes[0].set_title("SWAD: contiguous low-loss late valley")

    axes[1].plot(t, drift, color="#e45756", lw=2.2)
    axes[1].scatter([13], [drift[13]], color="#e45756", s=70)
    axes[1].set_ylabel("drift")
    axes[1].set_title("STAWA: low checkpoint-level calmness")

    axes[2].plot(t, cov, color="#f58518", lw=2.2)
    dcola_steps = np.array([4, 6, 8, 11, 17, 18, 39, 40])
    axes[2].bar(dcola_steps, cov[dcola_steps], color="#f58518", alpha=0.35)
    axes[2].set_ylabel("global stat")
    axes[2].set_title("D-COLA: safe nonuniform soup from complementary checkpoints")

    axes[3].plot(t, mult, color="#54a24b", lw=2.2)
    axes[3].axvspan(3, 18, color="#54a24b", alpha=0.10)
    axes[3].axvspan(30, 40, color="#54a24b", alpha=0.10)
    axes[3].set_ylabel("multiplicity")
    axes[3].set_title("CORA: connected set plus examplewise consensus structure")
    axes[3].set_xlabel("Checkpoint index")

    fig.tight_layout()
    save(fig, "method_contrast.pdf")


if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    cora_overview()
    connected_rashomon_set()
    consensus_core_heatmap()
    barycenter_geometry()
    objective_decomposition()
    method_contrast()
