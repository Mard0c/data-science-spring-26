import duckdb
import pyarrow


def insert_test_data(data):

    db = duckdb.connect("database.db")

    arrow_table = pyarrow.Table.from_pylist(data)
    print(type(arrow_table["Datum"][0]))
    db.register("data_view", arrow_table)

    # might be useful:
    # tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    # print(tables)
    table_exists = (
        db.sql(
            "SELECT * FROM information_schema.tables WHERE table_name = 'sample'"
        ).fetchall()
        != []
    )
    print(f"table_exists: {table_exists}")

    if not table_exists:
        db.sql("CREATE TABLE sample AS SELECT * FROM data_view")
    else:
        db.sql("TRUNCATE TABLE sample")
        db.sql("INSERT INTO sample SELECT * FROM data_view")
    db.close()


def show_db_contents(table: str):
    db = duckdb.connect("database.db")
    try:
        db.table(table).show()
    except duckdb.Error as error:
        print(f"couldn't open '{table}': {error}")
