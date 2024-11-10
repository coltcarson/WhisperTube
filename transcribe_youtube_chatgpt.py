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
            video_title = (
                re.sub(r"[^a-zA-Z0-9\s]", "_", video_title).strip().replace(" ", "_")
            )
        return os.path.join(output_path, "audio.wav"), video_title
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
    if ffmpeg_location:
        os.environ["PATH"] += os.pathsep + ffmpeg_location

    model = whisper.load_model("base")
    with tqdm(total=100, desc="Transcribing Audio", unit="%") as pbar:
        result = model.transcribe(file_path)
        pbar.update(100)
    return result["text"]


def summarize_transcription(transcription: str) -> Optional[str]:
    """
    Use OpenAI's GPT-4o-mini model to summarize and enhance the transcription.

    Args:
        transcription (str): The transcription text to be summarized.

    Returns:
        Optional[str]: The summarized transcription text, or None if an error occurs.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = (
        "Please summarize and enhance the following transcript to make it more concise, engaging, and logically coherent. Assume the transcription may contain inaccuracies, especially in mathematical expressions. Correct any apparent errors and reformat all formulas using LaTeX syntax within Markdown for proper rendering in VSCode. Use inline math (e.g., $x^2 + y^2 = z^2$) for simple expressions and separate code blocks with double dollar signs ($$...$$) for complex equations. Structure the summary with clear explanations, headings, bullet points, and formatted code blocks for readability.:\n"
        + transcription
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=16384,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
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


def main() -> None:
    """
    Main function to orchestrate downloading, transcribing, summarizing, and saving a YouTube video's audio.
    """
    youtube_url = input("Enter YouTube video URL: ")
    ffmpeg_location = input("Enter ffmpeg location (or press Enter to use default): ")
    ffmpeg_location = ffmpeg_location if ffmpeg_location.strip() else None

    # Verify ffmpeg_location if provided
    if ffmpeg_location and not shutil.which(os.path.join(ffmpeg_location, "ffmpeg")):
        print(f"The specified ffmpeg location '{ffmpeg_location}' is not valid.")
        return

    # Create a temporary directory to hold files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Step 1: Download the video as audio and extract title
        with tqdm(total=100, desc="Downloading YouTube Video", unit="%") as pbar:
            audio_file, video_title = download_youtube_video(
                youtube_url, output_path=temp_dir, ffmpeg_location=ffmpeg_location
            )
            pbar.update(100)
        if not audio_file:
            return

        # Step 2: Transcribe using Whisper
        transcription = transcribe_audio(audio_file, ffmpeg_location=ffmpeg_location)
        print("Transcription completed successfully.")

        # Step 3: Summarize using OpenAI's GPT-4o-mini model
        summary = summarize_transcription(transcription)
        if summary:
            print("Summary completed successfully.")

        # Step 4: Save transcription and summary to transcripts folder in local directory
        save_transcription(
            transcription, summary, output_path=os.getcwd(), video_title=video_title
        )


if __name__ == "__main__":
    main()
