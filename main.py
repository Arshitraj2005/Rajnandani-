import subprocess
from flask import Flask
import threading
import os
import time

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"
VIDEO_DRIVE_ID = "1SqqVbApLnkj8rSnmfYBH7Yva90MxhPwa"
AUDIO_DRIVE_ID = "1ilOvOl76gwquhWU-Xz78rcTOwLPdnizY"

VIDEO_FILE = "overlay.mp4"
AUDIO_FILE = "audio.mp3"

# ==== FLASK SERVER ====
app = Flask(__name__)
@app.route("/")
def home():
    return "✅ Stream Running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== DOWNLOAD FILES ====
def download_from_drive(drive_id, output_file):
    if os.path.exists(output_file):
        print(f"⚡ {output_file} already exists, skipping download...")
        return
    print(f"⬇️ Downloading {output_file} from Google Drive...")
    url = f"https://drive.google.com/uc?id={drive_id}&export=download"
    cmd = ["yt-dlp", "-f", "best", "-o", output_file, url]
    subprocess.run(cmd, check=True)
    print(f"✅ {output_file} downloaded successfully.")

# ==== START STREAM ====
def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-re", "-i", VIDEO_FILE,   # loop input
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,   # loop input
        "-map", "0:v:0",
        "-map", "1:a:0",

        # Force re-encode to YouTube-friendly format
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "2500k",   # YouTube 720p standard
        "-maxrate", "2500k",
        "-bufsize", "5000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",        # 30fps → 2s GOP
        "-r", "30",        # force 30fps output
        "-vf", "scale=-2:720",  # maintain aspect ratio, 720p height

        # Audio
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",

        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

# ==== MAIN ====
if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    download_from_drive(VIDEO_DRIVE_ID, VIDEO_FILE)
    download_from_drive(AUDIO_DRIVE_ID, AUDIO_FILE)
    while True:
        try:
            start_stream()
        except Exception as e:
            print(f"⚠️ Stream crashed: {e}")
            print("⏳ Restarting in 5 seconds...")
            time.sleep(5)
