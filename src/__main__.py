import argparse

from src import databasecontroller, hospitalxml

# uv run python -m src.main


def add_one_year(path, year, pattern):
    year -= 1

    hospital_data = hospitalxml.retrieve_target_data(f"{path}/xml_{year}", pattern)
    databasecontroller.insert_data(hospital_data)
    databasecontroller.show_db_contents("dataset")


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ingestor",
    )
    parser.add_argument("year")
    parser.add_argument("path", nargs="?", default="input")
    parser.add_argument("pattern", nargs="?", default="*xml.xml")
    return parser.parse_args()


def main():
    arguments = get_arguments()
    if arguments.year == "2020" or arguments.year == "2018":
        print("dataset not available")
        return
    add_one_year(arguments.path, int(arguments.year), arguments.pattern)


if __name__ == "__main__":
    main()
