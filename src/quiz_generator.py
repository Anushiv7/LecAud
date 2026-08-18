# src/quiz_generator.py
"""Generate a JSON MCQ quiz from a transcript using Gemini."""
import json
import time
from google import genai
from google.genai import types
from typing import Tuple, Optional, List, Dict

MAX_RETRIES = 2
BASE_DELAY = 1.0


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
    """Generate a 5-question MCQ quiz."""
    client = genai.Client(api_key=api_key)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            prompt = QUIZ_PROMPT.format(transcript=transcript)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            raw = response.text.strip() if response.text else ""
            quiz = json.loads(raw)

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


class QuizGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_quiz(self, transcript: str) -> dict:
        success, quiz_list, error_msg = generate_quiz(transcript, self.api_key)
        if not success:
            raise ValueError(error_msg)
        return {"questions": quiz_list}

    def calculate_score(self, user_answers: dict, quiz: dict) -> dict:
        questions = quiz.get("questions", [])
        total = len(questions)
        score = sum(1 for i, q in enumerate(questions) if user_answers.get(i) == q.get("answer"))
        return {
            "score": score,
            "total": total,
            "percentage": (score / total * 100) if total > 0 else 0.0
        }
