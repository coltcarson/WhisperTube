"""Tests for WhisperTube's core functionality."""

import os
from unittest.mock import Mock, patch

from whispertube import (
    download_youtube_video,
    save_transcription,
    summarize_transcription,
    transcribe_audio,
)


def test_download_youtube_video(temp_dir, mock_video_info):
    """Test YouTube video download functionality."""
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
    """Test audio transcription functionality."""
    # Configure the mocks
    mock_path_exists.return_value = True
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
    """Test transcription summarization functionality."""
    # Configure the mock
    mock_chat_completion.return_value = {
        "choices": [{"message": {"content": "Summarized content"}}]
    }

    # Call the function
    result = summarize_transcription(mock_transcription)

    # Verify the results
    assert result == "Summarized content"

    # Verify API call parameters
    mock_chat_completion.assert_called_once()


def test_save_transcription(temp_dir, mock_transcription, mock_summary):
    """Test saving transcription and summary to file."""
    video_title = "test_video"

    # Call the function
    save_transcription(mock_transcription, mock_summary, temp_dir, video_title)

    # Verify file was created
    expected_path = os.path.join(
        temp_dir, "transcripts", f"{video_title}_transcription_summary_"
    )
    assert any(
        f.startswith(expected_path)
        for f in os.listdir(os.path.join(temp_dir, "transcripts"))
    )
