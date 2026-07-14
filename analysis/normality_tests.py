"""
Normality Tests: Crime Against Women in India (2001 vs 2021)
----------------------------------------------------------------------------
Recreates the Shapiro-Wilk and Kolmogorov-Smirnov normality checks from the
thesis "Crime Against Women in India: A Statistical and Comparative Study".

H0: The data follows a normal distribution.
H1: The data does not follow a normal distribution.

Usage:
    python normality_tests.py --data ../data/crime_data_2001_2021.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, kstest, norm

ALPHA = 0.05


def test_year(df, year, total_column="Total_Cases"):
    """Run Shapiro-Wilk and K-S tests for a given year's state-wise totals."""
    year_data = df[df["Year"] == year][total_column].dropna()

    shapiro_stat, shapiro_p = shapiro(year_data)
    ks_stat, ks_p = kstest(year_data, "norm",
                            args=(year_data.mean(), year_data.std()))

    print(f"\n=== Normality Test for {year} ===")
    print(f"Shapiro-Wilk: W = {shapiro_stat:.4f}, p = {shapiro_p:.5f}  "
          f"-> {'Normal' if shapiro_p > ALPHA else 'Not Normal'}")
    print(f"Kolmogorov-Smirnov: D = {ks_stat:.4f}, p = {ks_p:.5f}  "
          f"-> {'Normal' if ks_p > ALPHA else 'Not Normal'}")

    # Histogram with fitted normal curve, matching the thesis SPSS output style
    plt.figure(figsize=(8, 5))
    sns.histplot(year_data, bins=8, stat="count", color="#3E7CB1", edgecolor="white")
    x = pd.Series(range(int(year_data.min()), int(year_data.max()), 100))
    plt.title(f"Distribution of Total Crime Cases by State — {year}")
    plt.xlabel(f"Total Cases in {year}")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(f"histogram_{year}.png", dpi=150)
    plt.close()
    print(f"Saved histogram_{year}.png")

    return {
        "Year": year,
        "Shapiro_W": round(shapiro_stat, 4),
        "Shapiro_p": round(shapiro_p, 5),
        "KS_D": round(ks_stat, 4),
        "KS_p": round(ks_p, 5),
        "Conclusion": "Not Normal" if shapiro_p < ALPHA else "Normal",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normality tests on state-wise crime totals")
    parser.add_argument("--data", required=True, help="Path to crime data CSV")
    parser.add_argument("--years", nargs="+", type=int, default=[2001, 2021],
                         help="Years to test, e.g. --years 2001 2021")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    results = [test_year(data, y) for y in args.years]

    summary = pd.DataFrame(results)
    print("\n=== Summary ===")
    print(summary.to_string(index=False))
    summary.to_csv("normality_test_summary.csv", index=False)
