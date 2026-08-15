# Tech Stack: Free Tier AI & Tools

## Overview

Complete tech stack for Voice-Notes to Flashcards using **100% free tools**.

---

## 1. Frontend & Framework

### **Streamlit** (Web Framework)
- **Cost:** Free (Community Cloud tier)
- **What:** Python web framework for rapid UI prototyping
- **Why:** 
  - Built-in widgets for audio, file upload, tabs
  - No HTML/CSS/JS needed
  - Automatic rerun detection
  - Free deployment on Streamlit Cloud
- **Installation:**
  ```bash
  pip install streamlit==1.37.0
  ```
- **Free Tier Limits:**
  - 3 public apps
  - 1GB storage per app
  - Auto-sleep after 1 hour inactivity
  - Community support only
- **Docs:** https://docs.streamlit.io

---

## 2. AI & LLM Services

### **Google Gemini API** (Primary Choice)
- **Cost:** Free tier with rate limits
- **What:** Google's multimodal AI with audio/text/vision support
- **Why:**
  - Free tier allows 60 requests/minute
  - Built-in audio transcription
  - Supports JSON output mode
  - Excellent prompt engineering capabilities
- **Setup:**
  ```bash
  pip install google-generativeai==0.3.0
  
  # Get free API key at: https://ai.google.dev
  ```
- **API Key Setup:**
  ```bash
  # Create .streamlit/secrets.toml
  GEMINI_API_KEY = "your-api-key-here"
  ```
- **Free Tier Limits:**
  - 60 requests/minute
  - 1500 requests/day
  - 32K tokens context window
  - Audio files: <25MB, <10 mins (most audios are <5 mins)
- **Code Example:**
  ```python
  import genai
  
  genai.configure(api_key="YOUR_KEY")
  model = genai.GenerativeModel("gemini-1.5-flash")
  
  # Audio transcription
  audio_file = genai.upload_file("lecture.wav")
  response = model.generate_content([
      "Transcribe this audio:",
      audio_file
  ])
  ```
- **Docs:** https://ai.google.dev/docs

---

## 3. Deployment Platform

### **Streamlit Community Cloud**
- **Cost:** Free
- **What:** Managed hosting for Streamlit apps
- **Why:**
  - Direct GitHub integration
  - Auto-deploy on push
  - Free SSL/HTTPS
  - Custom domain support (optional)
- **Setup (3 steps):**
  1. Push code to GitHub (public repo)
  2. Go to: https://share.streamlit.io
  3. Connect GitHub account & select repo
- **Free Tier Limits:**
  - 3 apps
  - 1GB storage each
  - Auto-sleep after 1 hour inactivity
  - Community support
- **Environment Variables:**
  ```
  Set GEMINI_API_KEY in Streamlit Cloud Secrets dashboard
  ```
- **Docs:** https://docs.streamlit.io/deploy/streamlit-cloud

---

## 4. Version Control

### **GitHub**
- **Cost:** Free
- **What:** Git hosting + collaboration
- **Why:**
  - Integrates directly with Streamlit Cloud
  - Free public repos
  - Issue tracking
  - GitHub Actions (CI/CD)
- **Setup:**
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git branch -M main
  git remote add origin https://github.com/username/voice-notes-to-flashcards.git
  git push -u origin main
  ```
- **Free Tier:**
  - Unlimited public/private repos
  - 2000 Actions minutes/month
  - Codespaces (limited)
- **Repo Structure:**
  ```
  voice-notes-to-flashcards/
  ├── app.py
  ├── requirements.txt
  ├── .streamlit/secrets.toml (add to .gitignore)
  ├── src/
  ├── prompts/
  ├── utils/
  ├── docs/
  ├── README.md
  ├── review.md
  └── FLOW_OF_EXECUTION.md
  ```
- **Docs:** https://docs.github.com

---

## 5. Optional: Local AI (Ollama)

### **Ollama** (Local Open-Source Alternative)
- **Cost:** Free, 100% open-source
- **What:** Run LLMs locally without internet
- **Why:** 
  - If you want zero API costs
  - Works offline
  - Fast inference on CPU/GPU
  - Good for development/testing
- **Models:**
  - Llama 2 (70B - powerful)
  - Mistral (7B - fast)
  - Neural Chat (7B - conversational)
- **Setup:**
  ```bash
  # Download from: https://ollama.ai
  ollama pull mistral
  ollama serve
  
  # Use in Python
  import requests
  response = requests.post('http://localhost:11434/api/generate', 
    json={"model": "mistral", "prompt": "..."})
  ```
- **Note:** 
  - **Audio transcription:** Still need Whisper (separate)
  - Slower than Gemini API
  - Use Gemini API for main project (proven, reliable)

---

## 6. Audio Processing (Optional)

### **Librosa** (Python Audio Library)
- **Cost:** Free, open-source
- **What:** Audio analysis and feature extraction
- **Why:**
  - Extract audio metadata (duration, sample rate)
  - Optional: Audio visualization
  - Noise detection
- **Installation:**
  ```bash
  pip install librosa==0.10.0
  ```
- **Usage:**
  ```python
  import librosa
  
  # Load audio
  y, sr = librosa.load('audio.wav')
  
  # Get duration
  duration = librosa.get_duration(y=y, sr=sr)
  ```
- **Note:** Not required for main project, but nice-to-have

---

## 7. Data Processing

### **Pandas** (Data Manipulation)
- **Cost:** Free, open-source
- **What:** Tabular data processing
- **Why:**
  - Export quiz as CSV/Excel
  - Handle batch processing (future feature)
- **Installation:**
  ```bash
  pip install pandas==2.0.0
  ```
- **Usage:**
  ```python
  import pandas as pd
  
  # Create quiz DataFrame
  quiz_df = pd.DataFrame(st.session_state.quiz['questions'])
  quiz_df.to_csv('quiz.csv', index=False)
  ```

---

## 8. Environment & Secrets

### **.env (Local Development)**
```
GEMINI_API_KEY=your-key-here
STREAMLIT_SERVER_PORT=8501
```

### **Streamlit Secrets (Cloud)**
1. Go to https://share.streamlit.io
2. Select your app → Settings → Secrets
3. Add:
   ```
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. Save (auto-redeploys app)

