import duckdb

connection = duckdb.connect("main.duckdb")

print("Established database connection!")

# con.register("staging_df", df)
# con.execute("CREATE TABLE IF NOT EXISTS records AS SELECT * FROM staging_df")
