import duckdb
import pyarrow


def insert_data(data):
    main_table = "dataset"
    plz_bundesland_table = "plz_ort_bundesland"

    # replace with a in memory database first?
    db = duckdb.connect("database.db")

    arrow_table = pyarrow.Table.from_pylist(data)
    db.register("data_view", arrow_table)

    if not table_exists(db, plz_bundesland_table):
        create_postcode_to_bundesland_table(db, "plz_bundesland.csv")

    if not table_exists(db, main_table):
        db.sql(f"CREATE TABLE {main_table} AS SELECT * FROM data_view")
    else:
        # db.sql("TRUNCATE TABLE sample")
        db.sql(f"INSERT INTO {main_table} SELECT * FROM data_view")

    db.close()


def create_postcode_to_bundesland_table(db, path):
    db.sql(f"""
        CREATE TABLE plz_ort_bundesland AS
        SELECT
          Ort,
          CAST(Plz AS INTEGER) AS Plz,
          Bundesland
        FROM read_csv_auto({path}, delim=';', header=true);
        CREATE INDEX idx_plz_ort ON plz_ort_bundesland(Plz, Ort);
    """)


def table_exists(db, table) -> bool:
    # might be useful:
    # tables = [t[0] for t in db.execute("SHOW TABLES").fetchall()]
    try:
        return (
            db.sql(
                "SELECT * FROM information_schema.tables WHERE table_name = ?",
                params=[table],
            ).fetchall()
            != []
        )
    except duckdb.Error:
        return False


def show_db_contents(table: str):
    db = duckdb.connect("database.db")
    try:
        db.table(table).show()
    except duckdb.Error as error:
        print(f"couldn't open '{table}': {error}")
