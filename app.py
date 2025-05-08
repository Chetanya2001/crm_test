# app.py
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import os
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
CORS(app, origins=["https://castfrontend.vercel.app"])

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

@app.route("/")
def index():
    return {"status": "Cast backend is running."}

@socketio.on("connect")
def handle_connect():
    print(f"[🟢] Client connected: {request.sid}")

@socketio.on("disconnect")
def handle_disconnect():
    print(f"[🔌] Client disconnected: {request.sid}")

@socketio.on("join-room")
def handle_join(data):
    room = data if isinstance(data, str) else data.get("room")
    join_room(room)
    print(f"[🚪] {request.sid} joined room: {room}")

@socketio.on("leave-room")
def handle_leave(data):
    room = data if isinstance(data, str) else data.get("room")
    leave_room(room)
    print(f"[🚪] {request.sid} left room: {room}")

@socketio.on("screen-data")
def handle_screen(data):
    room = data.get("room")
    emit("screen-data", data.get("data"), room=room)

@socketio.on("audio-data")
def handle_audio(data):
    room = data.get("room")
    emit("audio-data", data.get("data"), room=room)

@socketio.on("video-data")
def handle_video(data):
    room = data.get("room")
    emit("video-data", data.get("data"), room=room)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
