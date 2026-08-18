import streamlit as st
import os
import json
import time

# 1. Import CLASSES not functions
from src.audio_processor import AudioProcessor
from src.transcriber import Transcriber
from src.study_guide_generator import StudyGuideGenerator
from src.quiz_generator import QuizGenerator
from src.exporter import Exporter
from utils.config import get_gemini_key, Config

# Page configuration
st.set_page_config(
    page_title="LecAud - Audio to Flashcards",
    page_icon="🎙️",
    layout="wide"
)

# Initialize Session State
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'study_guide' not in st.session_state:
    st.session_state.study_guide = None
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

# Sidebar Configuration
with st.sidebar:
    st.title("🎙️ LecAud")
    st.markdown("Transform lecture audio into study-ready material.")
    st.divider()
    
    st.subheader("Status")
    st.markdown(f"**Audio Uploaded:** {'✅' if st.session_state.audio_file else '❌'}")
    st.markdown(f"**Transcript:** {'✅' if st.session_state.transcript else '❌'}")
    st.markdown(f"**Study Guide:** {'✅' if st.session_state.study_guide else '❌'}")
    st.markdown(f"**Quiz:** {'✅' if st.session_state.quiz else '❌'}")
    
    st.divider()
    api_key = get_gemini_key()
    if not api_key:
        st.error("Gemini API Key missing! Check configuration.")
    else:
        st.success("API Key found.")

st.title("LecAud - Lecture Audio to Flashcards")

# Create 5 tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎙️ 1. Input", 
    "📝 2. Transcript", 
    "📚 3. Study Guide", 
    "❓ 4. Quiz", 
    "💾 5. Export"
])

# ==========================================
# TAB 1: Input (Audio Upload & Processing)
# ==========================================
with tab1:
    st.header("Upload Lecture Audio")
    st.info("Upload a lecture recording to begin the process.")
    
    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a', 'ogg'])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format='audio/wav')
        
        if st.button("Process Audio", type="primary"):
            if not api_key:
                st.error("Please configure your Gemini API Key first.")
            else:
                try:
                    st.session_state.audio_file = uploaded_file.name
                    
                    with st.spinner("Validating audio..."):
                        audio_processor = AudioProcessor()
                        try:
                            is_valid = audio_processor.validate_audio_file(uploaded_file)
                        except ValueError as ve:
                            st.error(str(ve))
                            is_valid = False
                            
                        if is_valid:
                            with st.spinner("Transcribing audio (this may take a minute)..."):
                                transcriber = Transcriber(api_key=api_key)
                                try:
                                    transcript = transcriber.transcribe_audio(uploaded_file)
                                    st.session_state.transcript = transcript
                                    st.success("Transcription complete! Move to the next tab.")
                                except ValueError as ve:
                                    st.error(f"Transcription failed: {str(ve)}")
                except Exception as e:
                    st.error(f"An error occurred during audio processing: {str(e)}")

