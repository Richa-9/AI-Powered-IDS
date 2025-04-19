from flask import Flask, render_template
from flask_socketio import SocketIO
import pandas as pd
import pickle
import time
import threading
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app)

# Load trained model
with open("ids_model.pkl", "rb") as f:
    model = pickle.load(f)

# Load dataset
df = pd.read_csv("new_network.traffic.csv")

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
        actual_label = "Malicious" if row["Attack Type"] != "Normal" else "Normal"

        # Determine reason
        if actual_label == "Malicious" and predicted_label == "Normal":
            reason = "False Negative"
        elif actual_label == "Normal" and predicted_label == "Malicious":
            reason = "False Positive"
        else:
            reason = "Correct"

        # Prepare data to emit
        data = {
            "Source IP": row["Source IP"],
            "Destination IP": row["Destination IP"],
            "Source Port": row["Source Port"],
            "Destination Port": row["Destination Port"],
            "Protocol": row["Protocol"],
            "Packet Size": row["Packet Size"],
            "Duration": row["Duration"],
            "Anomaly Score": row["Anomaly Score"],
            "Attack Type": row["Attack Type"],
            "Prediction": predicted_label,
            "Ground Truth": actual_label,
            "Reason": reason
        }

        socketio.emit("new_traffic", data)
        time.sleep(2)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    thread = threading.Thread(target=emit_traffic)
    thread.start()

if __name__ == "__main__":
    socketio.run(app, debug=True)
