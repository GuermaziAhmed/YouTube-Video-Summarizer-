import streamlit as st
import logging
import os
from services.audio import download_audio, transcribe_audio
from services.ai import summarize_transcript_gemini, ask_question_about_video
from utils.helpers import generate_tts

# Configure logging
logging.basicConfig(level=logging.INFO)

def process_video(url):
    audio_path = "audio.wav"
    audio_path = download_audio(url, audio_path)
    if not audio_path:
        return None

    transcript = transcribe_audio(audio_path)

    # Clean up
    if os.path.exists(audio_path):
        os.remove(audio_path)

    return transcript

def main():
    st.set_page_config(page_title="🎬 YouTube Summarizer+", layout="centered")
    st.title("📽️ YouTube Video Summarizer+")
    st.markdown("💡 Summarize, ask questions, download or listen to any YouTube video content.")

    if "transcript" not in st.session_state:
        st.session_state["transcript"] = None
    if "summary" not in st.session_state:
        st.session_state["summary"] = None

    st.markdown("---")
    video_url = st.text_input("🔗 YouTube Video URL")

    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.selectbox("📏 Summary Length", ["Short", "Medium", "Long"])
    with col2:
        style = st.selectbox("🎨 Summary Style", ["Standard", "Bullet Points", "Simple Language", "Professional"])
    with col3:
        language = st.selectbox("🌍 Summary Language", ["English", "Français", "Español", "Deutsch", "Arabic"])

    language_code_map = {
        "English": "en", "Français": "fr", "Español": "es", "Deutsch": "de", "Arabic": "ar"
    }

    if st.button("🚀 Summarize"):
        if video_url:
            transcript = process_video(video_url)
            if transcript:
                st.session_state["transcript"] = transcript
                with st.expander("📜 Full Transcript"):
                    st.write(transcript)

                summary = summarize_transcript_gemini(transcript, length, style, language)
                if summary:
                    st.session_state["summary"] = summary
            else:
                st.warning("⚠️ Failed to extract transcript.")
        else:
            st.warning("👉 Please enter a YouTube URL.")

    if st.session_state.get("summary"):
        st.success("✅ Summary:")
        st.write(st.session_state["summary"])
        st.download_button("📥 Download Summary (.txt)", st.session_state["summary"], file_name="summary.txt")

        mp3 = generate_tts(st.session_state["summary"], language_code_map[language])
        if mp3:
            st.audio(mp3, format="audio/mp3")

    st.markdown("---")
    st.subheader("🧠 Ask a question about the video")
    question = st.text_input("❓ Your question")

    if st.button("🎯 Answer Question"):
        transcript = st.session_state.get("transcript")
        if question and transcript:
            answer = ask_question_about_video(transcript, question, language)
            if answer:
                st.info(answer)
        else:
            st.warning("📌 You need both a question and a transcript.")

if __name__ == "__main__":
    main()