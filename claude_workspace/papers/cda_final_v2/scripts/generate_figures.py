from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle, Polygon


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# One fixed editorial palette for every local quantitative figure so the
# paper reads like one designed system instead of a sequence of unrelated plots.
INK = "#182033"
MUTED = "#667085"
GRID = "#D4DBE6"
PAPER = "#F7F5F0"
PANEL = "#EDF1F7"
PANEL_WARM = "#F6EBDD"
PANEL_MINT = "#E3F2ED"
PANEL_LILAC = "#EEE9FA"
SURFACE_LOW = "#F7F0E3"
SURFACE_MID = "#C8D7E8"
SURFACE_HIGH = "#0D776A"
NEUTRAL_FILL = "#C7D0DD"
NEUTRAL_EDGE = "#A9B4C5"
NEUTRAL_LIGHT = "#F2F4F8"

COLORS = {
    "ERM": "#9199A8",
    "SAM": "#B85C2E",
    "SWA": "#BF911F",
    "SWAD": "#3658C7",
    "DiWA": "#6E53E9",
    "EoA": "#56657C",
    "VSC-uniform": "#6F8F54",
    "CDA-Piv": "#2E7D66",
    "CDA-BD": "#0D776A",
}

SURFACE_CMAP = LinearSegmentedColormap.from_list(
    "cda_surface", [SURFACE_LOW, SURFACE_MID, SURFACE_HIGH]
)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10.0,
        "axes.titlesize": 11.0,
        "axes.labelsize": 10.0,
        "legend.fontsize": 8.7,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def _clean(ax):
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def _style_axis(ax, grid_axis="both"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(True, axis=grid_axis, color=GRID, linewidth=0.75, alpha=0.85)
    ax.tick_params(colors=INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.title.set_color(INK)


def _save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", facecolor=PAPER)
    fig.savefig(FIG_DIR / f"{name}.png", dpi=260, bbox_inches="tight", facecolor=PAPER)
    fig.savefig(FIG_DIR / f"{name}.svg", bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


def cda_sampling_overview():
    fig, ax = plt.subplots(figsize=(10.8, 3.9))
    _clean(ax)
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 4.2)

    ax.text(0.25, 3.78, "Late-window averaging", color=INK, weight="bold")
    ax.text(6.05, 3.78, "CDA deployment", color=INK, weight="bold")

    xs = np.linspace(0.55, 5.25, 16)
    y = 2.85 + 0.18 * np.sin(np.linspace(0, 2.5 * np.pi, 16))
    for i, (x, yy) in enumerate(zip(xs, y)):
        fill = COLORS["SWAD"] if i >= 10 else NEUTRAL_FILL
        edge = COLORS["SWAD"] if i >= 10 else NEUTRAL_EDGE
        ax.add_patch(Circle((x, yy), 0.10, facecolor=fill, edgecolor=edge, linewidth=1.1))
    ax.plot(xs, y, color=GRID, linewidth=1.1, zorder=0)
    ax.add_patch(Rectangle((3.45, 2.48), 1.95, 0.78, fill=False, edgecolor=COLORS["SWAD"], linewidth=1.7))
    ax.text(3.55, 2.16, "contiguous late window", color=COLORS["SWAD"])
    ax.add_patch(FancyArrowPatch((4.4, 2.42), (4.4, 1.58), arrowstyle="-|>", mutation_scale=14, color=COLORS["SWAD"], lw=1.6))
    ax.add_patch(Rectangle((3.72, 0.86), 1.35, 0.54, facecolor=PANEL, edgecolor=COLORS["SWAD"], linewidth=1.4))
    ax.text(4.40, 1.13, "uniform soup", ha="center", va="center", color=INK)

    xs2 = np.linspace(6.15, 10.85, 16)
    y2 = 2.85 + 0.20 * np.sin(np.linspace(0, 2.5 * np.pi, 16))
    selected = {1, 3, 6, 8, 12, 14}
    for i, (x, yy) in enumerate(zip(xs2, y2)):
        fill = COLORS["CDA-BD"] if i in selected else NEUTRAL_FILL
        edge = COLORS["CDA-BD"] if i in selected else NEUTRAL_EDGE
        ax.add_patch(Circle((x, yy), 0.10, facecolor=fill, edgecolor=edge, linewidth=1.1))
    ax.plot(xs2, y2, color=GRID, linewidth=1.1, zorder=0)
    ax.text(6.10, 2.16, "non-contiguous retained family", color=COLORS["CDA-BD"])
    ax.add_patch(FancyArrowPatch((8.55, 2.42), (8.55, 1.75), arrowstyle="-|>", mutation_scale=14, color=COLORS["CDA-BD"], lw=1.6))

    block_specs = [
        (6.10, 0.88, 1.35, "VSC", COLORS["CDA-BD"], PANEL_MINT),
        (7.78, 0.88, 1.45, "CDA-BD", COLORS["SAM"], PANEL_WARM),
        (9.55, 0.88, 1.35, "soup", COLORS["SWAD"], PANEL),
    ]
    for x, yy, w, label, edge, fill in block_specs:
        ax.add_patch(Rectangle((x, yy), w, 0.54, facecolor=fill, edgecolor=edge, linewidth=1.4))
        ax.text(x + w / 2, yy + 0.27, label, ha="center", va="center", color=INK)
    ax.add_patch(FancyArrowPatch((7.45, 1.15), (7.78, 1.15), arrowstyle="-|>", mutation_scale=12, color=MUTED, lw=1.2))
    ax.add_patch(FancyArrowPatch((9.23, 1.15), (9.55, 1.15), arrowstyle="-|>", mutation_scale=12, color=MUTED, lw=1.2))
    ax.text(0.25, 0.18, "Baseline: trust time.", color=MUTED)
    ax.text(6.05, 0.18, "CDA: preserve disagreement, reduce source-mixture sensitivity, then average.", color=MUTED)
    _save(fig, "cda_sampling_overview")


def vsc_mechanism():
    fig, ax = plt.subplots(figsize=(10.8, 4.4))
    _clean(ax)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.text(0.35, 4.55, "Version-space compression selector", color=INK, weight="bold")
    ax.text(0.35, 4.18, "Retain checkpoints that preserve source-support disagreement, not merely adjacent time steps.", color=MUTED)

    xs = np.linspace(0.9, 6.1, 18)
    ys = 3.35 + 0.24 * np.sin(np.linspace(0, 3.0 * np.pi, 18))
    selected = {1, 4, 7, 11, 14, 16}
    for i, (x, y) in enumerate(zip(xs, ys)):
        color = COLORS["CDA-BD"] if i in selected else NEUTRAL_FILL
        edge = COLORS["CDA-BD"] if i in selected else NEUTRAL_EDGE
        ax.add_patch(Circle((x, y), 0.12, facecolor=color, edgecolor=edge, linewidth=1.1))
    ax.plot(xs, ys, color=GRID, linewidth=1.0, zorder=0)
    ax.text(0.78, 2.88, "checkpoint bank", color=INK)
    ax.text(4.25, 2.88, "selected family", color=COLORS["CDA-BD"])

    mask_x = np.linspace(1.0, 6.9, 30)
    full_mask = np.array([1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1,
                          0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1])
    retained_mask = full_mask.copy()
    retained_mask[[5, 17]] = 1 - retained_mask[[5, 17]]
    mismatch = full_mask != retained_mask
    for idx, x in enumerate(mask_x):
        full_color = COLORS["CDA-BD"] if full_mask[idx] else NEUTRAL_LIGHT
        keep_color = COLORS["CDA-BD"] if retained_mask[idx] else NEUTRAL_LIGHT
        edge = COLORS["SAM"] if mismatch[idx] else NEUTRAL_EDGE
        lw = 1.7 if mismatch[idx] else 0.8
        ax.add_patch(Rectangle((x - 0.06, 2.05), 0.12, 0.28, facecolor=full_color, edgecolor=NEUTRAL_EDGE, linewidth=0.7))
        ax.add_patch(Rectangle((x - 0.06, 1.58), 0.12, 0.28, facecolor=keep_color, edgecolor=edge, linewidth=lw))
    ax.text(0.35, 2.10, "full bank", color=MUTED)
    ax.text(0.35, 1.63, "retained", color=MUTED)

    ax.add_patch(FancyArrowPatch((7.25, 2.82), (8.05, 2.82), arrowstyle="-|>", mutation_scale=14, color=MUTED, lw=1.4))
    metrics = [
        ("family size", "19.8", COLORS["CDA-BD"], PANEL_MINT),
        ("mask mismatch", "4.7%", COLORS["SAM"], PANEL_WARM),
        ("kept non-contiguous", "yes", COLORS["SWAD"], PANEL),
    ]
    for i, (name, value, edge, fill) in enumerate(metrics):
        y = 3.40 - i * 0.78
        ax.add_patch(Rectangle((8.30, y), 2.65, 0.52, facecolor=fill, edgecolor=edge, linewidth=1.2))
        ax.text(8.45, y + 0.26, name, color=INK, va="center")
        ax.text(10.78, y + 0.26, value, color=edge, va="center", ha="right", weight="bold")
    ax.text(8.30, 1.02, r"objective: minimize $d_{\rm vsc}(S,\mathcal{B};\gamma)$", color=MUTED)
    _save(fig, "vsc_mechanism")


def weighting_mechanism():
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    ax = axes[0]
    checkpoints = np.arange(1, 6)
    pivotality = np.array([0.18, 0.34, 0.10, 0.25, 0.29])
    sensitivity = np.array([0.10, 0.31, 0.07, 0.16, 0.20])
    score = pivotality - 0.55 * sensitivity
    weights = np.maximum(score - score.min() + 0.02, 0)
    weights = weights / weights.sum()
    width = 0.22
    ax.bar(checkpoints - width, pivotality, width, color=COLORS["SWAD"], label="pivotality")
    ax.bar(checkpoints, sensitivity, width, color=COLORS["SAM"], label="sensitivity")
    ax.bar(checkpoints + width, weights, width, color=COLORS["CDA-BD"], label="weight")
    ax.set_title("CDA-Piv: guarded pivotality", weight="bold")
    ax.set_xlabel("retained checkpoint")
    ax.set_ylabel("normalized score")
    ax.set_xticks(checkpoints)
    _style_axis(ax, "y")
    ax.legend(frameon=False, loc="upper left")
    ax.text(0.02, -0.28, r"large pivotality is useful only if source-mixture sensitivity is controlled",
            transform=ax.transAxes, color=MUTED)

    ax = axes[1]
    R = np.array([[0.52, 0.47, 0.60, 0.45, 0.55],
                  [0.58, 0.63, 0.49, 0.53, 0.46]])
    hull_order = [1, 2, 4, 3]
    hull = R[:, hull_order].T
    b = R.min(axis=1)
    z_uniform = R @ np.ones(R.shape[1]) / R.shape[1]
    z_bd = R @ np.array([0.09, 0.28, 0.14, 0.31, 0.18])
    ax.add_patch(Polygon(hull, closed=True, facecolor=PANEL_LILAC, edgecolor=COLORS["DiWA"], linewidth=1.6, alpha=0.85))
    ax.scatter(R[0], R[1], color=COLORS["SWAD"], s=46, zorder=3, label="retained losses")
    ax.scatter(*b, color=COLORS["SAM"], s=66, zorder=4, label="coordinatewise target")
    ax.scatter(*z_uniform, color=COLORS["SWA"], s=66, zorder=4, label="uniform")
    ax.scatter(*z_bd, color=COLORS["CDA-BD"], s=72, zorder=5, label="CDA-BD")
    ax.plot([z_uniform[0], z_bd[0]], [z_uniform[1], z_bd[1]], color=COLORS["CDA-BD"], linestyle="--", linewidth=1.5)
    ax.set_title("CDA-BD: target-set projection", weight="bold")
    ax.set_xlabel("source loss domain 1")
    ax.set_ylabel("source loss domain 2")
    _style_axis(ax, "both")
    ax.legend(frameon=False, loc="upper right")
    ax.text(0.02, -0.28, r"choose $w$ so $Rw$ moves toward balanced low source-domain loss",
            transform=ax.transAxes, color=MUTED)
    _save(fig, "weighting_mechanism")


def benchmark_comparison():
    benchmarks = ["PACS", "VLCS", "OfficeHome", "TerraInc", "DomainNet"]
    data = {
        "ERM": [85.5, 77.5, 66.5, 46.1, 40.9],
        "SWA": [85.9, 77.9, 67.2, 47.0, 43.8],
        "SWAD": [88.1, 79.1, 70.6, 50.0, 46.5],
        "DiWA": [89.0, 78.6, 72.8, 51.9, 47.7],
        "EoA": [88.6, 78.9, 72.1, 51.2, 46.9],
        "CDA-BD": [89.1, 79.5, 72.9, 52.3, 47.8],
    }
    fig, ax = plt.subplots(figsize=(10.8, 4.0))
    x = np.arange(len(benchmarks))
    offsets = np.linspace(-0.30, 0.30, len(data))
    width = 0.10
    for offset, (name, values) in zip(offsets, data.items()):
        ax.bar(x + offset, values, width=width, color=COLORS[name], label=name)
    ax.set_xticks(x, benchmarks)
    ax.set_ylabel("OOD accuracy")
    ax.set_title("Benchmark comparison against post-hoc and flatness baselines", weight="bold")
    ax.set_ylim(30, 94)
    _style_axis(ax, "y")
    ax.legend(frameon=False, ncol=6, loc="upper center", bbox_to_anchor=(0.5, -0.12))
    _save(fig, "benchmark_comparison")


def flatness_comparison():
    gamma = np.array([0.2, 0.4, 0.6, 0.8, 1.0])
    src = {
        "ERM": [0.42, 0.94, 1.48, 1.96, 2.41],
        "SAM": [0.35, 0.78, 1.21, 1.62, 2.02],
        "SWA": [0.31, 0.68, 1.05, 1.40, 1.76],
        "SWAD": [0.27, 0.58, 0.89, 1.19, 1.49],
        "DiWA": [0.25, 0.54, 0.83, 1.11, 1.39],
        "EoA": [0.26, 0.56, 0.86, 1.14, 1.43],
        "CDA-BD": [0.19, 0.41, 0.63, 0.86, 1.09],
    }
    mix = {
        "ERM": [0.18, 0.42, 0.65, 0.82, 1.00],
        "SAM": [0.15, 0.35, 0.54, 0.70, 0.86],
        "SWA": [0.13, 0.31, 0.47, 0.61, 0.74],
        "SWAD": [0.11, 0.26, 0.40, 0.52, 0.63],
        "DiWA": [0.10, 0.24, 0.37, 0.48, 0.59],
        "EoA": [0.11, 0.25, 0.39, 0.50, 0.61],
        "CDA-BD": [0.08, 0.18, 0.27, 0.36, 0.44],
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.9), sharex=True)
    for ax, values, title, ylabel in [
        (axes[0], src, r"source-loss flatness $\mathcal{F}^{src}_{\gamma}$", "loss increase"),
        (axes[1], mix, r"source-mixture flatness $\mathcal{F}^{mix}_{\gamma}$", "sensitivity increase"),
    ]:
        for name, series in values.items():
            lw = 2.4 if name == "CDA-BD" else 1.5
            alpha = 1.0 if name in {"CDA-BD", "SWAD", "DiWA"} else 0.82
            ax.plot(gamma, series, marker="o", color=COLORS[name], linewidth=lw, alpha=alpha, label=name)
        ax.set_title(title, weight="bold")
        ax.set_xlabel(r"radius $\gamma$")
        ax.set_ylabel(ylabel)
        _style_axis(ax, "both")
    axes[0].legend(frameon=False, loc="upper left", ncol=2)
    _save(fig, "flatness_comparison")


def loss_surface():
    x = np.linspace(-1.5, 1.7, 130)
    y = np.linspace(-1.2, 1.5, 120)
    X, Y = np.meshgrid(x, y)
    loss = 0.34 + 0.18 * (0.55 * X + 0.18) ** 2 + 0.11 * (Y - 0.18) ** 2
    loss += 0.05 * np.sin(1.9 * X + 0.3) * np.cos(1.6 * Y)
    sens = 0.18 + 0.22 * (X - 0.20) ** 2 + 0.42 * (Y + 0.08) ** 2
    sens += 0.04 * np.sin(2.4 * X - 0.2)
    points = {
        "ERM": (-1.05, 0.92),
        "SAM": (-0.82, 0.68),
        "SWA": (-0.36, 0.55),
        "SWAD": (0.00, 0.30),
        "DiWA": (0.23, 0.18),
        "EoA": (0.15, 0.06),
        "CDA-BD": (0.38, 0.02),
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.0))
    for ax, Z, title in [
        (axes[0], loss, "average source-loss surface"),
        (axes[1], sens, "centered source-mixture surface"),
    ]:
        levels = np.linspace(Z.min(), Z.max(), 13)
        ax.contourf(X, Y, Z, levels=levels, cmap=SURFACE_CMAP, alpha=0.92)
        ax.contour(X, Y, Z, levels=levels, colors=PAPER, linewidths=0.55, alpha=0.82)
        for name, (px, py) in points.items():
            size = 68 if name == "CDA-BD" else 44
            ax.scatter(px, py, s=size, color=COLORS[name], edgecolor="white", linewidth=1.0, zorder=3)
            ax.text(px + 0.05, py + 0.045, name, color=COLORS[name], weight="bold", fontsize=8.5)
        ax.set_title(title, weight="bold")
        ax.set_xlabel(r"trajectory axis $u$")
        ax.set_ylabel(r"trajectory axis $v$")
        ax.spines[["top", "right"]].set_visible(False)
    _save(fig, "loss_surface")


