from openai import OpenAI
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import re

load_dotenv()
AUDIO_FILE = '/Users/jsandor/Projects/Connect/Rodney Jackson and Sou Sassi Cole-20240524_120253-Meeting Recording.mp3'

# Load the OpenAI API key from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please check your .env file.")
# Initialize openai API client
client = OpenAI(api_key=OPENAI_API_KEY) 

# Create function for chat GPT text completion calls
def chatgpt(prompt: str, model="gpt-4o", max_tokens=None):
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    response = completion.choices[0].message.content
    return response


# Read audio file and create text transcription with Open AI API 
audio = open(AUDIO_FILE, "rb")
print("Processing audio file with openAI speech to text. This may take a minute...")
raw_transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio,
  response_format="text"
)
print("Raw transcript has been generated.")

# Save raw transcript to file 
raw_transcript_filename = "./output_transcripts/raw_transcript.txt"
with open(raw_transcript_filename, 'w') as file:
    file.write(raw_transcript)
print(f"Raw transcript was saved to {raw_transcript_filename} successfully.")

# Split the raw transcript into three chunks
chunk_size = len(raw_transcript) // 3
chunks = [
    raw_transcript[:chunk_size],
    raw_transcript[chunk_size:2*chunk_size],
    raw_transcript[2*chunk_size:]
]

# Updated prompt template

with open("./prompts/prompt_v2.txt", "r") as file: 
    prompt_template = file.read()

print('Processing transcript chunks. This may take a few minutes...')

# Process each chunk
processed_chunks = []
for i, chunk in enumerate(chunks, 1):
    print(f"Processing chunk {i}...")
    prompt = prompt_template.format(chunk)
    processed_chunk = chatgpt(prompt=prompt)
    processed_chunks.append(processed_chunk)
    print(f"Chunk {i} processed.")

    # Save each processed chunk to a separate file
    chunk_filename = f'./output_transcripts/processed_chunk_{i}.txt'
    with open(chunk_filename, 'w') as file:
        file.write(processed_chunk)
    print(f"Processed chunk {i} saved to {chunk_filename}")

# Function to ensure consistent speaker identification across chunks
def ensure_consistent_speakers(chunks):
    # Determine the first speaker in the first chunk
    first_speaker = re.match(r'(Interviewer|Interviewee):', chunks[0]).group(1)
    
    for i in range(1, len(chunks)):
        # Check the last speaker of the previous chunk
        last_speaker_prev = re.findall(r'(Interviewer|Interviewee):', chunks[i-1])[-1]
        # Check the first speaker of the current chunk
        first_speaker_curr = re.match(r'(Interviewer|Interviewee):', chunks[i]).group(1)
        
        # If they're the same, we need to flip the speakers in the current chunk
        if last_speaker_prev == first_speaker_curr:
            chunks[i] = chunks[i].replace('Interviewer:', 'TEMP_INTERVIEWER:')
            chunks[i] = chunks[i].replace('Interviewee:', 'TEMP_INTERVIEWEE:')
            chunks[i] = chunks[i].replace('TEMP_INTERVIEWER:', 'Interviewee:')
            chunks[i] = chunks[i].replace('TEMP_INTERVIEWEE:', 'Interviewer:')
    
    return chunks

# Ensure consistent speaker identification across chunks
processed_chunks = ensure_consistent_speakers(processed_chunks)

# Stitch the processed chunks together
final_transcript = "\n\n".join(processed_chunks)

# Save the final transcript
final_transcript_filename = './output_transcripts/final_transcript.txt'
with open(final_transcript_filename, 'w') as file:
    file.write(final_transcript)
print(f"Final transcript was saved to {final_transcript_filename} successfully.")

