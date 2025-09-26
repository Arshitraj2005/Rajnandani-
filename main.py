import subprocess
from flask import Flask
import threading

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"        # YouTube stream key
VIDEO_DRIVE_ID = "1SqqVbApLnkj8rSnmfYBH7Yva90MxhPwa"   # Drive ID of video/GIF
AUDIO_DRIVE_ID = "1ilOvOl76gwquhWU-Xz78rcTOwLPdnizY"  # Drive ID of audio

VIDEO_FILE = "overlay.mp4"   # Downloaded video/GIF
AUDIO_FILE = "audio.mp3"     # Downloaded audio

# ==== FLASK SERVER FOR PORT BIND ====
app = Flask(__name__)

@app.route("/")
def home():
    return "Stream Running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ==== DOWNLOAD FILE FROM DRIVE ====
def download_from_drive(drive_id, output_file):
    print(f"⬇️ Downloading {output_file} from Google Drive...")
    url = f"https://drive.google.com/uc?id={drive_id}&export=download"
    cmd = ["yt-dlp", "-f", "best", "-o", output_file, url]
    subprocess.run(cmd, check=True)
    print(f"✅ {output_file} downloaded successfully.")

# ==== START YOUTUBE STREAM ====
def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-re", "-i", VIDEO_FILE,  # video loop
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,  # audio loop
        "-map", "0:v:0",  # video from video file
        "-map", "1:a:0",  # audio from audio file
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
    
    # Download video and audio from Drive
    download_from_drive(VIDEO_DRIVE_ID, VIDEO_FILE)
    download_from_drive(AUDIO_DRIVE_ID, AUDIO_FILE)
    
    # Start stream
    while True:
        start_stream()
