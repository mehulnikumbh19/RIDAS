import pandas as pd
import json

df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv")
row = df.drop(columns=[" Label"]).iloc[0].to_dict()
print(json.dumps(row, indent=2))
