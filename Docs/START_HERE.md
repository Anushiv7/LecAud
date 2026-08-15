# 🎯 Voice-Notes to Flashcards: START HERE

**Project:** Capstone Project for MirAI School of Technology  
**Deadline:** August 25, 2026, 11:59 PM  
**Days Left:** ~14 days (as of Aug 11, 2026)  
**Your Name:** Anushiv Prakash  
**Problem Statement:** #8 - Voice-Notes to Flashcards

---

## 📋 Quick Overview

Convert chaotic lecture recordings into:
1. ✅ Structured **transcripts**(Necessary)
2. ✅ Comprehensive **study guides**(Necessary)
3. ✅ Interactive **MCQ quizzes**(Optional)
4. ✅ All exportable as **TXT/JSON**

**Why This Project?**
- 🎯 Score: 95-100/100 on rubric (all 6 categories maxed)
- ⏱️ Achievable in 14 days
- 🚀 Showcases your AI/ML skills
- 💰 Zero cost (all free APIs)
- 📱 Easily deployed to Streamlit Cloud

---

## 📚 Complete Documentation (6 Files)

Read in this order:

### 1. **PROBLEM_SELECTION.md** ← Start here
```
Why this problem?
Rubric score breakdown
Tech stack justification
Timeline overview
```

### 2. **PRD.md** (Product Requirements Document)
```
What the app does
Feature specifications
UI/UX design
Success criteria
Technical requirements
```

### 3. **SCAFFOLDING.md** (Project Structure)
```
Directory layout
Module descriptions
File purposes
Data flow diagrams
```

### 4. **FLOW_OF_EXECUTION.md** (How It Works)
```
Step-by-step execution
Code walkthroughs
Error handling
Session state management
Performance tips
```

### 5. **TECH_STACK.md** (Tools & Setup)
```
Free tier tools (Gemini, Streamlit, GitHub)
API setup guide
Requirements.txt
Cost breakdown ($0!)
Troubleshooting
```

### 6. **REVIEW.md** (Code Changes)
```
Every code change logged
Explanations documented
Testing status tracked
Update as you code!
```

---

## 🚀 Quick Start (5 Steps)

### Step 1: Setup Gemini API (5 minutes)
```bash
# Get free API key at:
https://ai.google.dev/tutorials/setup

# Copy this into .streamlit/secrets.toml:
GEMINI_API_KEY = "your-key-here"
```

### Step 2: Setup Project Structure (2 minutes)
```bash
mkdir -p src utils prompts tests docs assets
touch app.py requirements.txt .gitignore

# Create .streamlit/secrets.toml with API key
```

### Step 3: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt

# Content of requirements.txt:
# streamlit==1.37.0
# google-generativeai==0.3.0
# python-dotenv==1.0.0
# pandas==2.0.0
```

### Step 4: Run Locally (1 minute)
```bash
streamlit run app.py

# App launches at: http://localhost:8501
```

### Step 5: Deploy to Streamlit Cloud (5 minutes)
```bash
# 1. Push to GitHub (public repo)
git push origin main

# 2. Go to https://share.streamlit.io
# 3. Click "New app"
# 4. Connect GitHub → Select repo
# 5. Add GEMINI_API_KEY in Secrets
# 6. Done! Your app is live
```

---

## 📖 Development Timeline

### Week 1: Core Features (Aug 11-17)

**Aug 11-12: Audio Input**
- [ ] Create `src/audio_processor.py`
- [ ] Build Tab 1 UI (record/upload)
- [ ] Implement validation (format, size)

**Aug 13: Transcription**
- [ ] Create `src/transcriber.py`
- [ ] Integrate Gemini Audio API
- [ ] Implement retry logic
- [ ] Build Tab 2 (display transcript)

**Aug 14: Study Guide**
- [ ] Create `src/study_guide_generator.py`
- [ ] Write prompt template
- [ ] Build Tab 3 (render markdown)

**Aug 15-16: Quiz + Export**
- [ ] Create `src/quiz_generator.py`
- [ ] Write quiz prompt
- [ ] Build Tab 4 (interactive quiz)
- [ ] Create `src/exporter.py`
- [ ] Build Tab 5 (download buttons)

**Aug 17: Testing**
- [ ] Test all features locally
- [ ] Verify error handling
- [ ] Check API rate limits

### Week 2: Polish & Deploy (Aug 18-25)

**Aug 18-20: Refinement**
- [ ] UI polish (colors, spacing)
- [ ] Performance optimization
- [ ] Edge case handling

**Aug 21-23: Documentation**
- [ ] Write SYSTEM_DESIGN.md (diagrams)
- [ ] Write PROMPT_ENGINEERING.md (strategies)
- [ ] Create README.md for GitHub

**Aug 24: Deployment**
- [ ] Push final code to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Test live app

**Aug 25: Submission**
- [ ] Create LinkedIn post (tag @MirAI)
- [ ] Submit via internship portal
- [ ] Ensure live deployment link works

---

## 🎯 Rubric Checklist (100 Points)

### ✅ Technical Implementation (25 pts)
- [ ] No runtime errors (test locally first)
- [ ] Proper use of `st.session_state`
- [ ] Clean data pipelines with Pandas
- [ ] Modular, reusable code

**How to hit 25:**
```python
# Use session_state to prevent memory loss
if "transcript" not in st.session_state:
    st.session_state.transcript = ""

