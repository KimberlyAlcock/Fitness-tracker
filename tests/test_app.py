import json
from pathlib import Path

import pytest

import app as tracker_app


@pytest.fixture
def client():
    tracker_app.app.config["TESTING"] = True
    with tracker_app.app.test_client() as client:
        yield client


def test_normalize_boolean():
    assert tracker_app.normalize_boolean(True) is True
    assert tracker_app.normalize_boolean(False) is False
    assert tracker_app.normalize_boolean("true") is True
    assert tracker_app.normalize_boolean("0") is False
    assert tracker_app.normalize_boolean("yes") is True
    assert tracker_app.normalize_boolean(1) is True


def test_parse_iso_date_valid():
    assert tracker_app.parse_iso_date("2026-04-08") == "2026-04-08"


def test_parse_iso_date_invalid():
    with pytest.raises(ValueError):
        tracker_app.parse_iso_date("04/08/2026")


def test_validate_practice_payload_valid():
    payload = {
        "Date": "2026-04-08",
        "Planks": "true",
        "Pullups": "false",
        "Double-unders": "on",
    }
    entry = tracker_app.validate_practice_payload(payload)
    assert entry["Date"] == "2026-04-08"
    assert entry["Planks"] is True
    assert entry["Pullups"] is False
    assert entry["Double-unders"] is True


def test_generate_running_plan():
    plan = tracker_app.generate_running_plan(5.0, "10K")
    assert len(plan) == 4
    assert plan[0]["Goal"] == "10K"
    assert all("miles" in item["Easy Run"] for item in plan)


def test_get_crossfit_data(client):
    response = client.get("/api/crossfit")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_post_practice_entry(client, tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    monkeypatch.setattr(tracker_app, "PRACTICE_JSON", data_file)
    monkeypatch.setattr(tracker_app, "EXCEL_PATH", tmp_path / "practice-tracker.xlsx")

    payload = {
        "Date": "2026-04-08",
        "Planks": True,
        "Pullups": False,
        "Double-unders": True,
    }
    response = client.post("/api/practice", json=payload)

    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == "success"
    assert body["entry"]["Date"] == "2026-04-08"
    assert data_file.exists()
    content = json.loads(data_file.read_text(encoding="utf-8"))
    assert content[0]["Planks"] is True


def test_post_practice_invalid_json(client):
    response = client.post("/api/practice", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert "Invalid JSON body" in response.get_json()["error"]


def test_running_plan_endpoint(client):
    response = client.post("/api/running-plan", json={"currentMileage": 5, "goalDistance": "5K"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["goalDistance"] == "5K"
    assert len(data["plan"]) == 4


def test_running_plan_invalid_goal(client):
    response = client.post("/api/running-plan", json={"currentMileage": 5, "goalDistance": "100K"})
    assert response.status_code == 400
    assert "goalDistance must be one of" in response.get_json()["error"]


def test_read_json_invalid_json(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not a json", encoding="utf-8")
    assert tracker_app.read_json(bad_file) == []


def test_refresh_json_files_creates_empty_json_when_excel_missing(tmp_path, monkeypatch):
    practice_json = tmp_path / "data.json"
    crossfit_json = tmp_path / "crossfitData.json"
    monkeypatch.setattr(tracker_app, "EXCEL_PATH", tmp_path / "missing.xlsx")
    monkeypatch.setattr(tracker_app, "PRACTICE_JSON", practice_json)
    monkeypatch.setattr(tracker_app, "CROSSFIT_JSON", crossfit_json)

    tracker_app.refresh_json_files()

    assert practice_json.exists()
    assert crossfit_json.exists()
    assert json.loads(practice_json.read_text(encoding="utf-8")) == []
    assert json.loads(crossfit_json.read_text(encoding="utf-8")) == []


def test_static_routes_return_ok(client):
    for route in ["/", "/crossfit", "/planks", "/running"]:
        response = client.get(route)
        assert response.status_code == 200
        assert "text/html" in response.content_type


def test_security_headers(client):
    response = client.get("/")
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Referrer-Policy"] == "no-referrer-when-downgrade"


def test_post_practice_missing_date(client):
    response = client.post("/api/practice", json={"Planks": True, "Pullups": False, "Double-unders": True})
    assert response.status_code == 400
    assert "Date must be a non-empty string" in response.get_json()["error"]


def test_running_plan_invalid_mileage(client):
    response = client.post("/api/running-plan", json={"currentMileage": "abc", "goalDistance": "5K"})
    assert response.status_code == 400
    assert "currentMileage must be a number" in response.get_json()["error"]


def test_load_sheet_returns_empty_dataframe_when_excel_missing(monkeypatch, tmp_path):
    missing_excel = tmp_path / "missing.xlsx"
    monkeypatch.setattr(tracker_app, "EXCEL_PATH", missing_excel)
    df = tracker_app.load_sheet("practiceTracker")
    assert df.empty


def test_refresh_json_files_reads_excel_and_writes_json(tmp_path, monkeypatch):
    excel_path = tmp_path / "practice-tracker.xlsx"
    practice_json = tmp_path / "data.json"
    crossfit_json = tmp_path / "crossfitData.json"

    import pandas as pd
    practice_df = pd.DataFrame({"Date": ["2026-04-08"], "Planks": [True], "Pullups": [False], "Double-unders": [True]})
    crossfit_df = pd.DataFrame({"Skill": ["Snatch"], "Stat": ["100lbs"], "Date": ["2026-04-08"]})
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        practice_df.to_excel(writer, sheet_name="practiceTracker", index=False)
        crossfit_df.to_excel(writer, sheet_name="crossfitStats", index=False)

    monkeypatch.setattr(tracker_app, "EXCEL_PATH", excel_path)
    monkeypatch.setattr(tracker_app, "PRACTICE_JSON", practice_json)
    monkeypatch.setattr(tracker_app, "CROSSFIT_JSON", crossfit_json)

    tracker_app.refresh_json_files()

    assert practice_json.exists()
    assert crossfit_json.exists()
    practice_data = json.loads(practice_json.read_text(encoding="utf-8"))
    crossfit_data = json.loads(crossfit_json.read_text(encoding="utf-8"))
    assert practice_data[0]["Date"] == "2026-04-08"
    assert crossfit_data[0]["Skill"] == "Snatch"


def test_save_practice_entry_writes_excel_when_excel_exists(tmp_path, monkeypatch):
    data_file = tmp_path / "data.json"
    excel_path = tmp_path / "practice-tracker.xlsx"
    monkeypatch.setattr(tracker_app, "PRACTICE_JSON", data_file)
    monkeypatch.setattr(tracker_app, "EXCEL_PATH", excel_path)

    # Create an empty Excel file with the expected sheet
    import pandas as pd
    pd.DataFrame(columns=["Date", "Planks", "Pullups", "Double-unders"]).to_excel(excel_path, sheet_name="practiceTracker", index=False)

    entry = {"Date": "2026-04-09", "Planks": True, "Pullups": False, "Double-unders": False}
    tracker_app.save_practice_entry(entry)

    assert data_file.exists()
    loaded = json.loads(data_file.read_text(encoding="utf-8"))
    assert loaded[0]["Date"] == "2026-04-09"
    assert excel_path.exists()


def test_validate_practice_payload_non_dict_raises():
    with pytest.raises(ValueError):
        tracker_app.validate_practice_payload(None)
