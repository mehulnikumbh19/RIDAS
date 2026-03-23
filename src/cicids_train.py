import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# --- 1. Load Data ---
df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")

# --- 2. Drop missing values ---
df = df.dropna()

# --- 3. Find feature columns and label column ---
label_col = " Label"  # NOTE the space before 'Label'

print("Columns:", df.columns.tolist())

# --- 4. Encode categorical columns (if any) ---
cat_cols = [col for col in df.columns if df[col].dtype == "object" and col != label_col]
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# --- 5. Encode label column ---
le_label = LabelEncoder()
df["Label_enc"] = le_label.fit_transform(df[label_col])
print("Label classes:", le_label.classes_)

# --- 6. Split features and labels ---
X = df.drop(columns=[label_col, "Label_enc"])
y = df["Label_enc"]

# --- 7. Replace infinity values and drop NaNs ---
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X = X.dropna()
y = y[X.index]  # Keep labels matching features!

# --- 8. Train Random Forest ---
rf = RandomForestClassifier()
rf.fit(X, y)
print("Model trained!")

# --- 9. Save model ---
joblib.dump(rf, "models/cicids_rf.pkl")
print("Model saved to models/cicids_rf.pkl")
