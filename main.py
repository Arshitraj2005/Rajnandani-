import os
import subprocess
import gdown
from flask import Flask
import threading

# ===== Flask Server =====
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ YouTube Stream is Running via Render!"

# ===== YouTube Stream Key =====
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"

# ===== Google Drive File IDs =====
VIDEO_FILE_ID = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"  # 10-min Video
AUDIO_FILE_ID = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"  # Audio / Music

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# ===== Download video if not already present =====
if not os.path.exists(VIDEO_FILE):
    print("📥 Downloading video from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={VIDEO_FILE_ID}", VIDEO_FILE, quiet=False)

# ===== Download audio if not already present =====
if not os.path.exists(AUDIO_FILE):
    print("📥 Downloading audio from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={AUDIO_FILE_ID}", AUDIO_FILE, quiet=False)

# ===== Start FFmpeg for YouTube streaming (video & audio independent loops) =====
def start_stream():
    ffmpeg_command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1", "-i", VIDEO_FILE,   # Video loop
        "-stream_loop", "-1", "-i", AUDIO_FILE,   # Audio loop
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "6500k",           # Recommended for 1080p
        "-maxrate", "6500k",
        "-bufsize", "13000k",
        "-pix_fmt", "yuv420p",
        "-g", "60",                 # Keyframe every 2 sec
        "-c:a", "aac",
        "-b:a", "320k",             # High quality audio
        "-ar", "44100",
        "-f", "flv",
        f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
    ]

    subprocess.Popen(ffmpeg_command)

# ===== Flask Server Thread =====
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# ===== MAIN =====
if __name__ == "__main__":
    # Start Flask server in background
    threading.Thread(target=run_flask).start()
    
    # Start YouTube livestream
    start_stream()
