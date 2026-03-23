import pyshark
import pandas as pd

# Load your pcap file (update filename as needed)
cap = pyshark.FileCapture('data/mycapture.pcap')

records = []

for packet in cap:
    try:
        # Extract common fields: timestamp, src IP, dst IP, protocol, length
        timestamp = float(packet.sniff_timestamp)
        length = int(packet.length)
        protocol = packet.transport_layer if hasattr(packet, 'transport_layer') else packet.highest_layer
        src = packet.ip.src
        dst = packet.ip.dst
        srcport = packet[protocol].srcport if hasattr(packet[protocol], 'srcport') else None
        dstport = packet[protocol].dstport if hasattr(packet[protocol], 'dstport') else None

        records.append({
            'timestamp': timestamp,
            'src': src,
            'dst': dst,
            'protocol': protocol,
            'srcport': srcport,
            'dstport': dstport,
            'length': length
        })
    except AttributeError:
        # Some packets may not have all attributes (e.g., ARP, ICMPv6, etc.)
        continue

cap.close()

# Convert to DataFrame and inspect
df = pd.DataFrame(records)
print(df.head())

# (Optional) Save to CSV for further processing
df.to_csv("data/pyshark_features.csv", index=False)
