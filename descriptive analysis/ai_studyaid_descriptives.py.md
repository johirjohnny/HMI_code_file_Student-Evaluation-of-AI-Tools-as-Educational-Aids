### Save as ai\_studyaid\_descriptives.py.



##### Code: 



\#!/usr/bin/env python3

\# -\*- coding: utf-8 -\*-

"""

ai\_studyaid\_descriptives.py



Reverse-codes selected Likert items, builds composite scales,

exports descriptive tables (CSV) and plots (PNG) for:

\- Four composites (usage frequency, perceived usefulness, ethics, evaluation)

\- Weekly share (UF07) distribution

\- Demographics (SD03, SD04, SD05, SD06)



Run:

&nbsp; python ai\_studyaid\_descriptives.py --excel path/to/survey.xlsx --sheet test489968 --out ai\_studyaid\_descriptives\_out



Requirements:

&nbsp; python>=3.9, pandas, numpy, matplotlib, openpyxl

"""



import os

import argparse

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt



\# ------------- CLI -------------

def parse\_args():

&nbsp;   ap = argparse.ArgumentParser(description="Descriptives + plots for AI Study Aid survey.")

&nbsp;   ap.add\_argument("--excel", required=True, help="Path to Excel file (.xlsx/.xls/.xlsm).")

&nbsp;   ap.add\_argument("--sheet", default=None, help="Sheet name (default: first sheet).")

&nbsp;   ap.add\_argument("--out", default="ai\_studyaid\_descriptives\_out", help="Output directory.")

&nbsp;   ap.add\_argument("--dpi", type=int, default=200, help="DPI for saved figures.")

&nbsp;   ap.add\_argument("--binsize", type=float, default=0.25, help="Bin width for composite histograms.")

&nbsp;   return ap.parse\_args()



\# ------------- Config -------------

LIKERT\_MIN, LIKERT\_MAX = 1, 5



\# Item blocks

UF06 = \["UF06\_01", "UF06\_02", "UF06\_03", "UF06\_04"]                       # usage frequency

PU06 = \["PU06\_01", "PU06\_02", "PU06\_03", "PU06\_04", "PU06\_05"]             # perceived usefulness

EP06 = \["EP06\_01", "EP06\_02", "EP06\_03", "EP06\_04", "EP06\_05", "EP06\_06"]  # ethics (some reversed)

HL10 = \["HL10\_01", "HL10\_02", "HL10\_03", "HL10\_04", "HL10\_05", "HL10\_06", "HL10\_07", "HL10\_08"]  # evaluation



TO\_REVERSE = \["EP06\_01", "EP06\_02", "EP06\_05", "EP06\_06", "HL10\_08"]  # reverse-coded (1–5)



COMPOSITE\_LABELS = \[

&nbsp;   "Frequency of AI usage",

&nbsp;   "Perceived usefulness",

&nbsp;   "Ethical perceptions",

&nbsp;   "Evaluation of AI as a study aid",

]



DEMOGRAPHIC\_COLS = \["SD03", "SD04", "SD05", "SD06"]  # Age, Education level, Field of study, Gender (adjust as needed)



UF07\_COL = "UF07"  # weekly share categories column

UF07\_ORDER = \["<10%", "10–30%", "30–60%", "60–90%", ">90%"]



\# ------------- Helpers -------------

def reverse\_code(series, lo=LIKERT\_MIN, hi=LIKERT\_MAX):

&nbsp;   """Reverse-code a Likert series (1..5 -> 5..1)."""

&nbsp;   return (hi + lo) - series



def comp\_mean(frame: pd.DataFrame, items, min\_ratio=0.5, suffix="\_R"):

&nbsp;   """Row-wise mean if at least min\_ratio of items present. Uses \*\_R columns by default."""

&nbsp;   cols = \[f"{i}{suffix}" for i in items if f"{i}{suffix}" in frame.columns]

&nbsp;   m = frame\[cols].mean(axis=1)

&nbsp;   n = frame\[cols].count(axis=1)

&nbsp;   needed = np.ceil(len(cols) \* min\_ratio)

