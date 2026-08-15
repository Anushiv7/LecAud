# tests/conftest.py
"""Shared pytest fixtures for the Voice-Notes test suite."""
import pytest
from unittest import mock


@pytest.fixture
def sample_audio_path(tmp_path):
    """Create a small dummy wav file for testing."""
    file_path = tmp_path / "sample.wav"
    # Minimal WAV header bytes — enough for validation tests
    file_path.write_bytes(b"RIFF....WAVEfmt " + b"\x00" * 100)
    return str(file_path)


@pytest.fixture
def oversized_audio_path(tmp_path):
    """Create an audio file that exceeds the 25 MB limit."""
    file_path = tmp_path / "big.wav"
    file_path.write_bytes(b"\x00" * (26 * 1024 * 1024))  # 26 MB
    return str(file_path)


@pytest.fixture
def invalid_ext_path(tmp_path):
    """Create a file with an unsupported extension."""
    file_path = tmp_path / "notes.txt"
    file_path.write_text("not audio")
    return str(file_path)


@pytest.fixture
def mock_gemini_model():
    """Return a mock Gemini GenerativeModel."""
    model = mock.MagicMock()
    response = mock.MagicMock()
    response.text = "mock response"
    model.generate_content.return_value = response
    return model


@pytest.fixture
def sample_transcript():
    """Return a sample transcript string for guide/quiz tests."""
    return (
        "Today we will discuss photosynthesis. Photosynthesis is the process by which "
        "green plants convert sunlight into chemical energy. The key equation is: "
        "6CO2 + 6H2O + light energy -> C6H12O6 + 6O2. "
        "Chloroplasts contain chlorophyll which absorbs light. "
        "The two main stages are the light-dependent reactions and the Calvin cycle."
    )
