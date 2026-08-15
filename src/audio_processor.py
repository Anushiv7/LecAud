# src/audio_processor.py
"""Audio validation utilities.

Validates uploaded audio files for format and size before sending to Gemini.
"""
import os
from typing import Tuple

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a", ".ogg"}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


def _extension_allowed(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path.lower())
    return ext in ALLOWED_EXTENSIONS


def validate_audio(file_path: str) -> Tuple[bool, str]:
    """Validate an uploaded audio file.

    Returns
    -------
    (bool, str)
        True + success message if valid, False + error message if not.
    """
    if not os.path.isfile(file_path):
        return False, "File does not exist."

    if not _extension_allowed(file_path):
        return (
            False,
            f"Unsupported file type. Allowed extensions: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    size = os.path.getsize(file_path)
    if size > MAX_FILE_SIZE:
        return False, f"File too large ({size / 1_048_576:.1f} MB). Max size is 25 MB."

    return True, "File is valid."
