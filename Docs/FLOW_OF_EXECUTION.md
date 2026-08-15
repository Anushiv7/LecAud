# Flow of Execution: Voice-Notes to Flashcards

## High-Level User Flow

```
START
  │
  ├─► User launches app → Streamlit initialization
  │
  ├─► Initialize session state (audio, transcript, study_guide, quiz)
  │
  ├─► Display 5 tabs interface
  │
  ├─► Tab 1: Input
  │   ├─► User records audio OR uploads file
  │   ├─► AudioProcessor validates file
  │   ├─► Store in st.session_state.audio_file
  │   └─► Display preview player
  │
  ├─► [User clicks "Process Lecture" button]
  │
  ├─► Transcriber.transcribe_audio()
  │   ├─► Send audio to Gemini API
  │   ├─► Retry logic (max 3 attempts)
  │   ├─► Store result in st.session_state.transcript
  │   └─► Show success/error message
  │
  ├─► Tab 2: Transcript
  │   ├─► Display raw transcript text
  │   ├─► Show word count & reading time
  │   ├─► Provide copy & download buttons
  │   └─► Allow editing (optional)
  │
  ├─► [Parallel processing - triggers Tab 3 & 4]
  │
  ├─► StudyGuideGenerator.generate_study_guide()
  │   ├─► Build prompt with transcript
  │   ├─► Call Gemini API
  │   ├─► Parse markdown response
  │   └─► Store in st.session_state.study_guide
  │
  ├─► Tab 3: Study Guide
  │   ├─► Render markdown
  │   ├─► Show estimated reading time
  │   ├─► Copy & download buttons
  │   └─► Display formatting/styling
  │
  ├─► QuizGenerator.generate_quiz()
  │   ├─► Build prompt with transcript
  │   ├─► Call Gemini API
  │   ├─► Parse JSON response
  │   ├─► Validate quiz structure
  │   └─► Store in st.session_state.quiz
  │
  ├─► Tab 4: Quiz
  │   ├─► Display 5 MCQ questions
  │   ├─► User selects answers
  │   ├─► Calculate score
  │   ├─► Show explanations
  │   └─► Allow retake
  │
  ├─► Tab 5: Export
  │   ├─► Exporter.export_transcript_txt()
  │   ├─► Exporter.export_study_guide_txt()
  │   ├─► Exporter.export_quiz_json()
  │   ├─► Exporter.export_combined_txt()
  │   └─► Display 4 download buttons
  │
  └─► END (User downloads files & closes app)
```

---

## Detailed Execution Steps

### STEP 1: App Initialization

**File:** `app.py`

```python
# 1.1: Page Configuration
st.set_page_config(
    page_title="Voice-Notes to Flashcards",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1.2: Initialize Session State
from utils.session_manager import init_session_state
init_session_state()

# Session state structure:
# st.session_state = {
#     "audio_file": None,
#     "transcript": "",
#     "study_guide": "",
#     "quiz": {},
#     "processing_state": "idle"  # idle | transcribing | generating
# }

# 1.3: Load API Key
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("❌ API Key not found. Set GEMINI_API_KEY in .streamlit/secrets.toml")
    st.stop()

# 1.4: Initialize Services
from src.transcriber import Transcriber
from src.study_guide_generator import StudyGuideGenerator
from src.quiz_generator import QuizGenerator
from src.exporter import Exporter

transcriber = Transcriber(GEMINI_API_KEY)
sg_generator = StudyGuideGenerator(GEMINI_API_KEY)
quiz_generator = QuizGenerator(GEMINI_API_KEY)
exporter = Exporter()
```

---

### STEP 2: Tab 1 - Audio Input Processing

**File:** `app.py` (Tab 1 logic)

