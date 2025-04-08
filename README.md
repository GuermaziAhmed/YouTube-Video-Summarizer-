# 🎬 YouTube Video Summarizer+

A Streamlit app that extracts a YouTube video's transcript and generates a customizable summary using **Gemini Pro** (Google Generative AI). You can choose the summary length, style, and language. You can also ask questions about the content and even listen to the summary via text-to-speech.

![image](https://github.com/user-attachments/assets/5d8ebf1b-cfaa-4e36-b8d7-f6e0f726077a)


---

## 🚀 Features

- 🔍 **Extract YouTube Transcripts**
- 📝 **Summarize using Gemini AI**
- 🎯 **Choose Summary Style & Length**
- 🌍 **Multilingual Summaries** (English, Français, Español, Deutsch, Arabic)
- 🧠 **Ask Questions** about the video content
- 🔊 **Listen** to summaries with Text-to-Speech
- 📥 **Download** summaries as `.txt` files

---

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/youtube-summarizer.git
cd youtube-summarizer
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set your Gemini API Key**

Make sure to get an API key from [Google AI Studio](https://makersuite.google.com/app)  
Then create a `.env` file or set an environment variable:

```bash
export GEMINI_API_KEY=your_api_key_here  # On Windows: set GEMINI_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📄 Requirements

- Python 3.8+
- Streamlit
- google-generativeai
- youtube-transcript-api
- gTTS

You can install everything via:

```bash
pip install -r requirements.txt
```

---

## 📁 File Structure

```
📦youtube-summarizer
 ┣ 📜app.py                # Main Streamlit application
 ┣ 📜requirements.txt      # Python dependencies
 ┗ 📄README.md             # You're here!
```

---

## 🛠 To-Do / Ideas

- [ ] Export summaries as PDF
- [ ] Detect and use video title
- [ ] Add dark mode toggle
- [ ] Optional translation feature
- [ ] Deploy on Streamlit Cloud / Hugging Face Spaces

---

## 💡 Credits

Built using:
- [Streamlit](https://streamlit.io/)
- [Gemini Pro by Google](https://ai.google.dev/)
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- [gTTS - Google Text-to-Speech](https://pypi.org/project/gTTS/)

---

## 📬 Contact

Have suggestions or issues?  
 email me at `ahmed.guermazi@supcom.tn`

---

