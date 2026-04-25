from datetime import datetime
from pathlib import Path

import xmltodict


def retrieve_target_data(source_folder, source_file_pattern):
    # get paths
    paths = [str(p) for p in Path(source_folder).rglob(source_file_pattern)]

    # retrieve desired data from xml (for now just first 10 for dev)
    result = [process_one_hospital(path) for path in paths]  # [0:10]

    return result


def process_one_hospital(path):

    # open the file as a string
    xml_content = open(path, "r").read()
    # with open(".problem_output.xml", "w") as file:
    #     file.write(xml_content)
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

    # ADD HOSPITAL IK + NAME

    # Einleitung/Datensatz/Datum
    try:
        result["Datum"] = datetime.strptime(
            hospital_data["Einleitung"]["Datensatz"]["Datum"], "%Y-%m-%d"
        ).date()
    except KeyError:
        print("ERROR: could not find 'Datum'")
        result["Datum"] = None

    # Krankenhaus/.../Postleitzahl
    # Can have multiple bloody locations...
    # It's either Krankenhaus/Mehrere_Standorte
    #          or Krankenhaus/Ein_Standorte
    try:
        if "Ein_Standort" in hospital_data["Krankenhaus"]:
            result["IK"] = hospital_data["Krankenhaus"]["Ein_Standort"][
                "Krankenhauskontaktdaten"
            ]["IK"]
            result["Ort"] = hospital_data["Krankenhaus"]["Ein_Standort"][
                "Krankenhauskontaktdaten"
            ]["Kontakt_Zugang"]["Ort"]
            result["Postleitzahl"] = int(
                hospital_data["Krankenhaus"]["Ein_Standort"]["Krankenhauskontaktdaten"][
                    "Kontakt_Zugang"
                ]["Postleitzahl"]
            )
        elif "Mehrere_Standorte" in hospital_data["Krankenhaus"]:
            result["IK"] = hospital_data["Krankenhaus"]["Mehrere_Standorte"][
                "Krankenhauskontaktdaten"
            ]["IK"]
            result["Ort"] = hospital_data["Krankenhaus"]["Mehrere_Standorte"][
                "Krankenhauskontaktdaten"
            ]["Kontakt_Zugang"]["Ort"]
            result["Postleitzahl"] = int(
                hospital_data["Krankenhaus"]["Mehrere_Standorte"][
                    "Krankenhauskontaktdaten"
                ]["Kontakt_Zugang"]["Postleitzahl"]
            )
        elif "Krankenhauskontaktdaten" in hospital_data["Krankenhaus"]:
            result["IK"] = hospital_data["Krankenhaus"]["Krankenhauskontaktdaten"]["IK"]
            result["Ort"] = hospital_data["Krankenhaus"]["Krankenhauskontaktdaten"][
                "Kontakt_Zugang"
            ]["Ort"]
            result["Postleitzahl"] = int(
                hospital_data["Krankenhaus"]["Krankenhauskontaktdaten"][
                    "Kontakt_Zugang"
                ]["Postleitzahl"]
            )
        else:
            result["IK"] = hospital_data["Krankenhaus"]["Kontaktdaten"]["IK"]
            result["Ort"] = hospital_data["Krankenhaus"]["Kontaktdaten"][
                "Kontakt_Zugang"
            ]["Ort"]
            result["Postleitzahl"] = int(
                hospital_data["Krankenhaus"]["Kontaktdaten"]["Kontakt_Zugang"][
                    "Postleitzahl"
                ]
            )
        # convert postcode to bundesland from csv
    except KeyError as error:
        print(f"ERROR: could not find Postleitzahl: {error}")

        with open(f"./failed/{result['Datum']}.xml", "w") as file:
            file.write(xml)

        result["Postleitzahl"] = None
    # Anzahl_Betten
    try:
        result["Anzahl_Betten"] = int(hospital_data["Anzahl_Betten"])
    except KeyError:
        print("ERROR: could not find 'Anzahl_Betten'")
        result["Anzahl_Betten"] = None

    # Fallzahlen (all child elements)
    try:
        data = hospital_data["Fallzahlen"]
        result["Fallzahlen"] = {key: int(value) for key, value in data.items()}
    except KeyError:
        print("ERROR: could not find 'Fallzahlen'")
        result["Fallzahlen"] = {}

    return result
