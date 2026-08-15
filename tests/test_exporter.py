# tests/test_exporter.py
"""Tests for src/exporter.py – file export logic."""
import json
import os
import pytest
from src.exporter import export_text, export_json, get_text_bytes, get_json_bytes


class TestExportText:

    def test_creates_file(self, tmp_path):
        content = "# Study Guide\n- Point 1\n- Point 2"
        path = export_text(content, "guide.txt", out_dir=str(tmp_path))

        assert os.path.isfile(path)
        assert open(path, encoding="utf-8").read() == content

    def test_creates_directory(self, tmp_path):
        out_dir = str(tmp_path / "nested" / "exports")
        path = export_text("hello", "test.txt", out_dir=out_dir)

        assert os.path.isfile(path)

    def test_overwrites_existing(self, tmp_path):
        export_text("first", "out.txt", out_dir=str(tmp_path))
        path = export_text("second", "out.txt", out_dir=str(tmp_path))

        assert open(path, encoding="utf-8").read() == "second"


class TestExportJson:

    def test_creates_valid_json(self, tmp_path):
        data = [{"question": "Q1", "answer": "A"}]
        path = export_json(data, "quiz.json", out_dir=str(tmp_path))

        assert os.path.isfile(path)
        loaded = json.loads(open(path, encoding="utf-8").read())
        assert loaded == data

    def test_handles_nested_data(self, tmp_path):
        data = {"questions": [{"q": "Q1", "opts": ["a", "b"]}]}
        path = export_json(data, "nested.json", out_dir=str(tmp_path))

        loaded = json.loads(open(path, encoding="utf-8").read())
        assert loaded["questions"][0]["q"] == "Q1"


class TestByteHelpers:

    def test_text_bytes(self):
        result = get_text_bytes("hello world")
        assert isinstance(result, bytes)
        assert result == b"hello world"

    def test_json_bytes(self):
        data = {"key": "value"}
        result = get_json_bytes(data)
        assert isinstance(result, bytes)
        loaded = json.loads(result.decode("utf-8"))
        assert loaded == data
