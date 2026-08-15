# Scaffolding: Project Structure

## Project Directory Layout

```
voice-notes-to-flashcards/
│
├── app.py                          # Main Streamlit app entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml               # API keys (add to .gitignore)
│
├── src/                           # Core application logic
│   ├── __init__.py
│   ├── audio_processor.py         # Audio input & file handling
│   ├── transcriber.py             # Gemini audio transcription
│   ├── study_guide_generator.py   # Study guide creation logic
│   ├── quiz_generator.py          # MCQ quiz generation logic
│   └── exporter.py                # Export to TXT/JSON/PDF
│
├── prompts/                       # Prompt templates (separated for easy editing)
│   ├── system_prompts.py          # System-level prompts
│   ├── study_guide_prompt.txt     # Study guide template
│   └── quiz_prompt.txt            # Quiz generation template
│
├── utils/                         # Utility functions
│   ├── __init__.py
│   ├── constants.py               # Constants (file sizes, API limits)
│   ├── validators.py              # Input validation
│   ├── logger.py                  # Logging setup
│   └── session_manager.py         # Streamlit session state helpers
│
├── tests/                         # Unit tests
│   ├── test_transcriber.py
│   ├── test_generators.py
│   └── test_exporter.py
│
├── docs/                          # Documentation
│   ├── SYSTEM_DESIGN.md          # Architecture diagram
│   ├── PROMPT_ENGINEERING.md     # Detailed prompt strategies
│   ├── API_SETUP.md              # Gemini API configuration
│   └── DEPLOYMENT.md             # Streamlit Cloud guide
│
├── assets/                        # Static files
│   ├── icons/
│   ├── sample_audio.wav          # Test audio file
│   └── logo.png
│
├── .github/
│   └── workflows/                # CI/CD if needed
│
├── .gitignore                    # Git ignore file
├── README.md                     # Public-facing documentation
├── review.md                     # Code review trail
├── FLOW_OF_EXECUTION.md         # Execution flow diagram
│
└── .env.example                 # Example environment variables
```

---

## Core Module Descriptions

### 1. `app.py` (Main Streamlit App)
**Purpose:** Entry point, UI layout, state management

**Structure:**
```python
import streamlit as st
from src.audio_processor import AudioProcessor
from src.transcriber import Transcriber
from src.study_guide_generator import StudyGuideGenerator
from src.quiz_generator import QuizGenerator
from src.exporter import Exporter
from utils.session_manager import init_session_state

# Initialize session state
init_session_state()

# Page config
st.set_page_config(page_title="Voice-Notes to Flashcards", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    # API key, processing options, etc.

# Main UI: 5 Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎤 Input", 
    "📝 Transcript", 
    "📚 Study Guide", 
    "❓ Quiz", 
    "💾 Export"
])

# Tab 1: Audio Input
with tab1:
    # Audio upload logic
    pass

# Tab 2: Transcript Display
with tab2:
    # Show transcript
    pass

# Tab 3: Study Guide
with tab3:
    # Show study guide
    pass

# Tab 4: Quiz
with tab4:
    # Interactive quiz
    pass

# Tab 5: Export
with tab5:
    # Download buttons
    pass
```

---

### 2. `src/audio_processor.py`
**Purpose:** Handle audio input, validation, and file management

**Key Functions:**
```python
class AudioProcessor:
    def __init__(self):
        self.max_file_size = 25 * 1024 * 1024  # 25MB
        self.supported_formats = ['wav', 'mp3', 'm4a', 'ogg']
    
    def record_audio(self):
        """Record audio via st.audio_input()"""
        pass
    
    def upload_audio(self):
        """Handle file upload via st.file_uploader()"""
        pass
    
    def validate_audio(self, audio_file):
        """Validate file format and size"""
        pass
    
    def get_audio_metadata(self, audio_file):
        """Extract duration, format, etc."""
        pass
```

---

### 3. `src/transcriber.py`
**Purpose:** Interface with Gemini API for audio transcription

**Key Functions:**
```python
class Transcriber:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-flash-audio"
    
    def transcribe_audio(self, audio_file) -> str:
        """
        Convert audio to text using Gemini API
        
        Returns:
            str: Transcribed text
        """
        pass
    
    def transcribe_with_retry(self, audio_file, max_retries=3):
        """Transcribe with exponential backoff"""
        pass
```

---

### 4. `src/study_guide_generator.py`
**Purpose:** Generate structured study guide from transcript

**Key Functions:**
```python
class StudyGuideGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-flash"  # Text model
    
    def generate_study_guide(self, transcript: str) -> str:
        """
        Generate markdown study guide
        
        Returns:
            str: Markdown formatted study guide
        """
        prompt = self._build_prompt(transcript)
        response = self.client.generate_content(prompt)
        return response.text
    
    def _build_prompt(self, transcript: str) -> str:
        """Build dynamic prompt with transcript"""
        # Use prompt template from prompts/study_guide_prompt.txt
        pass
```

---