# Use st.form to batch API calls
with st.form("process_form"):
    submit = st.form_submit_button("Process")
    if submit:
        # Single API call, not on every rerun

# No terminal errors
# Test with sample audio before deployment
```

### ✅ AI Integration (20 pts)
- [ ] Advanced Gemini usage (audio + text + JSON)
- [ ] System prompts with context
- [ ] F-strings for dynamic prompts
- [ ] Multimodality (audio input works)

**How to hit 20:**
```python
# System prompt guides AI behavior
system_prompt = """You are an expert..."""

# F-strings inject dynamic context
prompt = f"""
Given this transcript:
{transcript}

Generate a study guide...
"""

# JSON mode forces structured output
response = model.generate_content(
    prompt,
    generation_config=GenerationConfig(
        response_mime_type="application/json"
    )
)
```

### ✅ UI/UX (20 pts)
- [ ] Professional dashboard (5 tabs)
- [ ] Proper layouts with columns/expanders
- [ ] Dynamic KPI cards (st.metric)
- [ ] Interactive elements (radio buttons, buttons)

**How to hit 20:**
```python
# Use columns for layout
col1, col2, col3 = st.columns(3)

# Use expanders for collapsible content
with st.expander("📖 Full Transcript"):
    st.text_area(...)

# Use st.metric for KPIs
st.metric("Word Count", 2500)

# Use interactive elements
st.radio("Choose:", ["A", "B", "C"])
st.checkbox("Show details")
st.download_button(...)
```

### ✅ Deployment (15 pts)
- [ ] Live on Streamlit Community Cloud
- [ ] Zero local dependencies in requirements.txt
- [ ] API key via Secrets (not hardcoded)
- [ ] App loads without errors

**How to hit 15:**
```
# Clean requirements.txt
streamlit==1.37.0
google-generativeai==0.3.0
python-dotenv==1.0.0
pandas==2.0.0

# NO local paths like:
# /Users/anu/myproject/src  ← WRONG

# Set secrets in Streamlit Cloud dashboard
# Not in code!
```

### ✅ GitHub Branding (10 pts)
- [ ] Public GitHub repo
- [ ] Customized README.md
- [ ] System architecture diagram (Mermaid)
- [ ] Setup instructions

**How to hit 10:**
```markdown
# Voice-Notes to Flashcards

🎤 Convert chaotic lectures into study materials

## Architecture

\`\`\`mermaid
graph LR
    A[Audio Input] --> B[Gemini API]
    B --> C[Transcript]
    B --> D[Study Guide]
    B --> E[Quiz]
\`\`\`

## Setup

\`\`\`bash
pip install -r requirements.txt
streamlit run app.py
\`\`\`

## Live Demo
[Link to Streamlit Cloud app]
```

### ✅ Documentation (10 pts)
- [ ] System design document
- [ ] Prompt engineering explanation
- [ ] Code flow diagrams
- [ ] This review.md file

**How to hit 10:**
- Write `docs/SYSTEM_DESIGN.md` (architecture, data flow)
- Write `docs/PROMPT_ENGINEERING.md` (how prompts work)
- Create Mermaid diagrams in README
- Update review.md as you code

---

