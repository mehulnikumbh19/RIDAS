from scapy.all import sniff
import pandas as pd

# List to store extracted features
packets_data = []

def extract_features(packet):
    # Basic feature extraction, can be expanded!
    try:
        packet_info = {
            "src_ip": packet[1].src if hasattr(packet[1], "src") else "",
            "dst_ip": packet[1].dst if hasattr(packet[1], "dst") else "",
            "proto": packet[1].name if hasattr(packet[1], "name") else "",
            "length": len(packet) if packet else 0
        }
        packets_data.append(packet_info)
    except Exception as e:
        print("Error extracting features:", e)

def main():
    print("Sniffing 20 packets and extracting features...")
    sniff(prn=extract_features, count=20)
    # Save to CSV
    df = pd.DataFrame(packets_data)
    df.to_csv("data/packet_features.csv", index=False)
    print("Saved extracted features to data/packet_features.csv")

if __name__ == "__main__":
    main()
