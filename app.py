from flask import Flask, render_template, request
import pandas as pd
import joblib
import shap
from features_columns import FEATURE_COLUMNS

app = Flask(__name__)

# Load the trained model once
model = joblib.load("models/xgboost_nids_model.pkl")

label_mapping = {
    0: "Benign",
    1: "Bot",
    2: "DDoS",
    3: "DoS GoldenEye",
    4: "DoS Hulk",
    5: "DoS Slowhttptest",
    6: "DoS slowloris",
    7: "FTP-Patator",
    8: "Heartbleed",
    9: "Infiltration",
    10: "PortScan",
    11: "SSH-Patator",
    12: "Web Attack - Brute Force",
    13: "Web Attack - Sql Injection",
    14: "Web Attack - XSS"
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # CHANGED
    file = request.files.get("file")

    # CHANGED
    if file is None or file.filename == "":
        return "<h2>Error: Please select a CSV file.</h2>"

    # CHANGED
    if not file.filename.lower().endswith(".csv"):
        return "<h2>Error: Please upload a CSV file.</h2>"

    try:
        df = pd.read_csv(file)
    except Exception:
        return "<h2>Error: Could not read the CSV file.</h2>"

    # CHANGED
    if df.empty:
        return "<h2>Error: CSV file is empty.</h2>"

    missing_columns = [
        col for col in FEATURE_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        return (
            "<h2>Error: Missing Required Columns</h2><br>"
            + "<br>".join(missing_columns)
        )

    # CHANGED
    df = df[FEATURE_COLUMNS]

    # CHANGED
    non_numeric_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # CHANGED
    if non_numeric_columns:
        return (
            "<h2>Error: Non-numeric values found in required columns</h2><br>"
            + "<br>".join(non_numeric_columns)
        )

    # CHANGED
    if df.isnull().any().any():
        return "<h2>Error: CSV contains missing/null values.</h2>"

    # Prediction
    predictions_numeric = model.predict(df)

    # CHANGED
    predictions = [
        label_mapping[int(prediction)]
        for prediction in predictions_numeric
    ]

    result = pd.DataFrame(
        predictions,
        columns=["Prediction"]
    )

    summary = result["Prediction"].value_counts().reset_index()
    summary.columns = ["Attack Type", "Count"]

    # ---------------- SHAP ----------------

    # CHANGED
    sample = df.iloc[[0]]

    # CHANGED
    predicted_class = int(predictions_numeric[0])

    # CHANGED
    explainer = shap.TreeExplainer(model)

    # CHANGED
    shap_values = explainer.shap_values(sample)

    # CHANGED
    if isinstance(shap_values, list):
        shap_values = shap_values[predicted_class]

    # CHANGED
    if hasattr(shap_values, "ndim") and shap_values.ndim == 3:
        shap_values = shap_values[0, :, predicted_class]

    # CHANGED
    elif hasattr(shap_values, "ndim") and shap_values.ndim == 2:
        shap_values = shap_values[0]

    # CHANGED
    shap_values = list(shap_values)

    # CHANGED
    shap_data = pd.DataFrame({
        "Feature": FEATURE_COLUMNS,
        "Impact": shap_values
    })

    # CHANGED
    shap_data["Abs Impact"] = shap_data["Impact"].abs()

    # CHANGED
    shap_data = shap_data.sort_values(
        "Abs Impact",
        ascending=False
    ).head(10)

    # CHANGED
    shap_data["Impact"] = shap_data["Impact"].round(6)

    # CHANGED
    shap_table = shap_data[
        ["Feature", "Impact"]
    ].to_html(
        index=False,
        classes="shap-table"
    )

    return render_template(
        "result.html",
        filename=file.filename,
        total_records=len(result),
        summary_table=summary.to_html(index=False),
        shap_table=shap_table,
        first_prediction=predictions[0]
    )


if __name__ == "__main__":
    app.run(debug=True)