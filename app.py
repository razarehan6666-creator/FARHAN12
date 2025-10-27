from flask import Flask, render_template, jsonify
import pandas as pd
import math

app = Flask(__name__)

# 🔗 Replace this link with your own Google Sheets CSV (Published link)
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugS1umqSfK/pub?output=csv"

def load_data():
    df = pd.read_csv(EXCEL_URL)
    df.fillna("NO DATA", inplace=True)
    return df

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/month/<month>')
def get_month_data(month):
    try:
        df = load_data()
        row = df.loc[df['Month'].str.lower() == month.lower()]

        if row.empty:
            return jsonify({"error": f"No data found for {month}"})

        row = row.iloc[0].to_dict()

        # Extract core values safely
        days_in_month = int(row.get("Days in Month", 0))
        days_coming = int(row.get("Days Coming", 0))

        # ✅ Auto calculations
        days_absent = days_in_month - days_coming
        amount = days_coming * 50  # ₹50 per day fixed rate

        result = {
            "Month": month.upper(),
            "Paid": row.get("Paid", "NO DATA"),
            "Days in Month": days_in_month,
            "Days Coming": days_coming,
            "Days Absent": days_absent,
            "Amount": f"{amount:.2f}",
            "Payment Mode": row.get("Payment Mode", "NO DATA")
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error loading data: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
