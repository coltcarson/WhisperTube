"""WhisperTube: A tool for transcribing and summarizing YouTube videos using OpenAI's models."""

from .transcriber import (
    download_youtube_video,
    save_transcription,
    summarize_transcription,
    transcribe_audio,
)

__version__ = "0.1.0"
__all__ = [
    "download_youtube_video",
    "transcribe_audio",
    "summarize_transcription",
    "save_transcription",
]
