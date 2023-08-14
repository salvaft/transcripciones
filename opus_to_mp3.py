"""
This module provides a function to convert audio files from .opus 
format to .mp3 format using the pydub library.

Module Dependencies:
    - pydub
    - consts (importing paths)

Functions:
    - convert_opus_to_mp3(opus_file, mp3_file)
        Convert an audio file from .opus format to .mp3 format.

        Parameters:
            opus_file (str): Path to the input .opus audio file.
            mp3_file (str): Path to the output .mp3 audio file.

        Notes:
            This function reads the input .opus file, converts it to a temporary WAV file,
            and then converts the WAV file to .mp3 format using the pydub library.

        Example:
            convert_opus_to_mp3("input.opus", "output.mp3")
"""

from pydub import AudioSegment
from consts import paths


def convert_opus_to_mp3(opus_file, mp3_file):
    """
    Convert an audio file from .opus format to .mp3 format.

    Parameters:
        opus_file (str): Path to the input .opus audio file.
        mp3_file (str): Path to the output .mp3 audio file.

    Notes:
        This function reads the input .opus file, converts it to a temporary WAV file,
        and then converts the WAV file to .mp3 format using the pydub library.

    Example:
        convert_opus_to_mp3("input.opus", "output.mp3")"""
    sound = AudioSegment.from_file(opus_file, format="ogg")
    sound.export(mp3_file, format="mp3")


for opus in paths.audios_dir.glob("*.opus"):
    mp3_filename = opus.with_suffix(".mp3")
    if not mp3_filename.exists():
        print(f"Converting {opus} to {mp3_filename}")
        convert_opus_to_mp3(opus, mp3_filename)
    else:
        print(f"Skipping {opus}")
