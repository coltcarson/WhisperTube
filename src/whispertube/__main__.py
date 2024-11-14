"""Command-line interface for WhisperTube."""

import argparse
import os
import tempfile
from getpass import getpass

from dotenv import load_dotenv

from . import (
    download_youtube_video,
    save_transcription,
    summarize_transcription,
    transcribe_audio,
)


def get_openai_key() -> str:
    """
    Get the OpenAI API key from various sources in order of precedence:
    1. Command line argument
    2. Environment variable
    3. .env file
    4. User input
    """
    # Try environment variable first (includes .env file if loaded)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        # Prompt user for API key
        print("\nOpenAI API key not found in environment variables or .env file.")
        print(
            "You can get your API key from https://platform.openai.com/account/api-keys"
        )
        api_key = getpass("Please enter your OpenAI API key (input will be hidden): ")

        # Save to environment variable for this session
        os.environ["OPENAI_API_KEY"] = api_key

        # Ask if user wants to save to .env file
        save = input(
            "\nWould you like to save your API key to a .env file for future use? (y/n): "
        ).lower()
        if save == "y":
            env_path = os.path.join(os.getcwd(), ".env")
            with open(env_path, "a") as f:
                f.write(f"\nOPENAI_API_KEY={api_key}")
            print(f"API key saved to {env_path}")

    return api_key


def main():
    """Main function to orchestrate downloading, transcribing, summarizing, and saving a YouTube video's audio."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Transcribe and summarize YouTube videos"
    )
    parser.add_argument("--url", "-u", help="YouTube video URL")
    parser.add_argument("--api-key", "-k", help="OpenAI API key")
    parser.add_argument(
        "--output-dir",
        "-o",
        help="Output directory for transcripts (default: current directory)",
        default=os.getcwd(),
    )
    args = parser.parse_args()

    # Load environment variables from .env file if it exists
    load_dotenv(override=True)

    # Set API key if provided as argument
    if args.api_key:
        os.environ["OPENAI_API_KEY"] = args.api_key
    else:
        # Get API key through our helper function
        get_openai_key()

    # Get the YouTube URL
    url = args.url
    while not url:
        url = input("Enter the YouTube URL: ")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

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
        save_transcription(transcription, summary, args.output_dir, video_title)


def run():
    """Entry point for the console script."""
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("If this persists, please report the issue on GitHub.")


if __name__ == "__main__":
    run()
