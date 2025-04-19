import pandas as pd
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Import XGBoost
from xgboost import XGBClassifier

# Define possible values for network traffic features
ip_addresses = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
destination_ips = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
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
    is_attack = random.choices([0, 1], weights=[0.7, 0.3])[0]
    attack_type = random.choice(attack_types) if is_attack else "Normal"
    anomaly_score = round(np.random.normal(0.2 if is_attack else 0.01, 0.05), 2)
    
    data.append([src_ip, dst_ip, src_port, dst_port, protocol, packet_size, duration, is_attack, attack_type, anomaly_score])

# Create DataFrame
df = pd.DataFrame(data, columns=["Source IP", "Destination IP", "Source Port", "Destination Port", "Protocol", "Packet Size", "Duration", "Is Attack", "Attack Type", "Anomaly Score"])
df.to_csv("ids_dataset.csv", index=False)
print("IDS dataset generated and saved as 'ids_dataset.csv'")

# Preprocessing
df = df.drop(columns=["Source IP", "Destination IP", "Attack Type"])
df = pd.get_dummies(df, columns=["Protocol"])

X = df.drop(columns=["Is Attack"])
y = df["Is Attack"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Use XGBoost
model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy (XGBoost): {accuracy:.4f}")
print(classification_report(y_test, y_pred))

import pickle

# Save the trained model to a .pkl file
with open("ids_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model saved as 'ids_model.pkl'")
