"""
Module containing constant paths for video, audio, and transcription directories.

Attributes:
    videos_dir (pathlib.Path): The directory path where video files are located.
        Default value: "./videos/".
        
    audios_dir (pathlib.Path): The directory path where audio files are located.
        Default value: "./audios/".

    transcriptions_dir (pathlib.Path): The directory path where transcription files are located.
        Default value: "./transcriptions/".
"""
import pathlib

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
############ DIRECTORIO TRANSCRIPCIONES ############
cwd = pathlib.Path(".")
############ DIRECTORIO TRANSCRIPCIONES ############


ZIP_SOURCE_DIR = pathlib.Path("/home/sft/Nextcloud/")
PROFE_DIR = pathlib.Path(".") / "profe"
PROFE_SORTED_DIR = PROFE_DIR / "sorted"
DUMP_DIR = PROFE_DIR / ".dump"
CHAT_FILE = DUMP_DIR / "_chat.txt"
