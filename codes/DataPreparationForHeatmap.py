import pandas as pd
import numpy as np

CSV_IN  = r"C:\Users\topgu\Desktop\Art\OSTATNIE ARTYKULY\BIOSTYMULACJA\WYNIKI BIOSTYMULACJA\MERGE\differences.csv"
CSV_OUT = r"C:\summary_plus_minus_by_variety_index_combination30B.csv"

# Filtr jak w figurach
FILTER_ALTITUDE = 50
FILTER_ANNOTATION = "Bounded"

METRICS = ["d12", "d23", "d34", "p12_%", "p23_%", "p34_%"]

def sum_plus(series):
    s = series.dropna()
    return float(s[s > 0].sum())

def sum_minus_abs(series):
    s = series.dropna()
    return float((-s[s < 0]).sum())

def main():
    df = pd.read_csv(CSV_IN)

    # filtr
    df = df[
        (df["altitude_m"] == FILTER_ALTITUDE) &
        (df["annotation_method"] == FILTER_ANNOTATION)
    ].copy()

    required = ["variety", "index", "combination"] + METRICS
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Brakuje kolumn: {missing}")

    rows = []

    for (variety, index, combination), g in df.groupby(
        ["variety", "index", "combination"], dropna=False
    ):
        out = {
            "variety": variety,
            "index": index,
            "combination": combination,
            "altitude_m": FILTER_ALTITUDE,
            "annotation_method": FILTER_ANNOTATION
        }

        for m in METRICS:
            out[f"{m}_plus_sum"] = sum_plus(g[m])
            out[f"{m}_minus_sum"] = sum_minus_abs(g[m])

        rows.append(out)

    out_df = (
        pd.DataFrame(rows)
        .sort_values(["variety", "index", "combination"])
        .reset_index(drop=True)
    )

    out_df.to_csv(CSV_OUT, index=False)

    print("✅ Saved.")
    print(f"📁 {CSV_OUT}")
    print(f"📊 Lines: {len(out_df)}")

if __name__ == "__main__":
    main()
