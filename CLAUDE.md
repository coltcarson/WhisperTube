# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

WhisperTube is a CLI tool that downloads a YouTube video's audio, transcribes it with OpenAI's Whisper (run locally), then summarizes/enhances the transcript with GPT-4o (LaTeX math formatting), and writes the result to a Markdown file.

## Commands

```bash
# Install for development (editable + dev deps)
pip install -r requirements-dev.txt
pip install -e .

# Run the CLI
whispertube                                        # prompts for URL
whispertube --url "https://youtube.com/watch?v=..." --output-dir "./transcripts"

# Tests
pytest                                             # all tests
pytest tests/test_transcribe_youtube.py::test_transcribe_audio   # single test

# Lint / format / type-check (mirrors pre-commit)
black .
isort --profile black .
flake8
mypy --ignore-missing-imports src

# Install git hooks (black/isort/flake8 on commit; mypy/pytest on push)
pre-commit install

# Regenerate pinned deps after editing .in files
pip-compile requirements.in
pip-compile requirements-dev.in -o requirements-dev.txt
```

## Architecture

The package lives in [src/whispertube/](src/whispertube/) and is a thin, four-stage pipeline. All core logic is in [transcriber.py](src/whispertube/transcriber.py) as standalone functions; [__main__.py](src/whispertube/__main__.py) orchestrates them.

Pipeline (driven by `main()` in [__main__.py](src/whispertube/__main__.py)):
1. `download_youtube_video(url, output_path)` — yt-dlp downloads bestaudio and FFmpeg extracts it to `audio.wav`. Runs inside a `tempfile.TemporaryDirectory`, so audio is discarded after the run.
2. `transcribe_audio(file_path, model_name="base")` — loads a local Whisper model and returns text.
3. `summarize_transcription(transcription)` — single GPT-4o chat completion; the prompt instructs LaTeX/Markdown formatting.
4. `save_transcription(...)` — writes `{video_title}_transcription_summary_{timestamp}.md` into a `transcripts/` subfolder of the output dir.

Key conventions:
- **Error handling is non-raising by design.** Core functions catch exceptions, `logger.error(...)`, and return a sentinel (`None`, `""`, or `(None, None)`). Callers check these falsy returns and abort the pipeline gracefully — do not change a function to raise without updating its caller in `main()`.
- **Public API** is whatever [__init__.py](src/whispertube/__init__.py) re-exports (`__all__`). Tests and the README's "Python API" import from the top-level `whispertube` package, so keep that surface stable.
- **API key resolution order** (`get_openai_key` in [__main__.py](src/whispertube/__main__.py)): `--api-key` flag → `OPENAI_API_KEY` env var → `.env` file → interactive `getpass` prompt (optionally appended to `.env`).

## Important constraints

- **Pinned to `openai==0.28.0`** (the legacy SDK). Code uses `openai.ChatCompletion.create(...)` and dict-style response access (`response["choices"][0]["message"]["content"]`). Do not migrate to the 1.x client API without updating both the dependency and all call sites.
- **Whisper is pinned to a specific git commit** in [pyproject.toml](pyproject.toml). It runs locally and requires **FFmpeg** on the system PATH (`ffmpeg -version`). Many functions accept an optional `ffmpeg_location` to point at a non-PATH binary.
- **Python 3.10** is the supported/CI version.

## Testing

Tests mock all external boundaries — `yt_dlp.YoutubeDL`, `whisper.load_model`, and `openai.ChatCompletion.create` — so no network, FFmpeg, or API key is needed to run them. When adding tests, follow this pattern and reuse the fixtures in [tests/conftest.py](tests/conftest.py) (`temp_dir`, `mock_video_info`, `sample_audio_path`, `mock_transcription`, `mock_summary`). `pythonpath = ["src"]` is set in [pyproject.toml](pyproject.toml), so import from `whispertube` directly.