&nbsp;   return m.where(n >= needed)



def hist\_with\_stats(frame: pd.DataFrame, col: str, out\_dir: str, dpi: int, binsize: float):

&nbsp;   """Plot histogram and return descriptive stats dict."""

&nbsp;   s = pd.to\_numeric(frame\[col], errors="coerce").dropna()

&nbsp;   if s.empty:

&nbsp;       print(f"\[WARN] No data for {col}")

&nbsp;       return None



&nbsp;   bins = np.arange(LIKERT\_MIN, LIKERT\_MAX + 0.001, binsize)



&nbsp;   mean = s.mean(); median = s.median(); sd = s.std()

&nbsp;   q1, q3 = s.quantile(.25), s.quantile(.75)



&nbsp;   plt.figure(figsize=(7.5, 4.5))

&nbsp;   plt.hist(s, bins=bins, edgecolor="black")

&nbsp;   plt.axvline(mean,   linewidth=2, linestyle="--", label=f"Mean = {mean:.2f}")

&nbsp;   plt.axvline(median, linewidth=2, linestyle="-.",  label=f"Median = {median:.2f}")

&nbsp;   plt.gca().text(

&nbsp;       0.02, 0.95, f"SD = {sd:.2f}", transform=plt.gca().transAxes,

&nbsp;       va="top", ha="left",

&nbsp;       bbox=dict(boxstyle="round", facecolor="white", alpha=0.7, linewidth=0.5)

&nbsp;   )

&nbsp;   plt.title(col)

&nbsp;   plt.xlabel("Scale score"); plt.ylabel("Count")

&nbsp;   plt.legend(); plt.tight\_layout()

&nbsp;   fname = os.path.join(out\_dir, f"hist\_{col.replace(' ', '\_')}.png")

&nbsp;   plt.savefig(fname, dpi=dpi)

&nbsp;   plt.close()



&nbsp;   return {

&nbsp;       "Scale": col, "N": int(s.count()), "Mean": mean, "Median": median, "SD": sd,

&nbsp;       "Min": s.min(), "Q1": q1, "Q3": q3, "Max": s.max(), "IQR": q3 - q1

&nbsp;   }



\# ------------- Main -------------

def main():

&nbsp;   args = parse\_args()

&nbsp;   out\_dir = os.path.abspath(args.out)

&nbsp;   plot\_dir = os.path.join(out\_dir, "plots\_histogram\_scales")

&nbsp;   demo\_dir = os.path.join(out\_dir, "demographics")

&nbsp;   os.makedirs(out\_dir, exist\_ok=True)

&nbsp;   os.makedirs(plot\_dir, exist\_ok=True)

&nbsp;   os.makedirs(demo\_dir, exist\_ok=True)



&nbsp;   # Load Excel

&nbsp;   xl = pd.ExcelFile(args.excel)

&nbsp;   sheet = args.sheet if args.sheet else xl.sheet\_names\[0]

&nbsp;   df = xl.parse(sheet)

&nbsp;   # If exported with a header row + an index row, drop first row as in your Colab logic

&nbsp;   # (Uncomment next line if needed)

&nbsp;   # df = df.iloc\[1:].reset\_index(drop=True)



&nbsp;   # Collect all item columns present

&nbsp;   all\_items = \[c for c in set(UF06 + PU06 + EP06 + HL10) if c in df.columns]

&nbsp;   df\[all\_items] = df\[all\_items].apply(pd.to\_numeric, errors="coerce")



&nbsp;   # Reverse-code to \*\_R copies

&nbsp;   for c in all\_items:

&nbsp;       df\[c + "\_R"] = reverse\_code(df\[c]) if c in TO\_REVERSE and c in df.columns else df\[c]



&nbsp;   print("Reversed items found:", \[c for c in TO\_REVERSE if c in df.columns])



&nbsp;   # Build composites (overwrite if pre-existing)

&nbsp;   for col in COMPOSITE\_LABELS:

&nbsp;       if col in df.columns:

&nbsp;           del df\[col]



&nbsp;   df\["Frequency of AI usage"]            = comp\_mean(df, UF06)

