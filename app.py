# app.py – Streamlit entry point for Voice‑Notes to Flashcards
"""Main Streamlit application.
Wires together modules in `src/` and provides a tab‑based UI.
"""

import os
import streamlit as st
from utils.config import get_gemini_api_key
from utils.logger import get_logger
from src.audio_processor import validate_audio
from src.transcriber import transcribe_audio
from src.study_guide_generator import generate_study_guide
from src.quiz_generator import generate_quiz
from src.exporter import export_text, export_json

logger = get_logger(__name__)

st.set_page_config(page_title="Voice‑Notes to Flashcards", layout="centered")

st.title("🎤 Voice‑Notes to Flashcards")

# Load API key
api_key = get_gemini_api_key()
if not api_key:
    st.error("Gemini API key not configured. Set it in `.streamlit/secrets.toml` or env var.")
    st.stop()

# Initialise session state
for key, default in {
    "audio_path": None,
    "transcript": "",
    "study_guide": "",
    "quiz": []
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# UI tabs
tab_audio, tab_transcript, tab_guide, tab_quiz, tab_export = st.tabs([
    "Audio Input", "Transcript", "Study Guide", "Quiz", "Export"
])

with tab_audio:
    st.header("1️⃣ Audio Input")
    uploaded = st.file_uploader("Upload audio (wav/mp3/m4a, ≤25 MB)", type=["wav", "mp3", "m4a"])
    if uploaded:
        # Save to temporary file
        os.makedirs("temp", exist_ok=True)
        path = os.path.join("temp", uploaded.name)
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        if validate_audio(path):
            st.success("Audio looks good!")
            st.session_state.audio_path = path
        else:
            st.error("Invalid file – check format and size.")

with tab_transcript:
    st.header("2️⃣ Transcript")
    if st.session_state.audio_path:
        if st.button("Transcribe"):
            with st.spinner("Transcribing…"):
                try:
                    txt = transcribe_audio(st.session_state.audio_path)
                    st.session_state.transcript = txt
                    st.success("Done")
                except Exception as e:
                    logger.exception("Transcription failed")
                    st.error(f"Error: {e}")
        if st.session_state.transcript:
            st.text_area("Transcript", st.session_state.transcript, height=300)
    else:
        st.info("Upload an audio file first.")

with tab_guide:
    st.header("3️⃣ Study Guide")
    if st.session_state.transcript:
        if st.button("Generate Guide"):
            with st.spinner("Generating guide…"):
                guide = generate_study_guide(st.session_state.transcript)
                st.session_state.study_guide = guide
                st.success("Guide ready")
        if st.session_state.study_guide:
            st.markdown(st.session_state.study_guide)
    else:
        st.info("Transcribe first.")

with tab_quiz:
    st.header("4️⃣ Quiz")
    if st.session_state.transcript:
        if st.button("Generate Quiz"):
            with st.spinner("Creating quiz…"):
                quiz = generate_quiz(st.session_state.transcript)
                st.session_state.quiz = quiz
                st.success("Quiz ready")
        if st.session_state.quiz:
            for i, q in enumerate(st.session_state.quiz, 1):
                st.subheader(f"Q{i}: {q['question']}")
                answer = st.radio("Answer", q["options"], key=f"quiz_{i}")
                if answer == q["answer"]:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong – correct: {q['answer']}")
    else:
        st.info("Transcribe first.")

with tab_export:
    st.header("5️⃣ Export")
    if st.session_state.study_guide:
        txt = export_text(st.session_state.study_guide, "study_guide.txt")
        st.download_button("Download Study Guide", txt, "study_guide.txt")
    if st.session_state.quiz:
        json_data = export_json(st.session_state.quiz, "quiz.json")
        st.download_button("Download Quiz", json_data, "quiz.json")
