# Repository Guidelines

## Project Structure & Module Organization

WhisperTube is a Python package laid out with source code under `src/whispertube/`. The CLI entry point is `src/whispertube/__main__.py`, and core download, transcription, summary, and save logic lives in `src/whispertube/transcriber.py`. Tests are in `tests/`, with shared pytest fixtures in `tests/conftest.py`. Dependency inputs are tracked in `requirements.in` and `requirements-dev.in`; compiled lock-style outputs are `requirements.txt` and `requirements-dev.txt`. Runtime transcript output is expected under `transcripts/` and should not contain secrets.

## Build, Test, and Development Commands

Create an environment with Python 3.10+:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
pip install -e .
```

Run tests with `pytest`. Install quality hooks with `pre-commit install`; hooks run formatting and checks on commit, with mypy and pytest on push. Refresh pinned dependencies with `pip-compile requirements.in` or `pip-compile requirements-dev.in -o requirements-dev.txt`.

## Coding Style & Naming Conventions

Use Black formatting and isort with the Black profile. Flake8 is configured for a 120-character max line length and docstring checks, with selected docstring rules ignored in `.flake8`. Prefer clear snake_case for functions, variables, fixtures, and test names. Keep CLI-specific behavior in `__main__.py`; keep reusable package behavior in `transcriber.py` or new focused modules under `src/whispertube/`.

## Testing Guidelines

Tests use pytest plus `unittest.mock` for external services. Add or update tests in `tests/test_*.py` when changing downloader, Whisper, OpenAI, or file-writing behavior. Mock YouTube, Whisper, and OpenAI calls rather than making network or paid API requests. Run `pytest` before opening a pull request; pre-push hooks also run the suite.

## Commit & Pull Request Guidelines

Follow Conventional Commits, as used in history: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, or `chore:`. Keep commits focused and descriptive. Pull requests should include a clear summary, linked issues when relevant, test results, and documentation or `CHANGELOG.md` updates for user-visible changes. Include screenshots or sample command output when changing CLI behavior or generated Markdown output.

## Security & Configuration Tips

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` locally; never commit `.env` or API keys. FFmpeg must be installed and available on `PATH` for audio processing. Treat generated transcripts as potentially sensitive user data.
