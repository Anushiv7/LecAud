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


class AudioProcessor:
    """Handle audio file uploads, validation, and metadata."""
    
    def __init__(self):
        """Initialize audio processor with configuration."""
        self.max_file_size = MAX_FILE_SIZE
        self.supported_formats = ALLOWED_EXTENSIONS
    
    def validate_file_format(self, filename: str) -> bool:
        """Validate audio file format."""
        is_valid, msg = validate_audio(filename)
        if not is_valid:
            raise ValueError(msg)
        return True
    
    def validate_audio_file(self, uploaded_file) -> bool:
        """Validate uploaded audio file from Streamlit."""
        filename = uploaded_file.name
        file_size = len(uploaded_file.getvalue())
        
        # Check extension
        _, ext = os.path.splitext(filename.lower())
        if ext not in self.supported_formats:
            raise ValueError(
                f"❌ Unsupported format: `{ext}`. "
                f"Supported: {', '.join(sorted(self.supported_formats))}"
            )
        
        # Check size
        if file_size > self.max_file_size:
            size_mb = file_size / (1024 * 1024)
            raise ValueError(
                f"❌ File exceeds 25MB limit. Your file: {size_mb:.1f}MB"
            )
        
        return True
    
    def get_audio_metadata(self, uploaded_file) -> dict:
        """Extract metadata from audio file."""
        file_size_bytes = len(uploaded_file.getvalue())
        file_size_mb = file_size_bytes / (1024 * 1024)
        _, file_ext = os.path.splitext(uploaded_file.name.lower())
        
        return {
            "filename": uploaded_file.name,
            "size_mb": round(file_size_mb, 2),
            "format": file_ext.lstrip('.'),
            "size_bytes": file_size_bytes,
        }