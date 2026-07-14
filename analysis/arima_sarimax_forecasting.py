"""
ARIMA / SARIMAX Time-Series Forecasting: Crime Against Women in India
----------------------------------------------------------------------------
Recreates the forecasting pipeline from the thesis
"Crime Against Women in India: A Statistical and Comparative Study".

Pipeline:
    1. Load yearly crime totals (2001-2021) by category
    2. Run Augmented Dickey-Fuller (ADF) test to check stationarity
    3. Difference the series if non-stationary
    4. Auto-select (p, d, q) via pmdarima's auto_arima
    5. Fit SARIMAX and forecast 10 years ahead (2022-2031)
    6. Plot actual vs forecasted values

Usage:
    python arima_sarimax_forecasting.py --data ../data/crime_data_2001_2021.csv
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

CRIME_TYPES = ["Rape", "DV", "AoW", "AoM", "DD", "K&A", "WT"]
FORECAST_YEARS = 10


def check_stationarity(series, label):
    result = adfuller(series.dropna())
    adf_stat, p_value = result[0], result[1]
    stationary = p_value < 0.05
    print(f"[{label}] ADF Statistic: {adf_stat:.3f}, p-value: {p_value:.3f} "
          f"-> {'Stationary' if stationary else 'Non-Stationary'}")
    return stationary


def forecast_crime(df, crime_col, years_ahead=FORECAST_YEARS):
    series = df.set_index("Year")[crime_col].astype(float)

    # Step 1: stationarity check (difference once if needed, matching thesis approach)
    is_stationary = check_stationarity(series, crime_col)
    d = 0 if is_stationary else 1

    # Step 2: auto-select (p, d, q)
    model = auto_arima(series, d=d, seasonal=False, suppress_warnings=True,
                        stepwise=True, trace=False)
    order = model.order
    print(f"[{crime_col}] Selected ARIMA order: {order}")

    # Step 3: fit SARIMAX with selected order
    sarimax_model = SARIMAX(series, order=order,
                             enforce_stationarity=False,
                             enforce_invertibility=False)
    fitted = sarimax_model.fit(disp=False)
    print(fitted.summary())

    # Step 4: forecast
    forecast = fitted.get_forecast(steps=years_ahead)
    forecast_index = range(series.index.max() + 1, series.index.max() + 1 + years_ahead)
    forecast_series = pd.Series(forecast.predicted_mean.values, index=forecast_index)

    # Step 5: plot actual vs forecast
    plt.figure(figsize=(9, 5))
    plt.plot(series.index, series.values, marker="o", label="Actual", color="#1f77b4")
    plt.plot(forecast_series.index, forecast_series.values, marker="x",
              linestyle="--", label="Forecast", color="#ff7f0e")
    plt.title(f"{crime_col} Cases: Actual vs Forecast (till {forecast_index[-1]})")
    plt.xlabel("Year")
    plt.ylabel(f"{crime_col} Cases")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{crime_col.replace(' ', '_')}_forecast.png", dpi=150)
    plt.close()
    print(f"Saved {crime_col}_forecast.png\n")

    combined = pd.concat([series, forecast_series])
    combined.name = crime_col
    return combined


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ARIMA/SARIMAX forecasting for crime data")
    parser.add_argument("--data", required=True, help="Path to crime data CSV (Year + crime columns)")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    all_forecasts = {}

    for crime in CRIME_TYPES:
        if crime in data.columns:
            all_forecasts[crime] = forecast_crime(data, crime)
        else:
            print(f"Column '{crime}' not found in data — skipping.")

    result_df = pd.DataFrame(all_forecasts)
    result_df.index.name = "Year"
    result_df.to_csv("forecast_2022_2031.csv")
    print("Saved combined forecast table to forecast_2022_2031.csv")
