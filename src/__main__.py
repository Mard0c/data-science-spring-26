from src import databasecontroller, hospitalxml


# uv run python -m src.main
def main():
    # in the terminal, use ctrl-c to stop this from reading every file.
    hospital_data = hospitalxml.retrieve_target_data("input/xml_2023", "*xml.xml")
    databasecontroller.insert_test_data(hospital_data)
    databasecontroller.show_db_contents("sample")
    # add some kind of cli tool?


def add_one_year(year):
    year -= 1

    hospital_data = hospitalxml.retrieve_target_data(f"input/xml_{year}", "*xml.xml")
    databasecontroller.insert_data(hospital_data)
    databasecontroller.show_db_contents("sample")


def test(input):
    print(input)


if __name__ == "__main__":
    main()
