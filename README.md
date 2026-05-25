# YouTube Video Summarizer

Paste a YouTube URL. Get a summary, five key takeaways, and five questions - in seconds.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-Llama3-orange)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## What it does

Paste any YouTube link. The app grabs the video transcript and uses an LLM to give you:

- A 3-5 sentence summary of what the video is about
- 5 key takeaways - the most important points
- 5 questions you could ask to explore the topic further

It works on tutorials, lectures, conference talks, podcasts - anything with captions. The whole thing takes about 5-15 seconds.

---

## Why I built this

YouTube has a huge amount of useful content, but you often can't tell if a video is worth watching until you're 20 minutes in. This lets you check in 30 seconds - paste the link, read the summary, decide.

---

## Tech stack

| Layer | Tool | Why |
|---|---|---|
| UI | Streamlit | Fast to build, easy to use |
| LLM | Groq (Llama 3.1 / 3.3) | Free API, very fast inference |
| Transcript | youtube-transcript-api | Pulls captions directly, no YouTube API key needed |
| Config | python-dotenv | Keeps API keys out of the code |
| Deployment | Streamlit Cloud | Free, deploys straight from GitHub |

Total cost: $0

---

## How it works

1. You paste a YouTube URL
2. The app pulls out the video ID and fetches the transcript from YouTube's caption system
3. The transcript goes to Groq (Llama 3) with a prompt asking for a summary, takeaways, and questions
4. The result comes back and is displayed in a clean layout
5. You can download the output as a text file

---

## Run it locally

**Step 1 - Get a free Groq API key**

Go to [console.groq.com](https://console.groq.com), sign up (no card needed), grab an API key.

**Step 2 - Clone and install**

```bash
git clone https://github.com/maroofwarsi/youtube-video-summarizer.git
cd youtube-video-summarizer

python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

**Step 3 - Add your key**

```bash
cp .env.example .env
# Open .env and add your Groq key
```

**Step 4 - Run**

```bash
streamlit run app.py
```

Opens at [http://localhost:8501](http://localhost:8501).

---

## Deploy to Streamlit Cloud (free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. New app -> select your repo -> main file: `app.py`
4. Under Advanced settings -> Secrets, add:
   ```
   GROQ_API_KEY = "your_actual_key_here"
   ```
5. Click Deploy - live in about 2 minutes

---

## Project structure

```
youtube-video-summarizer/
├── app.py              # All the logic and UI in one file
├── requirements.txt    # Dependencies
├── .env.example        # API key template
├── .gitignore
├── .streamlit/
│   └── config.toml     # App theme
└── README.md
```

---

## Limitations

- The video needs captions. Most tutorials, talks, and lectures have them. Some music videos and live streams don't.
- Very long videos (3+ hours) get their transcript trimmed to fit the model's context window - the summary will still cover the main content.
- Uses Groq's free tier, so there are rate limits if you're making a lot of requests quickly.

---

## Also see

- [DataChat](https://github.com/maroofwarsi/datachat) - ask questions about any CSV or Excel file in plain English
- [DocChat](https://github.com/maroofwarsi/dochat) - ask questions about any PDF and get cited answers
- [CV Analyzer](https://github.com/maroofwarsi/cv-analyzer) - compare a CV against a job description and get a match score

---

## License

MIT
