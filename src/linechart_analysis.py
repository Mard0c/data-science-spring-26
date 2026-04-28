import pandas as pd
import plotly.express as px
import os

# Load the forecast data
df = pd.read_csv("interim_csvs/forecast_results_all_states.csv")

# Make output folder
os.makedirs("output/charts_supply_demand_gap", exist_ok=True)

# Loop through all states
for state in df["state"].unique():
    subset = df[df["state"] == state].sort_values("year")

    # Build a long-format dataframe for Plotly
    chart_df = pd.DataFrame({
        "year": list(subset["year"]) * 3,
        "value": (
            list(subset["predicted_demand"]) +
            list(subset["predicted_supply"]) +
            list(subset["gap"])
        ),
        "variable": (
            ["Predicted Demand"] * len(subset) +
            ["Predicted Supply"] * len(subset) +
            ["Gap (Supply - Demand)"] * len(subset)
        )
    })

    # Create Plotly line chart
    fig = px.line(
        chart_df,
        x="year",
        y="value",
        color="variable",
        title=f"Forecast for {state}: Demand, Supply & Gap (2026–2035)",
        labels={"value": "Beds", "year": "Year"}
    )

    # Save chart as HTML
    filename = f"output/charts_supply_demand_gap/{state.replace(' ', '_')}.html"
fig.write_html(filename)