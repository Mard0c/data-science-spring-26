from pathlib import Path

import pandas as pd
import plotly.express as px

here = Path(__file__).resolve().parent
ROOT = (here / "../.." ).resolve()
df = pd.read_csv(ROOT / "interim_csvs/forecast_results_all_states.csv")
pop = pd.read_csv(ROOT / "interim_csvs/population_forecast.csv")
df = df.merge(pop, on=["state", "year"], how="left")

# Calculate gap per 1000 capita
df["gap_per_capita"] = df["gap"] / df["population"]
df["gap_per_capita"] = df["gap_per_capita"] * 1000

# Pivot so states are rows, years are columns
heatmap_df = df.pivot(index="state", columns="year", values="gap_per_capita")

fig = px.imshow(
    heatmap_df,
    color_continuous_scale="RdYlGn",  # Red = bad, Green = good
    aspect="auto",
    title="Gap Heatmap (Supply - Demand): Critical Shortage Identification per 1000 Capita",
)

fig.update_traces(
    colorbar_title="Free beds per 1000 capita",
    hovertemplate="year: %{x}<br>state: %{y}<br>free beds per 1000 capita: %{z}<extra></extra>",
)

fig.update_layout(xaxis_title="Year", yaxis_title="State")

fig.write_html(ROOT / "output/gap_heatmap.html", include_plotlyjs="cdn")
