from src import main


# run tests with: uv run -m pytest
def test_process_one_hospital():
    assert main.process_one_hospital("./tests/sample/one-location-hospital.xml") == {
        "Datum": "2025-11-06",
        "Postleitzahl": "88046",
        "Anzahl_Betten": "20",
        "Fallzahlen": {
            "Vollstationaere_Fallzahl": "0",
            "Teilstationaere_Fallzahl": "129",
            "Ambulante_Fallzahl": "311",
            "StaeB_Fallzahl": "0",
        },
    }
