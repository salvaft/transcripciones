# %%
import pathlib
import whisper
import librosa
import soundfile as sf

model = whisper.load_model("small")  # load the small model
# %%
# Get the list of video files from the Videos folder

############ DIRECTORIO VIDEOS ############
# videos_dir = pathlib.Path("D:\\")
videos_dir = pathlib.Path("./videos/")
############ DIRECTORIO VIDEOS ############
#
############ DIRECTORIO AUDIOS ############
audios_dir = pathlib.Path("./audios/")
############ DIRECTORIO AUDIOS ############
#
############ DIRECTORIO TRANSCRIPCIONES ############
transcriptions_dir = pathlib.Path("./transcriptions/")
############ DIRECTORIO TRANSCRIPCIONES ############
#
############ EXTENSIONES VIDEOS ############
video_extensions = ["*.mkv", "*.mp4"]
############ EXTENSIONES VIDEOS ############
# %%
video_files = []
for extension in video_extensions:
    video_files = video_files + list(videos_dir.glob("**/" + extension))

print(video_files)
# %%
audio_files = [file.stem for file in audios_dir.iterdir()]
# Loop through the video files and transcribe them
for video_file in video_files:
    if video_file.stem in audio_files:
        print(f"Skipping {video_file}")
        continue

    # Extract the audio from the video file using librosa
    audio_path = audios_dir + (video_file.stem + (".wav"))

    y, sr = librosa.load(
        video_file, sr=16000
    )  # Load the audio with 16 kHz sampling rate
    sf.write(audio_path, y, sr)  # Save the audio as a wav file
    print("Wrote " + audio_path)


# %%
# Transcribe the audio file using Whisper
audio_files = audios_dir.glob("**/*")
transcribed_files = [file.stem for file in transcriptions_dir.iterdir()]
for audio_file in audio_files:
    print(audio_file)
    if audio_file.stem in transcribed_files:
        print(f"Skiping {audio_file}")
        continue
    print("Doing " + audio_file.stem)
    result = model.transcribe(audio_file, language="spanish")

    text = result["text"].strip()
    text = text.replace(". ", ".\n")

    # Save the transcription as a text file
    text_file = audio_file.stem + ".txt"  # Replace the video extension with .txt
    text_path = transcriptions_dir + text_file
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)
