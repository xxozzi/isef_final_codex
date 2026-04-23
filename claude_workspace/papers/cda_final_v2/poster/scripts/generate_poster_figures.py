from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

PAPER = "#F7F5F0"
WHITE = "#FFFFFF"
INK = "#182033"
MUTED = "#667085"
GRID = "#D4DBE6"

COLORS = {
    "ERM": "#9199A8",
    "SAM": "#B85C2E",
    "SWA": "#BF911F",
    "SWAD": "#3658C7",
    "DiWA": "#6E53E9",
    "CDA": "#0D776A",
}

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 13,
        "axes.titlesize": 18,
        "axes.labelsize": 14,
        "legend.fontsize": 12,
        "figure.facecolor": PAPER,
        "axes.facecolor": WHITE,
        "savefig.facecolor": PAPER,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def style_axis(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.tick_params(colors=INK)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.title.set_color(INK)
    ax.grid(True, axis=grid_axis, color=GRID, linewidth=1.0, alpha=0.95)


def save(fig, name: str):
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{name}.png", dpi=260, bbox_inches="tight")
    plt.close(fig)


def core_benchmark_results():
    benchmarks = ["PACS", "VLCS", "OfficeHome", "TerraInc.", "DomainNet"]
    data = {
        "ERM": [85.5, 77.5, 66.5, 46.1, 40.9],
        "SWAD": [88.1, 79.1, 70.6, 50.0, 46.5],
        "DiWA": [89.0, 78.6, 72.8, 51.9, 47.7],
        "CDA": [89.1, 79.5, 72.9, 52.3, 47.8],
    }
    averages = {
        "ERM": 63.3,
        "SWAD": 66.9,
        "DiWA": 68.0,
        "CDA": 68.3,
    }

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0), gridspec_kw={"width_ratios": [2.2, 1.0]})

    ax = axes[0]
    x = np.arange(len(benchmarks))
    width = 0.18
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]
    order = ["ERM", "SWAD", "DiWA", "CDA"]
    for offset, method in zip(offsets, order):
        ax.bar(x + offset, data[method], width=width, color=COLORS[method], label=method)
    ax.set_xticks(x, benchmarks)
    ax.set_ylim(35, 92)
    ax.set_ylabel("OOD accuracy")
    ax.set_title("Five-benchmark comparison")
    style_axis(ax, "y")
    ax.legend(frameon=False, ncol=4, loc="upper left")

    ax = axes[1]
    avg_order = ["ERM", "SWAD", "DiWA", "CDA"]
    bars = ax.bar(avg_order, [averages[m] for m in avg_order], color=[COLORS[m] for m in avg_order], width=0.62)
    ax.set_ylim(60, 69.5)
    ax.set_ylabel("Average OOD accuracy")
    ax.set_title("Average across benchmarks")
    style_axis(ax, "y")
    for bar, method in zip(bars, avg_order):
        value = averages[method]
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.12, f"{value:.1f}", ha="center", va="bottom", color=INK, weight="bold")

    save(fig, "core_benchmark_results")


def pacs_generalization():
    methods = ["ERM", "SAM", "SWA", "SWAD", "CDA"]
    ood = [85.3, 85.5, 85.9, 87.1, 89.1]
    ind = [96.6, 97.4, 97.1, 97.7, 97.9]

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), sharey=False)

    ax = axes[0]
    bars = ax.bar(methods, ood, color=[COLORS[m] for m in methods], width=0.62)
    ax.set_ylim(84, 90)
    ax.set_ylabel("OOD accuracy")
    ax.set_title("PACS out-of-domain")
    style_axis(ax, "y")
    for bar, value in zip(bars, ood):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.08, f"{value:.1f}", ha="center", va="bottom", color=INK, weight="bold", fontsize=11)

    ax = axes[1]
    bars = ax.bar(methods, ind, color=[COLORS[m] for m in methods], width=0.62)
    ax.set_ylim(96.0, 98.2)
    ax.set_ylabel("In-domain accuracy")
    ax.set_title("PACS in-domain")
    style_axis(ax, "y")
    for bar, value in zip(bars, ind):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.03, f"{value:.1f}", ha="center", va="bottom", color=INK, weight="bold", fontsize=11)

    save(fig, "pacs_generalization")


if __name__ == "__main__":
    core_benchmark_results()
    pacs_generalization()
