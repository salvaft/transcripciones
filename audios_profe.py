"""
This module contains a script to process and organize audio files from a
 specified source directory, convert opus/ogg audio files to mp3 format, and 
 organize them into sorted folders based on chat message topics. It performs the following steps:

1. Moves .zip files from the specified source directory to a local "profe" directory.
2. Extracts the contents of the .zip files into a ".dump" subdirectory within the "profe" directory.
3. Reads chat data from a specified file "_chat.txt" within the ".dump" directory.
4. Extracts relevant information from the chat data, including dates, times, senders, and messages.
5. Organizes the audio files based on message topics in the "profe/sorted" directory.
6. Converts opus/ogg audio files to mp3 format and removes the original opus/ogg files.

Module Components:
- ZIP_SOURCE_DIR: The source directory containing .zip files to be processed.
- PROFE_DIR: The main processing directory.
- PROFE_SORTED_DIR: Directory where the sorted files will be organized.
- DUMP_DIR: Directory where the contents of the .zip files are extracted.
- CHAT_FILE: The chat data file to be processed.
- PATTERN: Regular expression pattern to extract message details.
- FILENAME_PATTERN: Regular expression pattern to extract attached filenames.
- Matching Files: Finds opus and ogg files within the sorted directory for conversion.

Note: This module relies on the 'utils' package, specifically 'opus_to_mp3.py' 
and 'delete_dir.py' within the 'utils' directory.

Usage:
1. Run the script to process the .zip files, extract chat data, organize files, 
and convert opus/ogg files to mp3.
2. Ensure the required 'utils' modules are present in the same directory as this script.

Please ensure you have the necessary permissions and correct file paths before running this script.
"""

from pathlib import Path
import shutil
import zipfile
import os
import re
import sys
import pickle
from utils.opus_to_mp3 import convert_opus_to_mp3
from utils.delete_dir import delete_directory


ZIP_SOURCE_DIR = Path("/home/sft/Nextcloud/")
PROFE_DIR = Path(".") / "profe"
PROFE_SORTED_DIR = PROFE_DIR / "sorted"
DUMP_DIR = PROFE_DIR / ".dump"
CHAT_FILE = DUMP_DIR / "_chat.txt"

if os.path.exists(DUMP_DIR):
    delete_directory(DUMP_DIR)

# Iterate through all files in the source directory with the specified file extension
for file_path in ZIP_SOURCE_DIR.glob("*profe.zip"):
    print(f"Moving file '{file_path}' to '{PROFE_DIR / file_path.name}'...")
    if not os.path.exists(PROFE_DIR):
        os.makedirs(PROFE_DIR)
    # Use the shutil.move() function to move the file from source to destination
    shutil.move(file_path, PROFE_DIR / file_path.name)
    print(f"File '{file_path}' moved to '{PROFE_DIR / file_path.name}' successfully.")

for zip_file in PROFE_DIR.glob("*profe.zip"):
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(DUMP_DIR)

# Read the file into a list of lines
if not CHAT_FILE.exists():
    sys.exit()

with open(CHAT_FILE, "r", encoding="UTF-8") as file:
    lines = file.readlines()

# Define the regular expression pattern to parse whatsapp messages
PATTERN = r"(\u200E)?\[(\d+/\d+/\d+), (\d+:\d+:\d+)\] ([\w\s]+): (.*)"

# The u200E utf character defines a system message that we use to parse attachments
FILENAME_PATTERN = r".*\u200E<attached: (.*)>"


if os.path.exists("pickle.pkl"):
    print("Loading pickle...")
    with open("pickle.pkl", "rb") as pkl_file:
        data_loaded = pickle.load(pkl_file)
        LAST_LINE = data_loaded["last_line"]
        temas = data_loaded["temas"]
else:
    temas = []
    LAST_LINE = 23

# Starting line is 23
for index, line in enumerate(lines[LAST_LINE:]):
    match = re.match(PATTERN, line)
    if match:
        tema = {}

        char, date, time, sender, message = match.groups()
        if "omitted" not in message and not char:
            tema["title"] = message.replace("/", "_")
            tema["files"] = []
            temas.append(tema)

        if char and "omitted" not in message:
            rematch = re.match(FILENAME_PATTERN, message.strip())
            if rematch:
                filename = rematch.groups()[0]
                audio_path = DUMP_DIR / filename
                temas[-1]["files"].append(audio_path)

LAST_LINE = len(lines)

with open("pickle.pkl", "wb") as pkl_file:
    data_to_save = {"last_line": LAST_LINE, "temas": temas}
    pickle.dump(data_to_save, pkl_file)

for tema in temas:
    if not os.path.exists(PROFE_SORTED_DIR / tema["title"]) and tema["files"]:
        os.makedirs(PROFE_SORTED_DIR / tema["title"])
    for file in tema["files"]:
        sorted_file_path = PROFE_SORTED_DIR / tema["title"] / file.name
        if sorted_file_path.suffix in [".ogg", ".opus"]:
            sorted_file_path = (
                PROFE_SORTED_DIR / tema["title"] / file.with_suffix(".mp3").name
            )

        if not sorted_file_path.exists():
            shutil.move(file, PROFE_SORTED_DIR / tema["title"])
        else:
            print(f"Skipping {file}")


OPUS_EXTENSION = "*.opus"
OGG_EXTENSION = "*.ogg"
matching_files = list(PROFE_SORTED_DIR.rglob(OPUS_EXTENSION)) + list(
    PROFE_SORTED_DIR.rglob(OGG_EXTENSION)
)

for file in matching_files:
    convert_opus_to_mp3(file)
    file.unlink()

# Zip the sorted directory
shutil.make_archive("audios_profe", "zip", PROFE_SORTED_DIR)
print(f"Folder '{PROFE_SORTED_DIR}' zipped to audios_profe.zip successfully.")
