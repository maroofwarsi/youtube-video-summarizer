# YouTube Video Summarizer — Full Project Documentation

> Written for anyone reading this project for the first time — including recruiters,
> collaborators, and your future self.

---

## Table of Contents

1. [What This Project Does](#1-what-this-project-does)
2. [Why I Built It](#2-why-i-built-it)
3. [How It Works — Plain English](#3-how-it-works--plain-english)
4. [Architecture](#4-architecture)
5. [Tech Stack and Why Each Tool Was Chosen](#5-tech-stack-and-why-each-tool-was-chosen)
6. [Key Engineering Decisions](#6-key-engineering-decisions)
7. [Known Limitations](#7-known-limitations)
8. [How to Run It Yourself](#8-how-to-run-it-yourself)
9. [Recruiter Q&A — AI Engineer Role](#9-recruiter-qa--ai-engineer-role)

---

## 1. What This Project Does

You paste a YouTube URL into a text box. Within about 10 seconds, the app gives you:

- A **summary** of the video in 3–5 sentences
- **5 key takeaways** — the most important points from the video
- **5 questions** you could ask to explore the topic further

It works on any public YouTube video that has captions: tutorials, lectures, conference talks, podcasts, documentaries, and more.

You do not need to watch a single second of the video. The app reads the transcript for you and uses an AI language model to extract what matters.

---

## 2. Why I Built It

There are millions of hours of educational content on YouTube. The problem is that watching a 45-minute lecture to find out if it's useful costs 45 minutes. There is no fast way to preview what a video actually covers.

This project solves that problem. It turns any video into a structured, readable summary in seconds — so you can decide whether to watch it, share it, or use it for research without investing your time upfront.

From an engineering perspective, this project demonstrates something important: **AI is most valuable when it is applied to a real, concrete problem with a clean interface around it.** The AI here is not the product — the time savings and the structured output are the product. The AI is just the engine underneath.

---

## 3. How It Works — Plain English

Here is the full journey from URL to summary, explained without jargon:

**Step 1 — You paste a URL**
The app accepts any YouTube URL format. Whether it is `youtube.com/watch?v=ABC123`, `youtu.be/ABC123`, or a Shorts link, the app extracts the unique 11-character video ID from it using pattern matching.

**Step 2 — The app fetches the transcript**
YouTube stores a text version of what is spoken in most videos (used for subtitles and accessibility). The app downloads this text directly using a Python library called `youtube-transcript-api`. No video file is downloaded — just the text. This is fast and free.

**Step 3 — The transcript is prepared for the AI**
A raw transcript can be very long. The app clips it to 28,000 characters to stay within the AI model's processing limit. For most videos under 2 hours, the full transcript fits. For longer videos, the most important content (typically near the start) is used.

**Step 4 — A prompt is sent to the AI**
The transcript is inserted into a carefully written instruction (called a "prompt") that tells the AI exactly what to produce: a summary in a specific format, five takeaways numbered clearly, and five questions. The format is enforced in the prompt so the output is always consistent and readable.

**Step 5 — The AI responds**
The prompt is sent to Groq, a cloud service that runs open-source language models at very high speed. The model reads the transcript and writes the summary, takeaways, and questions.

**Step 6 — The result is displayed**
The response is rendered back in the app with the video thumbnail shown above it. You can also download the result as a plain text file.

---

## 4. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                        │
│                                                          │
│   Paste URL  ──►  Click "Summarise"  ──►  Read results  │
└────────────────────────┬────────────────────────────────┘
                         │  HTTP
                         ▼
┌─────────────────────────────────────────────────────────┐
│               STREAMLIT APP  (app.py)                    │
│                                                          │
│  1. extract_video_id(url)                                │
│     Regex pattern matching → 11-char video ID            │
│                                                          │
│  2. get_transcript(video_id)                             │
│     YouTubeTranscriptApi().list(video_id)                │
│     → find best transcript (manual EN > auto EN > any)   │
│     → fetch() → join snippet.text into single string     │
│                                                          │
│  3. truncate_transcript(text, max_chars=28000)           │
│     Clips to fit model context window                    │
│                                                          │
│  4. build_prompt(transcript)                             │
│     Wraps transcript in structured instructions          │
│                                                          │
│  5. get_groq_response(api_key, prompt, model)            │
│     Groq client → chat.completions.create()              │
│     → returns summary text                               │
│                                                          │
│  6. st.markdown(result)                                  │
│     Renders formatted output to the browser              │
└──────────┬─────────────────────────┬────────────────────┘
           │                         │
           ▼                         ▼
┌──────────────────┐      ┌──────────────────────────────┐
│  YouTube servers │      │  Groq API                    │
│                  │      │                              │
│  Transcript XML  │      │  llama-3.1-8b-instant        │
│  fetched over    │      │  (or user-selected model)    │
│  HTTPS           │      │  Returns generated text      │
└──────────────────┘      └──────────────────────────────┘
```

**Data flow summary:**
`URL → video ID → transcript text → truncated text → prompt → LLM response → formatted display`

There is no database. No user data is stored. Everything lives in memory for the duration of the browser session. When you close the tab, nothing is retained.

---

## 5. Tech Stack and Why Each Tool Was Chosen

### Streamlit
Streamlit turns a Python script into a web app automatically. You write Python functions and Streamlit handles the HTML, CSS, buttons, and layout. This was chosen because:
- It gets a working UI running in minutes, not days
- It deploys for free directly from a GitHub repository
- It is widely used in the AI/ML industry for demos and internal tools
- It lets the focus stay on the AI logic, not on frontend code

### Groq
Groq is a cloud service for running open-source language models. It was chosen over alternatives because:
- It is **completely free** — no credit card required, no trial period
- It is **extremely fast** — Groq uses custom hardware (Language Processing Units) that runs models much faster than standard GPU servers
- It uses the **OpenAI-compatible API format**, which is the industry standard
- It runs **open-source models** (Meta's Llama) which is important for transparency and reproducibility

### youtube-transcript-api
This Python library fetches YouTube's closed-caption data directly. It was chosen because:
- It requires no YouTube Data API key or authentication
- It handles multiple languages and both manual and auto-generated captions
- It is lightweight — just a network request and XML parsing under the hood

### python-dotenv
Loads environment variables from a `.env` file during local development. This keeps API keys out of the source code. In production (Streamlit Cloud), secrets are injected directly by the platform instead.

### Llama 3.1 8B (default model)
Meta's open-source language model, running on Groq's infrastructure. The 8B (8 billion parameter) variant was chosen as the default because:
- It is fast enough to respond in 2–5 seconds
- It handles summarisation tasks with high quality
- It fits comfortably within Groq's free tier limits
- The 70B variant is available in the model selector for users who want higher quality output on complex videos

---

## 6. Key Engineering Decisions

### Why truncate at 28,000 characters instead of using the full transcript?
Language models have a fixed "context window" — a maximum amount of text they can process in one request. For Llama 3.1 8B on Groq, the practical limit for reliable output is around 8,000 tokens (roughly 32,000 characters). By clipping at 28,000 characters, the app leaves room for the prompt instructions and the model's response without hitting errors.

For a 1-hour video with roughly 8,000–10,000 words, the full transcript fits. For videos longer than about 2 hours, the tail is cut off. This is a deliberate trade-off: partial coverage of a very long video is still more useful than an error.

**What this means in practice:**
- Videos under ~90 minutes: full transcript is used
- Videos over ~90 minutes: the first 28,000 characters are used, and a note is appended to the transcript telling the model it was truncated
- The summary will still be accurate for the portion of content that was processed

### Why use a structured prompt format?
The prompt explicitly tells the model to use headers (`## Summary`, `## Key Takeaways`, `## Questions to Explore`) and numbered lists. Without this, the model might produce valid content but in an unpredictable format — sometimes a paragraph, sometimes bullet points, sometimes nothing labelled at all.

By enforcing the format in the prompt, the output is always consistent and renders cleanly in Streamlit's markdown display.

### Why prefer manually created transcripts over auto-generated ones?
YouTube has two types of captions: ones uploaded by the video creator (manually created) and ones generated automatically by YouTube's speech recognition (auto-generated). Manual transcripts are more accurate — auto-generated ones can mis-transcribe technical terms, names, and domain-specific vocabulary. The app tries manual English first, then auto-generated English, then any available language, in that priority order.

### Why no database or user accounts?
For a portfolio project that demonstrates AI skills, adding a database would introduce complexity without adding demonstrable value. The app is stateless by design: simpler to deploy, simpler to maintain, and no privacy concerns around storing what users have searched.

---

## 7. Known Limitations

### Long videos are truncated
As described above, videos longer than roughly 90 minutes will have their transcripts cut off. The summary covers only the first portion of the video. A future improvement would be to split the transcript into chunks, summarise each chunk separately, and then produce a final summary from the chunk summaries — a technique called **map-reduce summarisation**.

### Videos without captions cannot be processed
Some videos have no captions at all — certain music videos, livestreams, and videos in languages that YouTube's auto-captioning does not support. The app handles this gracefully with a clear error message, but it cannot process these videos. A future improvement would be to download the audio and run a speech-to-text model (such as OpenAI Whisper) to generate the transcript locally.

### The summary quality depends on the transcript quality
If YouTube's auto-generated captions are inaccurate (common for heavy accents, fast speech, or technical vocabulary), the AI summary will reflect those inaccuracies. The AI is reading the transcript, not the audio. Garbage in, garbage out.

### Rate limits on the free tier
Groq's free tier allows 30 requests per minute and 14,400 requests per day per model. For personal use or a demo, this is more than enough. If the app were deployed publicly at scale, a paid plan or request queuing system would be needed.

---

## 8. How to Run It Yourself

### Requirements
- Python 3.10 or higher
- A free Groq API key from [console.groq.com](https://console.groq.com) — no credit card needed

### Local setup
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/youtube-video-summarizer.git
cd youtube-video-summarizer

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac / Linux

# Install dependencies
pip install -r requirements.txt

# Add your API key
copy .env.example .env       # Windows
cp .env.example .env         # Mac / Linux
# Then open .env and set: GROQ_API_KEY=your_key_here

# Run
streamlit run app.py
```

### Deploy to Streamlit Cloud (free)
1. Push the repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub account
3. Select the repo, set main file to `app.py`
4. Under **Advanced settings → Secrets**, add: `GROQ_API_KEY = "your_key_here"`
5. Click Deploy — live in ~2 minutes

---

## 9. Recruiter Q&A — AI Engineer Role

These are the questions a technical recruiter or hiring manager is likely to ask about this project. Honest, direct answers are given below.

---

**Q: What problem does this solve and why does it matter?**

A: It solves the "preview problem" for YouTube content — the fact that you have to invest time watching a video before knowing if it's worth watching. This matters because it represents a broader class of real-world AI problems: taking unstructured, time-intensive content (video, audio, long documents) and converting it into structured, scannable information. The same architecture — fetch content, clean it, prompt an LLM, return structured output — applies to summarising meeting transcripts, legal documents, research papers, and customer support tickets.

---

**Q: Why Groq instead of OpenAI or Anthropic?**

A: Three reasons. First, Groq is free with no credit card, which makes the project fully reproducible by anyone. Second, Groq's hardware runs models significantly faster than GPU-based providers — responses come back in 2–3 seconds versus 8–15 seconds on comparable models elsewhere. Third, using an open-source model (Llama) rather than a proprietary one (GPT, Claude) is relevant to production AI engineering, where cost, transparency, and the ability to self-host matter.

---

**Q: What is prompt engineering and how did you apply it here?**

A: Prompt engineering is the practice of writing instructions to a language model that reliably produce the output format and quality you need. Here it means writing a prompt that: specifies the exact sections to output (Summary, Key Takeaways, Questions), specifies the length of each section, uses markdown headers so the output renders cleanly, and tells the model its role ("you are an expert at analysing transcripts"). Without this structure, the model produces valid but inconsistent output — sometimes a paragraph, sometimes bullet points, in no predictable order. Good prompt engineering is the difference between an AI feature that works reliably and one that works sometimes.

---

**Q: How would you handle a 3-hour video?**

A: The current approach clips at 28,000 characters, which covers roughly 90 minutes. For longer content, the right solution is **map-reduce summarisation**: split the transcript into overlapping chunks of a fixed size, summarise each chunk independently, then send all the chunk summaries together for a final synthesis pass. This keeps every individual request within the model's context window while covering the full content. I have not implemented this yet because it adds complexity and the current approach handles the most common case well, but it is the natural next step.

---

**Q: What would you change if this needed to handle 10,000 users per day?**

A: Several things. First, add a request queue so simultaneous users do not all hit the Groq API at the same moment. Second, add caching — if two users paste the same URL, the second request should return the stored result rather than calling the API again. A simple Redis cache with the video ID as the key would handle this. Third, move to a paid Groq plan or self-host the model on a GPU instance to remove the free tier rate limits. Fourth, add error monitoring (Sentry or similar) so failures are logged and visible.

---

**Q: What are the ethical considerations of a tool like this?**

A: A few worth mentioning. First, this tool only works with public content — it does not bypass any access controls. Second, users should be aware that AI summaries can miss nuance, misrepresent complex arguments, or reflect inaccuracies in the original transcript. It is a starting point, not a replacement for engaging with the source material. Third, the transcript data passes through Groq's servers, so users should not use this tool for confidential or sensitive video content. For a production deployment, the terms of service and privacy policy should be explicit about this.

---

**Q: How is the API key kept secure?**

A: Locally, the key is stored in a `.env` file which is listed in `.gitignore` — it is never committed to the repository. In production on Streamlit Cloud, the key is stored in the platform's encrypted secrets manager and injected as an environment variable at runtime. The app reads it with `os.getenv("GROQ_API_KEY")`. The key is never logged, never displayed in the UI, and never included in any response sent to the browser.

---

**Q: What did you learn building this?**

A: A few concrete things. The YouTube transcript API went through a major breaking version change (0.6.x to 1.x) mid-development, which meant debugging an XML parsing error and rewriting the transcript-fetching code for the new API. Google's Gemini free tier turned out to have a quota of zero for the model I initially chose, which is a good lesson about not assuming "free tier" means usable without verification. Switching to Groq was actually an improvement — faster, genuinely free, and with a simpler API. These kinds of real-world debugging problems are more representative of production AI engineering than tutorials suggest.

---

*Documentation written by M. Last updated May 2026.*
