import os
from pathlib import Path

import pandas as pd
import plotly.express as px

here = Path(__file__).resolve().parent
ROOT = (here / "../..").resolve()
# Load the forecast data
df = pd.read_csv(ROOT / "interim_csvs/forecast_results_all_states.csv")

# Make output folder
os.makedirs(ROOT / "output/charts_supply_demand_gap", exist_ok=True)

# Loop through all states
for state in df["state"].unique():
    subset = df[df["state"] == state].sort_values("year")

    # Build a long-format dataframe for Plotly
    chart_df = pd.DataFrame(
        {
            "year": list(subset["year"]) * 3,
            "value": (
                list(subset["predicted_demand"])
                + list(subset["predicted_supply"])
                + list(subset["gap"])
            ),
            "variable": (
                ["Predicted Demand"] * len(subset)
                + ["Predicted Supply"] * len(subset)
                + ["Gap (Supply - Demand)"] * len(subset)
            ),
        }
    )

    # Create Plotly line chart
    fig = px.line(
        chart_df,
        x="year",
        y="value",
        color="variable",
        title=f"{state} Forecast",
        labels={"value": "Beds", "year": "Year"},
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,  # move legend below the plot; tweak (-0.1 to -0.4) as needed
            xanchor="center",
            x=0.5,
        ),
        margin=dict(r=0, b=100),  # add bottom margin so legend isn't cut off
    )

    # Save chart as HTML
    filename = ROOT / f"output/charts_supply_demand_gap/{state.replace(' ', '_')}.html"
    fig.write_html(filename, include_plotlyjs="cdn")
