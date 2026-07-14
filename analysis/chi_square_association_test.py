"""
Chi-Square Test of Association: Crime Types vs. Zones of India (2001-2021)
----------------------------------------------------------------------------
Recreates the SPSS-based Pearson's Chi-Square analysis from the thesis
"Crime Against Women in India: A Statistical and Comparative Study".

Tests, for each 5-year segment (2001-05, 2006-10, 2011-15, 2016-20),
whether there is a significant association between crime type and zone.

H0: No significant association among crime types across zones.
H1: Significant association exists among crime types across zones.

Usage:
    python chi_square_association_test.py --data ../data/crime_data_2001_2021.csv
"""

import argparse
import pandas as pd
from scipy.stats import chi2_contingency

# Zones as used in the original study
ZONE_MAP = {
    "East Zone": ["West Bengal", "Odisha", "Jharkhand", "Bihar"],
    "Western Zone": ["Maharashtra", "Gujarat", "Goa"],
    "Northern Zone": ["Delhi", "Punjab", "Haryana", "Himachal Pradesh",
                       "Jammu & Kashmir", "Uttarakhand", "Chandigarh"],
    "Southern Zone": ["Tamil Nadu", "Kerala", "Karnataka", "Andhra Pradesh",
                        "Telangana", "Puducherry"],
    "Central Zone": ["Uttar Pradesh", "Madhya Pradesh", "Chhattisgarh", "Rajasthan"],
}

CRIME_COLUMNS = [
    "Rape", "Kidnapping_Abduction", "Dowry_Deaths",
    "Sexual_Harassment", "Cruelty_by_Husband_Relatives",
    "Importation_of_Girls", "Assault_on_Modesty",
]

SEGMENTS = {
    "2001-05": (2001, 2005),
    "2006-10": (2006, 2010),
    "2011-15": (2011, 2015),
    "2016-20": (2016, 2020),
}


def state_to_zone(state):
    for zone, states in ZONE_MAP.items():
        if state in states:
            return zone
    return "Unmapped"


def run_chi_square(df):
    """Run chi-square test per 5-year segment and return summary table."""
    df["Zone"] = df["State"].apply(state_to_zone)
    results = []

    for label, (start, end) in SEGMENTS.items():
        segment_df = df[(df["Year"] >= start) & (df["Year"] <= end)]
        contingency = segment_df.groupby("Zone")[CRIME_COLUMNS].sum()

        if contingency.shape[0] < 2 or contingency.shape[1] < 2:
            continue

        chi2_stat, p_value, dof, expected = chi2_contingency(contingency)
        conclusion = "Significant association" if p_value < 0.05 else "No significant association"

        results.append({
            "Segment": label,
            "Chi2_Statistic": round(chi2_stat, 3),
            "p_value": round(p_value, 5),
            "Degrees_of_Freedom": dof,
            "Conclusion": conclusion,
        })

        print(f"\n--- {label} ---")
        print(f"Chi-square statistic: {chi2_stat:.3f}")
        print(f"p-value: {p_value:.5f}")
        print(f"Conclusion: {conclusion}")

    return pd.DataFrame(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chi-square association test by zone")
    parser.add_argument("--data", required=True, help="Path to crime data CSV")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    summary = run_chi_square(data)

    print("\n=== Summary Table ===")
    print(summary.to_string(index=False))

    summary.to_csv("chi_square_summary.csv", index=False)
    print("\nSaved summary to chi_square_summary.csv")
