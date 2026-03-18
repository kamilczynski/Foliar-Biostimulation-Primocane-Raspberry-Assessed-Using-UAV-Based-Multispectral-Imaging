import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
from matplotlib.patches import FancyBboxPatch



CSV_PATH = r"C:\30B.csv"
OUTPUT_DIR = r"C:\30B"
os.makedirs(OUTPUT_DIR, exist_ok=True)



FONT_PANEL = 12
FONT_COMBINATION = 11
FONT_VALUES = 11
FONT_RANK = 10
FONT_AXIS = 11
FONT_COLORBAR = 11



panel_labels = {
    "Enrosadira": "(a) Enrosadira",
    "Polonez": "(b) Polonez",
    "Husaria": "(c) Husaria"
}



label_mapping = {
    "CONTROL": "C",
    "NATURAL": "AAA",
    "KAISHI": "PAA",
    "VALKIRIA": "SW",
    "KUMA": "SW+AAA"
}



df = pd.read_csv(CSV_PATH)

indices = [
    "GNDVI", "LCI", "MCARI", "MCARI2",
    "NDRE", "NDVI", "OSAVI", "SIPI2"
]

varieties = ["Enrosadira", "Polonez", "Husaria"]
combinations = ["CONTROL", "NATURAL", "KAISHI", "VALKIRIA", "KUMA"]
letters = ["1", "2", "3", "4", "5"]



green_scale = {
    "1": "#00441b",
    "2": "#1b7837",
    "3": "#5aae61",
    "4": "#a6dba0",
    "5": "#e5f5e0"
}
orange_scale = {
    "1": "#b35806",
    "2": "#e08214",
    "3": "#fdb863",
    "4": "#fddbc7",
    "5": "#fff5eb"
}



def clean_value(v):
    if abs(v) < 0.0005:
        return "0.000"
    return f"{v:.2f}"



def rank_values(values, positive=True):

    values = np.array(values)

    if positive:
        sorted_unique = sorted(set(values), reverse=True)
    else:
        sorted_unique = sorted(set(values), reverse=True)

    ranks = [""] * len(values)

    for letter, val in zip(letters, sorted_unique):
        indices_same = np.where(values == val)[0]
        for idx in indices_same:
            ranks[idx] = letter

    return ranks




for index_name in indices:

    sub = df[df["index"] == index_name]

    data = []
    labels = []
    letters_matrix = []
    variety_positions = []

    for v_i, variety in enumerate(varieties):

        block_values = []

        for comb in combinations:

            row = sub[
                (sub["variety"] == variety) &
                (sub["combination"] == comb)
            ]

            if not row.empty:
                r = row.iloc[0]

                values = [
                    r["p12_%_plus_sum"],
                    -r["p12_%_minus_sum"],
                    r["p23_%_plus_sum"],
                    -r["p23_%_minus_sum"],
                    r["p34_%_plus_sum"],
                    -r["p34_%_minus_sum"]
                ]

                block_values.append(values)

        block = np.array(block_values)

        col_ranks = []
        for col in range(block.shape[1]):

            column_values = block[:, col]

            if col in [0, 2, 4]:
                ranks = rank_values(column_values, positive=True)
            else:
                ranks = rank_values(column_values, positive=False)

            col_ranks.append(ranks)

        col_ranks = np.array(col_ranks).T

        variety_positions.append(len(data))

        for i, comb in enumerate(combinations):
            data.append(block[i])
            letters_matrix.append(col_ranks[i])
            labels.append(label_mapping.get(comb, comb))

        if v_i < len(varieties) - 1:
            data.append([np.nan] * 6)
            letters_matrix.append([""] * 6)
            labels.append("")

    data = np.array(data)
    letters_matrix = np.array(letters_matrix)

    vmax = np.nanmax(np.abs(data))
    vmin = -vmax

    fig, ax = plt.subplots(figsize=(11, 10))

    heat = sns.heatmap(
        data,
        cmap="bwr",
        center=0,
        vmin=vmin,
        vmax=vmax,
        annot=False,
        linewidths=0.4,
        cbar_kws={"label": "Change (%)"},
        ax=ax
    )

    heat.collections[0].colorbar.ax.tick_params(labelsize=FONT_COLORBAR)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):

            if np.isnan(data[i, j]):
                continue

            value = data[i, j]
            letter = letters_matrix[i, j]

            

            norm_val = (value - vmin) / (vmax - vmin)

            if value < 0 and norm_val < 0.25:
                text_color = "white"
            else:
                text_color = "black"

            
            if j in [0, 2, 4]:  
                rank_color = green_scale[letter]
            else:  
                rank_color = orange_scale[letter]

            box = FancyBboxPatch(
                (j + 0.75, i + 0.05),
                0.2,
                0.26,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                linewidth=0,
                facecolor=rank_color,
                zorder=5
            )
            ax.add_patch(box)

            ax.text(
                j + 0.85,
                i + 0.2,
                letter,
                ha="center",
                va="center",
                color="white" if letter in ["1", "2"] else "black",
                fontsize=FONT_RANK,
                fontweight="bold",
                zorder=6
            )

            ax.text(
                j + 0.5,
                i + 0.6,
                clean_value(value),
                ha="center",
                va="center",
                fontsize=FONT_VALUES,
                color=text_color
            )

    ax.set_yticks(np.arange(len(labels)) + 0.5)
    ax.set_yticklabels(labels, fontsize=FONT_COMBINATION, rotation=0)

    
    ax.tick_params(axis='y', length=4, width=0.8)

    ax.set_xticks(np.arange(6) + 0.5)
    ax.set_xticklabels(
        ["D12+", "D12−", "D23+", "D23−", "D34+", "D34−"],
        fontsize=FONT_AXIS,
        rotation=0
    )

   

    for pos, variety in zip(variety_positions, varieties):
        ax.text(
            -0.4,   
            pos - 0.4,
            panel_labels.get(variety, variety),
            ha="left",
            va="bottom",
            fontsize=FONT_PANEL
        )

    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{index_name}_heatmap_ranked_50bounded.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.savefig(
        os.path.join(OUTPUT_DIR, f"{index_name}_heatmap_ranked_50bounded.svg"),
        bbox_inches="tight"
    )

    plt.close()

print("✅ Heatmaps generated with selective contrast and corrected panel labels.")
