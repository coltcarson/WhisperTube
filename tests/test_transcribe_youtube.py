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

    # Create transcripts directory
    transcripts_dir = os.path.join(temp_dir, "transcripts")
    os.makedirs(transcripts_dir, exist_ok=True)

    # Call the function
    save_transcription(mock_transcription, mock_summary, temp_dir, video_title)

    # Verify file was created
    files = os.listdir(transcripts_dir)
    assert len(files) == 1, "Expected one file to be created"
    
    file_path = os.path.join(transcripts_dir, files[0])
    assert os.path.exists(file_path), "File should exist"
    assert files[0].startswith(f"{video_title}_transcription_summary_"), "File should have correct prefix"
    assert files[0].endswith(".md"), "File should have .md extension"

    # Verify file contents
    with open(file_path, 'r') as f:
        content = f.read()
        assert mock_summary in content, "Summary should be in the file"
        assert mock_transcription in content, "Transcription should be in the file"
