# import module
import xmltodict


def main():
    process_one_hospital("input/xml_2024/510841096-772822000-2024-xml.xml")


# "input/xml_2024/510841096-772822000-2024-xml.xml"
def process_one_hospital(path):

    # open the file as a string
    xml_content = open(path, "r").read()

    # select relevant data
    selected_hospital_data = select_hospital_data(xml_content)

    # (temporary) print data
    print(selected_hospital_data)


def select_hospital_data(xml: str) -> dict:
    # translate xml to dictionary
    all_hospital_data = xmltodict.parse(xml)["Qualitaetsbericht"]

    # collect target data in this dictionary
    result = {}

    # Einleitung/Datensatz/Datum
    try:
        result["Datum"] = all_hospital_data["Einleitung"]["Datensatz"]["Datum"]
    except KeyError:
        print("ERROR: could not find 'Datum'")
        result["Datum"] = None

    # Krankenhaus/.../Postleitzahl
    # Can have multiple bloody locations...
    # It's either Krankenhaus/Mehrere_Standorte
    #          or Krankenhaus/Ein_Standorte
    try:
        result["Postleitzahl"] = all_hospital_data["Krankenhaus"]["Ein_Standort"][
            "Krankenhauskontaktdaten"
        ]["Kontakt_Adresse"]["Postleitzahl"]
    except KeyError:
        print("ERROR: could not find 'Postleitzahl'")

        if "Mehrere_Standorte" in all_hospital_data["Krankenhaus"]:
            print("UNHANDLED EDGE CASE: has multiple locations")

        result["Postleitzahl"] = None

    # Anzahl_Betten
    try:
        result["Anzahl_Betten"] = all_hospital_data["Anzahl_Betten"]
    except KeyError:
        print("ERROR: could not find 'Anzahl_Betten'")
        result["Anzahl_Betten"] = None

    # Fallzahlen (all child elements)
    try:
        result["Fallzahlen"] = all_hospital_data["Fallzahlen"]
    except KeyError:
        print("ERROR: could not find 'Fallzahlen'")
        result["Fallzahlen"] = {}

    return result


if __name__ == "__main__":
    # paths = [str(p) for p in Path("input_files").rglob("*.txt")]
    main()
