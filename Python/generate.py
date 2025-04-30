import pandas as pd
import random
import numpy as np
import os

# Create the CSV folder if it doesn't exist
csv_folder_path = "CSV"
if not os.path.exists(csv_folder_path):
    os.makedirs(csv_folder_path)

ports = list(range(20, 1024))
protocols = ["TCP", "UDP", "ICMP"]
attack_types = ["Normal", "DDoS", "SQL Injection", "Brute Force", "XSS", "Malware"]

# Generate dataset
num_samples = 500000
data = []

for _ in range(num_samples):
    src_ip = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    dst_ip = f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    src_port = random.choice(ports)
    dst_port = random.choice(ports)
    protocol = random.choice(protocols)
    packet_size = random.randint(50, 1500)
    duration = round(random.uniform(0.01, 5.0), 2)
    is_attack = random.choices([0, 1], weights=[0.7, 0.3])[0]  # 70% normal, 30% attack
    attack_type = random.choice(attack_types) if is_attack else "Normal"
    anomaly_score = round(np.random.normal(0.2 if is_attack else 0.01, 0.05), 2)
    
    data.append([src_ip, dst_ip, src_port, dst_port, protocol, packet_size, duration, is_attack, attack_type, anomaly_score])

# Create DataFrame
df = pd.DataFrame(data, columns=["Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol", "Packet Size", "Duration", "Is Attack", "Attack Type", "Anomaly Score"])

# Save dataset to CSV in the 'CSV' folder
csv_file_path = os.path.join(csv_folder_path, "ids_dataset.csv")
df.to_csv(csv_file_path, index=False)

print(f"IDS dataset generated and saved as '{csv_file_path}'")
