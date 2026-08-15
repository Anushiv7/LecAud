# src/exporter.py
"""Export transcript, study guide, and quiz to TXT and JSON files."""
import json
import os
from pathlib import Path


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def export_text(content: str, filename: str, out_dir: str = "exports") -> str:
    """Write plain-text content to a file.

    Returns the absolute path of the created file.
    """
    _ensure_dir(out_dir)
    out_path = Path(out_dir) / filename
    out_path.write_text(content, encoding="utf-8")
    return str(out_path.resolve())


def export_json(data, filename: str, out_dir: str = "exports") -> str:
    """Serialize data to JSON and write it to a file.

    Returns the absolute path of the created file.
    """
    _ensure_dir(out_dir)
    out_path = Path(out_dir) / filename
    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return str(out_path.resolve())


def get_text_bytes(content: str) -> bytes:
    """Return content as UTF-8 bytes (for Streamlit download_button)."""
    return content.encode("utf-8")


def get_json_bytes(data) -> bytes:
    """Return data serialized as JSON bytes (for Streamlit download_button)."""
    return json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
