import pandas as pd

# Replace with the name of one of your CICIDS CSV files
df = pd.read_csv("data/Friday-WorkingHours-Afternoon-DDos.pcap_ISCSV.csv")
print(df.head())
print(df.columns)
