
# Interview Transcriber

## About

Interview Transcriber is a Python application designed to convert MP4 videos of a 2-person interview into a text transcription. It distinguishes between speakers and provides a clear and structured output.

## Features

- Converts video interviews into text transcription.
- Automatically distinguishes between speakers.
- Outputs structured and readable text files.

## Prerequisites

- Python 3.10 or higher.
- OpenAI API key.
- `ffmpeg` installed on your system.

## Getting Started

### Installing Visual Studio Code

1. Download and Install Visual Studio Code from [here](https://code.visualstudio.com/download).
2. Open Visual Studio Code and install the "Python" extension by Microsoft.

### Clone the Repository from GitHub

1. Open your terminal or command line.
2. Run:

    ```bash
    git clone https://github.com/lukerbs/InterviewTranscriber.git
    ```

3. Navigate into the repository folder:

    ```bash
    cd InterviewTranscriber
    ```

### Installation of Dependencies

1. Ensure Python is installed on your device by running:

    ```bash
    python3 --version
    ```

    Make sure the version is 3.10 or higher.
2. Open the project in a terminal.
3. Create a Python virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

4. Install the required dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

5. Install `ffmpeg` using Homebrew:
    - If you don't have Homebrew, install it:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    - Then install ffmpeg:

    ```bash
    brew install ffmpeg
    ```

### Set Up OpenAI API Key

1. Obtain your OpenAI API Key from a team lead or create your own at [OpenAI Platform](https://platform.openai.com/docs/overview).
2. Create a new file named `.env`:

    ```bash
    cp .env-example .env
    ```

3. Copy the contents from `.env-example` to the `.env` file.
4. Place your OpenAI API key in the `.env` file, replacing `xxxxxx`.
5. Save your changes.

## Usage

1. Launch the application by running:

    ```bash
    python app.py
    ```

2. A GUI will appear. Use the "Select Video File" button to choose your MP4 video file.
3. Click "TRANSCRIBE INTERVIEW" to start the transcription process.
4. Once completed, the transcription is displayed. You can save the transcript using the "Save to File" button.

## Directory Structure

- `app.py`: Main application script.
- `transcript_processor.py`: Handles the transcription processing.
- `audio_files/`: Directory for storing audio files and chunks.
- `.env-example`: Template for environment variables including API keys.

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

This project is licensed under the terms of the MIT license.
