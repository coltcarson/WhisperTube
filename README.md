# WhisperTube 🎥 ➡️ 📝

Transcribe YouTube videos using OpenAI's Whisper and summarize them using GPT-4, with special handling for mathematical expressions in LaTeX! ✨

## 🌟 Features

- 🎥 Download audio from YouTube videos
- 🎯 Transcribe audio using OpenAI's Whisper
- 🤖 Summarize transcriptions using GPT-4
- 📐 Format mathematical expressions in LaTeX
- 📝 Save transcriptions and summaries in Markdown
- ⚡ Command-line interface for easy use
- 🔒 Secure API key handling

## 🏗️ Project Structure

```
WhisperTube/
├── src/
│   └── whispertube/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # CLI entry point
│       └── transcriber.py   # Core functionality
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Test fixtures
│   └── test_transcribe_youtube.py
├── transcripts/            # Output directory
├── .env.example           # Environment variables template
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.in        # Core dependencies
└── requirements-dev.in    # Development dependencies
```

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WhisperTube.git
cd WhisperTube
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
# For development
pip install -r requirements-dev.txt

# For production
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your API key in this format:
# OPENAI_API_KEY=sk-your_api_key_here

# For example:
# OPENAI_API_KEY=sk-abc123def456...
```

> ⚠️ **Important**: Your OpenAI API key should start with 'sk-'. Keep this key secure and never commit it to version control.

## 🎮 Usage

### Command Line Interface 💻

```bash
# Basic usage (will prompt for URL)
whispertube

# Specify URL directly
whispertube --url "https://youtube.com/watch?v=..."

# Specify output directory
whispertube --url "..." --output-dir "./transcripts"
```

### Python API 🐍

```python
from whispertube import download_youtube_video, transcribe_audio, summarize_transcription

# Download video
audio_path, video_title = download_youtube_video(url, output_path)

# Transcribe audio
transcription = transcribe_audio(audio_path)

# Summarize transcription
summary = summarize_transcription(transcription)
```

## 🛠️ Development

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:
```bash
pre-commit install
```

3. Run tests:
```bash
pytest
```

4. Update dependencies:
```bash
# Update runtime dependencies
pip-compile requirements.in

# Update development dependencies
pip-compile requirements-dev.in -o requirements-dev.txt
```

## 📋 Requirements

- 🐍 Python 3.10+
- 🎵 FFmpeg
- 🔑 OpenAI API key

## 🔄 Workflow

1. Input: YouTube URL
2. Download: Extract audio using yt-dlp
3. Transcribe: Process audio with Whisper
4. Enhance: Summarize using GPT-4
5. Output: Save as Markdown with LaTeX formatting

## 📝 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- [OpenAI](https://openai.com) for their amazing Whisper and GPT models
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for reliable YouTube video downloading
- All contributors and users of this project

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Troubleshooting

- Ensure FFmpeg is installed and accessible
- Check your OpenAI API key is valid
- Verify your Python version is 3.10 or higher
- Make sure you have sufficient disk space for audio files

## 📬 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/WhisperTube/issues) page
2. Open a new issue if needed
3. Provide as much detail as possible about your problem
