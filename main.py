# import module
import xmltodict


def main():

    # open the file
    fileptr = open("input/xml_2024/510841096-772822000-2024-xml.xml", "r")

    # read xml content from the file
    xml_content = fileptr.read()
    print("XML content is:")
    print(xml_content)

    # change xml format to ordered dict
    my_ordered_dict = xmltodict.parse(xml_content)


if __name__ == "__main__":
    main()
