# src/study_guide_generator.py
"""Generate a markdown study guide from a transcript using Gemini."""
import time
from google import genai
from typing import Tuple, Optional

MAX_RETRIES = 2
BASE_DELAY = 1.0


STUDY_GUIDE_PROMPT = """You are a knowledgeable tutor.
Given the following lecture transcript, produce a concise, well-structured study guide in markdown.
Use headings, bullet points, and bold for key concepts.
Do not include any preamble or postscript.

Transcript:
"""


def generate_study_guide(
    transcript: str, api_key: str
) -> Tuple[bool, Optional[str], Optional[str]]:
    """Generate a markdown study guide.

    Returns (success, guide_markdown, error_message).
    """
    client = genai.Client(api_key=api_key)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            prompt = f'''{STUDY_GUIDE_PROMPT}\nTranscript:\n{transcript}'''
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )
            guide = response.text.strip() if response.text else ""
            if guide:
                return True, guide, None
            raise ValueError("Empty guide returned by Gemini.")
        except Exception as exc:
            if attempt == MAX_RETRIES:
                return False, None, f"Study guide generation failed: {exc}"
            time.sleep(BASE_DELAY * (2 ** (attempt - 1)))

    return False, None, "Unexpected generation error."


class StudyGuideGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_study_guide(self, transcript: str) -> str:
        success, guide, error_msg = generate_study_guide(transcript, self.api_key)
        if not success:
            raise ValueError(error_msg)
        return guide
