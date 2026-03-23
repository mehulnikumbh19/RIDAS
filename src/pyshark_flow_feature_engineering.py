import pandas as pd
import joblib

# Step 1: Load packet-level features CSV made with Pyshark
df = pd.read_csv('data/pyshark_features.csv')

# Step 2: Define flow key columns (edit if needed!)
groupers = ['src', 'dst', 'srcport', 'dstport', 'protocol']

# Step 3: Aggregate per flow to create flow-based features
flows = df.groupby(groupers).agg(
    packet_count    = ('length', 'count'),
    byte_count      = ('length', 'sum'),
    mean_length     = ('length', 'mean'),
    min_length      = ('length', 'min'),
    max_length      = ('length', 'max'),
    std_length      = ('length', 'std'),
    first_timestamp = ('timestamp', 'min'),
    last_timestamp  = ('timestamp', 'max')
).reset_index()

# Step 4: Compute flow duration (last - first packet timestamp)
flows['duration'] = flows['last_timestamp'] - flows['first_timestamp']

# Step 5: Save out to inspect or use for ML later
flows.to_csv('data/pyshark_flows.csv', index=False)
print("Aggregated flow features written to data/pyshark_flows.csv")
print(flows.head())

# Step 6: (Optional) ML Prediction With Existing Model
# UNCOMMENT THIS BLOCK ONLY if your model's features match the DataFrame columns!

# try:
#     model = joblib.load('models/cicids_rf.pkl')
#     # Get the list of required columns, using zeros for missing if needed
#     required_cols = model.feature_names_in_ if hasattr(model,'feature_names_in_') else flows.columns
#     for col in required_cols:
#         if col not in flows.columns:
#             flows[col] = 0
#     X = flows[required_cols].fillna(0)
#     preds = model.predict(X)
#     flows['ml_prediction'] = preds
#     print(flows[['src','dst','srcport','dstport','protocol','ml_prediction']].head())
#     flows.to_csv('data/pyshark_flows_predicted.csv', index=False)
#     print("Prediction results saved to data/pyshark_flows_predicted.csv")
# except Exception as e:
#     print("ML prediction error:", e)