### **.gitignore (Don't commit secrets)**
```
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
```

---

## 9. Complete Requirements.txt

```
# Core Framework
streamlit==1.37.0

# AI/LLM
google-generativeai==0.3.0

# Data Processing
pandas==2.0.0

# Environment Variables
python-dotenv==1.0.0

# Optional: Audio Processing
librosa==0.10.0

# Optional: Testing
pytest==7.4.0
pytest-asyncio==0.21.0
```

**Installation:**
```bash
pip install -r requirements.txt
```

---

## 10. Agentic AI Setup (For Code Generation)

### **Using Claude API (Optional - For Scaffolding)**

If you want to use **Claude API** to help generate code:

```bash
pip install anthropic==0.7.0
```

**Use case:** Generate boilerplate code for modules

```python
from anthropic import Anthropic

client = Anthropic()

# System prompt for code generation
system_prompt = """You are an expert Python developer helping build a Streamlit app.
Generate clean, well-documented Python code following the PRD and scaffolding specifications.
Always include docstrings, type hints, and error handling."""

conversation = [
    {"role": "user", "content": "Generate the Transcriber class based on the PRD"}
]

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=2048,
    system=system_prompt,
    messages=conversation
)

print(response.content[0].text)
```

**Note:** Claude API has free credits ($5/month equivalent), or use paid tier ($0.003/1K input tokens).

### **Alternative: GitHub Copilot (Recommended for Development)**

- **Cost:** Free (limited) or $10/month (unlimited)
- **What:** AI code suggestions in VS Code/PyCharm
- **Setup:**
  1. Install GitHub Copilot extension
  2. Login with GitHub account
  3. Start typing → AI suggests code
- **Free Tier:** 60 code completions/month

---

## 11. Monitoring & Logging

### **Simple Python Logging**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Usage
logger.info("Transcription started")
logger.error("API error occurred", exc_info=True)
```

### **Streamlit Built-in Logging**
```python
import streamlit as st

# Display messages to user
st.success("✅ Processing complete!")
st.error("❌ API error occurred")
st.warning("⚠️ Rate limited, retrying...")
st.info("ℹ️ Processing your audio...")
```

---

## 12. Cost Breakdown (14-day project)

| Service | Cost | Notes |
|---|---|---|
| Gemini API | Free | 60 req/min limit sufficient |
| Streamlit Cloud | Free | 3 apps allowed |
| GitHub | Free | Unlimited public repos |
| Librosa | Free | Optional |
| Pandas | Free | Optional |
| **Total** | **$0** | 100% free! |

---

## 13. API Rate Limit Strategy

**Gemini Free Tier:** 60 requests/minute

**Plan:**
1. Cache results in `st.session_state`
2. Batch requests when possible
3. Implement retry with backoff (see FLOW_OF_EXECUTION.md)
4. Show spinners during API calls

**Example Caching:**
```python
if "transcript" not in st.session_state or not st.session_state.transcript:
    # Only call API if not cached
    transcript = transcriber.transcribe_audio(audio_file)
    st.session_state.transcript = transcript
else:
    transcript = st.session_state.transcript
```

---

## 14. Troubleshooting Common Issues

### **Issue: "API Key not found"**
- **Fix:** Set `GEMINI_API_KEY` in `.streamlit/secrets.toml` (local) or Streamlit Cloud Secrets

### **Issue: "Rate limited"**
- **Fix:** Wait 1 minute between requests, or use retry backoff logic

### **Issue: "Audio file > 25MB"**
- **Fix:** Validate file size before upload, or split large files

### **Issue: "Deployment fails on Streamlit Cloud"**
- **Fix:** Check `requirements.txt` has no local paths, all packages are PyPI versions

### **Issue: "Transcript is empty or too short"**
- **Fix:** Record clearer audio, longer duration (>30 seconds)

### **Issue: "JSON parse error in quiz"**
- **Fix:** Add error handling, retry generation with adjusted prompt

---

## 15. Performance Tips

| Tip | Why |
|---|---|
| Use `st.session_state` to cache | Avoid re-processing audio on reruns |
| Use `st.spinner()` during API calls | Show user progress, prevent timeout perception |
| Limit context in prompts | Fewer tokens = faster response |
| Use `gemini-1.5-flash` not `pro` | Faster, cheaper, still powerful |
| Deploy to Streamlit Cloud | Free + auto-updates from GitHub |
| Use GitHub Actions for testing | Optional CI/CD, free tier |

---

## 16. Scaling Beyond Free Tier (Future)

When project goes live:

| Service | Paid Tier Cost |
|---|---|
| Gemini API | $0.075/1M input tokens, $0.30/1M output tokens |
| Streamlit Cloud Pro | $9/month for 1 app, more storage |
| AWS/GCP Hosting | $5-20/month for basic instance |
| **Total** | **$15-30/month** |

---

## Summary

✅ **All free tools**  
✅ **No credit card needed**  
✅ **Professional production-ready**  
✅ **Scalable to paid tier later**  

**Next Document:** REVIEW.md (Code review template)
