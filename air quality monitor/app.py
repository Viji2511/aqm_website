from flask import Flask, render_template, jsonify
import requests
import pandas as pd
import joblib
import os
from datetime import datetime

app = Flask(__name__)

# ThingSpeak API Channel ID (Public Access, no API Key required)
THINGSPEAK_CHANNEL_ID = "2823741"
THINGSPEAK_URL = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?results=1"

# Load AI Model and Scaler
MODEL_PATH = "dust_level_model.pkl"
SCALER_PATH = "scaler.pkl"

# Check if model and scaler files exist
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Model and scaler loaded successfully!")
else:
    model = None
    scaler = None
    print("Model or scaler not found. Please train the model first.")

# Fetch Latest Data from ThingSpeak
def fetch_current_data():
    response = requests.get(THINGSPEAK_URL)
    data = response.json().get("feeds", [{}])[0]
    return data

# Fetch Past Data from ThingSpeak
def fetch_past_air_quality_data():
    response = requests.get(f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?results=100")
    data = response.json().get("feeds", [])
    return data

# AI Prediction Route
@app.route("/api/predict")
def predict_air_quality():
    if model is None or scaler is None:
        return jsonify({"error": "Model or scaler not found. Train it first."})

    data = fetch_current_data()
    if not data:
        return jsonify({"error": "No data available."})

    try:
        # Prepare features for prediction
        features = [
            float(data.get("field1", 0)),  # MQ-7
            float(data.get("field2", 0))   # MQ-135
        ]
        print("Raw features:", features)

        # Scale features
        features_scaled = scaler.transform([features])
        print("Scaled features:", features_scaled)

        # Make prediction
        predicted_dust = model.predict(features_scaled)[0]
        return jsonify({"predicted_dust": round(predicted_dust, 2)})

    except Exception as e:
        return jsonify({"error": str(e)})

# Current Air Quality Route
@app.route("/api/current")
def current_data():
    data = fetch_current_data()
    return jsonify({
        "field1": data.get("field1", 0),  # MQ-7
        "field2": data.get("field2", 0),  # MQ-135
        "field3": data.get("field3", 0),  # Dust
    })

# Past Data Route
@app.route("/api/past")
def past_data():
    data = fetch_past_air_quality_data()
    return jsonify(data)

# Main Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/past-analysis")
def past_analysis():
    return render_template("past_analysis.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True)