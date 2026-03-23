import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load("models/cicids_rf.pkl")

# Load new feature data to predict (reuse the DDoS file for demo)
df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
df = df.dropna()
label_col = " Label"

# Encode categorical columns as in training
from sklearn.preprocessing import LabelEncoder
cat_cols = [col for col in df.columns if df[col].dtype == "object" and col != label_col]
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# Prepare features only (exclude label columns)
X = df.drop(columns=[label_col])
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X = X.dropna()

# Predict
preds = model.predict(X)
print("Predictions (0=BENIGN, 1=DDoS):")
print(preds[:20])  # Show first 20 predictions
