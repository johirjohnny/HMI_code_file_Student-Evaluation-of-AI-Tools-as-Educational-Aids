# === Correlation analysis for the AI-usage study (targeted reverse-coding) ===
# Reverse-coded items in this version:
#   EP06_01, EP06_02, EP06_05, EP06_06  (Ethics; 1<->5)
#   HL10_08                              (Evaluation; 1<->5)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# 0) CONFIG
# ----------------------------
# Use a raw string for Windows paths to avoid invalid escape sequences
DATA_PATH = r"D:\FUAS\Summer 25\HMI\data_test489968_2025-08-22_12-49.csv"  # <- change if needed
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

# Reverse-coding lists (exact columns you requested)
EP06_ITEMS_TO_REVERSE = ["EP06_01", "EP06_02", "EP06_05", "EP06_06"]
HL10_ITEMS_TO_REVERSE = ["HL10_08"]

# ----------------------------
# 1) LOAD DATA (UTF-16 TSV)
# ----------------------------
df = pd.read_csv(DATA_PATH, sep="\t", encoding="utf-16")

# ----------------------------
# 2) DEFINE ITEM GROUPS
# ----------------------------
UF_cols = [c for c in df.columns if c.startswith("UF06_")]  # Frequency
PU_cols = [c for c in df.columns if c.startswith("PU06_")]  # Usefulness
EP_cols = [c for c in df.columns if c.startswith("EP06_")]  # Ethics
HL_cols = [c for c in df.columns if c.startswith("HL10_")]  # Evaluation

print("Detected items:")
print("  Frequency (UF):", UF_cols)
print("  Usefulness (PU):", PU_cols)
print("  Ethics (EP):    ", EP_cols)
print("  Evaluation (HL):", HL_cols)

# ----------------------------
# 3) REVERSE-CODE REQUESTED ITEMS
# ----------------------------
def reverse_1_to_5(series: pd.Series) -> pd.Series:
    # Reverse 1..5 Likert into 5..1, keep NaNs untouched
    return series.replace({1:5, 2:4, 3:3, 4:2, 5:1})

actually_reversed_ep = []
for col in EP06_ITEMS_TO_REVERSE:
    if col in df.columns:
        df[col] = reverse_1_to_5(df[col])
        actually_reversed_ep.append(col)

actually_reversed_hl = []
for col in HL10_ITEMS_TO_REVERSE:
    if col in df.columns:
        df[col] = reverse_1_to_5(df[col])
        actually_reversed_hl.append(col)

print("\nReverse-coded items:")
print("  EP06 reversed:", actually_reversed_ep if actually_reversed_ep else "None found")
print("  HL10 reversed:", actually_reversed_hl if actually_reversed_hl else "None found")

# ----------------------------
# 4) COMPOSITE SCORES
# ----------------------------
composites = pd.DataFrame(index=df.index)

if UF_cols:
    composites["Frequency_mean"] = df[UF_cols].mean(axis=1, skipna=True)
if PU_cols:
    composites["Usefulness_mean"] = df[PU_cols].mean(axis=1, skipna=True)
if EP_cols:
    composites["Ethics_mean"] = df[EP_cols].mean(axis=1, skipna=True)
if HL_cols:
    composites["Evaluation_mean"] = df[HL_cols].mean(axis=1, skipna=True)

# Drop rows where all composites are NaN
composites = composites.dropna(how="all")

print("\nComposite head:")
try:
    display(composites.head())
except NameError:
    print(composites.head())

# ----------------------------
# 5) CORRELATIONS
# ----------------------------
pearson_corr  = composites.corr(method="pearson")
spearman_corr = composites.corr(method="spearman")

try:
    display(pearson_corr.round(3))
    display(spearman_corr.round(3))
except NameError:
    print("\nPearson correlations:\n", pearson_corr.round(3))
    print("\nSpearman correlations:\n", spearman_corr.round(3))

# Save tables
pearson_path  = OUTPUT_DIR / "construct_correlations_pearson.csv"
spearman_path = OUTPUT_DIR / "construct_correlations_spearman.csv"
composites_path = OUTPUT_DIR / "composite_scores.csv"
pearson_corr.to_csv(pearson_path)
spearman_corr.to_csv(spearman_path)
composites.to_csv(composites_path, index=False)

print(f"\nSaved: {pearson_path}")
print(f"Saved: {spearman_path}")
print(f"Saved: {composites_path}")

# ----------------------------
# 6) SINGLE HEATMAP (PEARSON)
# ----------------------------
fig = plt.figure(figsize=(6.5, 5.5))  # one figure, no subplots
plt.imshow(pearson_corr, interpolation="nearest")
plt.title("Correlation Heatmap (Pearson) — AI Study Constructs")
labels = list(pearson_corr.columns)
plt.xticks(ticks=np.arange(len(labels)), labels=labels, rotation=45, ha="right")
plt.yticks(ticks=np.arange(len(labels)), labels=labels)

# Annotate cells
for i in range(len(labels)):
    for j in range(len(labels)):
        val = pearson_corr.iloc[i, j]
        if pd.notnull(val):
            plt.text(j, i, f"{val:.2f}", ha="center", va="center")

plt.tight_layout()
heatmap_path = OUTPUT_DIR / "construct_correlation_heatmap.png"
plt.savefig(heatmap_path, dpi=200, bbox_inches="tight")
plt.show()
print(f"Saved: {heatmap_path}")

# ----------------------------
# 7) QUICK INTERPRETATION HINTS
# ----------------------------
print("\nInterpretation tips:")
print("- Pearson: linear association (treats composites as interval).")
print("- Spearman: rank-based; robust if Likert/ordinal or non-normal.")
print("- With EP06_01, _02, _05, _06 and HL10_08 reversed, all constructs should now align directionally.")
