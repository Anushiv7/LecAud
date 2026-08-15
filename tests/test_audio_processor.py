import pytest
from unittest import mock
from src.audio_processor import validate_audio_file

# Sample valid and invalid file metadata (path, size, extension)
VALID_AUDIO = {
    "path": "tests/sample.wav",
    "size": 2_000_000,  # 2 MB
    "extension": ".wav",
}

INVALID_EXTENSION = {
    "path": "tests/sample.txt",
    "size": 1_000,
    "extension": ".txt",
}

OVERSIZED = {
    "path": "tests/large.wav",
    "size": 30_000_000,  # 30 MB > 25 MB limit
    "extension": ".wav",
}

def mock_file(path, size, ext):
    mock_file_obj = mock.MagicMock()
    mock_file_obj.name = path
    mock_file_obj.stat.return_value.st_size = size
    mock_file_obj.suffix = ext
    return mock_file_obj

def test_validate_valid_audio(monkeypatch):
    mock_file_obj = mock_file(VALID_AUDIO["path"], VALID_AUDIO["size"], VALID_AUDIO["extension"])
    monkeypatch.setattr("pathlib.Path", lambda p: mock_file_obj)
    assert validate_audio_file(VALID_AUDIO["path"]) is True

def test_invalid_extension(monkeypatch):
    mock_file_obj = mock_file(INVALID_EXTENSION["path"], INVALID_EXTENSION["size"], INVALID_EXTENSION["extension"])
    monkeypatch.setattr("pathlib.Path", lambda p: mock_file_obj)
    with pytest.raises(ValueError, match="Unsupported file type"):
        validate_audio_file(INVALID_EXTENSION["path"]) 

def test_oversized_file(monkeypatch):
    mock_file_obj = mock_file(OVERSIZED["path"], OVERSIZED["size"], OVERSIZED["extension"])
    monkeypatch.setattr("pathlib.Path", lambda p: mock_file_obj)
    with pytest.raises(ValueError, match="File size exceeds limit"):
        validate_audio_file(OVERSIZED["path"]) 
