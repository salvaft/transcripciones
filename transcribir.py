"""
This module processes video files, extracts audio, transcribes the audio using 
the Whisper speech-to-text model, and saves the transcriptions as text files.

Module Dependencies:
    - whisper
    - librosa
    - soundfile (as sf)
    - consts (importing paths)

Global Constants:
    - MODEL: The Whisper model used for transcription, loaded with the "small" configuration.

Functions and Processes:
1. Preprocessing:
    - Create necessary folders for videos, audios, and transcriptions if they do not exist.

2. Extracting Audio:
    - Extract audio from video files with a 16 kHz sampling rate using librosa.
    - Save the extracted audio as WAV files in the audios folder.

3. Transcribing Audio:
    - Use the Whisper model to transcribe audio files.
    - Save transcriptions as text files in the transcriptions folder.
    - The Whisper model is specifically configured for Spanish language transcription.

Notes:
    - The module processes video files with the following extensions: *.mkv and *.mp4.
    - Extracted audio is saved as WAV files.
    - Transcribed text is saved as UTF-8 encoded text files.

Example Usage:
    - Import the necessary modules and constants.
    - Configure the paths for videos, audios, and transcriptions in consts.paths.
    - Run the module to process video files, extract audio, and transcribe the audio.
"""

# %%
import whisper
import librosa
import soundfile as sf
from consts import paths


MODEL = whisper.load_model("small")  # load the small model

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
    print("Doing " + video_file.stem)

    y, sr = librosa.load(
        video_file, sr=16000
    )  # Load the audio with 16 kHz sampling rate

    audio_path = paths.audios_dir / (video_file.stem + (".wav"))
    sf.write(audio_path, y, sr)  # Save the audio as a wav file
    print("Wrote " + audio_path)


# %%
# Transcribe the audio file using Whisper
audio_files = paths.audios_dir.glob("**/*.*")
transcribed_files = [file.stem for file in paths.transcriptions_dir.iterdir()]
for audio_file in audio_files:
    if audio_file.stem in transcribed_files:
        print(f"Skiping {audio_file}")
        continue
    print("Doing " + str(audio_file))
    result = MODEL.transcribe(str(audio_file), language="spanish")

    text = result["text"].strip()
    text = text.replace(". ", ".\n")

    text_file_path = (
        paths.transcriptions_dir
        / audio_file.relative_to(paths.audios_dir)
        / (audio_file.stem + ".txt")
    )

    # Ensure that the parent directory exists; create it if it doesn't
    text_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(text)
# %%
