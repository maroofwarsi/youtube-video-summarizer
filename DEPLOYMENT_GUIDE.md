# End-to-End Deployment Guide

**Zero to live app — free, step by step.**

This guide takes you from having the code on your computer to having a publicly shareable link that anyone can visit.

---

## Step 1 — Get Your Free Gemini API Key (2 minutes)

1. Go to **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**
2. Sign in with your Google account
3. Click **"Create API key"**
4. Copy the key — it looks like: `AIzaSy...`
5. Keep it safe — treat it like a password

> **Why Gemini?** It has a generous free tier (15 requests/minute, 1 million tokens/day) and no credit card is required.

---

## Step 2 — Set Up Python on Your Computer

If you already have Python 3.10+, skip to Step 3.

1. Go to **[https://python.org/downloads](https://python.org/downloads)**
2. Download and install the latest version
3. During install on Windows, **tick "Add Python to PATH"**
4. Verify it worked — open a terminal and type:
   ```
   python --version
   ```
   You should see something like `Python 3.12.x`

---

## Step 3 — Run the App Locally

Open a terminal (Command Prompt or PowerShell on Windows, Terminal on Mac).

```bash
# Navigate to your project folder
cd "YouTube Video Summarizer"

# Create a virtual environment (keeps dependencies isolated)
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac / Linux

# Install all dependencies
pip install -r requirements.txt

# Create your .env file from the template
copy .env.example .env         # Windows
cp .env.example .env           # Mac / Linux
```

Now open the `.env` file in any text editor and replace `your_gemini_api_key_here` with your actual key:

```
GEMINI_API_KEY=AIzaSy_your_actual_key_here
```

Save it, then run the app:

```bash
streamlit run app.py
```

Your browser will open to `http://localhost:8501`. Test it with a YouTube URL — if it works, you're ready to deploy!

---

## Step 4 — Push to GitHub

### 4a. Create a repository

1. Go to **[https://github.com/new](https://github.com/new)**
2. Repository name: `youtube-video-summarizer`
3. Set it to **Public** (required for free Streamlit deployment)
4. **Do NOT** tick "Add a README" — you already have one
5. Click **"Create repository"**

### 4b. Push your code

In your terminal (make sure you're in the project folder):

```bash
# Initialise Git
git init

# Stage all files
git add .

# Make your first commit
git commit -m "Initial commit: YouTube Video Summarizer"

# Connect to GitHub (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/youtube-video-summarizer.git

# Push!
git branch -M main
git push -u origin main
```

Refresh your GitHub page — all your files should be there.

> **Important:** Your `.env` file is in `.gitignore`, so your API key will NOT be uploaded. Good.

---

## Step 5 — Deploy on Streamlit Cloud (Free)

1. Go to **[https://share.streamlit.io](https://share.streamlit.io)**
2. Click **"Sign in with GitHub"** and authorise the app
3. Click **"New app"**
4. Fill in:
   - **Repository:** `YOUR_USERNAME/youtube-video-summarizer`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Advanced settings"**
6. Under **Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "AIzaSy_your_actual_key_here"
   ```
7. Click **"Deploy!"**

Streamlit will build your app — takes about 2 minutes. When it's done, you'll get a URL like:

```
https://your-app-name.streamlit.app
```

**That link is your live, public app.** Put it in your CV, LinkedIn, and GitHub profile.

---

## Step 6 — Update the README with Your Live URL

Open `README.md` and update the badge at the top:

```markdown
[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-actual-url.streamlit.app)
```

Also update the "Also see" link at the bottom with your actual GitHub username and Job vs CV Analyser link.

Then push the update:

```bash
git add README.md
git commit -m "Add live demo link"
git push
```

---

## Step 7 — Add to Your CV and LinkedIn

**CV bullet point (under Projects):**

> **YouTube Video Summarizer** | Python · Streamlit · Google Gemini AI | [Live Demo](https://your-app.streamlit.app) | [GitHub](https://github.com/YOUR_USERNAME/youtube-video-summarizer)
> Built an end-to-end AI web app that extracts YouTube transcripts and uses LLM prompt engineering to generate summaries, key takeaways, and study questions. Deployed on Streamlit Cloud.

**LinkedIn project entry:**
- Add it under your **Projects** section
- Include the live URL so recruiters can try it in one click

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Make sure your virtual environment is active (`venv\Scripts\activate`) |
| `TranscriptsDisabled` error | The video has captions turned off — try a different video |
| `Invalid API key` | Double-check you copied the full key with no extra spaces |
| Streamlit Cloud shows blank page | Check the Logs tab — most likely the secret isn't named exactly `GEMINI_API_KEY` |
| `pip` not found | Use `python -m pip install -r requirements.txt` instead |

---

## What's Next (Ideas to Extend the Project)

Once you're deployed, here are ways to make the project even stronger for your portfolio:

- **Add language support** — translate the summary into another language using Gemini
- **Batch mode** — summarise multiple videos at once from a playlist URL
- **Export to PDF** — generate a nicely formatted PDF of the summary
- **Comparison mode** — summarise two videos and compare their perspectives on the same topic
- **History** — store the last 5 summaries in the session so users can flip back

Each of these is a concrete talking point in a technical interview.
