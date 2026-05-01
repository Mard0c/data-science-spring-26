from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

here = Path(__file__).resolve().parent
ROOT = (here / "../.." ).resolve()

# Load Data
df_gap = pd.read_csv(ROOT / "interim_csvs/forecast_results_all_states.csv")
pop = pd.read_csv(ROOT / "interim_csvs/cleaned_population_2015-2024.csv", sep=";")

# Rename first column to state
pop = pop.rename(columns={"Unnamed: 0": "state"})

# Reshape to long format
pop_long = pop.melt(id_vars="state", var_name="date", value_name="population")

# Extract year (last 4 characters)
pop_long["year"] = pop_long["date"].str[-4:].astype(int)

# Keep only clean columns
pop_long = pop_long[["state", "year", "population"]]

# Forecast years
future_years = list(range(2025, 2040))

# Logistic Growth Model


def logistic(t, K, A, B):
    """Logistic growth curve."""
    return K / (1 + A * np.exp(-B * t))


forecast_rows = []

# Fit logistic curve per state

for state, group in pop_long.groupby("state"):
    group = group.sort_values("year")

    years = group["year"].values
    y = group["population"].values

    # Normalize years for numerical stability
    t = years - years.min()

    # Initial parameter guesses (typical chosen values)
    K0 = y.max() * 1.5  # Guess carrying capacity above observed max
    A0 = 1
    B0 = 0.05

    # Fit logistic curve
    try:
        params, _ = curve_fit(logistic, t, y, p0=[K0, A0, B0], maxfev=20000)
        K, A, B = params
    except:
        # Fallback (rare): linear growth
        K, A, B = K0, A0, B0

    # Forecast population for each future year
    for yr in future_years:
        t_future = yr - years.min()
        pred = logistic(t_future, K, A, B)
        forecast_rows.append([state, yr, pred])

# Save Results
pop_forecast = pd.DataFrame(forecast_rows, columns=["state", "year", "population"])

pop_forecast.to_csv(ROOT / "interim_csvs/population_forecast.csv", index=False)