# ==========================================
# TAB 2: Transcript
# ==========================================
with tab2:
    st.header("Lecture Transcript")
    
    if st.session_state.transcript:
        word_count = len(st.session_state.transcript.split())
        reading_time = max(1, word_count // 200) # Avg 200 words per minute
        
        col1, col2 = st.columns(2)
        col1.metric("Word Count", word_count)
        col2.metric("Estimated Reading Time", f"{reading_time} min")
        
        st.text_area("Transcript text", st.session_state.transcript, height=400)
    else:
        st.warning("No transcript available. Please process an audio file in Tab 1.")

# ==========================================
# TAB 3: Study Guide
# ==========================================
with tab3:
    st.header("Study Guide")
    
    if st.session_state.transcript:
        if st.button("Generate Study Guide", type="primary"):
            try:
                with st.spinner("Analyzing transcript and generating study guide..."):
                    guide_generator = StudyGuideGenerator(api_key=api_key)
                    guide = guide_generator.generate_study_guide(st.session_state.transcript)
                    
                    if guide:
                        st.session_state.study_guide = guide
                        st.success("Study guide generated successfully!")
                    else:
                        st.error("Failed to generate study guide.")
            except Exception as e:
                st.error(f"An error occurred generating the study guide: {str(e)}")
        
        if st.session_state.study_guide:
            st.divider()
            st.markdown(st.session_state.study_guide)
            
            # Simple download button for study guide
            st.download_button(
                label="Download Study Guide (MD)",
                data=st.session_state.study_guide,
                file_name="study_guide.md",
                mime="text/markdown"
            )
    else:
        st.warning("Need a transcript to generate a study guide. Please complete Tab 1.")

# ==========================================
# TAB 4: Quiz
# ==========================================
with tab4:
    st.header("Interactive Quiz")
    
    if st.session_state.transcript:
        if st.button("Generate Quiz", type="primary"):
            try:
                with st.spinner("Crafting 5 questions from the lecture..."):
                    quiz_gen = QuizGenerator(api_key=api_key)
                    quiz_data = quiz_gen.generate_quiz(st.session_state.transcript)
                    
                    if quiz_data:
                        st.session_state.quiz = quiz_data
                        st.session_state.quiz_answers = {} # reset answers
                        st.success("Quiz generated successfully!")
                    else:
                        st.error("Failed to generate quiz.")
            except Exception as e:
                st.error(f"An error occurred generating the quiz: {str(e)}")
        
        if st.session_state.quiz:
            st.divider()
            # Assuming quiz_data is a dict with a 'questions' list
            questions = st.session_state.quiz.get('questions', [])
            
            if not questions:
                st.error("Quiz data format was invalid.")
            else:
                score = 0
                for i, q in enumerate(questions):
                    st.subheader(f"Q{i+1}: {q.get('question', 'Question text missing')}")
                    
                    options = q.get('options', [])
                    selected = st.radio(
                        "Select an answer:",
                        options,
                        key=f"q_{i}",
                        index=None
                    )
                    
                    if selected:
                        st.session_state.quiz_answers[i] = selected
                        
                if st.button("Submit Answers"):
                    for i, q in enumerate(questions):
                        options = q.get('options', [])
                        correct_idx = q.get('correct_index', 0)
                        correct_answer = options[correct_idx] if correct_idx < len(options) else None
                        
                        user_answer = st.session_state.quiz_answers.get(i)
                        
                        if user_answer == correct_answer:
                            score += 1
                            st.success(f"**Q{i+1}: Correct!** {q.get('explanation', '')}")
                        else:
                            st.error(f"**Q{i+1}: Incorrect.** Correct answer was: {correct_answer}. {q.get('explanation', '')}")
                            
                    st.metric("Final Score", f"{score} / {len(questions)}")
                    if score == len(questions):
                        st.balloons()
    else:
        st.warning("Need a transcript to generate a quiz. Please complete Tab 1.")

# ==========================================
# TAB 5: Export
# ==========================================
with tab5:
    st.header("Export Materials")
    st.info("Download all your generated study materials.")
    
    exporter = Exporter()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Individual Exports")
        if st.session_state.transcript:
            st.download_button(
                label="Download Transcript (TXT)",
                data=st.session_state.transcript,
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True
            )
        if st.session_state.study_guide:
            st.download_button(
                label="Download Study Guide (MD)",
                data=st.session_state.study_guide,
                file_name="study_guide.md",
                mime="text/markdown",
                use_container_width=True
            )
        if st.session_state.quiz:
            quiz_json = json.dumps(st.session_state.quiz, indent=2)
            st.download_button(
                label="Download Quiz (JSON)",
                data=quiz_json,
                file_name="quiz.json",
                mime="application/json",
                use_container_width=True
            )
            
    with col2:
        st.subheader("Combined Package")
        if st.session_state.transcript and st.session_state.study_guide:
            try:
                combined_content = f"# LecAud Export\n\n## Transcript\n\n{st.session_state.transcript}\n\n{st.session_state.study_guide}"
                if st.session_state.quiz:
                    combined_content += f"\n\n## Quiz JSON\n\n```json\n{json.dumps(st.session_state.quiz, indent=2)}\n```"
                
                st.download_button(
                    label="Download All-in-One (MD)",
                    data=combined_content,
                    file_name="lecaud_full_export.md",
                    mime="text/markdown",
                    type="primary",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Could not generate combined package: {str(e)}")
        else:
            st.warning("Generate both a transcript and study guide to download the combined package.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Made with ❤️ by Anushiv Prakash | MirAI School of Technology Virtual Summer Internship 2026</div>", unsafe_allow_html=True)
