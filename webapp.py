from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("hello.html", name="alik")


if __name__ == "__main__":
    app.run()
