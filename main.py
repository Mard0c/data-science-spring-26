# import module
import xmltodict


def main():

    # open the file
    fileptr = open("sample-input/260100023-773287000-2024-xml copy.xml", "r")

    # read xml content from the file
    xml_content = fileptr.read()

    # change xml format to ordered dict
    my_ordered_dict = xmltodict.parse(xml_content)

    # select relevant data
    selected_hospital_data = select_hospital_data(my_ordered_dict)

    # (temporary) print data
    print(selected_hospital_data["Qualitaetsbericht"])


def select_hospital_data(all_hospital_data: dict) -> dict:
    result = {}

    # Einleitung/Datensatz/Datum
    try:
        result["Datum"] = all_hospital_data["Einleitung"]["Datensatz"]["Datum"]
    except KeyError:
        result["Datum"] = None

    # Krankenhaus/.../Postleitzahl
    try:
        result["Postleitzahl"] = all_hospital_data["Krankenhaus"]["Mehrere_Standorte"][
            "Krankenhauskontaktdaten"
        ]["Kontakt_Adresse"]["Postleitzahl"]
    except KeyError:
        result["Postleitzahl"] = None

    # Anzahl_Betten
    try:
        result["Anzahl_Betten"] = all_hospital_data["Anzahl_Betten"]
    except KeyError:
        result["Anzahl_Betten"] = None

    # Fallzahlen (all child elements)
    try:
        result["Fallzahlen"] = all_hospital_data["Fallzahlen"]
        fallzahlen_raw = all_hospital_data["Fallzahlen"]
        # Keep only children whose value looks numeric
        result["Fallzahlen"] = {
            k: v
            for k, v in fallzahlen_raw.items()
            if v is not None and str(v).lstrip("-").isdigit()
        }
    except KeyError:
        result["Fallzahlen"] = {}

    return result


if __name__ == "__main__":
    main()