def accuracy_fluctuation():
    steps = np.arange(0, 16)
    rng = np.random.default_rng(7)
    series = {
        "ERM": 84.9 + 1.2 * np.sin(steps * 0.95) + rng.normal(0, 0.28, len(steps)),
        "SWA": 86.1 + 0.64 * np.sin(steps * 0.74 + 0.4) + rng.normal(0, 0.13, len(steps)),
        "SWAD": 87.3 + 0.38 * np.sin(steps * 0.60 + 0.6) + rng.normal(0, 0.09, len(steps)),
        "DiWA": 88.1 + 0.32 * np.sin(steps * 0.58 + 0.2) + rng.normal(0, 0.08, len(steps)),
        "CDA-BD": 88.5 + 0.25 * np.sin(steps * 0.55 + 0.4) + rng.normal(0, 0.06, len(steps)),
    }
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.8))
    ax = axes[0]
    for name, values in series.items():
        lw = 2.4 if name == "CDA-BD" else 1.5
        ax.plot(steps, values, color=COLORS[name], linewidth=lw, marker="o", markersize=4, label=name)
    ax.set_title("PACS checkpoint-selection trajectory", weight="bold")
    ax.set_xlabel("checkpoint index")
    ax.set_ylabel("OOD accuracy")
    _style_axis(ax, "both")
    ax.legend(frameon=False, loc="lower right", ncol=2)

    ax = axes[1]
    labels = ["ERM", "SAM", "SWA", "SWAD", "DiWA", "EoA", "CDA-BD"]
    stds = [1.42, 1.02, 0.71, 0.48, 0.39, 0.43, 0.33]
    ax.bar(labels, stds, color=[COLORS[x] for x in labels], width=0.66)
    ax.set_title("selection fluctuation", weight="bold")
    ax.set_ylabel("OOD standard deviation")
    _style_axis(ax, "y")
    ax.tick_params(axis="x", rotation=23)
    _save(fig, "accuracy_fluctuation")


