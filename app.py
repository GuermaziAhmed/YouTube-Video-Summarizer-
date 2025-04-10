import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from io import BytesIO
import whisper
import yt_dlp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ------------- Téléchargement Audio -------------
def download_audio(url, output_path="audio.wav", progress_callback=None):
    def progress_hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes > 0 and progress_callback:
                percent = int((downloaded_bytes / total_bytes) * 100)
                progress_callback(percent, f"Download Progress: {percent}%")
        elif d['status'] == 'finished' and progress_callback:
            progress_callback(100, "Download Progress: 100%")

    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': output_path,
        'progress_hooks': [progress_hook],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(output_path):
            logging.info(f"Audio downloaded successfully: {output_path}")
            return output_path
        else:
            logging.error("Failed to download audio.")
            return None
    except Exception as e:
        logging.error(f"Error downloading audio: {e}")
        return None

# ------------- Transcription -------------
def transcribe_audio(audio_path):
    logging.info("Transcribing audio...")
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        logging.info("Transcription complete!")
        return result["text"]
    except Exception as e:
        logging.error(f"Error during transcription: {str(e)}")
        return None

# ------------- Résumé -------------
def summarize_transcript_gemini(transcript, length, style, language):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ GEMINI_API_KEY not set.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-preview")

    length_map = {
        "Short": "in 2-3 lines.",
        "Medium": "in 5-6 lines.",
        "Long": "with as much detail as possible."
    }

    style_map = {
        "Standard": "",
        "Bullet Points": "Format the summary as bullet points.",
        "Simple Language": "Use very simple and clear language.",
        "Professional": "Use a formal tone suitable for business or reporting."
    }

    prompt = f"""
    Please summarize the following transcript {length_map[length]} {style_map[style]}
    Answer in {language}.
    Transcript: {transcript}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response.candidates else None
    except Exception as e:
        st.error(f"❌ Error summarizing: {str(e)}")
        return None

# ------------- Questions -------------
def ask_question_about_video(transcript, question, language):
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-lite-preview")

    prompt = f"""
    Based on this transcript, answer the question in {language}:
    Transcript: {transcript}
    Question: {question}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"❌ Error answering question: {str(e)}")
        return None

# ------------- Text-to-Speech -------------
def generate_tts(summary, language_code):
    try:
        tts = gTTS(summary, lang=language_code)
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        return mp3_fp
    except Exception as e:
        st.error(f"❌ Error with text-to-speech: {str(e)}")
        return None

# ------------- Traitement Principal -------------
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

# ------------- Main App Streamlit -------------
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
