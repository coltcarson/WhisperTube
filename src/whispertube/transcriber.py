"""Core functionality for downloading, transcribing, and summarizing YouTube videos."""

import datetime
import logging
import os
import re
from typing import Any, Dict, Optional, Tuple

import openai
import whisper
import yt_dlp
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def download_youtube_video(
    url: str, output_path: str, ffmpeg_location: Optional[str] = None
) -> Tuple[Optional[str], Optional[str]]:
    """Download a YouTube video's audio in WAV format.

    Args:
        url: YouTube video URL to download.
        output_path: Directory where the audio file should be saved.
        ffmpeg_location: Optional path to ffmpeg executable.

    Returns:
        A tuple containing:
        - Path to the downloaded audio file (or None if failed)
        - Video title (or None if failed)

    Raises:
        ValueError: If URL or output path is invalid.
        Exception: If download or conversion fails.
    """
    try:
        ydl_opts: Dict[str, Any] = {
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
            video_title = re.sub(r"[^\w\-_]", "_", video_title)
            audio_path = os.path.join(output_path, "audio.wav")
            return audio_path, video_title

    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return None, None


def transcribe_audio(
    file_path: str, ffmpeg_location: Optional[str] = None, model_name: str = "base"
) -> str:
    """Transcribe an audio file using OpenAI's Whisper model.

    Args:
        file_path: Path to the audio file to transcribe.
        ffmpeg_location: Optional path to ffmpeg executable.
        model_name: Whisper model to use (default: "base").

    Returns:
        Transcribed text from the audio file.

    Raises:
        FileNotFoundError: If audio file doesn't exist.
        Exception: If transcription fails.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        if ffmpeg_location:
            os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_location)

        model = whisper.load_model(model_name)
        result = model.transcribe(file_path)
        return result["text"]

    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return ""


def summarize_transcription(transcription: str) -> Optional[str]:
    """Summarize and enhance a transcription using GPT-4.

    This function processes the transcription to:
    1. Make it more concise and engaging
    2. Correct potential transcription errors
    3. Format mathematical expressions using LaTeX
    4. Structure the content with proper Markdown formatting

    Args:
        transcription: Raw transcription text to process.

    Returns:
        Enhanced and summarized version of the transcription,
        or None if summarization fails.

    Raises:
        ValueError: If API key is missing or invalid.
        Exception: If API call fails.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        prompt = (
            "Please summarize and enhance the following transcript. "
            "Make it concise and engaging, correct any errors, and format "
            "mathematical expressions using LaTeX within Markdown. Use inline "
            "math (e.g., $x^2 + y^2 = z^2$) for simple expressions and "
            "separate code blocks with double dollar signs ($$...$$) for "
            "complex equations. Structure with headings and bullet points.\n\n"
            f"{transcription}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16384,
            temperature=0.7,
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.error(f"Error summarizing transcription: {str(e)}")
        return None


def save_transcription(
    transcription: str, summary: Optional[str], output_path: str, video_title: str
) -> None:
    """Save transcription and summary to a Markdown file.

    Args:
        transcription: Original transcription text.
        summary: Optional enhanced and summarized version.
        output_path: Directory where to save the file.
        video_title: Title of the video (used in filename).

    Raises:
        ValueError: If output path is invalid.
        IOError: If file creation fails.
    """
    try:
        video_title = re.sub(r"[^\w\-_]", "_", video_title)
        transcripts_folder = os.path.join(output_path, "transcripts")
        os.makedirs(transcripts_folder, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{video_title}_transcription_summary_{timestamp}.md"
        file_path = os.path.join(transcripts_folder, file_name)

        with open(file_path, "w") as file:
            if summary:
                file.write(summary)
            file.write("\n\n")
            file.write("# Original Transcription\n\n")
            file.write(transcription + "\n\n")

        logger.info(f"Transcription and summary saved to {file_path}")

    except Exception as e:
        logger.error(f"Error saving transcription: {str(e)}")
