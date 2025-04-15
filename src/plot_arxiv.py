from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots

THIS_DIR = Path(__file__).resolve().parent
ROOT = THIS_DIR.parent
FIGURES_DIR = ROOT / "assets" / "figures"
FIGURES_DIR.mkdir(exist_ok=True)
figure_file = FIGURES_DIR / "arxiv_per_year.png"

OUTPUTS_DIR = ROOT / "outputs"
csv_file = OUTPUTS_DIR / "arxiv_papers.csv"

# Load your CSV
df = pd.read_csv(csv_file)

# Check the structure
print(df.head())

# Convert year column to string (if not already)
df["year"] = df["year"].astype(str)

# Count papers per year
papers_per_year = df["year"].value_counts().sort_index()

plt.style.use(["science", "no-latex"])

# Plot
plt.figure(figsize=(4, 2))
papers_per_year.plot(kind="bar")

plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.title("Number of Papers per Year (arxiv physics.acc-ph)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(figure_file, dpi=300)