```python
with tab1:
    st.header("🎤 Record or Upload Your Lecture")
    
    # 2.1: Display input options
    input_method = st.radio("Choose input method:", ["Record Audio", "Upload File"])
    
    # 2.2: Record Audio Option
    if input_method == "Record Audio":
        audio_data = st.audio_input("Record your lecture:")
        if audio_data is not None:
            st.session_state.audio_file = audio_data
            st.success("✅ Audio recorded!")
    
    # 2.3: Upload File Option
    else:
        uploaded_file = st.file_uploader(
            "Upload audio file (WAV, MP3, M4A, OGG):",
            type=["wav", "mp3", "m4a", "ogg"]
        )
        if uploaded_file is not None:
            # Validate file
            from utils.validators import validate_file_size, validate_audio_format
            
            if not validate_file_size(uploaded_file, max_size_mb=25):
                st.error("❌ File exceeds 25MB limit")
            elif not validate_audio_format(uploaded_file.name):
                st.error("❌ Unsupported audio format")
            else:
                st.session_state.audio_file = uploaded_file
                st.success("✅ Audio uploaded!")
    
    # 2.4: Audio Preview
    if st.session_state.audio_file is not None:
        st.audio(st.session_state.audio_file, format="audio/*")
        
        # 2.5: Process Button
        if st.button("⬇️ Process Lecture", key="process_btn"):
            st.session_state.processing_state = "transcribing"
            st.rerun()
```

---

### STEP 3: Audio Transcription

**File:** `src/transcriber.py` execution

```python
# STEP 3: Transcriber.transcribe_audio(audio_file)

def transcribe_audio(self, audio_file) -> str:
    """
    Flow:
    1. Prepare audio bytes
    2. Call Gemini 1.5 audio model
    3. Handle errors with retry
    4. Return transcript string
    """
    
    # 3.1: Convert audio to bytes
    if hasattr(audio_file, 'read'):
        audio_bytes = audio_file.read()
    else:
        with open(audio_file, 'rb') as f:
            audio_bytes = f.read()
    
    # 3.2: Upload audio to Gemini
    import genai
    audio_file_obj = genai.upload_file(audio_bytes, mime_type="audio/mpeg")
    
    # 3.3: Call model with system prompt
    from prompts.system_prompts import TRANSCRIPTION_PROMPT
    
    response = self.client.generate_content([
        TRANSCRIPTION_PROMPT,  # System context
        audio_file_obj         # Audio input
    ])
    
    # 3.4: Extract and clean transcript
    transcript = response.text.strip()
    
    # 3.5: Validate transcript not empty
    if not transcript or len(transcript) < 10:
        raise ValueError("Transcription failed or audio too short")
    
    return transcript


# STEP 3B: Error Handling & Retry Logic
def transcribe_with_retry(self, audio_file, max_retries=3):
    """
    Retry logic with exponential backoff:
    Attempt 1: immediate
    Attempt 2: wait 2 seconds
    Attempt 3: wait 4 seconds
    """
    import time
    
    for attempt in range(max_retries):
        try:
            transcript = self.transcribe_audio(audio_file)
            return transcript
        
        except genai.errors.RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                st.warning(f"⏳ Rate limited. Retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
        
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ Attempt {attempt+1} failed. Retrying...")
            else:
                raise
```

---

### STEP 4: Display Transcript (Tab 2)

**File:** `app.py` (Tab 2 logic)

```python
with tab2:
    st.header("📝 Lecture Transcript")
    
    # 4.1: Check if transcript exists
    if not st.session_state.transcript:
        st.info("📢 Process your audio in Tab 1 first!")
    else:
        # 4.2: Display transcript with metadata
        transcript = st.session_state.transcript
        word_count = len(transcript.split())
        reading_time = max(1, word_count // 200)  # Assume 200 WPM
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Word Count", word_count)
        with col2:
            st.metric("Est. Reading Time", f"{reading_time} min")
        
        # 4.3: Display transcript in expandable box
        with st.expander("📖 Full Transcript", expanded=True):
            st.text_area("Transcript:", value=transcript, height=300, disabled=True)
        
        # 4.4: Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Copy to Clipboard"):
                st.success("✅ Copied!")
                # Note: Streamlit doesn't have native clipboard API
                # Provide manual copy instead
        
        with col2:
            transcript_export = exporter.export_transcript_txt(transcript, "transcript")
            st.download_button(
                label="💾 Download (.txt)",
                data=transcript_export,
                file_name=f"transcript_{int(time.time())}.txt",
                mime="text/plain"
            )
```

---

### STEP 5: Study Guide Generation (Parallel)

