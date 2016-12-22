from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from os import listdir
from os.path import isfile, join
from parser_xml import parse_standing_from_file as parse_file
from classes import TotalStandings
from submissions import get_submissions
import config

app = Flask(__name__)


@app.route("/")
def hello_world():
    files = getFiles(config.XML_DIR)
    totalStandings = TotalStandings(
        [parse_file(config.XML_DIR + file) for file in files])
    return render_template(
        "index.html", files=files,
        standings=None, totalStandings=totalStandings)


def getFiles(mypath):
    return sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])


@app.route("/showtable/<string:table>")
def showtable(table):
    files = getFiles(config.XML_DIR)
    standings = parse_file(config.XML_DIR + table) \
        if table in files else None

    return render_template(
        "index.html", files=files, standings=standings,
        totalStandings=None)


@app.route("/submissions", methods=["GET"])
def show_submissions():
    page_limit = config.PAGE_LIMIT
    page_p = request.args.get("page")
    page = 1 if page_p is None else int(page_p)
    range_p = request.args.get("range")

    files = getFiles(config.XML_DIR)
    totalStandings = TotalStandings(
        [parse_file(config.XML_DIR + file) for file in files])
    submissions = get_submissions(
        totalStandings, range_p)[(page - 1) * page_limit:page_limit * page]

    return render_template(
        "submissions.html", submissions=submissions, page=page)


if __name__ == "__main__":
    Bootstrap(app)
    app.run(host="0.0.0.0", port=1818, debug=True)
