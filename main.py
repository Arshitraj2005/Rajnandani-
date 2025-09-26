import subprocess
from flask import Flask
import threading
import os

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"   # YouTube stream key
VIDEO_FILE = "overlay.mp4"                 # Video file path
AUDIO_FILE = "audio.mp3"                   # Audio file path

# ==== FLASK SERVER FOR KEEP-ALIVE ====
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Stream Running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== START YOUTUBE STREAM ====
def start_stream():
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-re", "-i", VIDEO_FILE,  # loop video
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,  # loop audio
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",       # keep video original
        "-c:a", "copy",       # keep audio original
        "-f", "flv",
        rtmp_url
    ]
    subprocess.run(cmd)

# ==== MAIN ====
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Check if files exist
    if not os.path.exists(VIDEO_FILE):
        print(f"❌ Video file '{VIDEO_FILE}' not found.")
    elif not os.path.exists(AUDIO_FILE):
        print(f"❌ Audio file '{AUDIO_FILE}' not found.")
    else:
        while True:
            start_stream()