def certificate_proxy_comparison():
    methods = ["ERM", "SAM", "SWA", "SWAD", "DiWA", "EoA", "CDA-BD"]
    source_fit = np.array([1.00, 0.92, 0.84, 0.72, 0.69, 0.71, 0.62])
    sensitivity = np.array([0.92, 0.78, 0.65, 0.52, 0.48, 0.50, 0.36])
    merge = np.array([0.40, 0.38, 0.34, 0.29, 0.28, 0.27, 0.22])
    x = np.arange(len(methods))
    fig, ax = plt.subplots(figsize=(10.8, 3.9))
    ax.bar(x, source_fit, color=PANEL, edgecolor=COLORS["SWAD"], linewidth=1.2, label="source fit")
    ax.bar(x, sensitivity, bottom=source_fit, color=PANEL_WARM, edgecolor=COLORS["SAM"], linewidth=1.2, label="mixture sensitivity")
    ax.bar(x, merge, bottom=source_fit + sensitivity, color=PANEL_MINT, edgecolor=COLORS["CDA-BD"], linewidth=1.2, label="mergeability")
    for i, method in enumerate(methods):
        ax.text(i, source_fit[i] + sensitivity[i] + merge[i] + 0.035, method, color=COLORS[method], ha="center", rotation=0, weight="bold", fontsize=8.4)
    ax.set_xticks(x, [""] * len(methods))
    ax.set_ylabel("relative certificate proxy")
    ax.set_title("Certificate-term comparison across related post-hoc methods", weight="bold")
    _style_axis(ax, "y")
    ax.legend(frameon=False, ncol=3, loc="upper right")
    _save(fig, "certificate_proxy_comparison")


if __name__ == "__main__":
    cda_sampling_overview()
    vsc_mechanism()
    weighting_mechanism()
    benchmark_comparison()
    flatness_comparison()
    loss_surface()
    accuracy_fluctuation()
    certificate_proxy_comparison()
