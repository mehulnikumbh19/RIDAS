import pandas as pd
import joblib

# Load model
model = joblib.load("models/packet_rf_model.pkl")

# Load your CSV (or create a new DataFrame for a single packet)
df = pd.read_csv("data/packet_features.csv", encoding="latin1")

# Drop string columns to match training data
X = df.drop(columns=["label", "src_ip", "dst_ip", "proto"])

# Predict
predictions = model.predict(X)
print("Predictions for each packet:")
print(predictions)
