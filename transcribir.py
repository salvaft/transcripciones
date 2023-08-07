# %%
import whisper
import time
import librosa
import soundfile as sf
import re
import pathlib
import os

model = whisper.load_model("small")  # load the small model
# %%
# Get the list of video files from the Videos folder

############ DIRECTORIO VIDEOS ############
# videos_dir = pathlib.Path("D:\\")
videos_dir = pathlib.Path("./videos/")
############ DIRECTORIO VIDEOS ############
#
############ EXTENSIONES VIDEOS ############
video_extensions = ["*.mkv", "*.mp4"]
############ EXTENSIONES VIDEOS ############

video_files = []
for extension in video_extensions:
    video_files = video_files + list(videos_dir.glob("**/" + extension))

print(video_files)
# %%
audio_files = os.listdir("./audios")
# Loop through the video files and transcribe them
for video_file in video_files:
    if video_file.stem + ".wav" in audio_files:
        print(f"Skipping {video_file}")
        continue

    # Extract the audio from the video file using librosa
    audio_path = "./audios/" + (video_file.stem + (".wav"))

    y, sr = librosa.load(
        video_file, sr=16000
    )  # Load the audio with 16 kHz sampling rate
    sf.write(audio_path, y, sr)  # Save the audio as a wav file
    print("Wrote " + audio_path)


# %%
# Transcribe the audio file using Whisper
audio_files = os.listdir("./audios/")
transcribed_files = os.listdir("./transcriptions")
for audio_file in audio_files:
    if (audio_file[:-4] + ".txt") in transcribed_files:
        print(f"Skiping {audio_file}")
        continue
    print("Doing " + audio_file)
    result = model.transcribe(str("./audios/" + audio_file), language="spanish")

    text = result["text"].strip()
    text = text.replace(". ", ".\n")

    # Save the transcription as a text file
    text_file = audio_file[:-4] + ".txt"  # Replace the video extension with .txt
    text_path = "./transcriptions/" + text_file
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

# %%
