import pandas as pd

INPUT = r"C:/.csv"
OUTPUT = r"C:/.csv"

GROUP_COLS = [
    "variety",
    "altitude_m",
    "annotation_method",
    "index_name",
    "Type"
]

df = pd.read_csv(INPUT)

out = (
    df.groupby(GROUP_COLS)
    .agg(
        Mean_index_mean=("Mean index value", "mean"),
        SD_mean=("Index value SD", "mean"),
        CV_mean=("CV", "mean"),
        n=("Mean index value", "count")
    )
    .reset_index()
)

out.to_csv(OUTPUT, index=False)

print("Save:", OUTPUT)
