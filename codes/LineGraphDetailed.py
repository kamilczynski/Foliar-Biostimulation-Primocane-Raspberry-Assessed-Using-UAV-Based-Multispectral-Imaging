import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Patch



CSV_PATH = r"C:\.csv"
OUTPUT_DIR = r"C:\"
os.makedirs(OUTPUT_DIR, exist_ok=True)




ALTITUDE = 50
ANNOTATION = "Bounded"

VALUE_COLS = ["p12_%", "p23_%", "p34_%"]

BAR_HEIGHT = 2.4
BAR_SPACING = 2.6
MEAS_GAP = 0.4
TREAT_GAP = 1.5

POS_COLOR = "#ffb3b3"
NEG_COLOR = "#b3d9ff"

label_mapping = {
    "CONTROL": "Control",
    "NATURAL": "Animal-derived amino acids",
    "KAISHI": "Plant-derived amino acids",
    "VALKIRIA": "Seaweed extract",
    "KUMA": "Seaweed extract + Animal-derived amino acids"
}



df = pd.read_csv(CSV_PATH)

df = df[
    (df["altitude_m"] == ALTITUDE) &
    (df["annotation_method"] == ANNOTATION)
].copy()

indices = sorted(df["index"].unique())

varieties = ["Enrosadira", "Polonez", "Husaria"]

variety_display_names = {
    "Enrosadira": "(a) Enrosadira",
    "Polonez": "(b) Polonez",
    "Husaria": "(c) Husaria"
}

treatments = sorted(df["treatment_no"].unique())
combinations = ["CONTROL", "NATURAL", "KAISHI", "VALKIRIA", "KUMA"]

comb_color = {
    "CONTROL": "#E10600",
    "NATURAL": "#FF8C00",
    "KAISHI": "#2E8B57",
    "VALKIRIA": "#0000FF",
    "KUMA": "#B7410E"
}



for INDEX_TO_PLOT in indices:

    sub_index = df[df["index"] == INDEX_TO_PLOT]
    sub_index_plot = sub_index[sub_index["variety"].isin(varieties)].copy()

    all_vals = sub_index_plot[VALUE_COLS].values.flatten()
    all_vals = all_vals[~np.isnan(all_vals)]
    if len(all_vals) == 0:
        continue

    global_max = np.max(np.abs(all_vals))

    if global_max <= 5:
        step = 0.5
    elif global_max <= 10:
        step = 1
    elif global_max <= 25:
        step = 2
    elif global_max <= 50:
        step = 5
    else:
        step = 10

    limit = np.ceil(global_max / step) * step

    fig, axes = plt.subplots(
        1, len(varieties),
        figsize=(12, 10),
        sharex=True
    )

    if len(varieties) == 1:
        axes = [axes]

    for ax_i, (ax, variety) in enumerate(zip(axes, varieties)):

        sub_var = sub_index_plot[sub_index_plot["variety"] == variety]

        y = 0
        y_positions = []
        y_labels = []

        for t_i, t in enumerate(treatments):

            # 🔹 zapamiętujemy pozycję nagłówka T
            treatment_center = None
            treatment_start = y

            sub_t = sub_var[sub_var["treatment_no"] == t]

            for comb_i, comb in enumerate(combinations):

                row = sub_t[sub_t["combination"] == comb]
                if row.empty:
                    continue

                for step_col in VALUE_COLS:

                    val = row[step_col].values[0]
                    abs_val = abs(val)
                    sign_fill = POS_COLOR if val > 0 else NEG_COLOR

                    ax.barh(
                        y,
                        abs_val,
                        height=BAR_HEIGHT,
                        align='edge',
                        color=comb_color[comb]
                    )

                    ax.barh(
                        y,
                        limit - abs_val,
                        left=abs_val,
                        height=BAR_HEIGHT,
                        align='edge',
                        color=sign_fill,
                        alpha=0.45
                    )

                    if ax_i == 0:
                        y_positions.append(y + BAR_HEIGHT / 2)
                        #clean_label = step_col.replace("_%", "").upper()
                        clean_label = step_col.replace("p", "D").replace("_%", "").upper()
                        y_labels.append(f"   {clean_label}")  # wcięcie

                    y += BAR_SPACING

                if comb_i < len(combinations) - 1:
                    y += MEAS_GAP

            treatment_end = y
            treatment_center = (treatment_start + treatment_end) / 2

            if ax_i == 0:
                 🔹
                ax.text(
                    -limit * 0.16,  
                    treatment_center,
                    f"T{t}",
                    fontsize=9,
                    weight='bold',
                    va='center'
                )

            if t_i < len(treatments) - 1:
                y += TREAT_GAP

        ax.set_xlim(0, limit)
        ax.set_ylim(0, y)
        ax.set_xticks(np.arange(0, limit + step, step))
        ax.grid(axis='x', linestyle='-', linewidth=0.5, alpha=0.25)

        ax.set_axisbelow(True)
        ax.set_title(variety_display_names[variety], fontsize=12)
        ax.set_xlabel("Relative change (%)", fontsize=11)

        if ax_i == 0:
            ax.set_yticks(y_positions)
            ax.set_yticklabels(y_labels, fontsize=7)
        else:
            ax.set_yticks([])



    legend_elements = [
        Patch(facecolor=comb_color["CONTROL"], label=label_mapping["CONTROL"]),
        Patch(facecolor=comb_color["NATURAL"], label=label_mapping["NATURAL"]),
        Patch(facecolor=comb_color["KAISHI"], label=label_mapping["KAISHI"]),
        Patch(facecolor=comb_color["VALKIRIA"], label=label_mapping["VALKIRIA"]),
        Patch(facecolor=comb_color["KUMA"], label=label_mapping["KUMA"]),
        Patch(facecolor='none', edgecolor='none', label=""),
        Patch(facecolor=POS_COLOR, label="Positive change"),
        Patch(facecolor=NEG_COLOR, label="Negative change"),
    ]

    fig.legend(
        handles=legend_elements,
        loc="lower center",
        ncol=4,
        frameon=False,
        columnspacing=3,
        handlelength=1.8,
        bbox_to_anchor=(0.5, 0.06)
    )

    plt.tight_layout(rect=[0.07, 0.13, 1, 0.95])

    base_path = os.path.join(
        OUTPUT_DIR,
        f"{INDEX_TO_PLOT}_{ALTITUDE}_{ANNOTATION}"
    )

    plt.savefig(base_path + ".png", dpi=300)
    plt.savefig(base_path + ".svg")

    plt.close()

print("✅ Publication-ready version with compact T1–P12 style labels generated.")
