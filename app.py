from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Google Sheets CSV link
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

# Expected columns
EXPECTED_COLUMNS = [
    "MONTH",
    "PAID",
    "NO. OF DAYS IN MONTH",
    "NO. OF DAYS ABSENT",
    "NO. OF DAYS COMING",
    "PAYMENT MODE"
]

# Fixed rate per day
RATE_PER_DAY = 50


def get_month_data(month_name):
    """Fetch CSV and calculate amount = Days Coming × ₹50"""
    try:
        df = pd.read_csv(EXCEL_URL)
    except Exception as e:
        return {"error": f"Cannot fetch Google Sheet: {e}"}

    # Normalize column names
    df.columns = df.columns.str.strip().str.upper()

    # Check for missing columns
    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing:
        return {"error": f"Google Sheet missing expected columns: {', '.join(missing)}"}

    # Find row for the requested month
    mask = df['MONTH'].astype(str).str.strip().str.upper() == month_name.strip().upper()
    month_rows = df[mask]

    if month_rows.empty:
        return {"error": "No data found for this month"}

    row = month_rows.iloc[0]

    # Calculate amount safely
    try:
        days_coming = float(row.get("NO. OF DAYS COMING", 0))
    except (TypeError, ValueError):
        days_coming = 0

    calculated_amount = days_coming * RATE_PER_DAY

    return {
        "Month": row.get("MONTH", ""),
        "Paid": row.get("PAID", ""),
        "Days in Month": row.get("NO. OF DAYS IN MONTH", ""),
        "Days Absent": row.get("NO. OF DAYS ABSENT", ""),
        "Days Coming": days_coming,
        "Amount": f"₹{calculated_amount:.2f}",   # show as ₹1234.00
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

