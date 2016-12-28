from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from os import listdir
from os.path import isfile, join
from parser_xml import parse_standing_from_file as parse_file
from classes import TotalStandings
from submissions import get_submissions
import config

app = Flask(__name__)


def getFilesAndStanding():
    files = getFiles(config.XML_DIR)
    standings = []
    filesList = []
    for file in files:
        standing = parse_file(config.XML_DIR + file)
        standings.append(standing)
        filesList.append({"path": file, "name": standing.contest.name})
    totalStandings = TotalStandings(standings)
    return filesList, totalStandings


@app.route("/pcms_standings")
@app.route("/")
def hello_world():
    filesList, totalStandings = getFilesAndStanding()
    groups = totalStandings.get_groups()
    return render_template(
        "index.html", files=filesList, groups=groups,
        standings=None, totalStandings=totalStandings)


def getFiles(mypath):
    return sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])


@app.route("/pcms_standings/static/<path:path>")
def sent_static(path):
    return send_from_directory("static", path)


@app.route("/showtable/<string:table>")
@app.route("/pcms_standings/showtable/<string:table>")
def showtable(table):
    files, totalStandings = getFilesAndStanding()
    standings = parse_file(config.XML_DIR + table) \
        if table in [file["path"] for file in files] else None

    groups = standings.get_groups()
    return render_template(
        "index.html", files=files, standings=standings,
        totalStandings=None, groups=groups)


@app.route("/submissions", methods=["GET"])
@app.route("/pcms_standings/submissions", methods=["GET"])
def show_submissions():
    page_limit = config.PAGE_LIMIT
    page_p = request.args.get("page")
    page = 1 if page_p is None else int(page_p)
    range_p = request.args.get("range")
    group_p = request.args.get("group")

    files = getFiles(config.XML_DIR)
    totalStandings = TotalStandings(
        [parse_file(config.XML_DIR + file) for file in files])
    submissions = get_submissions(totalStandings, range_p, group_p)

    submissions = submissions[(page - 1) * page_limit:page_limit * page]

    return render_template(
        "submissions.html", submissions=submissions, page=page)


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host="0.0.0.0", port=1818, debug=True)
