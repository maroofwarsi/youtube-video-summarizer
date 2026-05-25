# YouTube Video Summarizer

**Paste a YouTube URL. Get a summary, five key takeaways, and five questions — in seconds.**

[![Live Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app.streamlit.app)
&nbsp;
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-orange)

---

## What Is This?

This is a web app that turns any YouTube video into a structured, readable summary — without you having to watch a single second of it.

You paste a link. The app reads the video's transcript and uses Google's Gemini AI to give you:

- A **3–5 sentence summary** of what the video is about
- **5 key takeaways** — the most important points
- **5 questions** you could ask to explore the topic further

It works on tutorials, lectures, conference talks, podcasts, documentaries — anything with captions.

---

## Why I Built This

As someone applying for AI engineering roles, I wanted to build something that demonstrates how Large Language Models (LLMs) can be used practically to save people time.

The problem: YouTube has millions of hours of educational content, but most people don't have hours to spend watching videos before knowing if they're worth it. A quick AI-generated summary changes that — you can decide in 30 seconds whether a video is worth your time, or extract the key ideas without watching.

This project shows:

- How to extract and process real-world data (video transcripts) from an API
- How to engineer effective prompts to get structured, useful output from an LLM
- How to build a clean, user-facing web interface around an AI model
- How to deploy a production-ready AI app on a free cloud platform

---

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| UI / Frontend | Streamlit | Fast to build, looks professional, ideal for AI demos |
| AI / LLM | Google Gemini 1.5 Flash | Free tier, fast, handles long transcripts well |
| Transcript extraction | youtube-transcript-api | Reliable, no YouTube API key needed |
| Environment management | python-dotenv | Keeps API keys safe and out of source code |
| Deployment | Streamlit Cloud | Free, one-click deploy from GitHub |

---

## How It Works (Plain English)

1. **You paste a YouTube URL** into the text box.
2. The app **extracts the video ID** from the URL (it handles all common YouTube URL formats).
3. It **downloads the transcript** directly from YouTube's caption system — no video is downloaded, just the text.
4. That transcript is **sent to Google Gemini** with a carefully crafted prompt that asks for a summary, takeaways, and questions in a specific format.
5. Gemini's response is **displayed back to you** in a clean, readable layout.
6. You can **download the result** as a text file.

The whole process takes about 5–15 seconds depending on the video length.

---

## How to Run Locally

### Prerequisites

- Python 3.10 or higher
- A free Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey) — no credit card needed)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/youtube-video-summarizer.git
cd youtube-video-summarizer

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Open .env and replace "your_gemini_api_key_here" with your actual key

# 5. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Deploying to Streamlit Cloud (Free)

1. Push this repository to GitHub (see the deployment guide below)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set main file to `app.py`
4. Under **Advanced settings → Secrets**, add:
   ```
   GEMINI_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy** — your app will be live in about 2 minutes

---

## Project Structure

```
youtube-video-summarizer/
├── app.py                  # Main application — all logic and UI
├── requirements.txt        # Python dependencies
├── .env.example            # Template for local API key setup
├── .gitignore              # Keeps secrets and junk out of Git
├── .streamlit/
│   └── config.toml         # App theme (dark mode, YouTube red)
└── README.md               # This file
```

---

## Limitations

- Videos must have captions enabled. Most educational content does; some music videos and live streams don't.
- Very long videos (3+ hours) will have their transcripts trimmed to fit the AI's context window. The summary will still be accurate for the majority of content.
- The app uses Gemini's free tier — rate limits apply if you're making many requests in a short time.

---

## Skills Demonstrated

This project was built to demonstrate practical AI engineering skills relevant to a professional role:

- **Prompt engineering** — designing a structured prompt that consistently returns well-formatted, useful output
- **API integration** — connecting two external services (YouTube + Gemini) with proper error handling
- **User experience thinking** — handling edge cases gracefully (no transcript, private video, bad URL) with clear error messages
- **Clean Python code** — modular functions, type hints, docstrings
- **Cloud deployment** — shipping a real, publicly accessible app for free

---

## Author

Built by **M** as part of a portfolio of AI engineering projects.

- **Also see:** [Job vs CV Analyser](https://github.com/YOUR_USERNAME/job-cv-analyser) — another project that uses AI to compare a job description against a CV and score how well they match.

---

## License

MIT — free to use, fork, and build on.
