# 🎬 YouTube Video Summarizer 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtube-video-summarizer-ahmed-guermazi.streamlit.app//)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered YouTube video processing system that provides intelligent summarization, Q&A capabilities, and audio conversion features.

![App Interface](https://via.placeholder.com/800x450.png?text=YouTube+Summarizer+Interface)

## 🌟 Key Features

| Feature                      | Technology Stack              |
|------------------------------|-------------------------------|
| YouTube Audio Extraction      | yt-dlp, FFmpeg                |
| AI-Powered Transcription      | OpenAI Whisper                |
| Smart Summarization           | Google Gemini Pro             |
| Multilingual Support          | 5 Languages                   |
| Text-to-Speech Conversion     | gTTS                          |
| Containerization Support      | Docker                        |

## 🛠️ Installation

### Method 1: Local Development
```bash
git clone https://github.com/GuermaziAhmed/YouTube-Video-Summarizer-.git
cd YouTube-Video-Summarizer-

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Method 2: Docker Container
```bash
# Build the Docker image
docker build -t yt-summarizer .

# Run the container
docker run -p 8501:8501 yt-summarizer
```

## ⚙️ Configuration
1. Obtain [Google Gemini API Key](https://ai.google.dev/)
2. Create `.env` file:
```ini
GEMINI_API_KEY=your_google_ai_key_here
```

## 📂 Project Structure
```
YouTube-Video-Summarizer-/
├── Dockerfile
├── requirements.txt
├── packages.txt
├── src/
│   ├── app.py            # Streamlit interface
│   ├── services/
│   │   ├── audio.py      # Audio processing
│   │   ├── ai.py         # AI integrations
│   │   └── __init__.py       
│   └── utils/
│       ├── __init__.py   
└──       └── helpers.py    # Utility functions
 
```

## 🚀 Launching the Application
```bash
# For local development
streamlit run src/app.py

# For Docker deployment
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key yt-summarizer
```

## 🌐 Live Demo
Experience the production version:  
[https://youtube-video-summarizer-ahmed-guermazi.streamlit.app/](https://youtube-video-summarizer-ahmed-guermazi.streamlit.app//)


## 🤝 Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open Pull Request

## 📜 License
Distributed under MIT License. See `LICENSE` for details.

## 📬 Contact
**Ahmed Guermazi**  
Email: [ahmed.guermazi@supcom.tn](mailto:ahmed.guermazi@supcom.tn)  
GitHub: [@GuermaziAhmed](https://github.com/GuermaziAhmed)
```
