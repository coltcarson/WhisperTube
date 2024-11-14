"""WhisperTube - A tool to transcribe YouTube videos using Whisper and summarize with ChatGPT."""

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
