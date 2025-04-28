import pandas as pd
import random
import numpy as np

# Define possible values for network traffic features
ports = list(range(20, 1024))
protocols = ["TCP", "UDP", "ICMP"]
attack_types = ["Normal", "DDoS", "SQL Injection", "Brute Force", "XSS", "Malware"]

# Function to generate detailed reason for attack
def generate_attack_reason(attack_type, packet_size, protocol, src_port, dst_port, duration, src_ip, dst_ip):
    if attack_type == "DDoS":
        return f"High-volume traffic ({packet_size} bytes) over {protocol} from {src_ip} targeting {dst_ip} on port {dst_port} within {duration}s indicates flooding behavior."
    elif attack_type == "SQL Injection":
        return f"Suspicious request from {src_ip} to {dst_ip}:{dst_port} using {protocol} protocol likely contains SQL payload due to unusual traffic pattern and duration of {duration}s."
    elif attack_type == "Brute Force":
        return f"Multiple access attempts detected from {src_ip} to login service on port {dst_port} using {protocol}, with short duration {duration}s and packet size {packet_size} bytes."
    elif attack_type == "XSS":
        return f"Injection attempt suspected from {src_ip} over {protocol} with small packet size ({packet_size} bytes), possibly script-laden payload targeting {dst_ip}:{dst_port}."
    elif attack_type == "Malware":
        return f"Unusual file behavior from {src_ip} to {dst_ip} via port {dst_port}, protocol {protocol}, size {packet_size} bytes and duration {duration}s suggests malware activity."
    else:
        return "N/A"

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
    is_attack = random.choices([0, 1], weights=[0.7, 0.3])[0]
    attack_type = random.choice(attack_types) if is_attack else "Normal"
    anomaly_score = round(np.random.normal(0.2 if is_attack else 0.01, 0.05), 2)
    attack_reason = generate_attack_reason(attack_type, packet_size, protocol, src_port, dst_port, duration, src_ip, dst_ip) if is_attack else "N/A"
    
    data.append([
        src_ip, dst_ip, src_port, dst_port, protocol,
        packet_size, duration, is_attack, attack_type,
        anomaly_score, attack_reason
    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol",
    "Packet Size", "Duration", "Is Attack", "Attack Type", "Anomaly Score", "Attack Reason"
])

# Save dataset to CSV in the CSV folder
df.to_csv("CSV/new_network_traffic.csv", index=False)

print("IDS dataset generated and saved as 'new_network.traffic.csv' in the 'CSV' folder")
