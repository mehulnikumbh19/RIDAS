import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load model and data
model = joblib.load("models/cicids_rf.pkl")
df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
df = df.dropna()
label_col = " Label"

# Encode categorical columns
cat_cols = [col for col in df.columns if df[col].dtype == "object" and col != label_col]
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

le_label = LabelEncoder()
df["Label_enc"] = le_label.fit_transform(df[label_col])

X = df.drop(columns=[label_col, "Label_enc"])
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X = X.dropna()
y_true = df.loc[X.index, "Label_enc"]

y_pred = model.predict(X)

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_true, y_pred))
print("Classification Report:\n", classification_report(y_true, y_pred, target_names=le_label.classes_))
