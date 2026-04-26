import duckdb
import plotly.express as px


# CURRENTLY JUST SELECTING BRANDENBURG
def select_data():
    db = duckdb.connect("database.db")
    # db.sql("""
    #     SELECT
    #       COUNT(DISTINCT COALESCE(Bundesland, 'Unknown')) AS n_states,
    #       COUNT(DISTINCT EXTRACT(YEAR FROM Datum))         AS n_years
    #     FROM dataset;
    #     """).show()
    # db.sql("""
    #         SELECT
    #           COUNT(DISTINCT COALESCE(Bundesland, 'Unknown')) AS n_states,
    #           COUNT(DISTINCT EXTRACT(YEAR FROM year))         AS n_years
    #         FROM populations;
    #         """).show()
    return db.sql("""
        WITH base AS (
          SELECT
            Bundesland,
            EXTRACT(year FROM Datum) AS year,
            IK,
            Anzahl_Betten,
            COALESCE(Fallzahlen.Vollstationaere_Fallzahl, 0) AS voll,
            COALESCE(Fallzahlen.Teilstationaere_Fallzahl, 0) AS teil
          FROM dataset
          -- WHERE Bundesland IS NOT NULL
        ),
        agg AS (
          SELECT
            Bundesland,
            year,
            SUM(voll) AS Vollstationaere_Fallzahl_sum,
            SUM(teil) AS Teilstationaere_Fallzahl_sum,
            SUM(Anzahl_Betten) AS Anzahl_Betten_sum,
            COUNT(DISTINCT IK) AS number_of_hospitals
          FROM base
          GROUP BY 1, 2
        ),
        result AS ( SELECT
          a.Bundesland,
          a.year,
          a.Vollstationaere_Fallzahl_sum,
          a.Teilstationaere_Fallzahl_sum,
          a.Anzahl_Betten_sum,
          a.number_of_hospitals,
          p.population
        FROM agg a
        LEFT JOIN populations p
          ON lower(trim(p.Bundesland)) = lower(trim(a.Bundesland))
        AND EXTRACT(YEAR FROM p.year) = a.year
        )
        SELECT *
        FROM result
        WHERE Bundesland = 'Brandenburg'
        ORDER BY Bundesland, year
    """).df()


def visualize():
    df = select_data()
    print(df)

    fig = px.line(
        df, x="year", y="population", title="Brandenburg population since 2015"
    )
    # fig = px.scatter(x=range(10), y=range(10))
    fig.write_html("output/graph.html")
    print("yup...")
