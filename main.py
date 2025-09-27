import os
import subprocess
import gdown
from flask import Flask
import threading

# ===== Flask Server =====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ YouTube Stream is Running (Source Quality Auto)!"

# ===== CONFIG =====
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"  # Your YouTube Stream Key
VIDEO_FILE_ID = "YOUR_VIDEO_DRIVE_ID"    # Any quality video
AUDIO_FILE_ID = "YOUR_AUDIO_DRIVE_ID"    # Any quality audio

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# ===== DOWNLOAD FILES =====
def download_file(file_id, output_file):
    if not os.path.exists(output_file):
        print(f"⬇️ Downloading {output_file} from Google Drive...")
        gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)
        print(f"✅ {output_file} downloaded.")
    else:
        print(f"✅ {output_file} already exists, skipping download.")

download_file(VIDEO_FILE_ID, VIDEO_FILE)
download_file(AUDIO_FILE_ID, AUDIO_FILE)

# ===== START YOUTUBE STREAM =====
def start_stream():
    ffmpeg_command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1", "-i", VIDEO_FILE,   # Loop video infinitely
        "-stream_loop", "-1", "-i", AUDIO_FILE,   # Loop audio infinitely
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-g", "60",                 # Keyframe every 2 sec for 30fps
        "-c:a", "aac",
        "-b:a", "320k",             # Audio will remain original quality
        "-ar", "44100",
        "-f", "flv",
        f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    ]

    print("📡 Starting YouTube livestream (source quality auto)...")
    subprocess.Popen(ffmpeg_command)

# ===== FLASK THREAD =====
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ===== MAIN =====
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()  # Flask server
    start_stream()                              # Start livestream
