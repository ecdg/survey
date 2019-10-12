import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    # Alerts user if fields are empty
    if not request.form.get("firstname"):
        return render_template("error.html", error="provide your first name")
    elif not request.form.get("lastname"):
        return render_template("error.html", error="provide your last name")
    elif not request.form.get("visited"):
        return render_template("error.html", error="answer the \"yes\" or \"no\" question")
    elif not request.form.get("country"):
        return render_template("error.html", error="select a country")
    elif len(request.form.getlist("city")) < 7:
        return render_template("error.html", error="check 7 boxes")
    elif len(request.form.getlist("city")) > 7:
        return render_template("error.html", error="only check 7 boxes")

    # Writes the form's values in survey.csv
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["firstname", "lastname", "visited", "country", "city"])
        writer.writerow({"firstname": request.form.get("firstname"),
                         "lastname": request.form.get("lastname"),
                         "visited": request.form.get("visited"),
                         "country": request.form.get("country"),
                         "city": (", ".join(str(i) for i in request.form.getlist("city")))})
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Reads survey.csv and displays it in a table on sheet.html
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        entries = list(reader)
    return render_template("sheet.html", entries=entries)