## 💡 Pro Tips for Success

### 1. **Cache Everything**
```python
if st.session_state.transcript:
    # Use cached transcript, don't re-call API
    transcript = st.session_state.transcript
else:
    # Only call API once
    transcript = transcriber.transcribe_audio(...)
    st.session_state.transcript = transcript
```

### 2. **Show Loading States**
```python
with st.spinner("🎙️ Transcribing..."):
    transcript = transcriber.transcribe_audio(...)
```

### 3. **Validate Everything**
```python
# Check file size before upload
if file.size > 25_000_000:
    st.error("❌ File too large")
    return

# Check transcript quality
if len(transcript) < 50:
    st.warning("⚠️ Transcript too short")
```

### 4. **Test Locally First**
```bash
# Test everything before deploying
streamlit run app.py

# Upload test audio (10-30 mins)
# Check transcription quality
# Verify study guide format
# Test quiz JSON
# Download files
```

### 5. **Use Free API Wisely**
- 60 requests/minute limit (Gemini free tier)
- Cache results in session state
- Batch operations when possible
- Retry with exponential backoff

### 6. **Git Commit Often**
```bash
git add src/transcriber.py
git commit -m "feat: add audio transcription with retry logic"
git push origin main
```

---

## ⚠️ Common Pitfalls (Avoid These!)

| ❌ Mistake | ✅ Fix |
|---|---|
| Hardcode API key in code | Use `.streamlit/secrets.toml` |
| Re-transcribe on every click | Cache in `st.session_state` |
| No error handling for API | Use try-except + retry logic |
| App takes >10s to load | Use spinners, lazy loading |
| Files don't export correctly | Test download_button locally |
| GitHub has secrets in history | Add to `.gitignore` before push |
| Deployment fails | Check requirements.txt has no local paths |

---

## 📞 Quick Reference

### Gemini API Key
```python
import genai
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

### Streamlit Commands
```python
st.write()              # Display text
st.metric()             # Display KPI
st.markdown()           # Render markdown
st.audio_input()        # Record audio
st.file_uploader()      # Upload file
st.tabs()               # Create tabs
st.spinner()            # Loading indicator
st.download_button()    # File download
st.session_state        # Persist data
```

### Python Commands
```bash
streamlit run app.py              # Run locally
pip install -r requirements.txt   # Install deps
git push origin main              # Push to GitHub
```

---

## 📊 Expected Outcomes

### By Aug 25, 2026:

✅ **Working App**
- Transcribes 30-minute lectures in <30 seconds
- Generates study guides in <15 seconds
- Creates 5-question quizzes in <15 seconds
- Downloads work without corruption

✅ **Code Quality**
- Zero runtime errors
- Clean, modular architecture
- Proper error handling
- 800+ lines of code

✅ **Deployment**
- Live on Streamlit Cloud
- GitHub repo with clean history
- README with system diagram
- API key secured (not in code)

✅ **Rubric Score**
- Technical: 25/25 ✅
- AI Integration: 20/20 ✅
- UI/UX: 20/20 ✅
- Deployment: 15/15 ✅
- GitHub: 10/10 ✅
- Documentation: 10/10 ✅
- **TOTAL: 100/100** 🎯

---

## 🎬 Next Steps

1. **Right Now:** Read PROBLEM_SELECTION.md
2. **Today:** Setup Gemini API key
3. **Tomorrow:** Create project structure
4. **This Week:** Code core features
5. **Next Week:** Polish & deploy
6. **Aug 25:** Submit!

---

## 📧 Questions?

Refer to:
- **Prompt engineering issues?** → TECH_STACK.md (Gemini docs)
- **Code structure questions?** → SCAFFOLDING.md
- **Deployment stuck?** → FLOW_OF_EXECUTION.md
- **UI/UX ideas?** → PRD.md (design section)
- **Error handling?** → FLOW_OF_EXECUTION.md (error handling flow)

---

**Good luck! You've got this! 🚀**

Deadline: Aug 25, 2026, 11:59 PM  
Estimated effort: 40-50 hours over 14 days  
Difficulty: Medium (building on Streamlit/Gemini basics)  
Impact: 100/100 rubric score potential

---

**Created by:** Anushiv Prakash  
**Date:** Aug 11, 2026  
**Status:** Ready to start development 🎯
