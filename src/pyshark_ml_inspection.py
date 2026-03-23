import pandas as pd
import joblib

# Step 1: Load flow features
flows = pd.read_csv('data/pyshark_flows.csv')

# Step 2: Load your trained ML model
model = joblib.load('models/cicids_rf.pkl')  # Change path if needed

# Step 3: Prepare feature columns for prediction
# Use the model's expected columns, fill missing with zeros
if hasattr(model, 'feature_names_in_'):
    expected = list(model.feature_names_in_)
else:
    expected = flows.columns.tolist()

for col in expected:
    if col not in flows.columns:
        flows[col] = 0
X = flows[expected].fillna(0)

# Step 4: Run predictions
predictions = model.predict(X)
flows['ml_prediction'] = predictions

# Step 5: Save predictions to CSV
flows.to_csv('data/pyshark_flows_predicted.csv', index=False)
print("Flow prediction saved to data/pyshark_flows_predicted.csv")

# Optional: Inspect and summarize detection
print("First predictions:")
print(flows[['src', 'dst', 'srcport', 'dstport', 'protocol', 'ml_prediction']].head())

# Summary statistics
print("\nSummary:")
print(flows['ml_prediction'].value_counts())
