# Student Evaluation of AI Tools as Educational Aids

This repository contains analysis scripts (Python and R) used to study **how university students’ frequency of AI tool usage, perceived usefulness, and ethical perceptions influence their evaluation of AI as a helpful and legitimate study aid**.

---

## 📂 Project Structure

---

## 🔧 Requirements

### Python
- Python 3.9+  
- Libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`

Install with:
bash
pip install -r requirements.txt
R

R (4.0 or higher recommended)

Useful packages: psych, tidyverse


**
Run the correlation analysis script:**

python correlation_analysis.py
**
This will:

Reverse-code specific items (EP06_01, EP06_02, EP06_05, EP06_06, HL10_08)

Compute Pearson & Spearman correlation matrices

Save results in /outputs**
**
R

Run reliability analyses:**
source("CronbachAlphaEthics.r")
source("CronbachAlphaHelpfullness.r")
source("CronbachAlphaUsefullness.r")
📊 Key Analyses

Correlation Analysis: Examines relationships between Frequency, Usefulness, Ethics, and Evaluation composites.

Reliability (Cronbach’s Alpha): Evaluates internal consistency of multi-item scales.

📝 Notes

Dataset files (*.csv) are ignored by Git and not included in this repo.

Reverse-coded items: EP06_01, EP06_02, EP06_05, EP06_06, HL10_08.

See outputs folder for saved correlation tables and heatmaps.


