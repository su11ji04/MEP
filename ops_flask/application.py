from flask import Flask, render_template
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/korea")
def view_korea():
    return render_template("korea_index.html")

@application.route("/china")
def view_china():
    return render_template("china_index.html")

@application.route("/japan")
def view_japan():
    return render_template("japan_index.html")

@application.route("/west")
def view_west():
    return render_template("westerm_index.html")

@application.route("/fast")
def view_fast():
    return render_template("fastfood.html")

@application.route("/desert")
def view_desert():
    return render_template("desert_index.html")

@application.route("/foodcourse")
def view_foodcourse():
    return render_template("foodcourse.html")

@application.route("/mep_registration")
def view_registration():
    return render_template("mep_registration.html")


if __name__ == "__main__":
    application.run(host='0.0.0.0')
    application.run(debug=True)
