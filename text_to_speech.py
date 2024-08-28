from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os

load_dotenv()

# Load the OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize openai API client
client = OpenAI(api_key=OPENAI_API_KEY) 

# Create function for chat GPT text completion calls
def chatgpt(prompt: str, model="gpt-4o", max_tokens=None):
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,  # 4000
        messages=[{"role": "user", "content": prompt}],
    )
    response = completion.choices[0].message.content
    return response

# FUNCTION FOR CONVERTING MP4 FILES TO MP3 AUDIO
def mp4_to_mp3(input_file, output_file):
  print(f"Converting {input_file} to mp3.")
  audio = AudioSegment.from_file(input_file, format='mp4')
  audio.export(output_file, format="mp3")
  print(f"MP3 was successfully saved to {output_file}")

# Convert video to mp3
input_file = './video_files/interview.mp4'
audio_file = './audio_files/interview.mp3'
mp4_to_mp3(input_file=input_file, output_file=audio_file)


# Read audio file and create text transcription with Open AI API 
audio = open(audio_file, "rb")
print("processing audio file with openAI speech to text. This may take a minute...")
raw_transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio,
  response_format="text"
)
print(f"Raw transcript has been generated.")

# Save raw transcript to file 
filename = "./output_transcripts/raw_transcript.txt"# Open the file in write mode and write the string
with open(filename, 'w') as file:
    file.write(raw_transcript)
print(f"Raw transcript was saved to {filename} successfully.")


# Read prompt for converting raw transcript to transcript segmented by speaker using chatgpt API
print(f"Loading prompt for ChatGPT")
with open('./prompts/prompt.txt', 'r') as file:
    prompt = file.read()

print('Splitting raw transcript into two speakers. This may take a minute...')
prompt = prompt.replace('TRANSCRIPT_HERE', raw_transcript)
final_transcript = chatgpt(prompt=prompt)
filename = './output_transcripts/final_transcript.txt'
with open(filename, 'w') as file:
    file.write(final_transcript)
print(f"Raw transcript was saved to {filename} successfully.")



