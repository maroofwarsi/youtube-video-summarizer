"""
YouTube Video Summarizer
========================
Paste any public YouTube URL and get back:
  - A concise summary
  - 5 key takeaways
  - 5 questions to deepen your understanding

Powered by: youtube-transcript-api v1.x + Groq (free, no credit card)
"""

import os
import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript,
)
from groq import Groq, RateLimitError, AuthenticationError, APIStatusError
from dotenv import load_dotenv

load_dotenv()

# ── Helpers ───────────────────────────────────────────────────────────────────

def extract_video_id(url: str) -> str | None:
    """Extract the 11-character YouTube video ID from any common URL format."""
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[&?#]|$)",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"embed\/([0-9A-Za-z_-]{11})",
        r"shorts\/([0-9A-Za-z_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id: str) -> str:
    """Fetch the full transcript for a video ID using youtube-transcript-api v1.x."""
    api = YouTubeTranscriptApi()
    transcript_list = api.list(video_id)
    try:
        transcript = transcript_list.find_manually_created_transcript(["en"])
    except NoTranscriptFound:
        try:
            transcript = transcript_list.find_generated_transcript(["en"])
        except NoTranscriptFound:
            transcript = next(iter(transcript_list))
    fetched = transcript.fetch()
    return " ".join(snippet.text for snippet in fetched)


def truncate_transcript(text: str, max_chars: int = 28_000) -> str:
    """Keep transcript within the model's context window."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[Transcript truncated for length]"


def build_prompt(transcript: str) -> str:
    return f"""You are an expert at analysing video transcripts and extracting the most valuable insights.

Below is the transcript of a YouTube video. Please provide:

1. **Summary** (3-5 sentences): A clear, concise overview of what the video is about.

2. **5 Key Takeaways**: The most important points, lessons, or facts from the video. Each takeaway should be 1-2 sentences.

3. **5 Questions You Could Ask**: Thoughtful questions a curious viewer might ask after watching - useful for further research, interviews, or deeper study.

Format your response exactly like this:

## Summary
[Your summary here]

## Key Takeaways
1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]
4. [Takeaway 4]
5. [Takeaway 5]

## Questions to Explore
1. [Question 1]
2. [Question 2]
3. [Question 3]
4. [Question 4]
5. [Question 5]

---
Transcript:
{transcript}
"""


def get_groq_response(api_key: str, prompt: str, model: str) -> str:
    """Send the prompt to Groq and return the response text."""
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="YouTube Video Summarizer",
    page_icon="▶️",
    layout="centered",
)

st.markdown(
    """
    <h1 style='text-align:center;'>▶️ YouTube Video Summarizer</h1>
    <p style='text-align:center; color:#AAAAAA;'>
        Paste any YouTube URL - get a summary, key takeaways, and questions in seconds.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────

api_key = os.getenv("GROQ_API_KEY", "")

with st.sidebar:
    st.header("Configuration")

    if not api_key:
        api_key = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_...",
            help="Free key at https://console.groq.com - no credit card needed",
        )
        st.caption(
            "Get your free key at [console.groq.com](https://console.groq.com). "
            "No credit card required."
        )
    else:
        st.success("API key loaded from environment")

    st.divider()

    selected_model = st.selectbox(
        "Model",
        options=[
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
        ],
        index=0,
        help=(
            "llama-3.1-8b-instant: fastest, great for most videos\n"
            "llama-3.3-70b-versatile: smarter, best for complex content\n"
            "mixtral-8x7b-32768: large context window"
        ),
    )
    st.caption("All models are **free** on Groq's free tier.")

    st.divider()
    st.markdown("**How it works**")
    st.markdown(
        """
        1. Paste a YouTube URL
        2. The app fetches the video transcript
        3. An LLM reads it and produces:
           - A summary
           - 5 key takeaways
           - 5 questions to explore
        """
    )
    st.divider()
    st.markdown("Powered by [Groq](https://groq.com) + [Llama](https://llama.meta.com)")

# ── Main input ────────────────────────────────────────────────────────────────

url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed",
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    summarise_btn = st.button(
        "Summarise Video", use_container_width=True, type="primary"
    )

# ── Processing ────────────────────────────────────────────────────────────────

if summarise_btn:
    if not api_key:
        st.error(
            "Please enter your Groq API key in the sidebar. "
            "Get one free at https://console.groq.com"
        )
        st.stop()

    if not url.strip():
        st.warning("Please paste a YouTube URL above.")
        st.stop()

    video_id = extract_video_id(url.strip())
    if not video_id:
        st.error(
            "Couldn't recognise that as a YouTube URL. "
            "Try formats like youtube.com/watch?v=... or youtu.be/..."
        )
        st.stop()

    with st.status("Fetching transcript...", expanded=True) as status:
        try:
            st.write("Extracting video transcript...")
            transcript = get_transcript(video_id)
            word_count = len(transcript.split())
            st.write(f"Got transcript - {word_count:,} words")

            st.write(f"Sending to {selected_model}...")
            prompt = build_prompt(truncate_transcript(transcript))
            result = get_groq_response(api_key, prompt, selected_model)
            st.write("Analysis complete!")
            status.update(label="Done!", state="complete")

        except VideoUnavailable:
            st.error("This video is unavailable or private.")
            st.stop()
        except TranscriptsDisabled:
            st.error(
                "Transcripts are disabled for this video. "
                "Try a different video - most tutorials, talks, and lectures have them."
            )
            st.stop()
        except NoTranscriptFound:
            st.error("No transcript found for this video.")
            st.stop()
        except CouldNotRetrieveTranscript as e:
            st.error(f"Could not retrieve transcript: {e}")
            st.stop()
        except AuthenticationError:
            st.error(
                "Invalid Groq API key. "
                "Double-check you copied the full key from console.groq.com"
            )
            st.stop()
        except RateLimitError:
            st.error(
                "Groq rate limit hit. Wait a moment and try again - "
                "the free tier allows 30 requests/minute."
            )
            st.stop()
        except APIStatusError as e:
            st.error(f"API error: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    st.divider()

    st.image(
        f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg",
        use_column_width=True,
    )

    st.divider()
    st.markdown(result)

    st.divider()
    st.download_button(
        label="Download as text",
        data=result,
        file_name="video_summary.txt",
        mime="text/plain",
    )

# ── Empty state ───────────────────────────────────────────────────────────────

if not summarise_btn:
    st.markdown(
        """
        <div style='text-align:center; padding: 3rem 0; color:#666;'>
            <p style='font-size:3rem;'>🎬</p>
            <p>Paste a YouTube URL above and click <strong>Summarise Video</strong></p>
            <p style='font-size:0.85rem;'>Works with tutorials, lectures, talks, podcasts - any video with captions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
