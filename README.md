# Network Intrusion Detection System (NIDS)

## 📌 Project Overview

This project is a **Network Intrusion Detection System (NIDS)** built using Machine Learning to detect and classify different types of network traffic and cyber attacks.

The system uses the **CICIDS2017 dataset** and an **XGBoost multiclass classification model** to identify whether network traffic is benign or belongs to a specific attack category.

The trained model is deployed using a **Flask web application**, where users can upload a CSV file and receive predictions along with **SHAP-based explanations** showing which network features influenced the prediction.

## 🎯 Objectives

- Detect malicious network traffic.
- Classify network traffic into different attack categories.
- Use Machine Learning for automated intrusion detection.
- Provide explainable predictions using SHAP.
- Create a simple web interface for CSV-based prediction.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- SHAP
- Flask
- Jupyter Notebook
- Joblib

## 📊 Dataset

The project uses the **CICIDS2017** dataset.

The dataset contains both benign traffic and different types of network attacks.

After data preprocessing and feature engineering, **43 features** are used by the Machine Learning model.

## 🤖 Machine Learning Model

The project uses **XGBoost** for multiclass classification.

The model classifies network traffic into **15 classes**:

1. Benign
2. Bot
3. DDoS
4. DoS GoldenEye
5. DoS Hulk
6. DoS Slowhttptest
7. DoS slowloris
8. FTP-Patator
9. Heartbleed
10. Infiltration
11. PortScan
12. SSH-Patator
13. Web Attack - Brute Force
14. Web Attack - Sql Injection
15. Web Attack - XSS

## 🔍 Explainable AI

**SHAP (SHapley Additive exPlanations)** is used to explain model predictions.

For each prediction, the application displays the **top 10 features** that had the greatest impact on the model's decision.

This makes the NIDS more interpretable instead of providing only an attack label.

## 🌐 Flask Web Application

The Flask application allows users to:

1. Upload a CSV file.
2. Validate the required features.
3. Process the network traffic data.
4. Predict the attack type.
5. Display a prediction summary.
6. Show SHAP explanations for the first record.

## 📁 Project Structure

```text
NIDS_PROJECT/
│
├── app.py
├── features_columns.py
│
├── models/
│   └── xgboost_nids_model.pkl
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   └── 04_Model_Training.ipynb
│
└── README.md
