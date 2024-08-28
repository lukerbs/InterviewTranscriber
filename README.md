# INSTRUCTIONS FOR USAGE
## Installation of Dependencies
1. Make sure to have Python installed on your device
2. Clone the reposotory with Git
3. Open the project in terminal
4. Create a Python virtual environment in the project root directory:
    - python3 -m venv venv  (create the virtual env)
    - source venv/bin/activate  (activate the virtual env)
5. Install the required dependencies
    - pip3 install -r requirements.txt

## Set Up OpenAI API Key
1. Create a new file called '.env' 
2. Copy the contents of '.env-example' into the '.env' file you just created. 
3. Replace the 'xxxxx' in the .env file with your OpenAI API key (do not wrap the API key with quotes).
4. Save the changes to the .env file.

## Usage
1. Rename your video file to 'interview.mp4'
2. Move 'interview.mp4' file to the './video_files' folder.
3. Open terminal and run the program:
    - python3 text_to_speech.py
4. After running the program, the resulting transcript will be saved to './output_transcripts/final_transcript.txt'