from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load your trained model
model = joblib.load("models/cicids_rf.pkl")

# Example: list of all feature columns, copy from your training script (excluding label columns)
feature_columns = [
    ' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets',
    'Total Length of Fwd Packets', ' Total Length of Bwd Packets', ' Fwd Packet Length Max',
    ' Fwd Packet Length Min', ' Fwd Packet Length Mean', ' Fwd Packet Length Std',
    # ... add ALL columns from your file except ' Label' and 'Label_enc'
]

@app.route('/predict', methods=['POST'])
def predict():
    # Expect a JSON payload matching your feature columns, e.g. {' Destination Port': 80, ...}
    data = request.get_json()
    print("Received prediction request:", data)
    df = pd.DataFrame([data])
    # Clean inf values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df = df.dropna()
    # Predict!
    pred = model.predict(df)[0]
    return jsonify({'prediction': int(pred)})  # 0=BENIGN, 1=DDoS

if __name__ == '__main__':
    app.run(port=5000)
