import json
import os
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import BadRequest

BASE_DIR = Path(__file__).resolve().parent
STATIC_JSON_DIR = BASE_DIR / "static" / "src"
EXCEL_PATH = BASE_DIR / "data" / "practice-tracker.xlsx"
PRACTICE_JSON = STATIC_JSON_DIR / "data.json"
CROSSFIT_JSON = STATIC_JSON_DIR / "crossfitData.json"
PRACTICE_SHEET = "practiceTracker"
CROSSFIT_SHEET = "crossfitStats"
ALLOWED_GOAL_DISTANCES = {"5K", "10K", "Half Marathon", "Marathon"}

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JSON_SORT_KEYS"] = False


def ensure_data_dir():
    STATIC_JSON_DIR.mkdir(parents=True, exist_ok=True)


def load_sheet(sheet_name):
    try:
        return pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
    except (FileNotFoundError, ValueError):
        return pd.DataFrame()


def write_json(path, records):
    with path.open("w", encoding="utf-8") as output_file:
        json.dump(records, output_file, indent=2)


def excel_date_to_iso(date_value):
    if pd.isna(date_value):
        return None
    if isinstance(date_value, str):
        return value if (value := date_value) else None
    return pd.Timestamp(date_value).strftime("%Y-%m-%d")


def refresh_json_files():
    ensure_data_dir()
    if EXCEL_PATH.exists():
        practice_df = load_sheet(PRACTICE_SHEET)
        if "Date" in practice_df.columns:
            practice_df["Date"] = practice_df["Date"].apply(excel_date_to_iso)
        write_json(PRACTICE_JSON, practice_df.to_dict(orient="records"))

        crossfit_df = load_sheet(CROSSFIT_SHEET)
        if "Date" in crossfit_df.columns:
            crossfit_df["Date"] = crossfit_df["Date"].apply(excel_date_to_iso)
        write_json(CROSSFIT_JSON, crossfit_df.to_dict(orient="records"))
    else:
        if not PRACTICE_JSON.exists():
            PRACTICE_JSON.write_text("[]", encoding="utf-8")
        if not CROSSFIT_JSON.exists():
            CROSSFIT_JSON.write_text("[]", encoding="utf-8")


def read_json(path):
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as input_file:
            return json.load(input_file)
    except json.JSONDecodeError:
        return []


def normalize_boolean(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "on")
    return bool(value)


def parse_iso_date(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Date must be a non-empty string in YYYY-MM-DD format.")
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD format.")


def validate_practice_payload(payload):
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    return {
        "Date": parse_iso_date(payload.get("Date")),
        "Planks": normalize_boolean(payload.get("Planks")),
        "Pullups": normalize_boolean(payload.get("Pullups")),
        "Double-unders": normalize_boolean(payload.get("Double-unders")),
    }


def save_practice_entry(entry):
    practice_data = read_json(PRACTICE_JSON)
    practice_data.append(entry)
    practice_data.sort(key=lambda item: item.get("Date", ""))
    write_json(PRACTICE_JSON, practice_data)

    if EXCEL_PATH.exists():
        df = pd.DataFrame(practice_data)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=PRACTICE_SHEET, index=False)


def generate_running_plan(current_miles, goal_distance, race_date, runs_per_week):
    targets = {"5K": 3.1, "10K": 6.2, "Half Marathon": 13.1, "Marathon": 26.2}
    goal_miles = targets.get(goal_distance, 3.1)
    
    today = date.today()
    weeks_until_race = max(1, (race_date - today).days // 7)
    
    # Determine long run increase based on plan length
    if weeks_until_race >= 12:
        long_run_increase = 1.0  # 1 mile per week
    elif weeks_until_race >= 8:
        long_run_increase = 1.5  # 1.5 miles per week
    else:
        long_run_increase = 2.0  # 2 miles per week
    
    plan = []
    base_mileage = max(current_miles, 3.0)
    
    for week in range(1, weeks_until_race + 1):
        long_run = round_up_to_half_mile(min(base_mileage + week * long_run_increase, goal_miles * 0.75))
        
        week_runs = {}
        if runs_per_week >= 1:
            week_runs["Easy Run"] = f"{round_up_to_half_mile(max(2.0, base_mileage + (week - 1) * 0.75))} miles"
        if runs_per_week >= 2:
            week_runs["Tempo Run"] = f"{round_up_to_half_mile(max(2.0, long_run - 0.5))} miles"
        if runs_per_week >= 3:
            week_runs["Hill Repeats"] = f"{round_up_to_half_mile(max(1.0, long_run * 0.3))} miles"
        if runs_per_week >= 4:
            week_runs["Intervals"] = f"{round_up_to_half_mile(max(1.5, long_run * 0.4))} miles"
        
        plan.append({
            "Week": week,
            "Long Run": f"{long_run} miles",
            **week_runs,
            "Goal": goal_distance,
        })
    
    return plan


import math

def round_up_to_half_mile(distance):
    # Round up to nearest half mile
    return math.ceil(distance * 2) / 2


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=()"
    return response


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/crossfit")
def crossfit_page():
    return render_template("crossfit.html")


@app.route("/planks")
def planks_page():
    return render_template("planks.html")


@app.route("/running")
def running_page():
    return render_template("running.html")


@app.route("/api/practice", methods=["GET"])
def practice_data():
    return jsonify(read_json(PRACTICE_JSON))


@app.route("/api/practice", methods=["POST"])
def add_practice():
    try:
        payload = request.get_json(force=True)
    except BadRequest:
        return jsonify({"error": "Invalid JSON body."}), 400

    try:
        entry = validate_practice_payload(payload)
        save_practice_entry(entry)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Unable to save the practice entry."}), 500

    return jsonify({"status": "success", "entry": entry}), 201


@app.route("/api/crossfit", methods=["GET"])
def crossfit_data():
    return jsonify(read_json(CROSSFIT_JSON))


@app.route("/api/running-plan", methods=["POST"])
def running_plan():
    try:
        payload = request.get_json(force=True)
    except BadRequest:
        return jsonify({"error": "Invalid JSON body."}), 400

    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        current_miles = float(payload.get("currentMileage", 0) or 0)
    except (TypeError, ValueError):
        return jsonify({"error": "currentMileage must be a number."}), 400

    goal_distance = payload.get("goalDistance", "5K")
    if goal_distance not in ALLOWED_GOAL_DISTANCES:
        return jsonify({"error": f"goalDistance must be one of {sorted(ALLOWED_GOAL_DISTANCES)}."}), 400

    race_date_str = payload.get("raceDate")
    if not race_date_str:
        return jsonify({"error": "raceDate is required."}), 400
    try:
        race_date = datetime.fromisoformat(race_date_str).date()
    except ValueError:
        return jsonify({"error": "raceDate must be in YYYY-MM-DD format."}), 400

    try:
        runs_per_week = int(payload.get("runsPerWeek", 3))
        if not 1 <= runs_per_week <= 4:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "runsPerWeek must be an integer between 1 and 4."}), 400

    return jsonify({"goalDistance": goal_distance, "plan": generate_running_plan(current_miles, goal_distance, race_date, runs_per_week)})


if __name__ == "__main__":
    refresh_json_files()
    use_debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=use_debug, host="127.0.0.1", port=5000)
