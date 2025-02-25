from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

# Function to simulate real-time traffic data
def generate_traffic():
    while True:
        time.sleep(2)  # Simulating data every 2 seconds
        data = {
            'source_ip': f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            'destination_ip': f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            'protocol': random.choice(["TCP", "UDP", "ICMP"]),
            'packet_length': random.randint(64, 1500),
            'traffic_type': random.choice(["Legitimate", "Malicious"]),
            'total_packets': random.randint(100, 500),
            'malicious_packets': random.randint(0, 50)
        }
        socketio.emit('update_traffic', data)

# Start background thread for real-time data
threading.Thread(target=generate_traffic, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, debug=True)
