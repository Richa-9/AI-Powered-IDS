import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import pandas as pd
import os
from flask_cors import CORS
from xgboost import XGBClassifier

# Initialize app
app = Flask(__name__)
CORS(app)

# Use eventlet async mode
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Base paths
base_dir = os.path.dirname(__file__)
csv_folder_path = os.path.join(base_dir, 'CSV')

# Load model
model = XGBClassifier()
model.load_model(os.path.join(base_dir, "ids_model.json"))

# Load dataset
dataset_path = os.path.join(csv_folder_path, "new_network_traffic.csv")
df = pd.read_csv(dataset_path)

# Data preprocessing
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

# Emit function
def emit_traffic():
    for _, row in df.iterrows():
        preprocessed = preprocess_row(row)
        prediction = model.predict(preprocessed)[0]
        predicted_label = "Malicious" if prediction == 1 else "Normal"
        actual_label = "Malicious" if row.get("Attack Type") != "Normal" else "Normal"

        reason = (
            "False Negative" if actual_label == "Malicious" and predicted_label == "Normal" else
            "False Positive" if actual_label == "Normal" and predicted_label == "Malicious" else
            "Correct"
        )

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
        socketio.sleep(2)  # Yield to eventlet

# Route for API testing
@app.route('/dashboard')
def index():
    return "React app is running at http://localhost:3000"

# WebSocket connection
@socketio.on("connect")
def handle_connect():
    socketio.start_background_task(emit_traffic)

# Run using eventlet
if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)

