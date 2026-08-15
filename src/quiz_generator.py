# src/quiz_generator.py
"""Generate a JSON MCQ quiz from a transcript using Gemini."""
import json
import time
import google.generativeai as genai
from typing import Tuple, Optional, List, Dict

MAX_RETRIES = 2
BASE_DELAY = 1.0


def _configure_api(api_key: str) -> None:
    genai.configure(api_key=api_key)


QUIZ_PROMPT = """You are an expert quiz-maker.
Create a JSON array of exactly 5 multiple-choice questions based on the following transcript.
Each object must have:
- "question": string
- "options": list of 4 strings
- "answer": string (the correct option text)

Return ONLY raw JSON, no extra text.

Transcript:
{transcript}
"""


def generate_quiz(
    transcript: str, api_key: str
) -> Tuple[bool, Optional[List[Dict]], Optional[str]]:
    """Generate a 5-question MCQ quiz.

    Returns (success, quiz_list, error_message).
    quiz_list is a list of dicts with keys: question, options, answer.
    """
    _configure_api(api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            prompt = QUIZ_PROMPT.format(transcript=transcript)
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json"
                ),
            )
            raw = response.text.strip() if response.text else ""
            quiz = json.loads(raw)

            # Gemini may return {"questions": [...]} or just [...]
            if isinstance(quiz, dict) and "questions" in quiz:
                quiz = quiz["questions"]

            if isinstance(quiz, list) and len(quiz) >= 1:
                return True, quiz, None

            raise ValueError(f"Unexpected quiz structure: {type(quiz)}")
        except json.JSONDecodeError as exc:
            if attempt == MAX_RETRIES:
                return False, None, f"Failed to parse quiz JSON: {exc}"
            time.sleep(BASE_DELAY * (2 ** (attempt - 1)))
        except Exception as exc:
            if attempt == MAX_RETRIES:
                return False, None, f"Quiz generation failed: {exc}"
            time.sleep(BASE_DELAY * (2 ** (attempt - 1)))

    return False, None, "Unexpected quiz failure."
