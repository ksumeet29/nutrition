#!/usr/bin/env python3
"""Flask front-end for the C++ macros calculator.

Renders an input form (index.html) and a results page (result.html),
delegating the actual TDEE/macro calculation to the Bazel-built `main`
binary from the parent project.
"""
import json
import os
import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Where to find the compiled calculator binary. Allows overriding via env var
# (used by the Docker image, which copies the binary to a fixed location)
# and otherwise falls back to Bazel's default output path.
MAIN_BINARY = os.environ.get(
    "MACROS_BINARY", os.path.join(PROJECT_ROOT, "bazel-bin", "main")
)

GOAL_LABELS = {"1": "Fat Loss", "2": "Maintenance", "3": "Muscle Gain"}
SEX_LABELS = {"1": "Male", "2": "Female"}
ACTIVITY_LABELS = {
    "1.2": "Sedentary (little/no exercise)",
    "1.375": "Lightly Active (1-3 days/week)",
    "1.55": "Moderately Active (3-5 days/week)",
    "1.725": "Very Active (6-7 days/week)",
    "1.9": "Extra Active (hard daily training/physical job)",
}
TDEE_METHOD_LABELS = {
    "1": "Mifflin-St Jeor",
    "2": "Harris-Benedict",
    "3": "Katch-McArdle",
}


def ensure_binary_built():
    """Build the //:main Bazel target on first use if it isn't there yet."""
    if not os.path.isfile(MAIN_BINARY):
        subprocess.run(
            ["bazel", "build", "-c", "opt", "//:main"],
            cwd=PROJECT_ROOT,
            check=True,
        )


def convert_inputs(form):
    weight = float(form["weight"])
    height = float(form["height"])
    weight_unit = form.get("weight_unit", "kg")
    height_unit = form.get("height_unit", "cm")

    if isinstance(weight_unit, list):
        weight_unit = weight_unit[0] if weight_unit else "kg"
    if isinstance(height_unit, list):
        height_unit = height_unit[0] if height_unit else "cm"

    if weight_unit == "lb":
        weight = weight * 0.45359237
    if height_unit == "in":
        height = height * 2.54

    return weight, height


def run_calculator(form):
    ensure_binary_built()
    weight_kg, height_cm = convert_inputs(form)
    deficit = form.get("deficit", "0") or "0"
    tdee_method = form.get("tdee_method", "1") or "1"
    sex_value = form.get("sex_value") or form.get("sex")
    goal_value = form.get("goal_value") or form.get("goal")

    args = [
        MAIN_BINARY,
        str(weight_kg),
        str(height_cm),
        form["age"],
        sex_value,
        form["bodyfat"],
        form["trainingdays"],
        goal_value,
        form["mul"],
        deficit,
        tdee_method,
    ]
    proc = subprocess.run(args, capture_output=True, text=True, check=True)
    return json.loads(proc.stdout)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok", 200


@app.route("/result", methods=["POST"])
def result():
    error = None
    data = None
    try:
        data = run_calculator(request.form)
    except Exception as exc:  # noqa: BLE001 - surface any calc/parse failure to the page
        error = str(exc)

    mul_value = request.form.get("mul")
    weight_unit = request.form.get("weight_unit", "kg")
    height_unit = request.form.get("height_unit", "cm")
    if isinstance(weight_unit, list):
        weight_unit = weight_unit[0] if weight_unit else "kg"
    if isinstance(height_unit, list):
        height_unit = height_unit[0] if height_unit else "cm"
    tdee_method = request.form.get("tdee_method", "1")
    sex_value = request.form.get("sex_value") or request.form.get("sex")
    goal_value = request.form.get("goal_value") or request.form.get("goal")
    inputs = {
        "weight": request.form.get("weight"),
        "height": request.form.get("height"),
        "weight_unit": weight_unit,
        "height_unit": height_unit,
        "age": request.form.get("age"),
        "sex": SEX_LABELS.get(sex_value, "-"),
        "sex_value": sex_value,
        "bodyfat": request.form.get("bodyfat"),
        "trainingdays": request.form.get("trainingdays"),
        "goal": GOAL_LABELS.get(goal_value, "-"),
        "goal_value": goal_value,
        "mul": mul_value,
        "mul_label": ACTIVITY_LABELS.get(mul_value, "Custom"),
        "deficit": request.form.get("deficit", "0"),
        "tdee_method": tdee_method,
        "tdee_method_label": TDEE_METHOD_LABELS.get(tdee_method, "Mifflin-St Jeor"),
    }

    return render_template("result.html", data=data, error=error, inputs=inputs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Enable debug/auto-reload for local development so edits to this file or
    # the templates take effect immediately. Set FLASK_DEBUG=0 in production.
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
