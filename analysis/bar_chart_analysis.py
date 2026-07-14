"""
Bar Chart Analysis: Crime Against Women in India (Chapter 5 of thesis)
----------------------------------------------------------------------------
Recreates:
    1. Period-wise average bar charts for each crime type
       (Period 1: <2010, Period 2: 2010-2015, Period 3: >2015)
    2. State-wise comparison bar charts for 2001 and 2021

Usage:
    python bar_chart_analysis.py --data ../data/crime_data_2001_2021.csv --statedata ../data/statewise_crime_data.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt

CRIME_TYPES = ["Rape", "DV", "K&A", "DD", "AoW", "AoM", "WT"]


def assign_period(year):
    if year < 2010:
        return 1
    elif 2010 <= year <= 2015:
        return 2
    else:
        return 3


def plot_period_wise_averages(df, crime_cols):
    df["Period"] = df["Year"].apply(assign_period)

    for crime in crime_cols:
        period_avg = df.groupby("Period")[crime].mean()

        plt.figure(figsize=(7, 5))
        colors = ["#3498db", "#1a5276", "#a3123a"]
        plt.bar(period_avg.index.astype(str), period_avg.values, color=colors)
        plt.title(f"Period-wise Average of {crime} Cases Reported in India (2001-2021)")
        plt.xlabel("Period")
        plt.ylabel(f"Mean of {crime} Cases")
        plt.tight_layout()
        safe_name = crime.replace("&", "and")
        plt.savefig(f"{safe_name}_period_bar.png", dpi=150)
        plt.close()
        print(f"Saved {safe_name}_period_bar.png")


def plot_statewise_comparison(state_df, year):
    year_df = state_df[state_df["Year"] == year].sort_values("Total_Cases", ascending=False)

    plt.figure(figsize=(14, 6))
    plt.bar(year_df["State"], year_df["Total_Cases"], color="#2e86c1")
    plt.title(f"State-wise Comparison of Crime Against Women in India ({year})")
    plt.xlabel("State")
    plt.ylabel("Sum Total")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"statewise_{year}.png", dpi=150)
    plt.close()
    print(f"Saved statewise_{year}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bar chart analysis for crime data")
    parser.add_argument("--data", required=True,
                         help="Path to yearly crime data CSV (Year + crime columns)")
    parser.add_argument("--statedata", required=False,
                         help="Path to state-wise crime data CSV (State, Year, Total_Cases)")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    available_cols = [c for c in CRIME_TYPES if c in data.columns]

    if not available_cols:
        raise ValueError(
            f"None of the expected crime columns {CRIME_TYPES} were found. "
            f"Available columns are: {list(data.columns)}."
        )

    plot_period_wise_averages(data, available_cols)

    if args.statedata:
        state_data = pd.read_csv(args.statedata)
        plot_statewise_comparison(state_data, 2001)
        plot_statewise_comparison(state_data, 2021)
    else:
        print("No --statedata provided, skipping state-wise comparison charts.")
