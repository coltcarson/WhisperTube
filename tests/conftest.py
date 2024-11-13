import pytest
import os
import tempfile

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def sample_audio_path(temp_dir):
    """Create a mock audio file path."""
    return os.path.join(temp_dir, "audio.wav")

@pytest.fixture
def mock_video_info():
    """Return mock video information."""
    return {
        "title": "Test Video Title",
        "duration": 120,
        "description": "Test video description"
    }

@pytest.fixture
def mock_transcription():
    """Return a mock transcription text."""
    return "This is a test transcription of the audio content."

@pytest.fixture
def mock_summary():
    """Return a mock summary text."""
    return "This is a summarized version of the transcription."
