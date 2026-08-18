# Deployment Guide

## 1. Pre-deployment Checklist

- [ ] `requirements.txt` is updated.
- [ ] `.env` is ignored in `.gitignore`.
- [ ] Application runs locally without errors.
- [ ] Gemini API key is active.

## 2. GitHub Push & Streamlit Cloud Setup

### GitHub Push
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Streamlit Cloud Setup
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **New app**.
3. Select your GitHub repository and `main` branch.
4. Set **Main file path** to your entry point (e.g., `app.py`).
5. Click **Advanced settings** -> **Secrets** and add:
   ```toml
   GEMINI_API_KEY="your-api-key-here"
   ```
6. Click **Deploy**.

## 3. Troubleshooting

*   **Missing Dependencies**: Ensure all required packages are listed in `requirements.txt`. Check Streamlit logs for import errors.
*   **API Key Errors**: Verify that `GEMINI_API_KEY` is correctly set in Streamlit Secrets, not hardcoded.
*   **Audio Upload Fails**: Streamlit Cloud has a default upload limit (usually ~200MB). Check `server.maxUploadSize` in `.streamlit/config.toml` if larger files are needed.

## 4. Final Submission Instructions

### Submission Portal
1. Submit your public GitHub repository URL.
2. Submit your live Streamlit Cloud app URL.
3. Ensure the repository contains a comprehensive `README.md`.

### LinkedIn Post
1. Share a brief demo video or screenshot of the app in action.
2. Tag relevant mentors or organizations (e.g., Mirai).
3. Include links to the live app and GitHub repository.