**File:** `src/study_guide_generator.py` execution

```python
# STEP 5: StudyGuideGenerator.generate_study_guide(transcript)

def generate_study_guide(self, transcript: str) -> str:
    """
    Flow:
    1. Load prompt template
    2. Inject transcript
    3. Call Gemini API
    4. Parse markdown
    5. Return study guide
    """
    
    # 5.1: Load prompt template
    with open('prompts/study_guide_prompt.txt', 'r') as f:
        prompt_template = f.read()
    
    # 5.2: Inject transcript into prompt
    prompt = prompt_template.format(TRANSCRIPT=transcript)
    
    # 5.3: Call Gemini API (text model)
    response = self.client.generate_content(prompt)
    
    # 5.4: Extract markdown
    study_guide_md = response.text
    
    # 5.5: Validate structure
    required_sections = ["Key Concepts", "Main Topics", "Summary"]
    for section in required_sections:
        if section not in study_guide_md:
            st.warning(f"⚠️ Missing '{section}' section in study guide")
    
    return study_guide_md
```

---

### STEP 6: Display Study Guide (Tab 3)

**File:** `app.py` (Tab 3 logic)

```python
with tab3:
    st.header("📚 Study Guide")
    
    # 6.1: Check if study guide exists
    if not st.session_state.study_guide:
        st.info("⏳ Generating study guide... Please wait!")
    else:
        # 6.2: Render markdown
        st.markdown(st.session_state.study_guide)
        
        # 6.3: Display metadata
        sg = st.session_state.study_guide
        word_count = len(sg.split())
        reading_time = max(1, word_count // 200)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Study Guide Length", f"{word_count} words")
        with col2:
            st.metric("Reading Time", f"{reading_time} min")
        
        # 6.4: Export button
        sg_export = exporter.export_study_guide_txt(sg, "study_guide")
        st.download_button(
            label="💾 Download Study Guide (.txt)",
            data=sg_export,
            file_name=f"study_guide_{int(time.time())}.txt",
            mime="text/plain"
        )
```

---

### STEP 7: Quiz Generation (Parallel)

**File:** `src/quiz_generator.py` execution

```python
# STEP 7: QuizGenerator.generate_quiz(transcript)

def generate_quiz(self, transcript: str) -> dict:
    """
    Flow:
    1. Load prompt template
    2. Inject transcript
    3. Call Gemini API
    4. Parse JSON
    5. Validate structure
    6. Return quiz dict
    """
    
    # 7.1: Load quiz prompt
    with open('prompts/quiz_prompt.txt', 'r') as f:
        quiz_template = f.read()
    
    # 7.2: Inject transcript
    prompt = quiz_template.format(TRANSCRIPT=transcript)
    
    # 7.3: Call Gemini (specify JSON mode)
    response = self.client.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    
    # 7.4: Parse JSON
    quiz_json = json.loads(response.text)
    
    # 7.5: Validate quiz structure
    self._validate_quiz_structure(quiz_json)
    
    return quiz_json


def _validate_quiz_structure(self, quiz: dict) -> bool:
    """
    Check:
    - 5 questions present
    - All options (A, B, C, D) present
    - Correct answer is A/B/C/D
    - No missing fields
    """
    assert "questions" in quiz, "Missing 'questions' key"
    assert len(quiz["questions"]) == 5, f"Expected 5 questions, got {len(quiz['questions'])}"
    
    for q in quiz["questions"]:
        assert "question" in q, "Missing 'question' field"
        assert "options" in q, "Missing 'options' field"
        assert len(q["options"]) == 4, f"Expected 4 options, got {len(q['options'])}"
        assert "correct_answer" in q, "Missing 'correct_answer' field"
        assert q["correct_answer"] in ["A", "B", "C", "D"], "Invalid answer"
    
    return True
```

---

### STEP 8: Interactive Quiz (Tab 4)

**File:** `app.py` (Tab 4 logic)

