import subprocess
from flask import Flask
import threading

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"  # Apna YouTube stream key
DRIVE_ID = "1lI8B7mRLwfAnvUaB98wViRP2xAT9CVtA"  # Drive file ID
AUDIO_FILE = "audio.mp3"
OVERLAY_PATH = "Project_09-26(2)_HD 720p_MEDIUM_FR30.mp4"  # ya overlay.gif

# ==== FLASK SERVER FOR PORT BIND ====
app = Flask(__name__)

@app.route("/")
def home():
    return "Stream Running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== DOWNLOAD AUDIO FROM DRIVE ====
def download_audio():
    print("🎵 Downloading audio from Google Drive...")
    drive_url = f"https://drive.google.com/uc?id={DRIVE_ID}&export=download"
    cmd = [
        "yt-dlp", "-x", "--audio-format", "mp3",
        "-o", AUDIO_FILE, drive_url
    ]
    subprocess.run(cmd, check=True)
    print("✅ Audio downloaded successfully.")

# ==== START YOUTUBE STREAM ====
def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-re", "-i", OVERLAY_PATH,   # video loop
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,     # audio loop
        "-map", "0:v:0",  # video from first input
        "-map", "1:a:0",  # audio from second input
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    # Flask server for port binding
    threading.Thread(target=run_flask).start()
    
    # Download audio
    download_audio()
    
    # Start stream
    while True:
        start_stream()
