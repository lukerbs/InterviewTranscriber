import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment from .env file
load_dotenv()

# Load the OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please check your .env file.")

# Initialize openai API client
client = OpenAI(api_key=OPENAI_API_KEY) 



def chatgpt_json(instructions: str, content: str, response_format: BaseModel) -> dict:
    """This function is used to return content from OpenAI Chat Completions API as a structured dictionary response. 
    
    Args:
        instructions (str): Instructions for the LLM (how the LLM should process the input content).
        content (str): Information that the LLM is supposed to process. 
        response_format (BaseModel): The output format defined by a Pydantic Basemodel.

    Returns:
        dict: The structured output response from the LLM.
    """
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": content},
        ],
        response_format=response_format,
    )

    structured_response = completion.choices[0].message.parsed
    return structured_response.model_dump()


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


def segment_by_speaker(transcription: str) -> str:
    """This function labels the speakers of a two way interview using the raw text of the interview transcription.

    Args:
        transcription (str): Raw text from a two way interview

    Returns:
        str: Interview transcription with labeled speakers.
    """
    print(f"RAW TRANSCRIPTION: \n{transcription}")
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