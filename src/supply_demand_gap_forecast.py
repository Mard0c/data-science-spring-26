import duckdb
import pandas as pd
import numpy as np
from pathlib import Path

# export data from duckdb
db = duckdb.connect("../database.db")  # adjust if needed

db.sql(f"""
COPY (
    WITH base AS (
        SELECT
            EXTRACT(year FROM Datum) AS year,
            Bundesland AS state,
            COALESCE(Fallzahlen.Vollstationaere_Fallzahl, 0) AS voll
        FROM dataset
    )
    SELECT year, state, SUM(voll) AS value
    FROM base
    GROUP BY year, state
) TO '{"interim_csvs/vollstationaere_fallzahl.csv"}' (HEADER);
""")

db.sql(f"""
COPY (
    WITH base AS (
        SELECT
            EXTRACT(year FROM Datum) AS year,
            Bundesland AS state,
            COALESCE(Fallzahlen.Teilstationaere_Fallzahl, 0) AS teil
        FROM dataset
    )
    SELECT year, state, SUM(teil) AS value
    FROM base
    GROUP BY year, state
) TO '{"interim_csvs/teilstationaere_fallzahl.csv"}' (HEADER);
""")

db.sql(f"""
COPY (
    WITH base AS (
        SELECT
            EXTRACT(year FROM Datum) AS year,
            Bundesland AS state,
            Anzahl_Betten AS betten
        FROM dataset
    )
    SELECT year, state, SUM(betten) AS value
    FROM base
    GROUP BY year, state
) TO '{"interim_csvs/anzahl_betten.csv"}' (HEADER);
""")

voll = pd.read_csv("interim_csvs/vollstationaere_fallzahl.csv")
teil = pd.read_csv("interim_csvs/teilstationaere_fallzahl.csv")
betten = pd.read_csv("interim_csvs/anzahl_betten.csv")

# Merge 
df = voll.merge(teil, on=["state", "year"], suffixes=("_voll", "_teil"))
df = df.merge(betten, on=["state", "year"])
df = df.rename(columns={"value": "supply_beds"})

# compute demand and supply

# Demand formula: inpatient (7.2 days) + partial inpatient (0.8 days)
df["demand"] = (7.2 * df["value_voll"] + 0.8 * df["value_teil"]) / 365
df["supply"] = df["supply_beds"]

# Drop outliers / small values
df = df[df["demand"] > 50]
df = df[df["supply"] > 200]


# Long-term German healthcare drift trends:
DRIFT_DEMAND = -0.002   # -0.2% per year
DRIFT_SUPPLY = -0.01    # -1.0% per year

# smoothing and forecasting
def smooth_series(y):
    """Rolling median smoothing to remove noise/spikes."""
    return pd.Series(y).rolling(window=3, center=True, min_periods=1).median().values

def forecast_random_walk_with_drift(y_smooth, years, future_years, drift):
    """Forecast using last smoothed value and a drift-based random walk."""
    last_value = y_smooth[-1]
    last_year = years[-1]

    preds = []
    for fy in future_years:
        steps = fy - last_year
        value = last_value * ((1 + drift) ** steps)
        preds.append(max(1, value))

    return np.array(preds)

future_years = list(range(df["year"].max() + 1, df["year"].max() + 16))
forecast_rows = []

for state, group in df.groupby("state"):
    group = group.sort_values("year")

    years = group["year"].values

   
   # smooth demand
    y_demand = group["demand"].values
    y_demand_smooth = smooth_series(y_demand)

    # forecast demand
    demand_pred = forecast_random_walk_with_drift(
        y_demand_smooth, years, future_years, drift=DRIFT_DEMAND
    )

    # smooth supply
    y_supply = group["supply"].values
    y_supply_smooth = smooth_series(y_supply)

    # forecast supply
    supply_pred = forecast_random_walk_with_drift(
        y_supply_smooth, years, future_years, drift=DRIFT_SUPPLY
    )

    # add rows to forecast table
    for fy, d_val, s_val in zip(future_years, demand_pred, supply_pred):
        forecast_rows.append([state, fy, d_val, s_val])

# make forecast dataframe
forecast_df = pd.DataFrame(forecast_rows,
                           columns=["state", "year", "forecast_demand", "forecast_supply"])

# Compute gap
forecast_df["forecast_gap"] = forecast_df["forecast_supply"] - forecast_df["forecast_demand"]

OUT = "interim_csvs/forecast_supply_demand_gap.csv"
forecast_df.to_csv(OUT, index=False)
