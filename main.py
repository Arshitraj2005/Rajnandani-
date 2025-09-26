import subprocess

# ==== FIXED CONFIG ====
STREAM_KEY = "cec7-xy4y-9y7e-xk7t-4qxa"
DRIVE_ID = "1lI8B7mRLwfAnvUaB98wViRP2xAT9CVtA"
AUDIO_FILE = "audio.mp3"

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
        # black background video generate karega (720x1280 vertical format)
        "-f", "lavfi", "-i", "color=size=720x1280:rate=30:color=black",
        "-stream_loop", "-1", "-re", "-i", AUDIO_FILE,
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",  # video sirf audio ke duration tak chalega, phir loop
        "-f", "flv",
        rtmp_url
    ]

    subprocess.run(cmd)

if __name__ == "__main__":
    download_audio()
    while True:
        start_stream()
