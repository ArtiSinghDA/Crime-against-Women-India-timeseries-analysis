"""
Heatmap Analysis: Crime Against Women in India (2001-2021)
----------------------------------------------------------------------------
Recreates the two heatmaps from the thesis
"Crime Against Women in India: A Statistical and Comparative Study" (Chapter 6, Test-2).

Produces:
    1. Crime-type-by-Year heatmap  -> shows intensity of each crime category
       across 2001-2021 (darker = higher case count)
    2. Correlation heatmap         -> shows pairwise correlation between
       crime variables (Rape, K&A, DD, AoW, AoM, DV, WT)

Usage:
    python heatmap_analysis.py --data ../data/crime_data_2001_2021.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CRIME_TYPES = ["Rape", "K&A", "DD", "AoW", "AoM", "DV", "WT"]


def plot_year_heatmap(df, crime_cols):
    """Heatmap: rows = crime types, columns = years, values = case counts."""
    heat_data = df.set_index("Year")[crime_cols].transpose()

    plt.figure(figsize=(14, 6))
    sns.heatmap(heat_data, annot=True, fmt=".0f", cmap="YlOrRd",
                linewidths=0.5, cbar_kws={"label": "Number of Cases"})
    plt.title("Crime Against Women in India (2001-2021) — Heatmap by Year")
    plt.xlabel("Year")
    plt.ylabel("Crime Type")
    plt.tight_layout()
    plt.savefig("heatmap_by_year.png", dpi=150)
    plt.close()
    print("Saved heatmap_by_year.png")


def plot_correlation_heatmap(df, crime_cols):
    """Correlation heatmap between crime variables (and Year)."""
    corr_cols = ["Year"] + crime_cols
    corr_matrix = df[corr_cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
                vmin=0, vmax=1, linewidths=0.5)
    plt.title("Correlation Heatmap of Crime Dataset")
    plt.tight_layout()
    plt.savefig("correlation_heatmap.png", dpi=150)
    plt.close()
    print("Saved correlation_heatmap.png")

    return corr_matrix


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Heatmap analysis for crime data")
    parser.add_argument("--data", required=True, help="Path to crime data CSV (Year + crime columns)")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    available_cols = [c for c in CRIME_TYPES if c in data.columns]

    if not available_cols:
        raise ValueError(
            f"None of the expected crime columns {CRIME_TYPES} were found in the CSV. "
            f"Available columns are: {list(data.columns)}. "
            f"Update CRIME_TYPES at the top of this script to match your data."
        )

    plot_year_heatmap(data, available_cols)
    corr_matrix = plot_correlation_heatmap(data, available_cols)

    corr_matrix.to_csv("correlation_matrix.csv")
    print("Saved correlation_matrix.csv")
