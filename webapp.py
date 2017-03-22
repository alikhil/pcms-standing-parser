"""
Web applicaiton for browsing pcms standing results, submission and analytics
"""

import time
from os import listdir
from os.path import isfile, join
from datetime import datetime

from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_bootstrap import Bootstrap

from parser_xml import parse_standing_from_file as parse_file
from classes import TotalStandings
from submissions import get_submissions
from analytics import get_analytics
import config

app = Flask(__name__)

def parse_date(range_p):
    if range_p is None:
        return None
    try:
        dates = range_p.split("-")
        start = time.mktime(
            datetime.strptime(dates[0], "%d.%m.%Y").timetuple())
        end = time.mktime(
            datetime.strptime(dates[1], "%d.%m.%Y").timetuple()) + 86399
        return (start, end)
    except:
        print("Unable to parse date from:" + range_p)
        return None

def get_files_and_standing():
    """Read from samples directory standings and list of files"""

    files = get_files(config.XML_DIR)
    standings = []
    files_list = []
    for file in files:
        standing = parse_file(config.XML_DIR + file)
        standings.append(standing)
        files_list.append({"path": file, "name": standing.contest.name})
    total_standings = TotalStandings(standings)
    files_list = sorted(files_list, key=lambda t: t["name"])
    return files_list, total_standings


@app.route("/pcms_standings")
@app.route("/")
def main_route():
    files_list, total_standings = get_files_and_standing()
    groups = total_standings.get_groups()
    return render_template(
        "index.html", files=files_list, groups=groups,
        standings=None, totalStandings=total_standings)


def get_files(mypath):
    """Get list of files in samples directory"""
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]

@app.route("/pcms_standings/static/<path:path>")
def sent_static(path):
    """Route for static resources"""
    return send_from_directory("static", path)


@app.route("/showtable/<string:table>")
@app.route("/pcms_standings/showtable/<string:table>")
def show_table(table):
    """Return standing table for chosen file"""

    files, total_standings = get_files_and_standing()
    standings = parse_file(config.XML_DIR + table) \
        if table in [file["path"] for file in files] else None

    groups = standings.get_groups()
    return render_template(
        "index.html", files=files, standings=standings,
        totalStandings=None, groups=groups)


@app.route("/submissions", methods=["GET"])
@app.route("/pcms_standings/submissions", methods=["GET"])
def show_submissions():
    """List submission by filter"""

    page_limit = config.PAGE_LIMIT
    page_p = request.args.get("page")
    page = 1 if page_p is None else int(page_p)
    range_p = parse_date(request.args.get("range"))
    group_p = request.args.get("group")

    files = get_files(config.XML_DIR)
    total_standings = TotalStandings(
        [parse_file(config.XML_DIR + file) for file in files])
    submissions = get_submissions(total_standings, range_p, group_p)

    submissions = submissions[(page - 1) * page_limit:page_limit * page]

    return render_template(
        "submissions.html", submissions=submissions, page=page)

@app.route("/analytics", methods=["GET"])
@app.route("/pcms_standings/analytics", methods=["GET"])
def analytics():
    return render_template("analytics.html")

@app.route("/analytics/get_data", methods=["GET"])
@app.route("/pcms_standings/analytics/get_data", methods=["GET"])
def get_data():

    group_p = request.args.get("group")
    range_p = parse_date(request.args.get("range"))
    data_type_p = request.args.get("data_type")
    if data_type_p not in ["day", "month"]:
        data_type_p = "month"
    files = get_files(config.XML_DIR)
    total_standings = TotalStandings(
        [parse_file(config.XML_DIR + file) for file in files])
    submissions = get_submissions(total_standings, range_p, group_p)
    result = get_analytics(submissions, data_type_p)

    return jsonify(result)

if __name__ == "__main__":
    Bootstrap(app)
    app.run(host="0.0.0.0", port=1818, debug=True)