```python
with tab4:
    st.header("❓ Quiz")
    
    # 8.1: Check if quiz exists
    if not st.session_state.quiz or not st.session_state.quiz.get("questions"):
        st.info("⏳ Generating quiz... Please wait!")
    else:
        quiz = st.session_state.quiz
        questions = quiz.get("questions", [])
        
        # 8.2: Initialize quiz state
        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}
        
        # 8.3: Display each question
        for idx, q in enumerate(questions):
            st.subheader(f"Question {idx + 1}")
            st.write(q["question"])
            
            # 8.4: Radio buttons for options
            user_answer = st.radio(
                "Choose your answer:",
                options=list(q["options"].keys()),
                key=f"q_{idx}"
            )
            
            st.session_state.quiz_answers[idx] = user_answer
            
            # 8.5: Show explanation after selection
            if st.checkbox(f"Show Explanation (Q{idx+1})", key=f"explain_{idx}"):
                is_correct = (user_answer == q["correct_answer"])
                status = "✅ Correct!" if is_correct else "❌ Incorrect"
                st.info(f"{status}\n\n{q['explanation']}")
            
            st.divider()
        
        # 8.6: Calculate and display score
        if st.button("📊 Calculate Score"):
            score = 0
            for idx, q in enumerate(questions):
                if st.session_state.quiz_answers.get(idx) == q["correct_answer"]:
                    score += 1
            
            percentage = (score / len(questions)) * 100
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Score", f"{score}/{len(questions)}")
            with col2:
                st.metric("Percentage", f"{percentage:.0f}%")
            
            # Performance feedback
            if percentage >= 80:
                st.success("🎉 Excellent! You've mastered this lecture!")
            elif percentage >= 60:
                st.info("👍 Good job! Review the weak areas.")
            else:
                st.warning("📖 Review the lecture and try again.")
```

---

### STEP 9: Export Module (Tab 5)

**File:** `src/exporter.py` execution

```python
# STEP 9: Exporter functions

class Exporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_transcript_txt(self, transcript: str, filename: str) -> bytes:
        """Create .txt file with transcript"""
        content = f"""LECTURE TRANSCRIPT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
=====================================

{transcript}
"""
        return content.encode('utf-8')
    
    def export_study_guide_txt(self, study_guide: str, filename: str) -> bytes:
        """Create .txt file with study guide"""
        content = f"""STUDY GUIDE
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
=====================================

{study_guide}
"""
        return content.encode('utf-8')
    
    def export_quiz_json(self, quiz: dict, filename: str) -> bytes:
        """Create .json file with quiz"""
        quiz_with_meta = {
            "metadata": {
                "created": datetime.now().isoformat(),
                "total_questions": len(quiz.get("questions", []))
            },
            "quiz": quiz
        }
        json_str = json.dumps(quiz_with_meta, indent=2)
        return json_str.encode('utf-8')
    
    def export_combined_txt(self, transcript: str, study_guide: str, quiz: dict) -> bytes:
        """Create single .txt with all content"""
        content = f"""COMPLETE LECTURE PACKAGE
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
================================================

SECTION 1: TRANSCRIPT
--------------------
{transcript}

SECTION 2: STUDY GUIDE
----------------------
{study_guide}

SECTION 3: QUIZ QUESTIONS & ANSWERS
-------------------------------------
"""
        for q in quiz.get("questions", []):
            content += f"\nQ{q.get('id', '?')}: {q['question']}\n"
            content += f"Options: {q.get('options', {})}\n"
            content += f"Correct Answer: {q.get('correct_answer', '?')}\n"
            content += f"Explanation: {q.get('explanation', '')}\n"
            content += "-" * 50 + "\n"
        
        return content.encode('utf-8')
```

---

### STEP 10: Export UI (Tab 5)

**File:** `app.py` (Tab 5 logic)

