import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("data/packet_features.csv", encoding="latin1")

X = df.drop(columns=["label", "src_ip", "dst_ip", "proto"])  # Only use numerical columns
y = df["label"]

# Encode labels
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_encoded = le.fit_transform(y)

model = RandomForestClassifier()
model.fit(X, y_encoded)
print("Trained RandomForestClassifier!")

# Save model
import joblib
joblib.dump(model, "models/packet_rf_model.pkl")
print("Saved trained model to models/packet_rf_model.pkl")
