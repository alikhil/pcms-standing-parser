from xmljson import badgerfish as bf
from json import dumps, loads
from xml.etree.ElementTree import fromstring
from classes import Standings


def parse_standing_from_file(filename):

    with open(filename, "r", encoding="utf8") as f:
        xmlData = f.read()
        print("xml read from " + filename)

    json = dumps(bf.data(fromstring(xmlData))).replace("@", "")
    obj = loads(json)
    standing = Standings(**obj["standings"])
    return standing


standing = parse_standing_from_file("input.xml")
print(standing.contest.sessions[0].submitted_problems[1].runs[0].accepted)
