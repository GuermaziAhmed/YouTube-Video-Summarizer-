import google.generativeai as genai
import os


def summarize_transcript_gemini(transcript, length, style, language):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
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
        return None