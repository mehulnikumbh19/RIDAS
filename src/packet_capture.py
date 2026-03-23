from scapy.all import sniff

def packet_callback(packet):
    print(packet.summary())

if __name__ == "__main__":
    print("Sniffing 10 packets...")
    sniff(prn=packet_callback, count=10)
    print("Finished sniffing.")