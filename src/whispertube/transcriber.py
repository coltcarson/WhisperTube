"""Core functionality for downloading, transcribing, and summarizing YouTube videos."""

import os
import whisper
import tempfile
import subprocess
from tqdm import tqdm
import yt_dlp
import shutil
import openai
import datetime
from dotenv import load_dotenv
import re
from typing import Optional, Tuple

# Load environment variables from .env file
load_dotenv()


def download_youtube_video(
    url: str, output_path: str, ffmpeg_location: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Download a YouTube video as a WAV file using yt-dlp.

    Args:
        url (str): The URL of the YouTube video to download.
        output_path (str): The directory where the audio file should be saved.
        ffmpeg_location (Optional[str]): The location of the ffmpeg executable. Defaults to None.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the path to the downloaded audio file and the video title.
                                            Returns (None, None) if an error occurs.
    """
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_path, "audio.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                }
            ],
        }
        if ffmpeg_location:
            ydl_opts["ffmpeg_location"] = ffmpeg_location

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_title = info.get("title", "Unknown Title").lower()
            # Replace any characters that are not valid for filenames with an underscore
            video_title = re.sub(r'[^\w\-_]', '_', video_title)
            audio_path = os.path.join(output_path, "audio.wav")
            return audio_path, video_title

    except Exception as e:
        print(f"An error occurred while downloading the video: {e}")
        return None, None


def transcribe_audio(file_path: str, ffmpeg_location: Optional[str] = None) -> str:
    """
    Transcribe an audio file using the Whisper model.

    Args:
        file_path (str): The path to the audio file to transcribe.
        ffmpeg_location (Optional[str]): The location of the ffmpeg executable. Defaults to None.

    Returns:
        str: The transcribed text from the audio file.
    """
    try:
        if ffmpeg_location:
            os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_location)

        model = whisper.load_model("base")
        result = model.transcribe(file_path)
        return result["text"]

    except Exception as e:
        print(f"An error occurred while transcribing the audio: {e}")
        return ""


def summarize_transcription(transcription: str) -> Optional[str]:
    """
    Use OpenAI's GPT model to summarize and enhance the transcription.

    Args:
        transcription (str): The transcription text to be summarized.

    Returns:
        Optional[str]: The summarized transcription text, or None if an error occurs.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes transcriptions while preserving the key information.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize this transcription, highlighting the main points and key information:\n\n{transcription}",
                },
            ],
        )

        return response.choices[0].message["content"]

    except Exception as e:
        print(f"An error occurred while summarizing the transcription: {e}")
        return None


def save_transcription(
    transcription: str, summary: Optional[str], output_path: str, video_title: str
) -> None:
    """
    Save the original transcription and its summary to a Markdown file.

    Args:
        transcription (str): The transcription text to be saved.
        summary (Optional[str]): The summarized transcription text, if available.
        output_path (str): The directory where the Markdown file should be saved.
        video_title (str): The title of the YouTube video.
    """
    transcripts_folder = os.path.join(output_path, "transcripts")
    os.makedirs(transcripts_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{video_title}_transcription_summary_{timestamp}.md"
    file_path = os.path.join(transcripts_folder, file_name)
    try:
        with open(file_path, "w") as file:
            if summary:
                file.write(summary)
            file.write("\n\n")
            file.write("# Original Transcription\n\n")
            file.write(transcription + "\n\n")

        print(f"Transcription and summary saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the transcription: {e}")
