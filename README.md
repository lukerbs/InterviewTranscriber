# Interview Transcriber
## About 
Interview Transcriber is a Python tool used to convert MP4 videos of a 2-person interview into a text transcription of the two individuals speaking. The resulting text transcription is saved to a .txt file.

# Instructions
## Installing Visual Studio Code
1. Download and Install Visual Studio Code from:
    - https://code.visualstudio.com/download
2. Open the Visual Studio Code desktop app
3. Install the "Python" Visual Studio Code extension by Microsoft

## Clone the Repo from GitHub
1. Open your terminal or command line
2. Run: `git clone https://github.com/lukerbs/InterviewTranscriber.git`
3. Enter (or 'cd') into the repo folder by running:
    - `cd InterviewTranscriber`

## Installation of Dependencies
1. Make sure to have Python installed on your device
    - You can check by running: `python3 --version`
    - make sure you have 3.10 or higher installed
3. Open the project in terminal
4. Create a Python virtual environment in the project root directory by running the commands in terminal:
    - `python3 -m venv venv`  (create the virtual env)
    - `source venv/bin/activate`  (activate the virtual env)
5. Install the required dependencies
    - `pip3 install -r requirements.txt`
6. Install ffmpeg
    - Step1: install homebrew if you don't have it
        - `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)`
    - Step2: install ffmpeg
        - `brew install ffmpeg`
## Set Up OpenAI API Key
1. Get your OpenAI API Key:
    - Get your OpenAI API key from a team lead or create your own personal API key at https://platform.openai.com/docs/overview 
2. Create a new file called '.env':
    - Run: `cp .env-example .env`
3. Copy the contents of '.env-example' into the '.env' file you just created. 
4. Replace the 'xxxxxx' in the .env file with your OpenAI API key (do not wrap the API key with quotes).
5. Save the changes to the .env file.

## Usage
1. go to convert_mp4_to_mp3 
2. put in the folder path with the mp4s
3. go to speech_to_text.py
4. copy file path of mp3 to line 8 (AUDIO_FILE =)
5. click the run button or type python3 speech_to_text.py
6. After running the program, the resulting transcript will be saved to './output_transcripts/final_transcript.txt'