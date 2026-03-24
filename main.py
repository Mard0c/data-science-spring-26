# import module
import xmltodict


def main():

    # open the file
    fileptr = open("input/xml_2024/510841096-772822000-2024-xml.xml", "r")

    # read xml content from the file
    xml_content = fileptr.read()

    # change xml format to ordered dict
    my_ordered_dict = xmltodict.parse(xml_content)

    # select relevant data
    selected_hospital_data = select_hospital_data(my_ordered_dict["Qualitaetsbericht"])

    # (temporary) print data
    print(selected_hospital_data)


def select_hospital_data(all_hospital_data: dict) -> dict:
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
    # or          Krankenhaus/Ein_Standorte
    try:
        result["Postleitzahl"] = all_hospital_data["Krankenhaus"]["Ein_Standort"][
            "Krankenhauskontaktdaten"
        ]["Kontakt_Adresse"]["Postleitzahl"]
    except KeyError:
        print("ERROR: could not find 'Postleitzahl'")
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
    main()
