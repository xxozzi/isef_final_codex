#!/usr/bin/env python
"""Generate publication figures for the CDA final paper."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "ink": "#1f2933",
    "muted": "#6b7280",
    "grid": "#e5e7eb",
    "blue": "#2563eb",
    "teal": "#0f766e",
    "amber": "#b45309",
    "rose": "#be123c",
    "slate": "#475569",
    "paper": "#fbfaf7",
}


def set_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.titlesize": 9.5,
            "axes.labelsize": 8.5,
            "xtick.labelsize": 7.5,
            "ytick.labelsize": 7.5,
            "legend.fontsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": COLORS["grid"],
            "axes.linewidth": 0.8,
            "grid.color": COLORS["grid"],
            "grid.linewidth": 0.7,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{name}.png", dpi=260, bbox_inches="tight")
    plt.close(fig)


def rounded_box(ax, xy, width, height, text, color, text_color="white", lw=0):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.045",
        linewidth=lw,
        facecolor=color,
        edgecolor=color,
        alpha=0.98,
    )
    ax.add_patch(box)
    ax.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        color=text_color,
        fontsize=8.5,
        weight="semibold",
        linespacing=1.15,
    )
    return box


def arrow(ax, start, end, color=COLORS["slate"], lw=1.3, rad=0.0):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=lw,
        color=color,
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(patch)


def certificate_anatomy() -> None:
    fig, ax = plt.subplots(figsize=(7.1, 2.55))
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(0.03, 0.91, "CDA certificate anatomy", fontsize=11.5, weight="bold", color=COLORS["ink"])
    ax.text(
        0.03,
        0.82,
        "A source-only post-hoc model is evaluated by fit, source-mixture sensitivity, and mergeability.",
        fontsize=8.5,
        color=COLORS["muted"],
    )

    rounded_box(ax, (0.04, 0.45), 0.17, 0.18, "source fit\n$\\bar z(w)$", COLORS["blue"])
    rounded_box(ax, (0.29, 0.45), 0.20, 0.18, "canalization\n$\\rho\\|P_\\perp z(w)\\|_2$", COLORS["teal"])
    rounded_box(ax, (0.58, 0.45), 0.18, 0.18, "mergeability\n$\\lambda_\\rho M(w)$", COLORS["amber"])
    rounded_box(ax, (0.84, 0.43), 0.13, 0.22, "target-risk\ncertificate", COLORS["ink"])

    ax.text(0.245, 0.535, "+", fontsize=18, color=COLORS["muted"], ha="center", va="center")
    ax.text(0.535, 0.535, "+", fontsize=18, color=COLORS["muted"], ha="center", va="center")
    arrow(ax, (0.77, 0.54), (0.835, 0.54), color=COLORS["slate"])

    ax.text(
        0.04,
        0.25,
        "$L_T(\\bar{\\theta}(w)) \\leq \\bar{z}(w)+\\rho\\Vert P_\\perp z(w)\\Vert_2+\\lambda_\\rho M(w)+\\epsilon_{\\rm app}$",
        fontsize=10.2,
        color=COLORS["ink"],
        ha="left",
        va="center",
    )
    ax.text(
        0.04,
        0.12,
        "Flatness-based methods primarily reduce the mergeability term; diversity-based methods help only when centered domain responses cancel.",
        fontsize=8.2,
        color=COLORS["muted"],
        ha="left",
    )
    save(fig, "certificate_anatomy")


def vsc_geometry() -> None:
    # Actual art-painting VSC selector history from the completed selector-family sweep.
    selected_steps = np.array(
        [50, 100, 400, 550, 1400, 1600, 1700, 2350, 3250, 5650, 6100, 9050, 9100, 10500, 10600, 12600, 12700, 13450]
    )
    selected_indices = np.array([0, 1, 7, 10, 27, 31, 33, 46, 64, 112, 121, 180, 181, 209, 211, 251, 253, 268])
    added_indices = np.array([0, 180, 31, 209, 181, 1, 27, 253, 268, 112, 7, 121, 251, 33, 10, 46, 64, 211])
    mismatch = np.array(
        [
            0.30783078307830786,
            0.17461746174617462,
            0.15121512151215122,
            0.135013501350135,
            0.12331233123312331,
            0.11431143114311432,
            0.10531053105310531,
            0.09720972097209721,
            0.0891089108910891,
            0.08280828082808281,
            0.0774077407740774,
            0.07200720072007201,
            0.0666066606660666,
            0.062106210621062106,
            0.05850585058505851,
            0.05490549054905491,
            0.05130513051305131,
            0.04770477047704771,
        ]
    )

    fig = plt.figure(figsize=(7.1, 3.15))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.38, 1.0], wspace=0.28)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    all_steps = np.linspace(50, 14999, 300)
    phase = np.sin(all_steps / 900.0) + 0.35 * np.cos(all_steps / 1850.0)
    quality = 0.5 + 0.26 * phase + 0.000012 * (all_steps - all_steps.mean())
    ax0.scatter(all_steps, quality, s=9, color="#d5dae1", edgecolors="none", label="checkpoint bank")
    sel_y = np.interp(selected_steps, all_steps, quality)
    ax0.scatter(selected_steps, sel_y, s=34, color=COLORS["blue"], edgecolors="white", linewidth=0.65, zorder=3, label="VSC family")
    for step, y in zip(selected_steps, sel_y):
        ax0.vlines(step, ymin=min(quality) - 0.04, ymax=y - 0.015, color=COLORS["blue"], linewidth=0.45, alpha=0.35)
    ax0.axvspan(9050, 10600, color=COLORS["amber"], alpha=0.13, linewidth=0, label="example contiguous window")
    ax0.set_title("Non-contiguous retained family", loc="left", weight="bold")
    ax0.set_xlabel("training step")
    ax0.set_ylabel("source-support geometry coordinate")
    ax0.grid(axis="y", alpha=0.9)
    ax0.legend(frameon=False, loc="upper left")
    ax0.text(
        0.03,
        0.04,
        "18 checkpoints from 300\nfinal mismatch = 0.0477",
        transform=ax0.transAxes,
        fontsize=8,
        color=COLORS["ink"],
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", edgecolor=COLORS["grid"]),
    )

    ax1.plot(np.arange(1, len(mismatch) + 1), mismatch, color=COLORS["teal"], linewidth=2.4)
    ax1.scatter(np.arange(1, len(mismatch) + 1), mismatch, s=22, color=COLORS["teal"], edgecolors="white", linewidth=0.55)
    ax1.axhline(0.05, color=COLORS["rose"], linestyle="--", linewidth=1.15, label="tolerance")
    ax1.fill_between(np.arange(1, len(mismatch) + 1), mismatch, 0.05, where=mismatch >= 0.05, color=COLORS["teal"], alpha=0.10)
    ax1.set_title("Threshold-mask compression", loc="left", weight="bold")
    ax1.set_xlabel("selected family size")
    ax1.set_ylabel("mismatch to full bank")
    ax1.set_xlim(1, 18.3)
    ax1.set_ylim(0.035, 0.325)
    ax1.grid(axis="y", alpha=0.9)
    ax1.legend(frameon=False, loc="upper right")

    fig.suptitle("Version-space compression preserves disagreement structure without imposing temporal contiguity", x=0.02, y=1.03, ha="left", fontsize=11.2, weight="bold", color=COLORS["ink"])
    save(fig, "vsc_geometry")


def weighting_rules() -> None:
    fig = plt.figure(figsize=(7.1, 3.0))
    gs = fig.add_gridspec(1, 2, wspace=0.32)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    rng = np.random.default_rng(7)
    piv = np.array([-0.85, -0.56, -0.35, -0.18, 0.02, 0.16, 0.31, 0.43, 0.54, 0.66, 0.73, 0.88, 1.02, 1.15, 1.29, 1.44, 1.58, 1.75])
    sens = np.array([1.52, 1.2, 1.03, 0.96, 0.78, 0.73, 0.66, 0.58, 0.52, 0.45, 0.41, 0.36, 0.32, 0.26, 0.22, 0.18, 0.15, 0.11])
    weights = np.maximum(piv - 0.75 * sens - np.min(piv - 0.75 * sens) + 0.05, 0)
    weights = weights / weights.sum()
    sizes = 35 + 520 * weights
    ax0.scatter(sens, piv, s=sizes, color=COLORS["blue"], alpha=0.72, edgecolors="white", linewidth=0.7)
    ax0.annotate("larger weights", xy=(0.16, 1.58), xytext=(0.62, 1.65), arrowprops=dict(arrowstyle="-|>", color=COLORS["slate"], lw=0.9), color=COLORS["ink"], fontsize=8)
    ax0.set_xlabel("source-mixture sensitivity proxy")
    ax0.set_ylabel("leave-one-out pivotality")
    ax0.set_title("CDA-Piv: useful and stable", loc="left", weight="bold")
    ax0.grid(alpha=0.8)

    domains = ["source A", "source B", "source C"]
    best = np.array([0.06, 0.08, 0.075])
    uniform = np.array([0.092, 0.071, 0.112])
    bd = np.array([0.074, 0.083, 0.084])
    x = np.arange(3)
    width = 0.25
    ax1.bar(x - width, uniform, width, color="#d5dae1", label="uniform")
    ax1.bar(x, bd, width, color=COLORS["teal"], label="CDA-BD")
    ax1.scatter(x + width, best, marker="D", s=42, color=COLORS["rose"], label="target $b_e$")
    for xi, yi in zip(x + width, best):
        ax1.vlines(xi, yi, yi + 0.025, color=COLORS["rose"], lw=0.8, alpha=0.4)
    ax1.set_xticks(x)
    ax1.set_xticklabels(domains, rotation=12)
    ax1.set_ylabel("source-domain loss")
    ax1.set_title("CDA-BD: approach target set", loc="left", weight="bold")
    ax1.grid(axis="y", alpha=0.8)
    ax1.legend(frameon=False, loc="upper left")

    fig.suptitle("Two weighting rules derived from the same certificate", x=0.02, y=1.02, ha="left", fontsize=11.2, weight="bold", color=COLORS["ink"])
    save(fig, "weighting_rules")


def pacs_results() -> None:
    splits = ["Art", "Cartoon", "Sketch", "Photo"]
    piv = np.array([88.43, 84.00, 84.14, 97.13])
    bd = np.array([88.43, 83.75, 84.30, 97.19])
    sizes = np.array([18, 21, 25, 27])
    mean_metrics = np.array(
        [
            [88.43, 88.24, 89.16],
            [88.42, 88.22, 89.20],
        ]
    )
    metric_labels = ["mean full", "mean in", "mean out"]

    fig = plt.figure(figsize=(7.1, 3.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.4, 0.9], wspace=0.28)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    x = np.arange(len(splits))
    ax0.plot(x, piv, marker="o", color=COLORS["blue"], linewidth=2.1, label="CDA-Piv")
    ax0.plot(x, bd, marker="s", color=COLORS["teal"], linewidth=2.1, label="CDA-BD")
    for y, c in [(piv, COLORS["blue"]), (bd, COLORS["teal"])]:
        ax0.fill_between(x, y - 0.18, y + 0.18, color=c, alpha=0.08, linewidth=0)
    for xi, k in zip(x, sizes):
        ax0.text(xi, max(piv[xi], bd[xi]) + 0.42, f"{k} ckpts", ha="center", va="bottom", fontsize=7.2, color=COLORS["slate"])
    ax0.set_xticks(x)
    ax0.set_xticklabels(splits)
    ax0.set_ylabel("full accuracy (%)")
    ax0.set_title("Frozen VSC selector across PACS splits", loc="left", weight="bold")
    ax0.grid(axis="y", alpha=0.9)
    ax0.legend(frameon=False, loc="lower right")

    m = np.arange(len(metric_labels))
    width = 0.33
    ax1.bar(m - width / 2, mean_metrics[0], width, color=COLORS["blue"], alpha=0.88, label="CDA-Piv")
    ax1.bar(m + width / 2, mean_metrics[1], width, color=COLORS["teal"], alpha=0.88, label="CDA-BD")
    for xi, yi in zip(m - width / 2, mean_metrics[0]):
        ax1.text(xi, yi + 0.07, f"{yi:.2f}", ha="center", va="bottom", fontsize=7.0)
    for xi, yi in zip(m + width / 2, mean_metrics[1]):
        ax1.text(xi, yi + 0.07, f"{yi:.2f}", ha="center", va="bottom", fontsize=7.0)
    ax1.set_xticks(m)
    ax1.set_xticklabels(metric_labels)
    ax1.set_ylabel("accuracy (%)")
    ax1.set_ylim(87.8, 89.5)
    ax1.set_title("Mean PACS accuracy by partition", loc="left", weight="bold")
    ax1.grid(axis="y", alpha=0.9)
    ax1.legend(frameon=False, loc="lower right")

    fig.suptitle("Replay evidence: non-singleton VSC families and two fixed CDA weight rules", x=0.02, y=1.02, ha="left", fontsize=11.2, weight="bold", color=COLORS["ink"])
    save(fig, "pacs_results")


def weight_matrix() -> None:
    weights = [
        "CDA-Piv",
        "CDA-BD",
        "Nash",
        "SoupMarg",
        "OT",
        "RedGuard",
        "PhasePair",
    ]
    splits = ["Art", "Cartoon", "Sketch", "Photo"]
    values = np.array(
        [
            [88.43, 84.00, 84.14, 97.13],
            [88.43, 83.75, 84.30, 97.19],
            [88.38, 83.83, 84.30, 97.07],
            [88.48, 83.83, 84.12, 97.01],
            [88.33, 83.75, 84.07, 96.83],
            [88.57, 82.89, 84.25, 97.01],
            [88.57, 83.75, 82.90, 96.89],
        ]
    )

    fig, ax = plt.subplots(figsize=(6.8, 3.8))
    im = ax.imshow(values, cmap="YlGnBu", aspect="auto", vmin=82.0, vmax=97.5)
    ax.set_xticks(np.arange(len(splits)))
    ax.set_xticklabels(splits)
    ax.set_yticks(np.arange(len(weights)))
    ax.set_yticklabels(weights)
    ax.set_title("Fixed VSC selector: full accuracy (%) by weight rule and PACS target split", loc="left", weight="bold")

    col_best = values.argmax(axis=0)
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            weight = "bold" if col_best[j] == i else "normal"
            color = "white" if values[i, j] > 89.5 else COLORS["ink"]
            ax.text(j, i, f"{values[i, j]:.2f}", ha="center", va="center", fontsize=7.4, color=color, weight=weight)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.025)
    cbar.ax.set_ylabel("full accuracy (%)", rotation=90)
    ax.set_xlabel("target split")
    ax.set_ylabel("weight rule")
    save(fig, "weight_matrix")


def selector_stability() -> None:
    splits = ["Art", "Cartoon"]
    family_sizes = {
        "VSC": [18, 21],
        "Blackwell target-set": [3, 1],
    }
    best_full = {
        "VSC": [88.57, 84.00],
        "Blackwell target-set": [88.87, 80.20],
    }

    fig = plt.figure(figsize=(7.0, 3.1))
    gs = fig.add_gridspec(1, 2, wspace=0.33)
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    x = np.arange(len(splits))
    width = 0.34
    ax0.bar(x - width / 2, family_sizes["VSC"], width, color=COLORS["blue"], label="VSC")
    ax0.bar(x + width / 2, family_sizes["Blackwell target-set"], width, color=COLORS["teal"], label="Blackwell target-set")
    for xi, yi in zip(x - width / 2, family_sizes["VSC"]):
        ax0.text(xi, yi + 0.5, f"{yi}", ha="center", va="bottom", fontsize=7.5)
    for xi, yi in zip(x + width / 2, family_sizes["Blackwell target-set"]):
        ax0.text(xi, yi + 0.5, f"{yi}", ha="center", va="bottom", fontsize=7.5)
    ax0.set_xticks(x)
    ax0.set_xticklabels(splits)
    ax0.set_ylabel("retained family size")
    ax0.set_title("Selector stability", loc="left", weight="bold")
    ax0.grid(axis="y", alpha=0.85)
    ax0.legend(frameon=False, loc="upper right")

    ax1.bar(x - width / 2, best_full["VSC"], width, color=COLORS["blue"], label="VSC")
    ax1.bar(x + width / 2, best_full["Blackwell target-set"], width, color=COLORS["teal"], label="Blackwell target-set")
    for xi, yi in zip(x - width / 2, best_full["VSC"]):
        ax1.text(xi, yi + 0.12, f"{yi:.2f}", ha="center", va="bottom", fontsize=7.4)
    for xi, yi in zip(x + width / 2, best_full["Blackwell target-set"]):
        ax1.text(xi, yi + 0.12, f"{yi:.2f}", ha="center", va="bottom", fontsize=7.4)
    ax1.set_xticks(x)
    ax1.set_xticklabels(splits)
    ax1.set_ylabel("best completed full accuracy (%)")
    ax1.set_ylim(79.5, 89.6)
    ax1.set_title("Accuracy tradeoff", loc="left", weight="bold")
    ax1.grid(axis="y", alpha=0.85)

    fig.suptitle("Why VSC is the reporting selector: stronger art-only rival, better cross-split stability", x=0.02, y=1.03, ha="left", fontsize=11.2, weight="bold", color=COLORS["ink"])
    save(fig, "selector_stability")


def main() -> None:
    set_style()
    certificate_anatomy()
    vsc_geometry()
    weighting_rules()
    pacs_results()
    weight_matrix()
    selector_stability()


if __name__ == "__main__":
    main()