### 5. `src/quiz_generator.py`
**Purpose:** Generate MCQ quiz questions as JSON

**Key Functions:**
```python
class QuizGenerator:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-1.5-flash"
    
    def generate_quiz(self, transcript: str) -> dict:
        """
        Generate 5 MCQ questions as JSON
        
        Returns:
            dict: Quiz with questions, options, answers
        """
        prompt = self._build_prompt(transcript)
        response = self.client.generate_content(prompt)
        quiz_json = self._parse_json(response.text)
        return quiz_json
    
    def _parse_json(self, text: str) -> dict:
        """Safely parse JSON from LLM response"""
        pass
```

---

### 6. `src/exporter.py`
**Purpose:** Export study materials in TXT/JSON formats

**Key Functions:**
```python
class Exporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def export_transcript_txt(self, transcript: str, filename: str) -> bytes:
        """Export transcript as .txt"""
        pass
    
    def export_study_guide_txt(self, study_guide: str, filename: str) -> bytes:
        """Export study guide as .txt"""
        pass
    
    def export_quiz_json(self, quiz: dict, filename: str) -> bytes:
        """Export quiz as .json"""
        pass
    
    def export_combined_txt(self, transcript: str, study_guide: str, quiz: dict) -> bytes:
        """Export all 3 combined in single .txt"""
        pass
```

---

### 7. `utils/session_manager.py`
**Purpose:** Manage Streamlit session state

**Key Functions:**
```python
def init_session_state():
    """Initialize all session state variables"""
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""
    if "study_guide" not in st.session_state:
        st.session_state.study_guide = ""
    if "quiz" not in st.session_state:
        st.session_state.quiz = {}

def set_transcript(transcript: str):
    """Thread-safe transcript setter"""
    st.session_state.transcript = transcript

def get_transcript() -> str:
    """Thread-safe transcript getter"""
    return st.session_state.get("transcript", "")
```

---

### 8. `utils/validators.py`
**Purpose:** Input validation and error handling

**Key Functions:**
```python
def validate_file_size(file, max_size_mb=25) -> bool:
    """Check file doesn't exceed size limit"""
    pass

def validate_audio_format(filename: str) -> bool:
    """Check file extension is supported"""
    pass

def validate_transcript_not_empty(transcript: str) -> bool:
    """Ensure transcript has content"""
    pass

def validate_json_quiz(quiz_dict: dict) -> bool:
    """Ensure quiz JSON is well-formed"""
    pass
```

---

## Configuration Files

### `requirements.txt`
```
streamlit==1.37.0
google-generativeai==0.3.0
python-dotenv==1.0.0
pandas==2.0.0
```

### `.streamlit/secrets.toml`
```toml
GEMINI_API_KEY = "your-api-key-here"
APP_ENV = "production"
```

### `.env.example`
```
GEMINI_API_KEY=your_api_key_here
STREAMLIT_SERVER_PORT=8501
```

### `.gitignore`
```
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
```

---

## Prompt Templates Structure

### `prompts/study_guide_prompt.txt`
```
You are an expert study guide creator. Given a lecture transcript, generate a comprehensive study guide.

# Transcript:
{TRANSCRIPT}

# Output Format (markdown):
## Key Concepts
- ...

## Main Topics
### Topic 1
...

## Summary
...

## Formulas/Definitions
...

## Real-World Applications
- ...
```

### `prompts/quiz_prompt.txt`
```
You are a quiz master. Generate 5 multiple-choice questions from this transcript.

# Transcript:
{TRANSCRIPT}

# Output Format (JSON only, no markdown):
{{
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}
```

---

## Data Flow Architecture

```
┌─────────────────────┐
│   User Input        │
│  (Audio/Upload)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Audio Processor     │
│ (Validate + Store)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Transcriber        │
│ (Gemini Audio API)  │
└──────────┬──────────┘
           │
           ▼
   ┌───────┴────────┐
   │                │
   ▼                ▼
┌─────────────┐ ┌──────────────┐
│ Study Guide │ │ Quiz         │
│ Generator   │ │ Generator    │
└──────┬──────┘ └────────┬─────┘
       │                │
       └────────┬───────┘
              │
              ▼
        ┌─────────────┐
        │  Exporter   │
        │ (TXT/JSON)  │
        └─────────────┘
              │
              ▼
        ┌─────────────┐
        │  Download   │
        │  Button UI  │
        └─────────────┘
```

---

## Testing Structure

### `tests/test_transcriber.py`
```python
def test_transcriber_with_sample_audio():
    """Test transcription with sample_audio.wav"""
    pass

def test_api_error_handling():
    """Test retry logic on API failure"""
    pass
```

### `tests/test_generators.py`
```python
def test_study_guide_generation():
    """Test study guide markdown output"""
    pass

def test_quiz_json_parsing():
    """Test quiz JSON is valid"""
    pass
```

---

## Next Document: FLOW_OF_EXECUTION.md

This scaffolding defines all files, their purpose, and dependencies. Use this as your reference when building each module.
