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
   month_row = df[df['MONTH'].str.strip().str.upper() == month_name.upper()]

row = month_row.iloc[0]
return {
    "Month": row["MONTH"],
    "Paid": row["PAID"],
    "Days in Month": row["NO. OF DAYS IN MONTH"],
    "Days Absent": row["NO. OF DAYS ABSENT"],
    "Days Coming": row["NO. OF DAYS COMING"],
    "Amount": row["AMOUNT"]
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






