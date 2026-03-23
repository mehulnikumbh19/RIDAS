from scapy.all import sniff
import joblib
import pandas as pd

# 1. Signature-based detection rules (edit with real values if needed)
malicious_ips = {"1.2.3.4", "10.0.0.2"}
malicious_ports = {666, 31337}

def check_signature(packet):
    if packet.haslayer('IP'):
        src = packet["IP"].src
        dst = packet["IP"].dst
        if src in malicious_ips or dst in malicious_ips:
            return True
    if packet.haslayer('TCP'):
        sport = packet["TCP"].sport
        dport = packet["TCP"].dport
        if sport in malicious_ports or dport in malicious_ports:
            return True
    return False

# 2. Extract packet features (make sure to expand/features match your trained model!)
def extract_features(packet):
    features = {}
    if packet.haslayer('IP'):
        features['ip_len'] = getattr(packet['IP'], 'len', 0)
        features['src'] = packet['IP'].src
        features['dst'] = packet['IP'].dst
    if packet.haslayer('TCP'):
        features['tcp_sport'] = packet['TCP'].sport
        features['tcp_dport'] = packet['TCP'].dport
        features['tcp_flags'] = int(packet['TCP'].flags)
    # TODO: Add more features to match the columns your ML model expects!
    return features

# 3. Load trained ML model (update path if needed)
model = joblib.load("models/cicids_rf.pkl")

def ml_predict(features_dict):
    df = pd.DataFrame([features_dict])
    try:
        pred = model.predict(df)[0]
    except Exception as e:
        print(f"ML prediction error: {e}")
        pred = None
    return pred  # 0 = BENIGN, 1 = Attack

# 4. Main packet processing

def process_packet(packet):
    sig_alert = check_signature(packet)
    features = extract_features(packet)
    ml_alert = None
    if features and len(features) > 0:
        ml_alert = ml_predict(features)
    # Output/alert logic
    if sig_alert and ml_alert == 1:
        print("ALERT: Threat detected by BOTH signature & anomaly-based detection!")
    elif sig_alert:
        print("ALERT: Threat detected by signature-based rules!")
    elif ml_alert == 1:
        print("ALERT: Threat detected by ML anomaly detection!")
    else:
        print("Packet appears normal.")

if __name__ == "__main__":
    print("Capturing 50 packets... (Run as administrator if needed)")
    sniff(count=50, prn=process_packet, store=0)