&nbsp;   df\["Perceived usefulness"]             = comp\_mean(df, PU06)

&nbsp;   df\["Ethical perceptions"]              = comp\_mean(df, EP06)

&nbsp;   df\["Evaluation of AI as a study aid"]  = comp\_mean(df, HL10)



&nbsp;   scale\_cols = COMPOSITE\_LABELS



&nbsp;   # Histograms + summary table

&nbsp;   rows = \[]

&nbsp;   for c in scale\_cols:

&nbsp;       stats = hist\_with\_stats(df, c, plot\_dir, args.dpi, args.binsize)

&nbsp;       if stats:

&nbsp;           rows.append(stats)



&nbsp;   summary = pd.DataFrame(rows)\[\["Scale","N","Mean","Median","SD","Min","Q1","Q3","Max","IQR"]]

&nbsp;   # Round for readability

&nbsp;   summary\_round = summary.copy()

&nbsp;   summary\_round\[\["Mean","Median","SD","Min","Q1","Q3","Max","IQR"]] = summary\_round\[

&nbsp;       \["Mean","Median","SD","Min","Q1","Q3","Max","IQR"]

&nbsp;   ].astype(float).round(3)



&nbsp;   csv\_summary = os.path.join(out\_dir, "composite\_summary\_after\_reverse.csv")

&nbsp;   summary\_round.to\_csv(csv\_summary, index=False)

&nbsp;   print("✅ Saved composite summary to:", csv\_summary)

&nbsp;   print("✅ Saved histograms to:", plot\_dir)



&nbsp;   # Weekly share UF07 (if present)

&nbsp;   if UF07\_COL in df.columns:

&nbsp;       valid = df\[UF07\_COL].dropna()

&nbsp;       freq = valid.value\_counts().reindex(UF07\_ORDER, fill\_value=0)

&nbsp;       pct = (freq / freq.sum() \* 100)



&nbsp;       table\_full = pd.DataFrame({

&nbsp;           "Category": UF07\_ORDER,

&nbsp;           "n": freq.values,

&nbsp;           "%": pct.values.round(1)

&nbsp;       })

&nbsp;       table\_min = table\_full\[\["Category", "%"]].copy()



&nbsp;       csv\_full = os.path.join(out\_dir, "UF07\_frequencies\_VALID\_full.csv")

&nbsp;       csv\_min  = os.path.join(out\_dir, "UF07\_frequencies\_VALID\_minimal.csv")

&nbsp;       table\_full.to\_csv(csv\_full, index=False)

&nbsp;       table\_min.to\_csv(csv\_min, index=False)

&nbsp;       print("✅ Saved UF07 tables:")

&nbsp;       print("   -", csv\_full)

&nbsp;       print("   -", csv\_min)



&nbsp;       # Horizontal bar chart (percent only)

&nbsp;       palette = \["#F28E2B", "#59A14F", "#E15759", "#B07AA1", "#EDC948"]

&nbsp;       fig, ax = plt.subplots(figsize=(7.2, 4.4), dpi=args.dpi)

&nbsp;       ax.barh(table\_min\["Category"], table\_min\["%"], edgecolor="black", color=palette)



&nbsp;       max\_pct = table\_min\["%"].max()

&nbsp;       offset = max(0.8, max\_pct \* 0.02)

&nbsp;       for i, p in enumerate(table\_min\["%"]):

&nbsp;           ax.text(p + offset, i, f"{p:.1f}%", va="center", fontsize=11)



&nbsp;       ax.set\_title("AI use across weekly study sessions", pad=6, fontsize=12)

&nbsp;       ax.set\_xlabel(""); ax.set\_ylabel("")

&nbsp;       ax.set\_xlim(0, max(5, max\_pct + 10))

&nbsp;       ax.grid(axis="x", linestyle=":", alpha=.35)

&nbsp;       plt.tight\_layout()

&nbsp;       bar\_path = os.path.join(out\_dir, "UF07\_horizontal\_bar\_percent\_only\_titled.png")

&nbsp;       plt.savefig(bar\_path, dpi=args.dpi, bbox\_inches="tight")

&nbsp;       plt.close()

