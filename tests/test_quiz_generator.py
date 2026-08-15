# tests/test_quiz_generator.py
"""Tests for src/quiz_generator.py – JSON parsing, validation, error handling."""
import json
import pytest
from unittest import mock

VALID_QUIZ_JSON = json.dumps([
    {"question": "What is photosynthesis?", "options": ["A", "B", "C", "D"], "answer": "A"},
    {"question": "Where does it occur?", "options": ["A", "B", "C", "D"], "answer": "B"},
    {"question": "What is chlorophyll?", "options": ["A", "B", "C", "D"], "answer": "C"},
    {"question": "What is the Calvin cycle?", "options": ["A", "B", "C", "D"], "answer": "D"},
    {"question": "What gas is produced?", "options": ["A", "B", "C", "D"], "answer": "A"},
])


class TestQuizGenerator:

    @mock.patch("src.quiz_generator.genai")
    def test_successful_quiz(self, mock_genai, sample_transcript):
        from src.quiz_generator import generate_quiz

        mock_response = mock.MagicMock()
        mock_response.text = VALID_QUIZ_JSON
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.GenerationConfig = mock.MagicMock()

        success, quiz, error = generate_quiz(sample_transcript, api_key="fake-key")

        assert success is True
        assert isinstance(quiz, list)
        assert len(quiz) == 5
        assert error is None

    @mock.patch("src.quiz_generator.genai")
    def test_quiz_wrapped_in_dict(self, mock_genai, sample_transcript):
        """Gemini sometimes returns {"questions": [...]}."""
        from src.quiz_generator import generate_quiz

        wrapped = json.dumps({"questions": json.loads(VALID_QUIZ_JSON)})
        mock_response = mock.MagicMock()
        mock_response.text = wrapped
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.GenerationConfig = mock.MagicMock()

        success, quiz, error = generate_quiz(sample_transcript, api_key="fake-key")

        assert success is True
        assert len(quiz) == 5

    @mock.patch("src.quiz_generator.genai")
    def test_invalid_json(self, mock_genai, sample_transcript):
        from src.quiz_generator import generate_quiz

        mock_response = mock.MagicMock()
        mock_response.text = "{ this is not valid json }"
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.GenerationConfig = mock.MagicMock()

        success, quiz, error = generate_quiz(sample_transcript, api_key="fake-key")

        assert success is False
        assert quiz is None
        assert "json" in error.lower() or "parse" in error.lower()

    @mock.patch("src.quiz_generator.genai")
    def test_api_exception(self, mock_genai, sample_transcript):
        from src.quiz_generator import generate_quiz

        mock_model = mock.MagicMock()
        mock_model.generate_content.side_effect = Exception("API failure")
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.GenerationConfig = mock.MagicMock()

        success, quiz, error = generate_quiz(sample_transcript, api_key="fake-key")

        assert success is False
        assert quiz is None
        assert error is not None
