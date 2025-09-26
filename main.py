import subprocess
from flask import Flask
import threading
import os

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"        # YouTube stream key
VIDEO_DRIVE_ID = "1SqqVbApLnkj8rSnmfYBH7Yva90MxhPwa"   # Drive ID of video/GIF
AUDIO_DRIVE_ID = "1ilOvOl76gwquhWU-Xz78rcTOwLPdnizY"  # Drive ID of audio

VIDEO_FILE = "overlay.mp4"   # Downloaded video/GIF
AUDIO_FILE = "audio.mp3"     # Downloaded audio

# ==== FLASK SERVER FOR KEEP-ALIVE ====
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Stream Running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== DOWNLOAD FILE FROM DRIVE ====
def download_from_drive(drive_id, output_file):
    if os.path.exists(output_file):
        print(f"⚡ {output_file} already exists, skipping download...")
        return
    print(f"⬇️ Downloading {output_file} from Google Drive...")
    url = f"https://drive.google.com/uc?id={drive_id}&export=download"
    cmd = ["yt-dlp", "-f", "bestaudio/best", "-o", output_file, url]
    subprocess.run(cmd, check=True)
    print(f"✅ {output_file} downloaded successfully.")

# ==== START YOUTUBE STREAM ====
def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-i", VIDEO_FILE,   # infinite video loop
        "-stream_loop", "-1", "-i", AUDIO_FILE,   # infinite audio loop
        "-map", "0:v:0",  # video from file
        "-map", "1:a:0",  # audio from file
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "2500k",
        "-maxrate", "2500k",
        "-bufsize", "5000k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-shortest",              # dono inputs ko sync karega
        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    # Flask server for keep-alive
    threading.Thread(target=run_flask, daemon=True).start()
    
    # Download video and audio from Drive
    download_from_drive(VIDEO_DRIVE_ID, VIDEO_FILE)
    download_from_drive(AUDIO_DRIVE_ID, AUDIO_FILE)
    
    # Stream loop
    while True:
        start_stream()
