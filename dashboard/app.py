import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import plotly.figure_factory as ff

# Load the trained model
model = joblib.load("models/cicids_rf.pkl")

# Load dataset (change filename if you want to use another scenario)
df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
df = df.dropna()
label_col = " Label"

# Encode categorical columns (repeat training logic)
cat_cols = [col for col in df.columns if df[col].dtype == "object" and col != label_col]
for col in cat_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

le_label = LabelEncoder()
df["Label_enc"] = le_label.fit_transform(df[label_col])

# Prepare features for prediction
X = df.drop(columns=[label_col, "Label_enc"])
X.replace([np.inf, -np.inf], np.nan, inplace=True)
X = X.dropna()
df = df.loc[X.index]  # align indices

# Make predictions
preds = model.predict(X)
df["Prediction"] = preds

st.title("CICIDS DDoS Dashboard")
st.write("First 20 packets and their predicted label (0=BENIGN, 1=DDoS):")
st.dataframe(df[[label_col, "Prediction"]].head(20))

benign_cnt = (df["Prediction"] == 0).sum()
ddos_cnt = (df["Prediction"] == 1).sum()
st.write(f"Total BENIGN packets predicted: {benign_cnt}")
st.write(f"Total DDoS packets predicted: {ddos_cnt}")

# Accuracy and confusion matrix
y_true = df["Label_enc"].values
accuracy = accuracy_score(y_true, preds)
st.write(f"Prediction Accuracy: {accuracy:.3f}")

cm = confusion_matrix(y_true, preds)
labels = list(le_label.classes_)
fig = ff.create_annotated_heatmap(
    z=cm,
    x=labels,
    y=labels,
    colorscale="Viridis"
)
st.subheader("Confusion Matrix")
st.plotly_chart(fig)
