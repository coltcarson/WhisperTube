# WhisperTube

WhisperTube is an open-source tool designed to simplify transcription and summarization of YouTube videos. It uses OpenAI's Whisper model to transcribe audio from YouTube, while also leveraging GPT-based models to provide concise and engaging summaries. The output is saved in a Markdown format for easy readability, making it suitable for educational content, podcast summaries, or generating quick insights from long-form video content.

## Key Features
- **Download YouTube Audio**: Automatically download YouTube videos as audio using yt-dlp.
- **High-Quality Transcription**: Transcribe audio with OpenAI's Whisper model, supporting multiple languages.
- **Summarization**: Generate concise and engaging summaries using GPT models.
- **Markdown Output**: Save transcriptions and summaries in Markdown format for easy sharing.
- **Customization**: Customize settings for FFmpeg location and environment configurations.

## Use Cases
- **Educational Content**: Create detailed transcripts and summaries from educational videos, lectures, or tutorials.
- **Podcast Summaries**: Extract key insights from podcasts or long videos for quicker content consumption.
- **Accessibility**: Facilitate accessibility by providing written content for audio/video files.

## Technologies Used
- **Python**: For scripting and orchestration.
- **Whisper**: For accurate audio transcription.
- **OpenAI GPT**: For generating summaries and enhancing transcription quality.
- **yt-dlp**: For seamless video downloads.
- **FFmpeg**: For audio extraction.

## Installation

To install WhisperTube, clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/WhisperTube.git

# Navigate to the project directory
cd WhisperTube

# Install dependencies
pip install -r requirements.txt
```

Ensure that **FFmpeg** is installed and accessible from your system's PATH.

## How to Use
1. Run the script and provide the YouTube video URL:

    ```bash
    python transcribe_youtube_chatgpt.py
    ```

2. Enter the YouTube URL when prompted and specify the location of **FFmpeg** (or press Enter to use the default).

3. The transcription and summary will be saved in the `transcripts` folder in Markdown format.

## Contributing
Contributions are welcome! Whether it's a bug fix, feature addition, or documentation improvement, feel free to submit a pull request.

Please follow the [contribution guidelines](CONTRIBUTING.md) when contributing to the project.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [OpenAI](https://openai.com) for their Whisper and GPT models.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading.
- All contributors for their support and ideas.
