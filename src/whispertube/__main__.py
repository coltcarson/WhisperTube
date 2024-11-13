"""Command-line interface for WhisperTube."""

import os
import tempfile
from dotenv import load_dotenv
from . import (
    download_youtube_video,
    transcribe_audio,
    summarize_transcription,
    save_transcription,
)

def main():
    """Main function to orchestrate downloading, transcribing, summarizing, and saving a YouTube video's audio."""
    # Load environment variables
    load_dotenv()

    # Get the YouTube URL from user input
    url = input("Enter the YouTube URL: ")

    # Create a temporary directory for audio files
    with tempfile.TemporaryDirectory() as temp_dir:
        print("\nDownloading video...")
        audio_path, video_title = download_youtube_video(url, temp_dir)

        if not audio_path or not video_title:
            print("Failed to download video. Please check the URL and try again.")
            return

        print("\nTranscribing audio...")
        transcription = transcribe_audio(audio_path)

        if not transcription:
            print("Failed to transcribe audio.")
            return

        print("\nSummarizing transcription...")
        summary = summarize_transcription(transcription)

        if not summary:
            print("Failed to summarize transcription.")
            # Continue anyway, as we still have the transcription

        # Save both the transcription and summary
        current_dir = os.getcwd()
        save_transcription(transcription, summary, current_dir, video_title)

if __name__ == "__main__":
    main()
