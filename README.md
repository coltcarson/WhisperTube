# WhisperTube 🚀🎶

WhisperTube is an open-source tool designed to simplify transcription and summarization of YouTube videos. It uses OpenAI's Whisper model to transcribe audio from YouTube, while also leveraging GPT-based models to provide concise and engaging summaries. The output is saved in a Markdown format for easy readability, making it suitable for educational content, podcast summaries, or generating quick insights from long-form video content.

## Key Features ✨
- **Download YouTube Audio** 🎵: Automatically download YouTube videos as audio using `yt-dlp`.
- **High-Quality Transcription** 📜: Transcribe audio with OpenAI's Whisper model, supporting multiple languages.
- **Summarization** 📝: Generate concise and engaging summaries using GPT models.
- **Markdown Output** 📄: Save transcriptions and summaries in Markdown format for easy sharing.
- **Customization** ⚙️: Customize settings for FFmpeg location and environment configurations.

## Use Cases 💡
- **Educational Content** 🎓: Create detailed transcripts and summaries from educational videos, lectures, or tutorials.
- **Podcast Summaries** 🎙️: Extract key insights from podcasts or long videos for quicker content consumption.
- **Accessibility** ♿: Facilitate accessibility by providing written content for audio/video files.

## Technologies Used 🛠️
- **Python** 🐍: For scripting and orchestration.
- **Whisper** 🔊: For accurate audio transcription.
- **OpenAI GPT** 🤖: For generating summaries and enhancing transcription quality.
- **yt-dlp** 📹: For seamless video downloads.
- **FFmpeg** 🎥: For audio extraction.

## Installation 💻

To install WhisperTube, clone the repository and install the required dependencies:

### Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies and avoid conflicts with other projects:

```bash
# Create a virtual environment with Python 3.10
python3.10 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/yourusername/WhisperTube.git

# Navigate to the project directory
cd WhisperTube

# Install dependencies
pip install -r requirements.txt
```

### Using pip-tools 🛠️

To manage dependencies in a more efficient way, you can use `pip-tools`. This allows you to keep your `requirements.txt` updated easily:

1. Install `pip-tools`:
   ```bash
   pip install pip-tools
   ```

2. Create or update `requirements.in` with your main dependencies.

3. Compile the `requirements.txt` file:
   ```bash
   pip-compile requirements.in
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Installing FFmpeg 🎛️

WhisperTube requires FFmpeg for audio processing. Follow the steps below to install FFmpeg on your system.

#### Windows Installation 🪟
1. Download the latest FFmpeg build from [FFmpeg.org](https://ffmpeg.org/download.html). Select the Windows version.
2. Extract the downloaded zip file to a directory of your choice (e.g., `C:\ffmpeg`).
3. Add FFmpeg to your system's PATH:
   - Open **Control Panel** > **System and Security** > **System** > **Advanced system settings**.
   - Click **Environment Variables**.
   - Under **System Variables**, find **Path**, select it, and click **Edit**.
   - Click **New** and add the path to the `bin` folder of FFmpeg (e.g., `C:\ffmpeg\bin`).
   - Click **OK** to save the changes.

#### macOS Installation 🍏
1. Install Homebrew if it is not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Use Homebrew to install FFmpeg:
   ```bash
   brew install ffmpeg
   ```

Ensure that FFmpeg is installed and accessible from your system's PATH.

## How to Use 🚀
1. Run the script and provide the YouTube video URL:

    ```bash
    python transcribe_youtube_chatgpt.py --url <youtube_url> --ffmpeg <ffmpeg_path>
    ```

2. Enter the YouTube URL when prompted and specify the location of **FFmpeg** (or press Enter to use the default).

3. The transcription and summary will be saved in the `transcripts` folder in Markdown format.

## Project Structure 📂
```
.
├── transcribe_youtube_chatgpt.py  # Main script
├── .env                           # Environment variables file for API key
├── transcripts/                   # Folder where transcripts are saved
├── README.md                      # Project documentation
└── test_transcribe_youtube.py     # Pytest file for unit tests
```

## Configuration ⚙️

- **Environment Variables**: Create a `.env` file in the project directory to store your OpenAI API key:
  ```
  OPENAI_API_KEY=your_openai_api_key_here
  ```
- **Model Configuration**: The script uses the Whisper "base" model for transcription by default. This can be customized in the script if needed.

## Running Tests 🧪

We use `pytest` for testing the main functionalities of WhisperTube. To run the tests, make sure you have `pytest` installed:

```bash
pip install pytest
```

To run the tests:

```bash
pytest test_transcribe_youtube.py
```

## Contributing 🤝
Contributions are welcome! Whether it's a bug fix, feature addition, or documentation improvement, feel free to submit a pull request.

Please follow the [contribution guidelines](CONTRIBUTING.md) when contributing to the project.

## License 📜
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏
- [OpenAI](https://openai.com) for their Whisper and GPT models.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading.
- All contributors for their support and ideas.
