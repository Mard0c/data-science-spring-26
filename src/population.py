import duckdb
import pandas as pd


def create_population_table():
    path = "cleaned_population_2015-2024.csv"

    df_wide = pd.read_csv(path, sep=";", header=0)

    # rename the top left cell to "Bundesland" column header
    # renaming by index wasn't working the "normal way" so I did something kind of weird.
    mapping = {0: "Bundesland"}
    df_wide.rename(
        columns={df_wide.columns[i]: new for i, new in mapping.items()}, inplace=True
    )

    # melt the wide table into a long table to fit into duckdb
    df_long = df_wide.melt(
        id_vars="Bundesland", var_name="year", value_name="population"
    )

    df_long["year"] = pd.to_datetime(df_long["year"], format="%d.%m.%Y").dt.date
    print(df_long)

    db = duckdb.connect("database.db")

    tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    print(tables)

    db.register("df_populations", df_long)
    db.sql("""
            CREATE TABLE populations AS
            SELECT *
            FROM df_populations;
        """)

    db.close()


def check():
    db = duckdb.connect("database.db")
    tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    print(tables)
    db.sql("SELECT * FROM populations LIMIT 20").show()
    # db.sql("""
    #     SELECT Bundesland
    #     FROM populations
    #     EXCEPT
    #     SELECT Bundesland
    #     FROM plz_ort_bundesland;

    #     SELECT Bundesland
    #     FROM plz_ort_bundesland
    #     EXCEPT
    #     SELECT Bundesland
    #     FROM populations;
    #     """).show()
    # db.sql("""
    #     SELECT Bundesland, Ort, Plz
    #     FROM plz_ort_bundesland
    #     WHERE Bundesland IS NULL;
    #     """).show()
    db.sql("""
        SELECT
          COALESCE(a.Bundesland, b.Bundesland) AS Bundesland_key,
          a.Bundesland AS bundesland_in_plz,
          b.Bundesland AS bundesland_in_pop
        FROM plz_ort_bundesland a
        FULL OUTER JOIN populations b
          ON a.Bundesland = b.Bundesland
        WHERE a.Bundesland IS NULL
           OR b.Bundesland IS NULL
           OR a.Bundesland IS DISTINCT FROM b.Bundesland
        ORDER BY 1;
        """).show()
    db.close()
