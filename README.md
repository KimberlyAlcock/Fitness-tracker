# Fitness Tracker

A Flask-based fitness website that loads practice and CrossFit data from Excel and exposes it in a web application.

## Setup

1. Create and activate the virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. Run the app locally:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

4. Open the app in your browser:

   `http://127.0.0.1:5000`

## Development

- The app loads practice and CrossFit data from `data/practice-tracker.xlsx` on startup.
- Practice entries are persisted to both `static/src/data.json` and back into the Excel workbook.
- The running page generates a simple 4-week plan based on the current mileage and goal distance.

## Security and quality notes

- The app now validates incoming JSON payloads and rejects malformed requests with `400`.
- Security response headers are set to reduce common browser-based risks.
- The app uses the environment variable `FLASK_DEBUG=1` only when explicitly set, so debug mode is not enabled by default.
- A `.gitignore` file is included to keep generated files and local environment artifacts out of version control.

## Tests

Run tests locally after installing dependencies:

```powershell
.\.venv\Scripts\python.exe -m pytest tests
```

Run coverage with:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing tests
```

Or use the VS Code tasks: `Run Tests` or `Run Coverage`.

## Cleanup

This project currently contains an unused `node_modules` folder and `package.json` from an older Node/Express setup. Those are not required for the current Flask application.

## Notes

- Do not run the app with debug mode enabled in production.
- Use `FLASK_DEBUG=1` only for local development if you need live debugging.
