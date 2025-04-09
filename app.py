import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from gtts import gTTS
import os
from io import BytesIO
import requests

# ------------- Transcript Extraction using YouTube Transcript API -------------
def get_video_transcript(video_url):
    try:
        # Extract video ID
        video_id = video_url.split("v=")[1].split("&")[0]
        
        # First attempt: Try direct YouTube Transcript API
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = " ".join([entry["text"] for entry in transcript_list])
            return transcript
        except Exception as direct_error:
            st.warning("⚠️ Direct transcript extraction failed, trying alternative method...")
            
            # Second attempt: Use a free public API that provides transcript service
            try:
                # Using a public API service that returns transcripts
                api_url = f"https://youtubetranscript.com/?server_vid={video_id}"
                response = requests.get(api_url)
                
                if response.status_code == 200:
                    # Parse the response to extract the transcript text
                    data = response.json()
                    if "text" in data:
                        return data["text"]
                    else:
                        st.error("❌ No transcript data found in the response.")
                        return None
                else:
                    st.error(f"❌ API request failed with status code: {response.status_code}")
                    return None
            except Exception as api_error:
                st.error(f"❌ Alternative method failed: {str(api_error)}")
                
                # Third attempt: Manual input
                st.error("❌ All automated transcript methods failed.")
                st.info("💡 You can manually paste the transcript below:")
                
                manual_transcript = st.text_area("Manual Transcript Input", height=200)
                if manual_transcript and len(manual_transcript) > 50:  # Ensure it's not empty or too short
                    return manual_transcript
                return None
    except Exception as e:
        st.error(f"❌ Error extracting transcript: {str(e)}")
        return None

# ------------- Summarization via Gemini -------------
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
        if not response.candidates:
            st.error("⚠️ No response candidates returned by Gemini.")
            return None
        return response.text.strip()
    except Exception as e:
        st.error(f"❌ Error summarizing: {str(e)}")
        return None

# ------------- Ask a Question -------------
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

# ------------- Main App -------------
def main():
    st.set_page_config(page_title="🎬 YouTube Summarizer+", layout="centered")
    st.title("📽️ YouTube Video Summarizer+")
    st.markdown("💡 Summarize, ask questions, download or listen to any YouTube video content.")

    # --- Session state initialization ---
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
            transcript = get_video_transcript(video_url)
            if transcript:
                st.session_state["transcript"] = transcript

                with st.expander("📜 Full Transcript"):
                    st.write(transcript)

                summary = summarize_transcript_gemini(transcript, length, style, language)
                if summary:
                    st.session_state["summary"] = summary
                else:
                    st.session_state["summary"] = None
            else:
                st.warning("⚠️ Failed to extract transcript.")
        else:
            st.warning("👉 Please enter a YouTube URL.")

    # --- Display Summary if exists ---
    if st.session_state.get("summary"):
        st.success("✅ Summary:")
        st.write(st.session_state["summary"])

        # Download as .txt
        st.download_button("📥 Download Summary (.txt)", st.session_state["summary"], file_name="summary.txt")

        # Text-to-Speech
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
