from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Google Sheets CSV link
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

# Expected columns in sheet
EXPECTED_COLUMNS = [
    "MONTH",
    "PAID",
    "NO. OF DAYS IN MONTH",
    "NO. OF DAYS ABSENT",
    "NO. OF DAYS COMING",
    "LITRE PER DAY",
    "PAYMENT MODE"
]

# Fixed rate per litre
RATE_PER_LITRE = 50


def get_month_data(month_name):
    """Fetch CSV, normalize, and return month data with calculated amount."""
    try:
        df = pd.read_csv(EXCEL_URL)
    except Exception as e:
        return {"error": f"Cannot fetch Google Sheet: {e}"}

    df.columns = df.columns.str.strip().str.upper()

    # Check for missing columns
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        return {"error": f"Google Sheet missing columns: {', '.join(missing)}"}

    # Filter by month (case insensitive)
    mask = df['MONTH'].astype(str).str.strip().str.upper() == month_name.strip().upper()
    month_rows = df[mask]

    if month_rows.empty:
        return {"error": "No data found for this month"}

    row = month_rows.iloc[0]

    # Convert to numbers safely
    days_coming = pd.to_numeric(row.get("NO. OF DAYS COMING", 0), errors="coerce") or 0
    litre_per_day = pd.to_numeric(row.get("LITRE PER DAY", 0), errors="coerce") or 0

    # Calculate the amount
    calculated_amount = days_coming * litre_per_day * RATE_PER_LITRE

    return {
        "Month": row.get("MONTH", ""),
        "Paid": row.get("PAID", ""),
        "Days in Month": row.get("NO. OF DAYS IN MONTH", ""),
        "Days Absent": row.get("NO. OF DAYS ABSENT", ""),
        "Days Coming": row.get("NO. OF DAYS COMING", ""),
        "Amount": row.get("AMOUNT", "")
        "Payment Mode": row.get("PAYMENT MODE", "")
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/month/<month_name>")
def month_data(month_name):
    return jsonify(get_month_data(month_name))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


