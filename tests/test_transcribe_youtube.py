import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from whispertube import (
    download_youtube_video,
    save_transcription,
    summarize_transcription,
    transcribe_audio,
)


def test_download_youtube_video(temp_dir, mock_video_info):
    url = "https://www.youtube.com/watch?v=test123"

    with patch("yt_dlp.YoutubeDL") as mock_ydl:
        # Configure the mock
        mock_ydl_instance = Mock()
        mock_ydl_instance.extract_info.return_value = mock_video_info
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        # Call the function
        audio_path, video_title = download_youtube_video(url, temp_dir)

        # Verify the function called YoutubeDL with correct parameters
        mock_ydl.assert_called_once()
        assert mock_ydl_instance.extract_info.called_with(url, download=True)


@patch("whisper.load_model")
@patch("os.path.exists")
def test_transcribe_audio(mock_path_exists, mock_load_model, sample_audio_path):
    # Configure the mocks
    mock_path_exists.return_value = True  # Simulate file exists
    mock_model = Mock()
    mock_model.transcribe.return_value = {"text": "Test transcription"}
    mock_load_model.return_value = mock_model

    # Call the function
    result = transcribe_audio(sample_audio_path)

    # Verify the results
    assert result == "Test transcription"
    mock_load_model.assert_called_once_with("base")
    mock_model.transcribe.assert_called_once_with(sample_audio_path)


@patch("openai.ChatCompletion.create")
def test_summarize_transcription(mock_chat_completion, mock_transcription):
    # Configure the mock to match the actual OpenAI API response structure
    mock_chat_completion.return_value = {
        "choices": [{"message": {"content": "Summarized content"}}]
    }

    # Call the function
    result = summarize_transcription(mock_transcription)

    # Verify the results
    assert result == "Summarized content"

    # Verify the API was called with correct parameters
    mock_chat_completion.assert_called_once_with(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": "Please summarize and enhance the following transcript to make it more concise, engaging, and logically coherent. Assume the transcription may contain inaccuracies, especially in mathematical expressions. Correct any apparent errors and reformat all formulas using LaTeX syntax within Markdown for proper rendering in VSCode. Use inline math (e.g., $x^2 + y^2 = z^2$) for simple expressions and separate code blocks with double dollar signs ($$...$$) for complex equations. Structure the summary with clear explanations, headings, bullet points, and formatted code blocks for readability.:\n"
                + mock_transcription,
            }
        ],
        max_tokens=16384,
        temperature=0.7,
    )


def test_save_transcription(temp_dir, mock_transcription, mock_summary):
    video_title = "test_video"

    # Call the function
    save_transcription(mock_transcription, mock_summary, temp_dir, video_title)

    # Check if the transcripts directory was created
    transcripts_dir = os.path.join(temp_dir, "transcripts")
    assert os.path.exists(transcripts_dir)

    # List files in the transcripts directory
    files = os.listdir(transcripts_dir)
    assert len(files) == 1  # Should have exactly one file

    # Check if the file starts with the video title
    saved_file = files[0]
    assert saved_file.startswith(f"{video_title}_transcription_summary_")
    assert saved_file.endswith(".md")

    # Verify file contents
    with open(os.path.join(transcripts_dir, saved_file), "r") as f:
        content = f.read()
        assert mock_summary in content
        assert mock_transcription in content
