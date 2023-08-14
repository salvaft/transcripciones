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


def convert_opus_to_mp3(opus_file):
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
    mp3_file = opus_file.with_suffix(".mp3")
    sound.export(mp3_file, format="mp3")
