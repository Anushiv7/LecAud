# src/transcriber.py
"""Audio transcription via Gemini with retry logic and exponential back-off."""
import time
import google.generativeai as genai
from typing import Tuple, Optional

MAX_RETRIES = 3
BASE_DELAY = 1.0  # seconds


def _configure_api(api_key: str) -> None:
    genai.configure(api_key=api_key)


def transcribe(audio_path: str, api_key: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Transcribe an audio file using Gemini.

    Parameters
    ----------
    audio_path : str
        Path to the audio file on disk.
    api_key : str
        Gemini API key.

    Returns
    -------
    (success, transcript, error_message)
        success      – True if transcription succeeded.
        transcript   – the text returned by Gemini (or None on failure).
        error_message – description of the failure (or None on success).
    """
    _configure_api(api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Upload the audio file to Gemini
            audio_file = genai.upload_file(audio_path)
            response = model.generate_content(
                ["Please transcribe the following audio accurately.", audio_file]
            )
            transcript = response.text.strip() if response.text else ""
            if transcript:
                return True, transcript, None
            raise ValueError("Empty transcript returned by Gemini.")
        except Exception as exc:
            if attempt == MAX_RETRIES:
                return (
                    False,
                    None,
                    f"Transcription failed after {MAX_RETRIES} attempts: {exc}",
                )
            time.sleep(BASE_DELAY * (2 ** (attempt - 1)))

    return False, None, "Unexpected transcription error."
