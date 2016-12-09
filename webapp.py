from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from os import listdir
from os.path import isfile, join
from parser_xml import parse_standing_from_file as parse_file

app = Flask(__name__)


@app.route("/")
def hello_world():
    files = getFiles("./samples")
    return render_template("index.html", files=files, standings=None)


def getFiles(mypath):
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]


@app.route("/showtable/<string:table>")
def showtable(table):
    files = getFiles("./samples")
    standings = parse_file("./samples/" + table) \
        if table in files else None

    return render_template("index.html", files=files, standings=standings)


if __name__ == "__main__":
    Bootstrap(app)
    app.run(debug=True)
