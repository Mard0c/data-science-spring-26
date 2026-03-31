import duckdb
import pyarrow


def playground(data):

    db = duckdb.connect("database.db")

    arrow_table = pyarrow.Table.from_pylist(data)
    db.register("data_view", arrow_table)

    # might be useful: tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    table_exists = (
        db.sql(
            "SELECT * FROM information_schema.tables WHERE table_name = 'sample'"
        ).fetchall()
        != []
    )

    if not table_exists:
        db.sql("CREATE TABLE sample AS SELECT * FROM data_view")
    db.table("sample").show()
    db.close()
