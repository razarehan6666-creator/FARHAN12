from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# 🔗 Your Google Sheets CSV link
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

def load_data():
    df = pd.read_csv(EXCEL_URL)
    # normalize column names (remove spaces and make uppercase)
    df.columns = df.columns.str.strip().str.upper()
    df.fillna("NO DATA", inplace=True)
    return df

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/month/<month>')
def get_month_data(month):
    try:
        df = load_data()

        # ✅ Check if 'MONTH' column exists
        if 'MONTH' not in df.columns:
            return jsonify({"error": "Google Sheet missing required column: MONTH"})

        # ✅ Find row (case-insensitive match)
        mask = df['MONTH'].astype(str).str.strip().str.upper() == month.strip().upper()
        month_rows = df[mask]

        if month_rows.empty:
            return jsonify({"error": f"No data found for {month}"})

        row = month_rows.iloc[0].to_dict()

        # ✅ Safely extract numbers
        try:
            days_in_month = int(row.get("NO. OF DAYS IN MONTH", 0))
            days_coming = int(row.get("NO. OF DAYS COMING", 0))
        except ValueError:
            days_in_month = 0
            days_coming = 0

        # ✅ Auto-calculated fields
        days_absent = days_in_month - days_coming
        total_bill = days_coming * 50  # ₹50 per day

        # ✅ Lowercase all JSON keys for consistency
        result = {
            "month": row.get("MONTH", month),
            "paid": row.get("PAID", "NO DATA"),
            "days_in_month": days_in_month,
            "days_coming": days_coming,
            "days_absent": days_absent,
            "amount": f"{total_bill:.2f}",
            "payment_mode": row.get("PAYMENT MODE", "NO DATA")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error loading data: {e}"})

if __name__ == '__main__':
    # ✅ Added explicit port
    app.run(host="0.0.0.0", port=5000, debug=True)
