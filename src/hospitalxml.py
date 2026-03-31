from pathlib import Path

import xmltodict


def retrieve_target_data(source_folder, source_file_pattern):
    # get paths
    paths = [str(p) for p in Path(source_folder).rglob(source_file_pattern)]

    # retrieve desired data from xml (for now just first 10 for dev)
    result = [process_one_hospital(path) for path in paths[0:10]]

    return result


def process_one_hospital(path):

    # open the file as a string
    xml_content = open(path, "r").read()

    # select relevant data
    selected_hospital_data = select_hospital_data(xml_content)

    # (temporary) print data
    print(selected_hospital_data)
    return selected_hospital_data


def select_hospital_data(xml: str) -> dict:
    # translate xml to dictionary
    hospital_data = xmltodict.parse(xml)["Qualitaetsbericht"]

    # collect target data in this dictionary
    result = {}

    # Einleitung/Datensatz/Datum
    try:
        result["Datum"] = hospital_data["Einleitung"]["Datensatz"]["Datum"]
    except KeyError:
        print("ERROR: could not find 'Datum'")
        result["Datum"] = None

    # Krankenhaus/.../Postleitzahl
    # Can have multiple bloody locations...
    # It's either Krankenhaus/Mehrere_Standorte
    #          or Krankenhaus/Ein_Standorte
    try:
        result["Postleitzahl"] = hospital_data["Krankenhaus"]["Ein_Standort"][
            "Krankenhauskontaktdaten"
        ]["Kontakt_Adresse"]["Postleitzahl"]
    except KeyError:
        print("ERROR: could not find 'Postleitzahl'")

        if "Mehrere_Standorte" in hospital_data["Krankenhaus"]:
            print("UNHANDLED EDGE CASE: has multiple locations")

        result["Postleitzahl"] = None

    # Anzahl_Betten
    try:
        result["Anzahl_Betten"] = hospital_data["Anzahl_Betten"]
    except KeyError:
        print("ERROR: could not find 'Anzahl_Betten'")
        result["Anzahl_Betten"] = None

    # Fallzahlen (all child elements)
    try:
        result["Fallzahlen"] = hospital_data["Fallzahlen"]
    except KeyError:
        print("ERROR: could not find 'Fallzahlen'")
        result["Fallzahlen"] = {}

    return result
