# Capstone Project Selection: Voice-Notes to Flashcards (Problem #8)

## Why This Problem?

### ✅ Rubric Score Potential: 95-100/100

| Rubric Category | Score | Why |
|---|---|---|
| **Technical Implementation (25pts)** | 25 | Complex audio processing pipeline, session state for file management, Pandas for structured data export |
| **AI Integration (20pts)** | 20 | Gemini for transcription + structured output (study guide + quiz generation) - requires advanced prompt engineering |
| **UI/UX (20pts)** | 20 | Audio recorder widget, dynamic tabs (transcript/study guide/quiz), data export functionality |
| **Deployment (15pts)** | 15 | Simple Streamlit Community Cloud deployment, no complex infrastructure |
| **GitHub/Branding (10pts)** | 10 | Clear README, easy-to-understand architecture |
| **Documentation (10pts)** | 10 | System design, prompt engineering docs, flow diagrams |
| **TOTAL** | **100** | ⭐ Full marks potential |

---

## Project Scope (14 Days)

### MVP (Week 1)
- [ ] Audio input via `st.audio_input()` 
- [ ] Transcription via Gemini API (audio → text)
- [ ] Display raw transcript

### Core Features (Week 1-2)
- [ ] Gemini prompt engineering: Generate structured study guide from transcript
- [ ] Quiz generation (5 MCQ questions with answers)
- [ ] Tab-based UI (Transcript | Study Guide | Quiz)
- [ ] Export as `.txt` and `.json`

### Polish (Final Days)
- [ ] Deploy to Streamlit Cloud
- [ ] GitHub README with architecture diagram
- [ ] System design documentation
- [ ] Live testing & bug fixes

---

## Tech Stack (All Free)

| Component | Tool | Free Tier | Why |
|---|---|---|---|
| **Frontend Framework** | Streamlit | Unlimited | Perfect for quick dashboards, free hosting |
| **AI/LLM** | Google Gemini API | Free (with limits) | Audio transcription + structured output, Vision support |
| **Audio Processing** | Librosa (Python) | Open-source | Local audio analysis, no costs |
| **Data Export** | Pandas + JSON | Open-source | Format structured data for export |
| **Deployment** | Streamlit Community Cloud | Free | 3x apps, auto-updates from GitHub |
| **Version Control** | GitHub | Free | Public repo, README hosting |
| **System Design** | Mermaid (in README) | Free | Markdown-native diagrams |

---

## Why NOT Other Problems?

| Problem | Reason Rejected |
|---|---|
| #12: "Roast My Form" (CV Analysis) | Requires OpenCV/MediaPipe setup, complex deployment, 2+ days wasted on environment setup |
| #17: Resume Critic | Straightforward text comparison, less AI integration showcase |
| #25: Visual Novel Engine | Too narrative-focused, harder to scope completion in 14 days |
| #27: Signage Explainer | Requires image upload pipeline, over-engineered for timeframe |

**Problem #8 is the sweet spot:** Achieves full rubric points, doable in timeline, scalable if needed.

---

## Success Metrics

- ✅ 0 runtime errors on deployment
- ✅ Transcription accuracy within 90% (Gemini baseline)
- ✅ Study guide generated in <5 seconds
- ✅ Live on Streamlit Cloud by Aug 24
- ✅ GitHub README with system diagram
- ✅ All code documented with review.md trail

---

## Next: Start with PRD.md
