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
DEFICIT_LABELS = {"1": "Aggressive", "2": "Moderate"}
SEX_LABELS = {"1": "Male", "2": "Female"}
ACTIVITY_LABELS = {
    "1.2": "Sedentary (little/no exercise)",
    "1.375": "Lightly Active (1-3 days/week)",
    "1.55": "Moderately Active (3-5 days/week)",
    "1.725": "Very Active (6-7 days/week)",
    "1.9": "Extra Active (hard daily training/physical job)",
}


def ensure_binary_built():
    """Build the //:main Bazel target on first use if it isn't there yet."""
    if not os.path.isfile(MAIN_BINARY):
        subprocess.run(
            ["bazel", "build", "-c", "opt", "//:main"],
            cwd=PROJECT_ROOT,
            check=True,
        )


def run_calculator(form):
    ensure_binary_built()
    args = [
        MAIN_BINARY,
        form["weight"],
        form["height"],
        form["age"],
        form["sex"],
        form["bodyfat"],
        form["trainingdays"],
        form["goal"],
        form["mul"],
        form["deficit"],
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
    inputs = {
        "weight": request.form.get("weight"),
        "height": request.form.get("height"),
        "age": request.form.get("age"),
        "sex": SEX_LABELS.get(request.form.get("sex"), "-"),
        "bodyfat": request.form.get("bodyfat"),
        "trainingdays": request.form.get("trainingdays"),
        "goal": GOAL_LABELS.get(request.form.get("goal"), "-"),
        "mul": mul_value,
        "mul_label": ACTIVITY_LABELS.get(mul_value, "Custom"),
        "deficit": DEFICIT_LABELS.get(request.form.get("deficit"), "-"),
    }

    return render_template("result.html", data=data, error=error, inputs=inputs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Enable debug/auto-reload for local development so edits to this file or
    # the templates take effect immediately. Set FLASK_DEBUG=0 in production.
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
