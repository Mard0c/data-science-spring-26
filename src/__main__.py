import argparse

from src import databasecontroller, hospitalxml

# uv run python -m src.main


def add_one_year(path, year, pattern):
    year -= 1

    # TODO prevent duplicate insertions
    hospital_data = hospitalxml.retrieve_target_data(f"{path}/xml_{year}", pattern)
    databasecontroller.insert_data(hospital_data)
    databasecontroller.debug_bundesland()


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ingestor",
    )
    parser.add_argument("year")
    parser.add_argument("path", nargs="?", default="input")
    parser.add_argument("pattern", nargs="?", default="*xml.xml")
    return parser.parse_args()


def main():
    # arguments = get_arguments()
    # if arguments.year == "2020" or arguments.year == "2018":
    #     print("dataset not available")
    #     return
    # add_one_year(arguments.path, int(arguments.year), arguments.pattern)
    # get_all(2015, 2025, arguments.path, arguments.pattern)
    databasecontroller.show_db_contents("dataset")


def get_all(start, end, path, pattern):
    for year in range(start, end):
        print(f"YEAR: {year}")
        if year == 2020 or year == 2018:
            print(f"no data for: {year}")
            continue
        add_one_year(path, year, pattern)


if __name__ == "__main__":
    main()
