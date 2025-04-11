import yt_dlp
import whisper
import os
import logging

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
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        
        'preferredquality': '160',  # Lower bitrate = smaller file
    }],
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
def transcribe_audio(audio_path):
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        logging.error(f"Transcription error: {e}")
        return None