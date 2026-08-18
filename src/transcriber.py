# src/transcriber.py
"""Audio transcription via Gemini with retry logic and exponential back-off."""
import os
import time
import tempfile
from google import genai
from typing import Tuple, Optional

MAX_RETRIES = 3
BASE_DELAY = 1.0  # seconds


def transcribe(audio_path: str, api_key: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Transcribe an audio file using Gemini."""
    client = genai.Client(api_key=api_key)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"[{attempt}/{MAX_RETRIES}] Uploading audio to Gemini...")
            audio_file = client.files.upload(file=audio_path)
            print(f"[{attempt}/{MAX_RETRIES}] Upload complete. File URI: {audio_file.uri}")
            
            print(f"[{attempt}/{MAX_RETRIES}] Asking Gemini to transcribe...")
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=["Please transcribe the following audio accurately.", audio_file]
            )
            print(f"[{attempt}/{MAX_RETRIES}] Received response from Gemini!")
            
            transcript = response.text.strip() if response.text else ""
            if transcript:
                return True, transcript, None
            raise ValueError("Empty transcript returned by Gemini.")
        except Exception as exc:
            print(f"[{attempt}/{MAX_RETRIES}] Error encountered: {exc}")
            if attempt == MAX_RETRIES:
                return (
                    False,
                    None,
                    f"Transcription failed after {MAX_RETRIES} attempts: {exc}",
                )
            print(f"[{attempt}/{MAX_RETRIES}] Retrying in {BASE_DELAY * (2 ** (attempt - 1))} seconds...")
            time.sleep(BASE_DELAY * (2 ** (attempt - 1)))

    return False, None, "Unexpected transcription error."


class Transcriber:
    """Wrapper class for audio transcription."""
    
    def __init__(self, api_key: str):
        """Initialize transcriber with API key."""
        self.api_key = api_key
    
    def transcribe_audio(self, audio_file) -> str:
        """
        Transcribe audio file to text.
        
        Parameters
        ----------
        audio_file : Streamlit UploadedFile
            Audio file from Streamlit uploader
            
        Returns
        -------
        str
            Transcribed text
            
        Raises
        ------
        ValueError
            If transcription fails
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.getvalue())
            tmp_path = tmp.name
        
        try:
            success, transcript, error_msg = transcribe(tmp_path, self.api_key)
            if success:
                return transcript
            else:
                raise ValueError(error_msg or "Transcription failed")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)