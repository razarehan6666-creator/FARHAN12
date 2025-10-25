from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Replace this with your Google Sheets CSV link
EXCEL_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTPIR5j2TyzJAorJsGX9reIhOXQKrTfyDbbv2GreXPDf2nWcBCddhoedW93yEaK1S93imugCke-dRD_/pub?output=csv"


def get_month_data(month_name):
    try:
        df = pd.read_csv(EXCEL_URL)
    except Exception as e:
        return {"error": f"Cannot fetch Google Sheet: {e}"}

    df = df.fillna("")  # Replace empty cells
    # Find the row that matches the month
    month_row = df[df['Month'].str.strip().str.upper() == month_name.upper()]
    if month_row.empty:
        return {"error": "No data found for this month"}

    row = month_row.iloc[0]
    return {
        "Month": row["Month"],
        "Paid": row["Paid"],
        "Days in Month": row["Days in Month"],
        "Days Absent": row["Days Absent"],
        "Days Coming": row["Days Coming"],
        "Amount": row["Amount"]
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/month/<month_name>")
def month_data(month_name):
    return jsonify(get_month_data(month_name))

if __name__ == "__main__":
    # Use host 0.0.0.0 for deployment platforms like Render
    app.run(host="0.0.0.0", port=5000, debug=True)





