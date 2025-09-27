import subprocess
from flask import Flask
import threading

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"        # YouTube stream key
VIDEO_DRIVE_ID = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"   # Drive ID of video/GIF
AUDIO_DRIVE_ID = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"  # Drive ID of audio

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
        "-stream_loop", "-1", "-re", "-i", VIDEO_FILE,   # loop video
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,   # loop audio
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-r", "30",              # fix fps at 30
        "-g", "60",              # keyframe interval (2 sec)
        "-b:v", "2000k",         # video bitrate
        "-maxrate", "2500k",     # max bitrate
        "-bufsize", "5000k",     # buffer size
        "-c:a", "aac",
        "-b:a", "128k",          # audio bitrate
        "-ar", "44100",          # audio sample rate
        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()

    download_from_drive(VIDEO_DRIVE_ID, VIDEO_FILE)
    download_from_drive(AUDIO_DRIVE_ID, AUDIO_FILE)

    while True:
        start_stream()
