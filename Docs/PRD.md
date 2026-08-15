# PRD: Voice-Notes to Flashcards

**Project:** Voice-Notes to Flashcards (Capstone AI Streamlit App)  
**Developer:** Anushiv Prakash  
**Timeline:** Aug 11-25, 2026 (14 days)  
**Deployment Target:** Streamlit Community Cloud  
**Tech Stack:** Streamlit + Gemini API + Python  

---

## 1. Problem Statement

**User Problem:**
Students spend 1-2 hours transcribing chaotic lecture notes into study materials. Handwritten notes are unstructured, and creating flashcards from raw audio is tedious.

**Solution:**
A Streamlit app that:
1. Records/uploads a voice lecture (5-30 mins)
2. Transcribes it via Gemini Audio API
3. Auto-generates a structured study guide
4. Creates 5 MCQ quiz questions with answers
5. Exports everything as `.txt` and `.json`

**User Flow:**
```
User speaks → Audio recorded → Gemini transcribes → Structured output → Export
```

---

## 2. Core Features (MVP)

### Feature 1: Audio Input Module
**Requirement:** Accept audio in 3 ways
- [ ] `st.audio_input()` - Record directly in browser
- [ ] `st.file_uploader()` - Upload `.wav`, `.mp3`, `.m4a`
- [ ] Display audio player for preview

**Constraints:**
- Max file size: 25MB (Gemini limit)
- Supported formats: WAV, MP3, M4A, OGG
- Session state must persist audio across reruns

**Acceptance Criteria:**
- Audio plays in UI ✅
- File size validation works ✅
- No session state loss on interaction ✅

---

### Feature 2: Transcription Engine
**Requirement:** Convert audio → text using Gemini 1.5 API

**Process:**
```
Audio → Gemini API (audio/transcribe model) → Raw Transcript
```

**Prompt Template:**
```
You are a lecture transcription assistant.
Transcribe the following audio accurately.
Preserve all technical terms and timestamps if available.
Output: Plain text, no formatting.
```

**Constraints:**
- API response time: <30 seconds for 30-min audio
- Retry logic (3 attempts) if API fails
- Show loading spinner during processing

**Acceptance Criteria:**
- Transcript accuracy >90% ✅
- Handles long-form audio (30+ mins) ✅
- Error handling for API failures ✅

---

### Feature 3: Study Guide Generator
**Requirement:** Analyze transcript → Generate structured study guide

**Prompt Engineering:**
```
You are an expert study guide creator.
Given a lecture transcript, generate a comprehensive study guide with:
1. **Key Concepts** (3-5 bullet points)
2. **Main Topics** (with brief explanations)
3. **Summary** (200-word synthesis)
4. **Important Formulas/Definitions** (if applicable)
5. **Real-World Applications** (2-3 examples)

Transcript:
{TRANSCRIPT}

Format as markdown with clear sections.
```

**Output Format:**
```markdown
# Study Guide: [Topic]

## Key Concepts
- ...

## Main Topics
### Topic 1
...

## Summary
...
```

**Constraints:**
- Generation time: <15 seconds
- Output length: 500-1000 words
- Structured markdown format

**Acceptance Criteria:**
- Markdown renders correctly in Streamlit ✅
- Content is relevant to transcript ✅
- Proper hierarchy/formatting ✅

---

### Feature 4: Quiz Generator
**Requirement:** Create 5 MCQ questions from transcript

**Prompt Engineering:**
```
You are a quiz master. Based on this lecture transcript, generate 5 multiple-choice questions (MCQ).

For each question:
1. The question
2. 4 options (A, B, C, D)
3. Correct answer with explanation

Transcript:
{TRANSCRIPT}

Format as JSON:
{
  "questions": [
    {
      "id": 1,
      "question": "...",
      "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
      "correct_answer": "A",
      "explanation": "..."
    }
  ]
}
```

**Output Format:**
```json
{
  "questions": [
    {
      "id": 1,
      "question": "...",
      "options": {...},
      "correct_answer": "A",
      "explanation": "..."
    }
  ]
}
```

**Constraints:**
- Questions must be diverse (not repetitive)
- At least 3 difficulty levels represented
- Answers must be factually correct

**Acceptance Criteria:**
- All 5 questions parse as JSON ✅
- Questions are diverse and relevant ✅
- Difficulty varies appropriately ✅

---

### Feature 5: Export Module
**Requirement:** Download study materials in multiple formats

**Export Options:**
1. **Study Guide as .txt** - Plain text, easy sharing
2. **Quiz as .json** - Machine-readable format
3. **Combined .txt** - Both transcript + study guide + quiz

**Constraints:**
- File naming: `{topic}_{timestamp}.{ext}`
- Max file size: <10MB (Streamlit limit)

**Acceptance Criteria:**
- Download button works ✅
- Files contain correct data ✅
- No corrupted files ✅

