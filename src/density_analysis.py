import pandas as pd
import json
import os 
import urllib.request
import plotly.express as px

beds = pd.read_csv("interim_csvs/anzahl_betten.csv")
population = pd.read_csv("interim_csvs/cleaned_population_2015-2024.csv", sep=';')

# Remove rows where the state is missing
beds = beds.dropna(subset=["state"])
# Convert year to integer
beds["year"] = beds["year"].astype(int)

# Rename 'value' to 'beds' for clarity
beds = beds.rename(columns={"value": "beds"})

# The first column is the state column (name varies)
state_col = population.columns[0]

# Reshape using melt()
population_long = population.melt(
    id_vars=[state_col],
    var_name="year",
    value_name="population"
)

# Rename the detected state column to "state"
population_long = population_long.rename(columns={state_col: "state"})

# Extract year from strings like "31.12.2015"
population_long["year"] = population_long["year"].str[-4:].astype(int)

df = beds.merge(population_long, on=["state", "year"], how="inner")
df["density"] = df["beds"] / df["population"]

# Remove years with incomplete state coverage
df = df[~df["year"].isin([2018, 2020])]

# Download Germany GeoJSON if not already present
geojson_url = "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/4_niedrig.geo.json"
geojson_file = "geo_germany.json"

if not os.path.exists(geojson_file):
    print("Downloading Germany GeoJSON...")
    urllib.request.urlretrieve(geojson_url, geojson_file)
    print("Download complete.")

    # Load the local copy
with open(geojson_file, "r", encoding="utf-8") as f:
    germany_geojson = json.load(f)

    # Build the automated choropleth animation
df = df.sort_values(["year", "state"])
fig = px.choropleth(
    df,
    geojson=germany_geojson,
    featureidkey="properties.name",
    locations="state",
    color="density",
    animation_frame="year",
    color_continuous_scale="Viridis",
    title="Beds per Population Density – Germany (Animated)"
)

fig.update_geos(fitbounds="locations", visible=False)

fig.update_layout(
    margin={"r":0, "t":40, "l":0, "b":0},
    coloraxis_colorbar=dict(title="Beds per Person")
)

fig.write_html("output/beds_density_animation.html")