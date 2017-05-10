from xml.etree.ElementTree import fromstring
from json import dumps, loads
from xmljson import badgerfish as bf
from models.standings import Standings


def parse_standing_from_file(filename):
    with open(filename, "r", encoding="utf8") as file:
        xml_data = file.read()
        print("xml read from " + filename)

    json = dumps(bf.data(fromstring(xml_data))).replace("@", "")
    obj = loads(json)
    standing = Standings(**obj["standings"])
    return standing