---

## 3. UI/UX Design

### Layout (3 Tabs)
```
┌─────────────────────────────────────┐
│ 🎤 Voice-Notes to Flashcards       │
├─────────────────────────────────────┤
│ [Tab 1] Input | [Tab 2] Transcript │ [Tab 3] Study Guide | [Tab 4] Quiz | [Tab 5] Export
├─────────────────────────────────────┤
│                                     │
│  Tab 1: Input                       │
│  ┌───────────────────────────────┐  │
│  │ 🎤 Record Audio               │  │
│  │ (or upload file)              │  │
│  │ [Audio Player]                │  │
│  │ ⬇️ [Process Lecture]          │  │
│  └───────────────────────────────┘  │
│                                     │
│  Tab 2: Transcript                  │
│  [Raw transcript text]              │
│  [Copy button] [Export .txt]        │
│                                     │
│  Tab 3: Study Guide                 │
│  [Markdown rendered]                │
│  [Copy] [Export .txt]               │
│                                     │
│  Tab 4: Quiz                        │
│  [Question 1] A/B/C/D               │
│  [Question 2] A/B/C/D               │
│  ...                                │
│                                     │
│  Tab 5: Export All                  │
│  ✅ Study Guide (.txt)              │
│  ✅ Quiz (.json)                    │
│  ✅ Combined (.txt)                 │
│                                     │
└─────────────────────────────────────┘
```

### UI Components
- **st.audio_input()** - Direct browser recording
- **st.file_uploader()** - File input fallback
- **st.spinner()** - Loading states during processing
- **st.tabs()** - Multi-section layout
- **st.metric()** - Stats (word count, reading time)
- **st.markdown()** - Render study guide
- **st.download_button()** - Export functionality
- **st.form()** - Prevent API spam on reruns

---

## 4. Technical Requirements

### 4.1 Dependencies
```
streamlit==1.37.0
google-generativeai==0.3.0
python-dotenv==1.0.0
pandas==2.0.0
```

### 4.2 API Configuration

**Gemini API Setup:**
- Free tier: 60 requests/minute
- File size limit: 25MB
- Supported audio formats: WAV, MP3, M4A, OGG

**Environment Variables:**
```
GEMINI_API_KEY=your_key_here
```

### 4.3 Session State Management
```python
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "study_guide" not in st.session_state:
    st.session_state.study_guide = ""
if "quiz" not in st.session_state:
    st.session_state.quiz = {}
```

### 4.4 Error Handling
- [ ] API rate limit handling (retry with backoff)
- [ ] File size validation (>25MB rejection)
- [ ] Invalid audio format detection
- [ ] Empty transcript handling
- [ ] JSON parsing errors in quiz

---

## 5. Success Criteria (Rubric Alignment)

| Rubric Category | Target | How We Hit It |
|---|---|---|
| **Technical (25pts)** | 25 | Clean Python, st.session_state, Pandas for data, 0 errors |
| **AI Integration (20pts)** | 20 | Gemini audio transcription + 2 advanced prompts (study guide + quiz) |
| **UI/UX (20pts)** | 20 | 5 tabs, st.metric cards, markdown rendering, download buttons |
| **Deployment (15pts)** | 15 | Streamlit Cloud, requirements.txt optimized, live link in README |
| **GitHub (10pts)** | 10 | Mermaid diagram, terminal-style README |
| **Documentation (10pts)** | 10 | System design, prompt engineering docs, this PRD |

---

## 6. Deployment Checklist

- [ ] GitHub repo created (public)
- [ ] `requirements.txt` verified (no local deps)
- [ ] Environment variables set in Streamlit Secrets
- [ ] App tested locally (0 errors)
- [ ] Deployed to Streamlit Community Cloud
- [ ] Live link added to GitHub README
- [ ] LinkedIn post created (tag @MirAI)
- [ ] Review.md updated with final changes

---

## 7. Timeline

| Week | Task | Status |
|---|---|---|
| **Aug 11-13** | Setup scaffolding, Gemini API setup | 🔲 |
| **Aug 14-17** | Core features (audio + transcription) | 🔲 |
| **Aug 18-20** | Study guide + Quiz generation | 🔲 |
| **Aug 21-23** | UI polish + Export module + Testing | 🔲 |
| **Aug 24-25** | Deployment + Documentation + Submission | 🔲 |

---

## 8. Known Risks & Mitigation

| Risk | Mitigation |
|---|---|
| Gemini API quota exceeded | Use free tier strategically, cache results in session state |
| Audio transcription inaccuracy | Test with 3-5 real lectures, adjust prompts |
| Deployment failure | Test locally first, use Streamlit secrets correctly |
| Long processing time | Add progress bars, optimize prompt length |

---

## End of PRD

**Next Document:** Scaffolding.md (Project structure)
