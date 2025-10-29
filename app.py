from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# ✅ Your published Google Sheets CSV link
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"

def load_data():
    df = pd.read_csv(EXCEL_URL)
    # Normalize column names (remove spaces + uppercase)
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

        if 'MONTH' not in df.columns:
            return jsonify({"error": "Google Sheet missing required column: MONTH"})

        # Find row for month (case-insensitive)
        mask = df['MONTH'].astype(str).str.strip().str.upper() == month.strip().upper()
        month_rows = df[mask]

        if month_rows.empty:
            return jsonify({"error": f"No data found for {month}"})

        row = month_rows.iloc[0].to_dict()

        # Convert safe values
        try:
            days_in_month = int(row.get("NO. OF DAYS IN MONTH", 0))
        except:
            days_in_month = 0
        try:
            days_coming = int(row.get("NO. OF DAYS COMING", 0))
        except:
            days_coming = 0

        # ✅ Auto calculations
        days_absent = max(days_in_month - days_coming, 0)
        total_bill = days_coming * 50  # ₹50 per day

        # ✅ Return consistent data
        result = {
            "month": row.get("MONTH", month),
            "paid": row.get("PAID", "NO DATA"),
            "days_in_month": days_in_month,
            "days_coming": days_coming,
            "days_absent": days_absent,
            "amount": total_bill,
            "payment_mode": row.get("PAYMENT MODE", "NO DATA")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error loading data: {e}"})

# ✅ Flask should run on all interfaces + port 5000 for Render
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


