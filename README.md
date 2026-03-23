# IS665 Cybersecurity Analytics Project

## Project ID
GitHub repository: https://github.com/mehulnikumbh19/IS665-cybersecurity-analytics

## What the project does
This project builds an end-to-end, Random Forest-based network threat detection pipeline using CICIDS-style flow data and packet-derived features. It includes:

- Training an ML model (`RandomForestClassifier`) to classify traffic as `BENIGN` (0) vs `DDoS` (1).
- Evaluating model performance with accuracy and a confusion matrix.
- Running predictions from code, a Streamlit dashboard, and a Flask API endpoint.
- Generating packet/flow feature CSVs from a pcap using `scapy` (live/packet sniffing) and `pyshark` (pcap parsing + flow aggregation).
- Optional signature-based detection combined with ML alerts for live packet sniffing.

## How this project was made
At a high level, the repository was built around the ML model artifact in `models/cicids_rf.pkl` and several scripts that (1) generate features, (2) train/evaluate/predict with the model, and (3) expose results via a dashboard/API.

Concretely, the workflow in this repo is:

- Add and version the datasets and generated feature CSVs under `data/` (large CSVs are stored with Git LFS via `.gitattributes`).
- Train `models/cicids_rf.pkl` using `src/cicids_train.py`.
- Use the trained model in the Streamlit dashboard (`dashboard/app.py`).
- Use the trained model in the Flask API (`src/cicids_api.py`).
- Generate additional feature datasets from PCAP files using `src/pyshark_packet_analysis.py` and `src/pyshark_flow_feature_engineering.py` (and `src/pyshark_ml_inspection.py` for predictions).
- Generate additional feature datasets from PCAP files using Scapy helpers in `src/packet_capture.py`, `src/feature_extraction.py`, and `src/live_packet_capture.py`.

## How it is structured
Key folders:

- `data/`: input datasets and generated feature/flow CSVs (the large CSVs are tracked with Git LFS).
- `models/`: saved model artifacts (`.pkl` files).
- `src/`: Python scripts for training, evaluation, prediction, and feature extraction.
- `dashboard/`: Streamlit app for visualization and interactive predictions.

## End-to-end workflow

### 1) Data used for ML training
The main CICIDS/DDoS model trains on:

`data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`

The training script expects a label column named exactly:

`" Label"` (note the leading space)

It also:

- Drops missing values (`dropna()`).
- Encodes categorical columns with `LabelEncoder`.
- Replaces `inf` / `-inf` with `NaN`, then drops rows with `NaN` after replacement.

### 2) Train the Random Forest model
Run:

```bash
python src/cicids_train.py
```

What it does:

- Loads `data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`.
- Encodes categorical columns (any columns with dtype `"object"`, excluding `" Label"`).
- Encodes the label into `Label_enc`.
- Trains `RandomForestClassifier()` using all features except `" Label"` and `Label_enc`.
- Saves the trained model to:

`models/cicids_rf.pkl`

### 3) Evaluate the model
Run:

```bash
python src/cicids_eval.py
```

What it does:

- Loads `models/cicids_rf.pkl`.
- Repeats the same preprocessing/label encoding steps used in training.
- Predicts on the same CSV (demo setup).
- Prints accuracy, confusion matrix, and classification report.

### 4) Batch prediction (demo)
Run:

```bash
python src/cicids_predict.py
```

What it does:

- Loads the trained model.
- Loads `data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`.
- Applies the same categorical encoding + `inf` cleaning + `dropna()` before predicting.
- Builds `X` by dropping only the `" Label"` column (it does not drop `Label_enc`), so `Label_enc` will be included as an input feature for this demo script.
- Prints the first predictions.

## Prediction interfaces

### Streamlit dashboard (visual demo)
The dashboard is implemented in:

`dashboard/app.py`

What it does:

- Loads `models/cicids_rf.pkl`.
- Loads `data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv`.
- Encodes categorical columns and encodes the label (`Label_enc`) using `LabelEncoder`.
- Predicts and shows:
  First 20 packets with actual label vs predicted label, total predicted BENIGN vs DDoS counts, prediction accuracy, and a confusion matrix heatmap (Plotly).

Run:

```bash
streamlit run dashboard/app.py
```

### Flask API (programmatic predictions)
The API is implemented in:

`src/cicids_api.py`

It exposes:

- `POST /predict`

What it expects:

- A JSON body with feature values.
- The code currently contains a placeholder `feature_columns` list and does not enforce a strict schema; for correct predictions you must provide values whose keys match the model’s expected feature column names and types.

Example request shape:

```json
{
  " Destination Port": 80,
  " Flow Duration": 123.45,
  "...": "..."
}
```

Run:

```bash
python src/cicids_api.py
```

By default it listens on port `5000`.

Important note about categorical features:

- The ML training encodes categorical columns with `LabelEncoder` fitted on the training CSV.
- The API endpoint does *not* replicate the same label-encoding steps; it only cleans `inf/-inf` and drops `NaN`.
- If your input includes categorical/string fields, you must send numeric-encoded values consistent with training, or update the API to apply the same encoders.

## Packet and flow feature generation (pcap to CSV)
The project also includes utilities to generate features from a pcap.

### Pyshark: pcap parsing -> packet features -> flow aggregation
1) Extract packet-level fields from a pcap:

`src/pyshark_packet_analysis.py`

Input:

`data/mycapture.pcap`

Output:

`data/pyshark_features.csv`

2) Aggregate packet records into flow-level features:

`src/pyshark_flow_feature_engineering.py`

It groups by:

`['src', 'dst', 'srcport', 'dstport', 'protocol']`

and computes packet count and length statistics, plus flow duration.

Output:

`data/pyshark_flows.csv`

3) Run model predictions for flow features:

`src/pyshark_ml_inspection.py`

Output:

`data/pyshark_flows_predicted.csv`

### Scapy: live sniffing helpers
These scripts are oriented around interactive sniffing and alerting:

- `src/packet_capture.py`: prints summaries for a small number of sniffed packets.
- `src/feature_extraction.py`: sniffs packets (default `count=20`) and writes extracted fields to `data/packet_features.csv`.
- `src/live_packet_capture.py`: combines simple signature checks with an ML-based alert. It currently extracts a small feature subset and will only produce meaningful ML predictions if the feature set matches what `models/cicids_rf.pkl` expects.

## Training for packet_features-based model (separate demo)
The repository also includes a packet-feature-only Random Forest demo:

- Train: `src/train_model.py` -> `models/packet_rf_model.pkl`
- Predict: `src/predict_packet.py`

This part expects `data/packet_features.csv` to include:

- a numeric/class label column named `label`
- string columns like `src_ip`, `dst_ip`, and `proto` (the script drops them before fitting)

## GitHub storage note (large CSVs)
Your `data/*.csv` files are stored using Git LFS (see `.gitattributes`), which is required because several CSVs exceed GitHub’s 100MB per-file limit.

To clone and download the real data files:

```bash
git lfs install
git lfs pull
```

## Dependencies
The code imports (at minimum) the following Python packages:

- `pandas`, `numpy`
- `scikit-learn`, `joblib`
- `flask` (API)
- `streamlit`, `plotly` (dashboard)
- `scapy` (live sniffing / packet capture)
- `pyshark` (pcap parsing)

If you use `pyshark`, you typically also need `tshark` installed (Wireshark tools) because `pyshark` calls it under the hood.

## What to run (quick start)
1. Train the main model:
   ```bash
   python src/cicids_train.py
   ```
2. Evaluate:
   ```bash
   python src/cicids_eval.py
   ```
3. Dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```
4. API:
   ```bash
   python src/cicids_api.py
   ```

