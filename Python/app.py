import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import pandas as pd
import pickle
import os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains


socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Base directory
base_dir = os.path.dirname(__file__)

# Set Python folder path correctly (same folder as app.py)
python_folder_path = base_dir

# Paths to CSV folder
csv_folder_path = os.path.join(python_folder_path, 'CSV')

# Load trained model
model_path = os.path.join(python_folder_path, "ids_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Load dataset
dataset_path = os.path.join(csv_folder_path, "new_network_traffic.csv")
df = pd.read_csv(dataset_path)

# Preprocess function for model input
def preprocess_row(row):
    input_df = pd.DataFrame([row])
    input_df = input_df.drop(columns=["Source IP", "Destination IP", "Attack Type", "Attack Reason"], errors="ignore")
    input_df = pd.get_dummies(input_df, columns=["Protocol"])

    expected_columns = [
        "Source Port", "Destination Port", "Packet Size", "Duration", "Anomaly Score",
        "Protocol_ICMP", "Protocol_TCP", "Protocol_UDP"
    ]

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    return input_df[expected_columns]

# Emit traffic row by row
def emit_traffic():
    for _, row in df.iterrows():
        preprocessed = preprocess_row(row)
        prediction = model.predict(preprocessed)[0]
        predicted_label = "Malicious" if prediction == 1 else "Normal"
        actual_label = "Malicious" if row.get("Attack Type") != "Normal" else "Normal"

        # Determine reason
        if actual_label == "Malicious" and predicted_label == "Normal":
            reason = "False Negative"
        elif actual_label == "Normal" and predicted_label == "Malicious":
            reason = "False Positive"
        else:
            reason = "Correct"

        # Prepare data to emit
        data = {
            "Source IP": row.get("Source IP", ""),
            "Destination IP": row.get("Destination IP", ""),
            "Source Port": row.get("Source Port", ""),
            "Destination Port": row.get("Destination Port", ""),
            "Protocol": row.get("Protocol", ""),
            "Packet Size": row.get("Packet Size", ""),
            "Duration": row.get("Duration", ""),
            "Anomaly Score": row.get("Anomaly Score", ""),
            "Attack Type": row.get("Attack Type", ""),
            "Prediction": predicted_label,
            "Ground Truth": actual_label,
            "Reason": reason
        }

        socketio.emit("new_traffic", data)
        socketio.sleep(2)  # Non-blocking sleep for eventlet


@app.route('/dashboard')
def index():
    return "React app is running at http://localhost:3000"

@socketio.on("connect")
def handle_connect():
    socketio.start_background_task(emit_traffic)

if __name__ == '__main__':
    socketio.run(app, port=5001)