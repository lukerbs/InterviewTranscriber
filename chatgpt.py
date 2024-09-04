import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment from .env file
load_dotenv()

# Load the OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please check your .env file.")

# Initialize openai API client
client = OpenAI(api_key=OPENAI_API_KEY) 

def chatgpt(prompt: str, model="gpt-4o", max_tokens=None):
    """Function for generating responses to text prompts with OpenAI's ChatGPT API

    Args:
        prompt (str): The prompt for ChatGPT to respond to
        model (str, optional): ChatGPT model to use. Defaults to "gpt-4o".
            - List of Available Models: https://platform.openai.com/docs/models/continuous-model-upgrades
        max_tokens (int, optional): Optional, the max tokens to be returned by response. Defaults to no limit (i.e. None).

    Returns:
        str: Returns the response to the prompt as a string value
    """
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    response = completion.choices[0].message.content
    return response

def transcribe_audio(audio_file: str) -> str:
    # Read audio file and create text transcription with Open AI API 
    audio = open(audio_file, "rb")
    print("Processing audio file with openAI speech to text. This may take a minute...")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio,
        response_format="text"
    )
    print("Raw transcript has been generated.")
    return transcription

def segment_by_speaker(transcription: str) -> str:
    """This function labels the speakers of a two way interview using the raw text of the interview transcription.

    Args:
        transcription (str): Raw text from a two way interview

    Returns:
        str: Interview transcription with labeled speakers.
    """
    with open('./prompts/prompt.txt', 'r') as file:
        prompt = file.read()
    
    prompt = prompt.replace('TRANSCRIPT_HERE', transcription)
    segmented_transcript = chatgpt(prompt=prompt)
    return segmented_transcript

if __name__ == "__main__":
    # Read the prompt from the custom_prompt.txt file
    with open('./prompts/custom_prompt.txt') as file:
        prompt = file.read()

    # Get response from ChatGPT
    response = chatgpt(prompt=prompt)
    print(response)