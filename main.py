import os
import subprocess
from flask import Flask
import threading
import gdown

# ===== CONFIG =====
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"        # YouTube stream key
VIDEO_DRIVE_ID = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"   # Google Drive ID of video
AUDIO_DRIVE_ID = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"   # Google Drive ID of audio

VIDEO_FILE = "video.mp4"
AUDIO_FILE = "audio.mp3"

# ===== FLASK SERVER FOR PORT BIND =====
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ YouTube Stream is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ===== DOWNLOAD FILES FROM GOOGLE DRIVE =====
def download_from_drive(drive_id, output_file):
    if not os.path.exists(output_file):
        print(f"⬇️ Downloading {output_file} from Google Drive...")
        gdown.download(f"https://drive.google.com/uc?id={drive_id}", output_file, quiet=False)
        print(f"✅ {output_file} downloaded successfully.")
    else:
        print(f"✅ {output_file} already exists, skipping download.")

# ===== START YOUTUBE STREAM =====
def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    ffmpeg_command = [
        "ffmpeg",
        "-re",
        "-stream_loop", "-1", "-i", VIDEO_FILE,      # Loop video infinitely
        "-stream_loop", "-1", "-i", AUDIO_FILE,      # Loop audio infinitely
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-b:v", "6800k",            # Recommended for 1080p 30fps
        "-maxrate", "6800k",
        "-bufsize", "13600k",
        "-pix_fmt", "yuv420p",
        "-g", "60",                  # Keyframe every 2 seconds
        "-c:a", "aac",
        "-b:a", "128k",              # YouTube recommended audio bitrate
        "-ar", "44100",
        "-f", "flv",
        rtmp_url
    ]

    # Run FFmpeg in background
    subprocess.Popen(ffmpeg_command)

# ===== MAIN =====
if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()

    # Download video and audio from Google Drive if not already present
    download_from_drive(VIDEO_DRIVE_ID, VIDEO_FILE)
    download_from_drive(AUDIO_DRIVE_ID, AUDIO_FILE)

    # Start YouTube livestream
    start_stream()
