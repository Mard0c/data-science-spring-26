from src import databasecontroller, hospitalxml


# uv run python -m src.main
def main():
    # in the terminal, use ctrl-c to stop this from reading every file.
    hospital_data = hospitalxml.retrieve_target_data("input", "*xml.xml")
    databasecontroller.playground(hospital_data)


if __name__ == "__main__":
    main()
