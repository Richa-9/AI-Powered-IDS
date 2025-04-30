import pandas as pd
import os
from xgboost import XGBClassifier

# File path for results
results_file = "CSV/predicted_traffic_results.csv"

# Reset the results file (clear previous content)
if os.path.exists(results_file):
    with open(results_file, "w") as file:
        file.write("Source IP,Destination IP,Source Port,Destination Port,Protocol,Packet Size,Duration,Anomaly Score,Attack Type,Predicted Attack,Prediction Result\n")
    print("🔄 Reset 'predicted_traffic_results.csv' in 'CSV' folder")

# Load the trained model from the JSON file
model = XGBClassifier()
model.load_model("ids_model.json")

# Load new network traffic data
csv_file = "CSV/new_network_traffic.csv"
df = pd.read_csv(csv_file)

if df.empty:
    print("⚠️ No new network traffic data found.")
    exit()

# Keep a copy of the original data for reference
original_df = df.copy()

# Drop non-numeric columns that were removed during training
df = df.drop(columns=["Source IP", "Destination IP", "Attack Type"], errors="ignore")

# One-hot encode the 'Protocol' column
df = pd.get_dummies(df, columns=["Protocol"], dtype=int)

# Ensure columns match what the model was trained on
expected_columns = [
    "Source Port", "Destination Port", "Packet Size", "Duration", "Anomaly Score", 
    "Protocol_ICMP", "Protocol_TCP", "Protocol_UDP"
]

# Add any missing protocol columns with default 0
for col in expected_columns:
    if col not in df.columns:
        df[col] = 0

# Reorder columns to match training data
df = df[expected_columns]

# Make predictions
predictions = model.predict(df)

# Add prediction results to original dataframe
original_df["Predicted Attack"] = predictions
original_df["Prediction Result"] = original_df["Predicted Attack"].apply(lambda x: "🚨 Malicious" if x == 1 else "✅ Normal")

# Display prediction results
for index, row in original_df.iterrows():
    if row["Predicted Attack"] == 1:
        print(f"🚨 ALERT! Malicious Traffic Detected: {row.get('Attack Type', 'Unknown')}")
    else:
        print("✅ Normal Traffic Detected")

# Append prediction results to CSV file
original_df.to_csv(results_file, mode="a", index=False, header=False)
print("✅ Predictions saved to 'CSV/predicted_traffic_results.csv'")
