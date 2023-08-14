# %%
import whisper
import librosa
import soundfile as sf
from consts import paths

model = whisper.load_model("small")  # load the small model

#
############ EXTENSIONES VIDEOS ############
video_extensions = ["*.mkv", "*.mp4"]
############ EXTENSIONES VIDEOS ############
#
############ EXTENSIONES AUDIOS ############
audio_extensions = ["*.wav", "*.opus"]
############ EXTENSIONES AUDIOS ############
# %%
# Create folders if they do not exist
paths.videos_dir.mkdir(parents=True, exist_ok=True)
paths.audios_dir.mkdir(parents=True, exist_ok=True)
paths.transcriptions_dir.mkdir(parents=True, exist_ok=True)

# %%
# Get the list of video files from the Videos folder
video_files = []
for extension in video_extensions:
    video_files = video_files + list(paths.videos_dir.glob("**/" + extension))

print(video_files)
# %%
audio_files = [file.stem for file in paths.audios_dir.iterdir()]
# Loop through the video files and transcribe them
for video_file in video_files:
    if video_file.stem in audio_files:
        print(f"Skipping {video_file}")
        continue

    # Extract the audio from the video file using librosa

    y, sr = librosa.load(
        video_file, sr=16000
    )  # Load the audio with 16 kHz sampling rate
    audio_path = paths.audios_dir / (video_file.stem + (".wav"))
    sf.write(audio_path, y, sr)  # Save the audio as a wav file
    print("Wrote " + audio_path)


# %%
# Transcribe the audio file using Whisper
audio_files = paths.audios_dir.glob("**/*")
transcribed_files = [file.stem for file in paths.transcriptions_dir.iterdir()]
for audio_file in audio_files:
    print(audio_file)
    if audio_file.stem in transcribed_files:
        print(f"Skiping {audio_file}")
        continue
    print("Doing " + audio_file.stem)
    result = model.transcribe(str(audio_file), language="spanish")

    text = result["text"].strip()
    text = text.replace(". ", ".\n")

    # Save the transcription as a text file
    text_file = audio_file.stem + ".txt"  # Replace the video extension with .txt
    text_path = paths.transcriptions_dir / text_file
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
# %%
