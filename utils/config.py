# utils/config.py
"""Configuration utilities – loads the Gemini API key."""
import os
from pathlib import Path
from typing import Optional


def get_gemini_key() -> Optional[str]:
    """Retrieve the Gemini API key.

    Checks in order:
    1. Streamlit secrets (GEMINI_API_KEY)
    2. Environment variable GEMINI_API_KEY
    3. .env file in project root

    Returns None if the key cannot be found.
    """
    # 1. Streamlit secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # 2. Environment variable
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key

    # 3. .env file fallback
    dotenv_path = Path(".env")
    if dotenv_path.is_file():
        for line in dotenv_path.read_text().splitlines():
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            if key.strip() == "GEMINI_API_KEY":
                return val.strip().strip('"').strip("'")

    return None

# Alias for backwards compatibility
get_gemini_api_key = get_gemini_key

class Config:
    """Application configuration constants."""
    MAX_FILE_SIZE_MB = 25
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    SUPPORTED_AUDIO_FORMATS = ('wav', 'mp3', 'm4a', 'ogg')
    GEMINI_MODEL_AUDIO = "gemini-3.6-flash"
    GEMINI_MODEL_TEXT = "gemini-3.6-flash"
    GEMINI_MAX_RETRIES = 3
    GEMINI_RETRY_WAIT_BASE = 1
    QUIZ_QUESTION_COUNT = 5
    QUIZ_OPTIONS_COUNT = 4
    APP_TITLE = "🎙️ LecAud"
    APP_ICON = "🎙️"
    PAGE_LAYOUT = "wide"
