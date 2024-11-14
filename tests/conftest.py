"""Test fixtures for WhisperTube tests."""

import os
import tempfile

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files.

    Yields:
        str: Path to temporary directory that is cleaned up after the test.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_video_info():
    """Provide mock video information for testing.

    Returns:
        dict: Mock video metadata including title and format information.
    """
    return {
        "title": "Test Video Title",
        "formats": [{"url": "http://example.com/audio.wav"}],
    }


@pytest.fixture
def sample_audio_path():
    """Provide a sample audio file path for testing.

    Returns:
        str: Path to a mock audio file.
    """
    return os.path.join(tempfile.gettempdir(), "audio.wav")


@pytest.fixture
def mock_transcription():
    """Provide sample transcription text for testing.

    Returns:
        str: Sample transcription text.
    """
    return "This is a test transcription."


@pytest.fixture
def mock_summary():
    """Provide sample summary text for testing.

    Returns:
        str: Sample summary text.
    """
    return "This is a test summary."
