from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch, Polygon


ROOT = Path(__file__).resolve().parents[1]
OUTDIR = ROOT / "figures_mockups"

COLORS = {
    "ink": "#10202f",
    "muted": "#5d6b78",
    "grid": "#d7dee7",
    "erm": "#8e9aaf",
    "swad": "#9c6644",
    "diwa": "#577590",
    "uniform": "#adb5bd",
    "piv": "#005f73",
    "bd": "#ae2012",
    "ours": "#0a9396",
    "accent": "#ee9b00",
    "violet": "#6d597a",
    "green": "#588157",
}

HEATMAP = LinearSegmentedColormap.from_list(
    "paper_heat",
    ["#f8fafc", "#d9e8f5", "#9ecae1", "#3182bd", "#0b4f6c"],
)


def set_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 180,
            "savefig.dpi": 240,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": "#8894a0",
            "axes.linewidth": 0.8,
            "axes.facecolor": "#fbfdff",
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "grid.color": COLORS["grid"],
            "grid.alpha": 0.8,
            "grid.linewidth": 0.8,
            "legend.frameon": False,
            "legend.fontsize": 8.6,
            "xtick.color": COLORS["ink"],
            "ytick.color": COLORS["ink"],
            "text.color": COLORS["ink"],
            "axes.labelcolor": COLORS["ink"],
            "axes.titlecolor": COLORS["ink"],
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(OUTDIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUTDIR / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def grouped_main_performance() -> None:
    splits = ["Art", "Cartoon", "Sketch", "Photo"]
    data = {
        "ERM": [85.7, 80.8, 81.2, 95.1],
        "SWAD": [88.1, 82.4, 82.9, 96.6],
        "DIWA": [89.0, 83.1, 83.4, 96.9],
        "Uniform Soup": [88.4, 83.3, 83.6, 97.0],
        "CDA-VSC + Piv": [89.3, 84.4, 84.8, 97.5],
        "CDA-VSC + BD": [89.2, 84.2, 85.0, 97.6],
    }
    palette = [
        COLORS["erm"],
        COLORS["swad"],
        COLORS["diwa"],
        COLORS["uniform"],
        COLORS["piv"],
        COLORS["bd"],
    ]

    x = np.arange(len(splits))
    width = 0.12
    fig, ax = plt.subplots(figsize=(8.6, 4.3))
    for idx, (label, vals) in enumerate(data.items()):
        ax.bar(x + (idx - 2.5) * width, vals, width=width, label=label, color=palette[idx], alpha=0.95)

    ax.set_xticks(x)
    ax.set_xticklabels(splits)
    ax.set_ylim(78, 99)
    ax.set_ylabel("full accuracy (%)")
    ax.set_title("Mock main benchmark figure: per-split PACS comparison", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend(ncols=3, loc="upper left")
    save(fig, "01_main_benchmark")


def mean_metrics() -> None:
    metrics = ["Mean full", "Mean in", "Mean out"]
    methods = ["ERM", "SWAD", "DIWA", "Uniform", "CDA-Piv", "CDA-BD"]
    vals = np.array(
        [
            [85.7, 84.9, 86.2],
            [87.5, 87.0, 88.1],
            [88.1, 87.7, 88.8],
            [88.4, 88.0, 89.0],
            [89.0, 88.8, 89.6],
            [89.0, 88.7, 89.8],
        ]
    )
    colors = [COLORS["erm"], COLORS["swad"], COLORS["diwa"], COLORS["uniform"], COLORS["piv"], COLORS["bd"]]

    x = np.arange(len(metrics))
    width = 0.12
    fig, ax = plt.subplots(figsize=(8.3, 4.1))
    for i, method in enumerate(methods):
        ax.bar(x + (i - 2.5) * width, vals[i], width=width, label=method, color=colors[i])
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylim(83.5, 90.5)
    ax.set_ylabel("accuracy (%)")
    ax.set_title("Mock mean full / in / out accuracy comparison", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend(ncols=3, loc="upper left")
    save(fig, "02_mean_metrics")


def checkpoint_timeline() -> None:
    families = {
        "Art": [50, 100, 400, 550, 1400, 1600, 1700, 2350, 3250, 5650, 6100, 9050, 9100, 10500, 10600, 12600, 12700, 13450],
        "Cartoon": [75, 250, 500, 800, 1200, 1650, 2100, 2750, 3450, 4100, 5600, 6400, 7850, 8900, 9600, 11000, 12750, 14950, 15100, 15300, 15600],
        "Sketch": [100, 300, 550, 800, 1250, 1650, 2100, 2550, 3000, 3550, 4100, 5000, 5900, 6700, 7850, 8800, 9900, 10800, 11550, 12750, 13300, 14000, 14500, 14950, 15350],
        "Photo": [50, 250, 500, 800, 1200, 1650, 2100, 2600, 3200, 3800, 4550, 5200, 6100, 7000, 7850, 8600, 9400, 10300, 11050, 11800, 12750, 13400, 14000, 14500, 14950, 15300, 15700],
    }
    fig, ax = plt.subplots(figsize=(9.0, 3.9))
    labels = list(families.keys())
    for row, split in enumerate(labels):
        steps = np.array(families[split])
        ax.scatter(steps, np.full_like(steps, len(labels) - 1 - row), s=38, color=COLORS["piv"] if split in {"Art", "Cartoon"} else COLORS["bd"], zorder=3)
        ax.hlines(len(labels) - 1 - row, 0, 16000, color=COLORS["grid"], linewidth=1.0, zorder=1)
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels[::-1])
    ax.set_xlim(0, 16000)
    ax.set_xlabel("training step")
    ax.set_title("Mock VSC selector timelines: non-contiguous checkpoints across splits", loc="left", weight="bold")
    ax.grid(axis="x")
    save(fig, "03_checkpoint_timeline")


def mismatch_curve() -> None:
    sizes = np.arange(1, 31)
    curves = {
        "Art": 0.32 * np.exp(-sizes / 6.5) + 0.018,
        "Cartoon": 0.35 * np.exp(-sizes / 7.5) + 0.028,
        "Sketch": 0.29 * np.exp(-sizes / 8.0) + 0.022,
        "Photo": 0.24 * np.exp(-sizes / 9.5) + 0.018,
    }
    colors = [COLORS["accent"], COLORS["piv"], COLORS["bd"], COLORS["violet"]]
    fig, ax = plt.subplots(figsize=(7.7, 4.2))
    for color, (label, vals) in zip(colors, curves.items()):
        ax.plot(sizes, vals, marker="o", ms=3.0, linewidth=2.1, color=color, label=label)
    ax.axhline(0.05, linestyle="--", color=COLORS["muted"], linewidth=1.2)
    ax.set_xlabel("retained family size")
    ax.set_ylabel("threshold-disagreement mismatch")
    ax.set_title("Mock mismatch curves for version-space compression", loc="left", weight="bold")
    ax.grid(True)
    ax.legend()
    save(fig, "04_vsc_mismatch")


def family_size_vs_accuracy() -> None:
    rng = np.random.default_rng(7)
    fig, ax = plt.subplots(figsize=(7.6, 4.3))
    selectors = {
        "Blackwell target-set": (rng.integers(1, 8, 18), 82.0 + rng.random(18) * 7.2, COLORS["accent"]),
        "Residual coverage": (rng.integers(4, 12, 18), 82.5 + rng.random(18) * 5.2, COLORS["violet"]),
        "VSC": (rng.integers(14, 30, 18), 83.5 + rng.random(18) * 5.6, COLORS["piv"]),
        "Clique": (rng.integers(5, 10, 18), 83.0 + rng.random(18) * 4.8, COLORS["green"]),
    }
    for label, (x, y, color) in selectors.items():
        ax.scatter(x, y, s=48, alpha=0.88, color=color, label=label, edgecolor="white", linewidth=0.6)
    ax.scatter([21, 25, 27], [84.4, 85.0, 97.6], s=90, marker="*", color=COLORS["bd"], label="CDA-reported picks", edgecolor="white", linewidth=0.8)
    ax.set_xlabel("family size")
    ax.set_ylabel("target full accuracy (%)")
    ax.set_title("Mock selector tradeoff: family size versus target accuracy", loc="left", weight="bold")
    ax.grid(True)
    ax.legend(ncols=2, loc="lower right")
    save(fig, "05_family_size_vs_accuracy")


def weight_heatmap() -> None:
    rules = ["ERM", "SWAD", "DIWA", "Uniform", "Nash", "OT", "CDA-Piv", "CDA-BD"]
    splits = ["Art", "Cartoon", "Sketch", "Photo"]
    vals = np.array(
        [
            [85.7, 80.8, 81.2, 95.1],
            [88.1, 82.4, 82.9, 96.6],
            [89.0, 83.1, 83.4, 96.9],
            [88.4, 83.3, 83.6, 97.0],
            [89.0, 83.8, 84.5, 97.3],
            [89.1, 83.7, 84.4, 97.2],
            [89.3, 84.4, 84.8, 97.5],
            [89.2, 84.2, 85.0, 97.6],
        ]
    )
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    im = ax.imshow(vals, aspect="auto", cmap=HEATMAP, vmin=80, vmax=98)
    ax.set_xticks(np.arange(len(splits)))
    ax.set_xticklabels(splits)
    ax.set_yticks(np.arange(len(rules)))
    ax.set_yticklabels(rules)
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            ax.text(j, i, f"{vals[i, j]:.1f}", ha="center", va="center", fontsize=7.4, color="white" if vals[i, j] > 89 else COLORS["ink"])
    ax.set_title("Mock weight-rule heatmap on a fixed retained family", loc="left", weight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cbar.ax.set_ylabel("full accuracy (%)")
    save(fig, "06_weight_heatmap")


def weight_distribution() -> None:
    steps = np.arange(1, 19)
    uniform = np.full(18, 1 / 18)
    piv = np.array([0.02, 0.03, 0.02, 0.04, 0.05, 0.08, 0.04, 0.07, 0.08, 0.06, 0.05, 0.05, 0.07, 0.08, 0.09, 0.06, 0.06, 0.05])
    bd = np.array([0.01, 0.02, 0.01, 0.03, 0.04, 0.07, 0.03, 0.07, 0.09, 0.06, 0.05, 0.05, 0.08, 0.10, 0.10, 0.07, 0.07, 0.05])
    fig, axes = plt.subplots(3, 1, figsize=(7.4, 5.6), sharex=True)
    for ax, vals, title, color in [
        (axes[0], uniform, "Uniform soup", COLORS["uniform"]),
        (axes[1], piv, "CDA-Piv", COLORS["piv"]),
        (axes[2], bd, "CDA-BD", COLORS["bd"]),
    ]:
        ax.bar(steps, vals, color=color, alpha=0.95)
        ax.set_ylabel("weight")
        ax.set_title(title, loc="left", fontsize=10, weight="bold")
        ax.grid(axis="y")
    axes[-1].set_xlabel("checkpoint index inside retained family")
    fig.suptitle("Mock weight distributions over the same retained VSC family", x=0.08, y=1.02, ha="left", fontsize=12, weight="bold")
    save(fig, "07_weight_distribution")


def pivotality_guard() -> None:
    idx = np.arange(1, 19)
    pivotality = np.array([0.12, 0.19, 0.15, 0.22, 0.25, 0.43, 0.31, 0.48, 0.54, 0.49, 0.42, 0.39, 0.45, 0.51, 0.56, 0.37, 0.34, 0.30])
    sensitivity = np.array([0.31, 0.28, 0.27, 0.25, 0.24, 0.18, 0.21, 0.16, 0.14, 0.17, 0.19, 0.20, 0.16, 0.13, 0.12, 0.22, 0.24, 0.26])
    score = pivotality - 0.6 * sensitivity
    fig, ax = plt.subplots(figsize=(8.0, 4.1))
    ax.bar(idx, pivotality, color=COLORS["piv"], alpha=0.75, label="leave-one-out pivotality")
    ax.plot(idx, sensitivity, color=COLORS["accent"], linewidth=2.0, marker="o", label="sensitivity penalty")
    ax.plot(idx, score, color=COLORS["bd"], linewidth=2.3, marker="s", label="guarded score")
    ax.set_xlabel("checkpoint index")
    ax.set_ylabel("normalized score")
    ax.set_title("Mock pivotality-shift guard diagnostics", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend(ncols=3, loc="upper left")
    save(fig, "08_pivotality_guard")


def blackwell_geometry() -> None:
    rng = np.random.default_rng(4)
    pts = rng.normal(size=(18, 2)) * [0.28, 0.22] + [0.3, 0.45]
    best = np.array([[0.12, 0.18], [0.10, 0.38], [0.22, 0.12], [0.18, 0.28]])
    hull = np.array([[0.08, 0.10], [0.08, 0.42], [0.26, 0.46], [0.30, 0.16]])
    uniform = np.array([0.34, 0.40])
    bd = np.array([0.18, 0.24])

    fig, ax = plt.subplots(figsize=(6.6, 5.0))
    ax.scatter(pts[:, 0], pts[:, 1], color=COLORS["uniform"], s=45, label="checkpoint loss vectors")
    ax.scatter(best[:, 0], best[:, 1], color=COLORS["green"], s=55, marker="D", label="per-domain best checkpoints")
    ax.add_patch(Polygon(hull, closed=True, facecolor="#dceef8", edgecolor=COLORS["diwa"], linewidth=1.5, alpha=0.55, label="target-set region"))
    ax.scatter(*uniform, color=COLORS["uniform"], s=90, marker="o", edgecolor="white", linewidth=0.8, label="uniform soup")
    ax.scatter(*bd, color=COLORS["bd"], s=110, marker="*", edgecolor="white", linewidth=0.8, label="CDA-BD solution")
    ax.add_patch(FancyArrowPatch(uniform, bd, arrowstyle="->", mutation_scale=14, linewidth=2.0, color=COLORS["bd"]))
    ax.set_xlabel("domain-loss component 1")
    ax.set_ylabel("domain-loss component 2")
    ax.set_title("Mock Blackwell-dual geometry in a 2D loss-vector projection", loc="left", weight="bold")
    ax.grid(True)
    ax.legend(loc="upper right")
    save(fig, "09_blackwell_geometry")


def pareto_in_out() -> None:
    methods = ["ERM", "SWAD", "DIWA", "Uniform", "CDA-Piv", "CDA-BD"]
    ins = np.array([84.9, 87.0, 87.7, 88.0, 88.8, 88.7])
    outs = np.array([86.2, 88.1, 88.8, 89.0, 89.6, 89.8])
    sizes = np.array([1, 4, 8, 18, 21, 21]) * 18
    colors = [COLORS["erm"], COLORS["swad"], COLORS["diwa"], COLORS["uniform"], COLORS["piv"], COLORS["bd"]]

    fig, ax = plt.subplots(figsize=(6.9, 5.0))
    for method, x, y, s, c in zip(methods, ins, outs, sizes, colors):
        ax.scatter(x, y, s=s, color=c, alpha=0.88, edgecolor="white", linewidth=0.8)
        ax.text(x + 0.05, y + 0.04, method, fontsize=8.2)
    ax.set_xlabel("mean in accuracy (%)")
    ax.set_ylabel("mean out accuracy (%)")
    ax.set_title("Mock Pareto view of in/out generalization", loc="left", weight="bold")
    ax.grid(True)
    save(fig, "10_pareto_in_out")


def support_vs_target() -> None:
    rng = np.random.default_rng(3)
    x = 0.06 + rng.random(36) * 0.08
    y = 90.4 - 48 * x + rng.normal(0, 0.45, 36)
    fig, ax = plt.subplots(figsize=(6.8, 4.5))
    ax.scatter(x, y, s=44, color=COLORS["diwa"], alpha=0.8, label="completed soups")
    coeffs = np.polyfit(x, y, deg=1)
    xs = np.linspace(x.min(), x.max(), 100)
    ax.plot(xs, coeffs[0] * xs + coeffs[1], color=COLORS["bd"], linewidth=2.2, label="trend")
    ax.scatter([0.083, 0.078], [89.3, 89.2], s=95, marker="*", color=COLORS["piv"], edgecolor="white", linewidth=0.8, label="CDA methods")
    ax.set_xlabel("source-side support loss")
    ax.set_ylabel("target full accuracy (%)")
    ax.set_title("Mock relation between source-side support loss and target performance", loc="left", weight="bold")
    ax.grid(True)
    ax.legend()
    save(fig, "11_support_vs_target")


def entropy_vs_accuracy() -> None:
    entropy = np.array([0.1, 0.22, 0.34, 0.46, 0.58, 0.72, 0.85, 0.96, 1.08, 1.22, 1.36, 1.48])
    accuracy = np.array([86.8, 87.3, 87.9, 88.5, 88.9, 89.2, 89.1, 88.9, 88.5, 88.0, 87.6, 87.2])
    fig, ax = plt.subplots(figsize=(6.7, 4.2))
    ax.plot(entropy, accuracy, color=COLORS["accent"], linewidth=2.4, marker="o")
    ax.axvspan(0.55, 0.95, color="#cdebe7", alpha=0.55)
    ax.text(0.60, 89.25, "effective range", fontsize=8.4, color=COLORS["ink"])
    ax.set_xlabel("weight entropy / effective family size proxy")
    ax.set_ylabel("target full accuracy (%)")
    ax.set_title("Mock weight concentration versus accuracy", loc="left", weight="bold")
    ax.grid(True)
    save(fig, "12_entropy_vs_accuracy")


def certificate_components() -> None:
    labels = ["ERM", "SWAD", "DIWA", "Uniform", "CDA-Piv", "CDA-BD"]
    flat = np.array([0.64, 0.72, 0.75, 0.78, 0.86, 0.84])
    div = np.array([0.31, 0.46, 0.55, 0.57, 0.68, 0.73])
    cert = np.array([0.42, 0.36, 0.31, 0.28, 0.22, 0.20])

    x = np.arange(len(labels))
    fig, ax1 = plt.subplots(figsize=(8.0, 4.5))
    ax1.bar(x - 0.17, flat, width=0.32, color=COLORS["piv"], alpha=0.82, label="flatness / mergeability proxy")
    ax1.bar(x + 0.17, div, width=0.32, color=COLORS["accent"], alpha=0.82, label="diversity / cancellation proxy")
    ax1.set_ylabel("proxy value (higher is better)")
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.grid(axis="y")
    ax2 = ax1.twinx()
    ax2.plot(x, cert, color=COLORS["bd"], linewidth=2.4, marker="o", label="certificate proxy")
    ax2.set_ylabel("certificate proxy (lower is better)")
    ax1.set_title("Mock CDA decomposition: flatness, diversity, and certificate value", loc="left", weight="bold")
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, ncols=2, loc="upper center")
    save(fig, "13_certificate_components")


def covariance_spectrum() -> None:
    ranks = np.arange(1, 13)
    spectra = {
        "ERM bank": np.exp(-0.18 * ranks),
        "Uniform retained family": np.exp(-0.26 * ranks),
        "VSC retained family": np.exp(-0.34 * ranks),
    }
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    colors = [COLORS["erm"], COLORS["uniform"], COLORS["piv"]]
    for color, (label, vals) in zip(colors, spectra.items()):
        ax.plot(ranks, vals, marker="o", linewidth=2.1, color=color, label=label)
    ax.set_yscale("log")
    ax.set_xlabel("eigenvalue rank")
    ax.set_ylabel("magnitude (log scale)")
    ax.set_title("Mock source-response covariance spectrum", loc="left", weight="bold")
    ax.grid(True, which="both")
    ax.legend()
    save(fig, "14_covariance_spectrum")


def certificate_ablation() -> None:
    methods = ["Uniform", "CDA-Piv", "CDA-BD"]
    source_fit = np.array([0.42, 0.36, 0.34])
    sensitivity = np.array([0.31, 0.21, 0.19])
    merge_gap = np.array([0.14, 0.11, 0.10])
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.bar(methods, source_fit, color=COLORS["uniform"], label="source fit")
    ax.bar(methods, sensitivity, bottom=source_fit, color=COLORS["accent"], label="sensitivity")
    ax.bar(methods, merge_gap, bottom=source_fit + sensitivity, color=COLORS["piv"], label="mergeability gap")
    ax.set_ylabel("certificate contribution")
    ax.set_title("Mock certificate-term ablation", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend()
    save(fig, "15_certificate_ablation")


def full_cross_heatmap() -> None:
    selectors = ["Blackwell", "Residual", "Clique", "VSC", "Stability", "Target-set"]
    weights = ["Uniform", "SWAD-style", "Nash", "OT", "CDA-Piv", "CDA-BD"]
    vals = np.array(
        [
            [88.7, 88.8, 88.9, 89.0, 88.9, 88.8],
            [88.0, 88.2, 88.3, 88.4, 88.5, 88.4],
            [88.2, 88.4, 88.6, 88.5, 88.6, 88.5],
            [88.4, 88.5, 89.0, 89.1, 89.3, 89.2],
            [87.9, 88.1, 88.4, 88.6, 88.7, 88.7],
            [88.6, 88.5, 88.7, 88.9, 88.8, 88.8],
        ]
    )
    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    im = ax.imshow(vals, cmap=HEATMAP, aspect="auto", vmin=87.8, vmax=89.4)
    ax.set_xticks(np.arange(len(weights)))
    ax.set_xticklabels(weights, rotation=20, ha="right")
    ax.set_yticks(np.arange(len(selectors)))
    ax.set_yticklabels(selectors)
    for i in range(vals.shape[0]):
        for j in range(vals.shape[1]):
            ax.text(j, i, f"{vals[i, j]:.1f}", ha="center", va="center", fontsize=7.2, color="white" if vals[i, j] > 88.8 else COLORS["ink"])
    ax.set_title("Mock complete selector × weight grid", loc="left", weight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.ax.set_ylabel("mean full accuracy (%)")
    save(fig, "16_full_cross_heatmap")


def family_strips() -> None:
    split_steps = {
        "Art": [50, 100, 400, 550, 1400, 1600, 1700, 2350, 3250, 5650, 6100, 9050, 9100, 10500, 10600, 12600, 12700, 13450],
        "Cartoon": [75, 500, 800, 1200, 1650, 2100, 2750, 3450, 5600, 7850, 9600, 11000, 12750, 14950],
        "Sketch": [100, 300, 800, 1250, 1650, 2550, 3550, 5000, 6700, 7850, 9900, 10800, 12750, 14000, 14950],
        "Photo": [50, 250, 800, 1200, 1650, 2600, 3200, 4550, 6100, 7850, 9400, 11050, 12750, 14000, 14950],
    }
    fig, axes = plt.subplots(4, 1, figsize=(8.0, 5.6), sharex=True)
    for ax, (split, steps) in zip(axes, split_steps.items()):
        ax.hlines(0, 0, 16000, color=COLORS["grid"], linewidth=2.2)
        ax.scatter(steps, np.zeros(len(steps)), s=55, color=COLORS["piv"] if split in {"Art", "Cartoon"} else COLORS["bd"])
        ax.set_yticks([])
        ax.set_ylabel(split, rotation=0, labelpad=25, va="center")
        ax.grid(axis="x")
    axes[-1].set_xlabel("training step")
    fig.suptitle("Mock split-wise retained-family strips", x=0.09, y=1.02, ha="left", fontsize=12, weight="bold")
    save(fig, "17_family_strips")


def hparam_robustness() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.7))
    eps = np.array([0.01, 0.02, 0.05, 0.08, 0.10])
    vsc = np.array([88.6, 88.9, 89.3, 89.0, 88.5])
    alpha = np.array([0.25, 0.5, 0.75, 1.0, 1.25])
    piv = np.array([88.7, 89.0, 89.3, 89.2, 88.9])
    lamb = np.array([0.0, 0.01, 0.02, 0.05, 0.10])
    bd = np.array([88.8, 89.1, 89.2, 89.0, 88.7])
    panels = [
        (eps, vsc, r"VSC $\epsilon_{\rm vsc}$", COLORS["piv"]),
        (alpha, piv, r"Pivotality $\alpha$", COLORS["accent"]),
        (lamb, bd, r"Blackwell $\lambda_{\rm ent}$", COLORS["bd"]),
    ]
    for ax, (x, y, title, color) in zip(axes, panels):
        ax.plot(x, y, marker="o", linewidth=2.1, color=color)
        ax.set_title(title, loc="left", fontsize=10.5, weight="bold")
        ax.set_ylim(88.3, 89.5)
        ax.grid(True)
    axes[0].set_ylabel("mean full accuracy (%)")
    fig.suptitle("Mock hyperparameter robustness slices", x=0.07, y=1.02, ha="left", fontsize=12, weight="bold")
    save(fig, "18_hparam_robustness")


def art_family_sweeps() -> None:
    families = ["Blackwell-3", "VSC-18", "Residual-8"]
    uniform = np.array([88.77, 88.38, 87.95])
    swad = np.array([88.80, 88.42, 88.05])
    ours = np.array([88.87, 88.57, 88.31])
    x = np.arange(len(families))
    width = 0.22
    fig, ax = plt.subplots(figsize=(7.5, 4.1))
    ax.bar(x - width, uniform, width=width, color=COLORS["uniform"], label="uniform family soup")
    ax.bar(x, swad, width=width, color=COLORS["swad"], label="SWAD-style weighting")
    ax.bar(x + width, ours, width=width, color=COLORS["piv"], label="best CDA-derived weighting")
    ax.set_xticks(x)
    ax.set_xticklabels(families)
    ax.set_ylim(87.7, 89.1)
    ax.set_ylabel("art full accuracy (%)")
    ax.set_title("Mock art-focused family sweeps", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend()
    save(fig, "19_art_family_sweeps")


def selector_collapse() -> None:
    selectors = ["Blackwell", "Residual", "Clique", "VSC", "Target-set", "Bootstrap"]
    art = np.array([3, 8, 6, 18, 2, 14])
    cartoon = np.array([1, 7, 6, 21, 1, 16])
    sketch = np.array([2, 8, 6, 25, 1, 15])
    photo = np.array([3, 7, 6, 27, 1, 18])
    x = np.arange(len(selectors))
    width = 0.18
    fig, ax = plt.subplots(figsize=(8.1, 4.3))
    for offset, vals, label, color in [
        (-1.5 * width, art, "Art", COLORS["accent"]),
        (-0.5 * width, cartoon, "Cartoon", COLORS["piv"]),
        (0.5 * width, sketch, "Sketch", COLORS["bd"]),
        (1.5 * width, photo, "Photo", COLORS["violet"]),
    ]:
        ax.bar(x + offset, vals, width=width, label=label, color=color, alpha=0.9)
    ax.axhline(1, color=COLORS["muted"], linestyle="--", linewidth=1.1)
    ax.text(-0.4, 1.35, "singleton collapse line", fontsize=8.0, color=COLORS["muted"])
    ax.set_xticks(x)
    ax.set_xticklabels(selectors, rotation=15, ha="right")
    ax.set_ylabel("retained family size")
    ax.set_title("Mock selector-collapse comparison across PACS targets", loc="left", weight="bold")
    ax.grid(axis="y")
    ax.legend(ncols=4, loc="upper left")
    save(fig, "20_selector_collapse")


def main() -> None:
    set_style()
    grouped_main_performance()
    mean_metrics()
    checkpoint_timeline()
    mismatch_curve()
    family_size_vs_accuracy()
    weight_heatmap()
    weight_distribution()
    pivotality_guard()
    blackwell_geometry()
    pareto_in_out()
    support_vs_target()
    entropy_vs_accuracy()
    certificate_components()
    covariance_spectrum()
    certificate_ablation()
    full_cross_heatmap()
    family_strips()
    hparam_robustness()
    art_family_sweeps()
    selector_collapse()


if __name__ == "__main__":
    main()