&nbsp;       print("✅ Saved UF07 chart:", bar\_path)

&nbsp;   else:

&nbsp;       print(f"\[WARN] Column '{UF07\_COL}' not found; skipping UF07 plots/tables.")



&nbsp;   # Demographics tables + plots

&nbsp;   demo\_vars = \[c for c in DEMOGRAPHIC\_COLS if c in df.columns]

&nbsp;   demo\_summary = {}



&nbsp;   for col in demo\_vars:

&nbsp;       if pd.api.types.is\_numeric\_dtype(df\[col]):

&nbsp;           # numeric -> full descriptive stats

&nbsp;           stats = df\[col].describe().rename({

&nbsp;               "count": "N", "mean": "Mean", "std": "SD",

&nbsp;               "min": "Min", "25%": "Q1", "50%": "Median", "75%": "Q3", "max": "Max"

&nbsp;           })

&nbsp;           demo\_summary\[col] = stats

&nbsp;           stats.to\_csv(os.path.join(demo\_dir, f"{col}\_descriptives.csv"))

&nbsp;       else:

&nbsp;           # categorical -> frequency counts

&nbsp;           freq = df\[col].value\_counts(dropna=False)

&nbsp;           pct = (freq / freq.sum() \* 100).round(2)

&nbsp;           tbl = pd.DataFrame({"n": freq, "%": pct})

&nbsp;           demo\_summary\[col] = tbl

&nbsp;           tbl.to\_csv(os.path.join(demo\_dir, f"{col}\_frequencies.csv"))



&nbsp;       # Plots

&nbsp;       plt.figure(figsize=(6, 4))

&nbsp;       if pd.api.types.is\_numeric\_dtype(df\[col]):

&nbsp;           plt.hist(df\[col].dropna(), bins=10, edgecolor="black")

&nbsp;           plt.ylabel("Count"); plt.title(f"Histogram — {col}")

&nbsp;       else:

&nbsp;           freq = df\[col].value\_counts()

&nbsp;           plt.bar(freq.index.astype(str), freq.values)

&nbsp;           plt.ylabel("Count"); plt.title(f"{col}")

&nbsp;           plt.xticks(rotation=30, ha="right")

&nbsp;       plt.tight\_layout()

&nbsp;       plot\_path = os.path.join(demo\_dir, f"{col}\_plot.png")

&nbsp;       plt.savefig(plot\_path, dpi=args.dpi)

&nbsp;       plt.close()



&nbsp;   print("✅ Demographic tables \& plots saved in:", demo\_dir)

&nbsp;   print("🎉 Done.")



if \_\_name\_\_ == "\_\_main\_\_":

&nbsp;   main()



### Save this as README.md:



\# AI Study Aid — Descriptives



This repository contains a Python script (`ai\_studyaid\_descriptives.py`) that processes survey data from SoSci Survey (or similar platforms) to:

\- Reverse-code selected Likert-scale items

\- Compute composite scales (Frequency of AI usage, Perceived usefulness, Ethical perceptions, Evaluation of AI as a study aid)

\- Generate descriptive statistics (CSV tables)

\- Create visualizations (histograms, horizontal bar charts)

\- Summarize demographic variables with tables and plots



It is designed to support research on AI adoption and perceptions in higher education.



---



\## Features

\- \*\*Reverse-coding:\*\* Automatically adjusts negatively worded items (Likert 1–5).

\- \*\*Composite scores:\*\* Builds mean scores for each construct if ≥50% of items are answered.

\- \*\*Descriptive statistics:\*\* Outputs means, medians, SD, quartiles, min/max, IQR for all constructs.

\- \*\*Visual outputs:\*\* Saves histograms for each composite, a horizontal bar chart for AI usage share (UF07), and plots/tables for demographics.

\- \*\*Customizable:\*\* Specify Excel sheet name, output directory, DPI, and histogram bin size via CLI arguments.



---



\## Requirements

\- Python ≥3.9

\- `pandas`

\- `numpy`

\- `matplotlib`

\- `openpyxl`



Install all requirements:

```bash

pip install -r requirements.txt