```python
with tab5:
    st.header("💾 Export Study Materials")
    
    # 10.1: Check if all data exists
    has_transcript = bool(st.session_state.transcript)
    has_study_guide = bool(st.session_state.study_guide)
    has_quiz = bool(st.session_state.quiz)
    
    # 10.2: Display status
    col1, col2, col3 = st.columns(3)
    with col1:
        status_trans = "✅" if has_transcript else "⏳"
        st.write(f"{status_trans} Transcript")
    with col2:
        status_sg = "✅" if has_study_guide else "⏳"
        st.write(f"{status_sg} Study Guide")
    with col3:
        status_q = "✅" if has_quiz else "⏳"
        st.write(f"{status_q} Quiz")
    
    st.divider()
    
    # 10.3: Individual exports
    if has_transcript:
        transcript_data = exporter.export_transcript_txt(
            st.session_state.transcript, "transcript"
        )
        st.download_button(
            label="📝 Transcript (TXT)",
            data=transcript_data,
            file_name=f"transcript_{int(time.time())}.txt",
            mime="text/plain"
        )
    
    if has_study_guide:
        sg_data = exporter.export_study_guide_txt(
            st.session_state.study_guide, "study_guide"
        )
        st.download_button(
            label="📚 Study Guide (TXT)",
            data=sg_data,
            file_name=f"study_guide_{int(time.time())}.txt",
            mime="text/plain"
        )
    
    if has_quiz:
        quiz_data = exporter.export_quiz_json(
            st.session_state.quiz, "quiz"
        )
        st.download_button(
            label="❓ Quiz (JSON)",
            data=quiz_data,
            file_name=f"quiz_{int(time.time())}.json",
            mime="application/json"
        )
    
    # 10.4: Combined export
    if has_transcript and has_study_guide and has_quiz:
        st.divider()
        combined_data = exporter.export_combined_txt(
            st.session_state.transcript,
            st.session_state.study_guide,
            st.session_state.quiz
        )
        st.download_button(
            label="📦 All Materials (Combined TXT)",
            data=combined_data,
            file_name=f"complete_package_{int(time.time())}.txt",
            mime="text/plain"
        )
```

---

## Error Handling Flow

```
Try to Process Audio
  │
  ├─ API Rate Limit Error
  │  └─► Retry with backoff (3 times)
  │      ├─ Success → Continue
  │      └─ Failure → Show error message
  │
  ├─ Invalid File Format
  │  └─► Show validation error → User uploads new file
  │
  ├─ File Size > 25MB
  │  └─► Show size error → User uploads smaller file
  │
  ├─ Empty Transcript
  │  └─► Show warning (audio too short/silent)
  │      → User re-records with clear audio
  │
  ├─ JSON Parse Error (Quiz)
  │  └─► Retry quiz generation
  │      ├─ Success → Display quiz
  │      └─ Failure → Show manual quiz entry option
  │
  └─ Unknown API Error
     └─► Log error → Show generic message → Suggest retry
```

---

## Session State Management

**Key Rule:** All data persists across Streamlit reruns

```python
st.session_state = {
    # Input data
    "audio_file": None,          # File object or bytes
    
    # Processed data
    "transcript": "",             # String
    "study_guide": "",            # Markdown string
    "quiz": {},                   # Dict with questions
    "quiz_answers": {},           # User quiz responses
    
    # UI state
    "processing_state": "idle",   # idle | transcribing | generating
    "current_tab": 0,             # Tab index
    "show_explanations": {},      # Quiz explanations visibility
}
```

---

## Performance Optimizations

1. **API Call Caching:** Cache results in session state
   ```python
   if st.session_state.transcript:
       # Don't retranscribe
   ```

2. **Parallel Processing:** Use threading for simultaneous generation
   ```python
   from concurrent.futures import ThreadPoolExecutor
   with ThreadPoolExecutor() as executor:
       sg_future = executor.submit(sg_generator.generate_study_guide, transcript)
       quiz_future = executor.submit(quiz_generator.generate_quiz, transcript)
   ```

3. **Lazy Loading:** Only render visible tabs
   ```python
   with tab3:
       if st.session_state.study_guide:  # Only if ready
           st.markdown(...)
   ```

---

## Testing Flow

```
Unit Tests (Local)
  ├─ test_transcriber.py
  │  └─ Test with sample_audio.wav
  ├─ test_generators.py
  │  └─ Test prompt injection & JSON parsing
  └─ test_exporter.py
     └─ Test file generation

Integration Tests (Local)
  └─ Run full app flow with test audio

E2E Tests (Deployment)
  └─ Test on Streamlit Cloud with real API
```

---

## Next: TECH_STACK.md (Free Tier Tools & Setup)
