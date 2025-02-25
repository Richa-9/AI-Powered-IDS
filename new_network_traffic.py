import pandas as pd
import random
import numpy as np
import time

# Define possible values for network traffic features
ip_addresses = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
destination_ips = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
ports = list(range(1024, 65535))
protocols = ["TCP", "UDP", "ICMP"]
attack_types = ["DDoS", "SQL Injection", "Brute Force", "XSS", "Malware"]

# File name for real-time data
csv_file = "new_network_traffic.csv"

# Clear file and write headers when script starts
df = pd.DataFrame(columns=["Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol", 
                           "Packet Size", "Duration", "Is Attack", "Attack Type", "Anomaly Score"])
df.to_csv(csv_file, index=False)

print("⚠️ File reset: 'new_network_traffic.csv' cleared and new data will be added.")

# Function to generate real-time network traffic with malicious and normal entries
def generate_network_traffic():
    while True:
        src_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        dst_ip = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        
        src_port = random.choice(ports)
        dst_port = random.choice(ports)
        protocol = random.choice(protocols)
        packet_size = random.randint(50, 1500)
        duration = round(random.uniform(0.01, 5.0), 2)
        
        # 20% chance of attack
        is_attack = random.choices([0, 1], weights=[0.7, 0.3])[0]  
        attack_type = random.choice(attack_types) if is_attack else "Normal"
        anomaly_score = round(np.random.normal(0.3 if is_attack else 0.01, 0.1), 2)  # Higher anomaly score for attacks

        # Create a DataFrame entry
        new_entry = pd.DataFrame([[src_ip, dst_ip, src_port, dst_port, protocol, packet_size, 
                                   duration, is_attack, attack_type, anomaly_score]],
                                 columns=["Source IP", "Destination IP", "Source Port", "Destination Port", 
                                          "Protocol", "Packet Size", "Duration", "Is Attack", 
                                          "Attack Type", "Anomaly Score"])
        
        # Append to CSV
        new_entry.to_csv(csv_file, mode="a", header=False, index=False)
        
        # Print logs with alert for malicious traffic
        if is_attack:
            print(f"🚨 ALERT! Malicious traffic detected: {attack_type}\n{new_entry}\n")
        else:
            print(f"✅ Normal traffic detected:\n{new_entry}\n")

        # Wait for 5 seconds before generating the next entry
        time.sleep(5)

# Run the generator
generate_network_traffic()