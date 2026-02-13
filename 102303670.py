import sys
import os
import glob
import yt_dlp
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


# -----------------------
# Create folders
# -----------------------
def create_dirs():
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)


# -----------------------
# Download videos
# -----------------------
def download_videos(singer, n):
    print("Downloading videos...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'videos/%(title)s.%(ext)s',
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{n}:{singer} songs"])


# -----------------------
# Convert video → audio
# -----------------------
def convert_to_audio():
    print("Converting videos to audio...")

    for video in glob.glob("videos/*"):
        name = os.path.splitext(os.path.basename(video))[0]
        audio_path = f"audios/{name}.mp3"

        clip = VideoFileClip(video)
        clip.audio.write_audiofile(audio_path)
        clip.close()


# -----------------------
# Trim first Y seconds
# -----------------------
def trim_audio(duration):
    print("Trimming audio...")

    for file in glob.glob("audios/*.mp3"):
        sound = AudioSegment.from_file(file)
        trimmed = sound[:duration * 1000]
        trimmed.export(file, format="mp3")


# -----------------------
# Merge all audio
# -----------------------
def merge(output):
    print("Merging audio...")

    combined = AudioSegment.empty()

    for file in glob.glob("audios/*.mp3"):
        combined += AudioSegment.from_file(file)

    combined.export(f"outputs/{output}", format="mp3")
    print("Saved → outputs/" + output)


# -----------------------
# Main
# -----------------------
def main():
    if len(sys.argv) != 5:
        print("Usage: python 102303670.py <SingerName> <NumberOfVideos> <Duration> <OutputFile>")
        return

    singer = sys.argv[1]
    n = int(sys.argv[2])
    duration = int(sys.argv[3])
    output = sys.argv[4]

    try:
        create_dirs()
        download_videos(singer, n)
        convert_to_audio()
        trim_audio(duration)
        merge(output)
        print("Mashup created successfully!")

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()