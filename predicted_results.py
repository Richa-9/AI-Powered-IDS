import pandas as pd
import pickle
import os

# File path for results
results_file = "predicted_traffic_results.csv"

# Reset the results file (clear previous content)
if os.path.exists(results_file):
    with open(results_file, "w") as file:
        file.write("Source IP,Destination IP,Source Port,Destination Port,Protocol,Packet Size,Duration,Anomaly Score,Attack Type,Predicted Attack,Prediction Result\n")
    print("🔄 Reset 'predicted_traffic_results.csv'")

# Load the trained model from the pickle file
with open("ids_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load new network traffic data
csv_file = "new_network_traffic.csv"
df = pd.read_csv(csv_file)

if df.empty:
    print("⚠ No new network traffic data found.")
    exit()

# Keep a copy of the original data for reference
original_df = df.copy()

# Drop non-numeric columns that were removed during training
df = df.drop(columns=["Source IP", "Destination IP", "Attack Type"], errors="ignore")

# Convert categorical values to numerical (one-hot encoding)
df = pd.get_dummies(df, columns=["Protocol"], dtype=int)

# Ensure columns match model training
expected_columns = [
    "Source Port", "Destination Port", "Packet Size", "Duration", "Anomaly Score", 
    "Protocol_ICMP", "Protocol_TCP", "Protocol_UDP"
]

# Add missing columns (if any)
for col in expected_columns:
    if col not in df.columns:
        df[col] = 0  # Add missing columns with default value 0

# Keep only necessary columns
df = df[expected_columns]

# Make predictions
predictions = model.predict(df)

# Add results to the original dataframe
original_df["Predicted Attack"] = predictions
original_df["Prediction Result"] = original_df["Predicted Attack"].apply(lambda x: "🚨 Malicious" if x == 1 else "✅ Normal")

# Display results
for index, row in original_df.iterrows():
    if row["Predicted Attack"] == 1:
        print(f"🚨 ALERT! Malicious Traffic Detected: {row['Attack Type']}")
    else:
        print(f"✅ Normal Traffic Detected")

# Save results to CSV (append mode after clearing initially)
original_df.to_csv(results_file, mode="a", index=False, header=False)
print("✅ Predictions saved to 'predicted_traffic_results.csv'")