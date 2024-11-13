import pytest
import os
from unittest.mock import Mock, patch
import tempfile
from whispertube import (
    download_youtube_video,
    transcribe_audio,
    summarize_transcription,
    save_transcription
)

def test_download_youtube_video(temp_dir, mock_video_info):
    url = "https://www.youtube.com/watch?v=test123"
    
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        # Configure the mock
        mock_ydl_instance = Mock()
        mock_ydl_instance.extract_info.return_value = mock_video_info
        mock_ydl.return_value.__enter__.return_value = mock_ydl_instance

        # Call the function
        audio_path, video_title = download_youtube_video(url, temp_dir)

        # Verify the function called YoutubeDL with correct parameters
        mock_ydl.assert_called_once()
        assert mock_ydl_instance.extract_info.called_with(url, download=True)

@patch('whisper.load_model')
def test_transcribe_audio(mock_load_model, sample_audio_path):
    # Configure the mock
    mock_model = Mock()
    mock_model.transcribe.return_value = {"text": "Test transcription"}
    mock_load_model.return_value = mock_model

    # Call the function
    result = transcribe_audio(sample_audio_path)

    # Verify the results
    assert result == "Test transcription"
    mock_load_model.assert_called_once_with("base")
    mock_model.transcribe.assert_called_once_with(sample_audio_path)

@patch('openai.ChatCompletion.create')
def test_summarize_transcription(mock_chat_completion, mock_transcription):
    # Configure the mock to match the actual OpenAI API response structure
    mock_chat_completion.return_value = type('Response', (), {
        'choices': [
            type('Choice', (), {
                'message': {
                    'content': 'Summarized content'
                }
            })()
        ]
    })()

    # Call the function
    result = summarize_transcription(mock_transcription)

    # Verify the results
    assert result == "Summarized content"
    mock_chat_completion.assert_called_once()

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
    with open(os.path.join(transcripts_dir, saved_file), 'r') as f:
        content = f.read()
        assert mock_summary in content
        assert mock_transcription in content
