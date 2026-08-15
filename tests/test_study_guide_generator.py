# tests/test_study_guide_generator.py
"""Tests for src/study_guide_generator.py."""
import pytest
from unittest import mock


class TestStudyGuideGenerator:

    @mock.patch("src.study_guide_generator.genai")
    def test_successful_generation(self, mock_genai, sample_transcript):
        from src.study_guide_generator import generate_study_guide

        mock_response = mock.MagicMock()
        mock_response.text = "# Study Guide\n\n- **Photosynthesis** converts sunlight to energy."
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        success, guide, error = generate_study_guide(sample_transcript, api_key="fake-key")

        assert success is True
        assert "Photosynthesis" in guide
        assert error is None

    @mock.patch("src.study_guide_generator.genai")
    def test_empty_response(self, mock_genai, sample_transcript):
        from src.study_guide_generator import generate_study_guide

        mock_response = mock.MagicMock()
        mock_response.text = ""
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        success, guide, error = generate_study_guide(sample_transcript, api_key="fake-key")

        assert success is False
        assert guide is None
        assert error is not None

    @mock.patch("src.study_guide_generator.genai")
    def test_api_exception(self, mock_genai, sample_transcript):
        from src.study_guide_generator import generate_study_guide

        mock_model = mock.MagicMock()
        mock_model.generate_content.side_effect = Exception("API down")
        mock_genai.GenerativeModel.return_value = mock_model

        success, guide, error = generate_study_guide(sample_transcript, api_key="fake-key")

        assert success is False
        assert guide is None
        assert "failed" in error.lower()

    @mock.patch("src.study_guide_generator.genai")
    def test_prompt_contains_transcript(self, mock_genai, sample_transcript):
        from src.study_guide_generator import generate_study_guide

        mock_response = mock.MagicMock()
        mock_response.text = "# Guide\n- Point 1"
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        generate_study_guide(sample_transcript, api_key="fake-key")

        # Verify the prompt sent to Gemini contains the transcript
        called_prompt = mock_model.generate_content.call_args[0][0]
        assert "photosynthesis" in called_prompt.lower()
