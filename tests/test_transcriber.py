# tests/test_transcriber.py
"""Tests for src/transcriber.py – retry logic, error handling."""
import pytest
from unittest import mock


class TestTranscribe:
    """Test the transcribe function with mocked Gemini API."""

    @mock.patch("src.transcriber.genai")
    def test_successful_transcription(self, mock_genai, sample_audio_path):
        from src.transcriber import transcribe

        mock_response = mock.MagicMock()
        mock_response.text = "This is a test transcript."
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.upload_file.return_value = "fake_file_ref"

        success, transcript, error = transcribe(sample_audio_path, api_key="fake-key")

        assert success is True
        assert transcript == "This is a test transcript."
        assert error is None

    @mock.patch("src.transcriber.genai")
    def test_empty_transcript_retries(self, mock_genai, sample_audio_path):
        from src.transcriber import transcribe

        mock_response = mock.MagicMock()
        mock_response.text = ""
        mock_model = mock.MagicMock()
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.upload_file.return_value = "fake_file_ref"

        success, transcript, error = transcribe(sample_audio_path, api_key="fake-key")

        assert success is False
        assert transcript is None
        assert "failed" in error.lower() or "empty" in error.lower()

    @mock.patch("src.transcriber.genai")
    @mock.patch("src.transcriber.time.sleep")  # skip actual delays
    def test_retry_on_exception(self, mock_sleep, mock_genai, sample_audio_path):
        from src.transcriber import transcribe

        mock_response = mock.MagicMock()
        mock_response.text = "Recovered transcript."
        mock_model = mock.MagicMock()
        # First call fails, second succeeds
        mock_model.generate_content.side_effect = [
            Exception("Transient error"),
            mock_response,
        ]
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.upload_file.return_value = "fake_file_ref"

        success, transcript, error = transcribe(sample_audio_path, api_key="fake-key")

        assert success is True
        assert transcript == "Recovered transcript."
        assert mock_model.generate_content.call_count == 2

    @mock.patch("src.transcriber.genai")
    @mock.patch("src.transcriber.time.sleep")
    def test_all_retries_exhausted(self, mock_sleep, mock_genai, sample_audio_path):
        from src.transcriber import transcribe

        mock_model = mock.MagicMock()
        mock_model.generate_content.side_effect = Exception("Permanent failure")
        mock_genai.GenerativeModel.return_value = mock_model
        mock_genai.upload_file.return_value = "fake_file_ref"

        success, transcript, error = transcribe(sample_audio_path, api_key="fake-key")

        assert success is False
        assert transcript is None
        assert "3 attempts" in error
