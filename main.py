import subprocess

# ==== CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"   # Apna YouTube stream key daalna
DRIVE_ID = "1lI8B7mRLwfAnvUaB98wViRP2xAT9CVtA"  # Apna Drive ID daalna
AUDIO_FILE = "audio.mp3"
OVERLAY_PATH = "overlay.mp4"  # Repo me jo GIF/Video upload karoge uska naam

def download_audio():
    print("🎵 Downloading audio from Google Drive...")
    drive_url = f"https://drive.google.com/uc?id={DRIVE_ID}&export=download"
    cmd = [
        "yt-dlp", "-x", "--audio-format", "mp3",
        "-o", AUDIO_FILE, drive_url
    ]
    subprocess.run(cmd, check=True)
    print("✅ Audio downloaded successfully.")

def start_stream():
    print("📡 Starting YouTube Live stream...")
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    cmd = [
        "ffmpeg",
        "-stream_loop", "-1", "-re", "-i", OVERLAY_PATH,   # GIF/Video infinite loop
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,     # Audio infinite loop
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
    download_audio()
    while True:
        start_stream()
