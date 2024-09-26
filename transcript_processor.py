
import re
from pprint import pprint
from itertools import islice

from chatgpt import chatgpt_json
from data_model import Transcriptions
from utils import get_split_points, chunk_mp3_file, combine_transcription_chunks, get_num_tokens



def merge_consecutive_speakers(transcript_segments: list[dict]):
    merged_transcriptions = []
    
    # Initialize variables to store the current speaker block
    current_speaker = None
    current_timestamp = None
    current_transcription = []

    for item in transcript_segments:
        speaker = item['speaker']
        transcription = item['transcription']
        timestamp = item['timestamp']
        
        # If this is a new speaker, append the previous speaker block to the list
        if speaker != current_speaker:
            if current_speaker is not None:
                # Add the previous speaker's data to the merged list
                merged_transcriptions.append({
                    'speaker': current_speaker,
                    'timestamp': current_timestamp,
                    'transcription': ' '.join(current_transcription)
                })
            
            # Reset to the new speaker
            current_speaker = speaker
            current_timestamp = timestamp
            current_transcription = [transcription]
        else:
            # Same speaker, just concatenate the transcription
            current_transcription.append(transcription)

    # Append the last block after the loop
    if current_speaker is not None:
        merged_transcriptions.append({
            'speaker': current_speaker,
            'timestamp': current_timestamp,
            'transcription': ' '.join(current_transcription)
        })
    
    # Return the new dict with merged transcriptions
    return merged_transcriptions


def chunk_transcript(raw_transcript: str, num_chunks: int):
    print(f"TOTAL TRANSCRIPT CHUNKS: {num_chunks}")
    # Calculate the size of each sublist
    lines = raw_transcript.splitlines()

    n = len(lines)
    avg_size = n // num_chunks
    remainder = n % num_chunks

    # Generate sublists using slices
    iterator = iter(lines)
    chunked_list = [list(islice(iterator, avg_size + (i < remainder))) for i in range(num_chunks)]

    transcript_chunks = []
    for i, chunk_segments in enumerate(chunked_list):
        preceding_chunk = ''
        following_chunk = ''

        if i != 0:
            # If not on first chunk:
            preceding_chunk_list = chunked_list[i-1]
            if len(preceding_chunk_list) >= 3:
                preceding_chunk = '\n'.join(preceding_chunk_list[-3:])
            else:
                preceding_chunk = '\n'.join(preceding_chunk_list)

        if i != (len(chunked_list) - 1):
            # If not on last chunk:
            following_chunk_list = chunked_list[i+1]
            if len(following_chunk_list) >= 3:
                following_chunk = '\n'.join(following_chunk_list[:3])
            else:
                following_chunk = '\n'.join(following_chunk_list)

        current_chunk = '\n'.join(chunked_list[i])
        current_chunk = f"\n\n***EXTRACT_START***\n{current_chunk.strip()}\n***EXTRACT_END***\n\n"
        chunk_text = f"{preceding_chunk.strip()}{current_chunk}{following_chunk.strip()}".strip()
        transcript_chunks.append(chunk_text)

        print('- - - - - - -')
        print(f"TRANSCRIPT CHUNK {i+1} ({get_num_tokens(chunk_text)} Tokens):")
        print(f"{chunk_text}")
        print('- - - - - - -\n\n')

    return transcript_chunks

def process_raw_transcript(raw_transcript: str):
    MAX_TOKEN_THRESHOLD = 4000

    num_tokens = get_num_tokens(string=raw_transcript)
    print(f"NUM TOKENS: {num_tokens}")


    if num_tokens > MAX_TOKEN_THRESHOLD:
        # Case where the full raw transcript exceeds max token length for OpenAI Chat Completion API
        # (Transcript needs to be chunked into segments and processed in smaller subsections)
        print(f"ALERT: Raw transcript exceeds max token length for OpenAI Chat Completion API. Processing in smaller segments...")
        with open('./chunk_instructions.txt', 'r') as file:
            instructions = file.read()

        num_chunks = (num_tokens // MAX_TOKEN_THRESHOLD) + 1
        transcript_chunks = chunk_transcript(raw_transcript=raw_transcript, num_chunks=num_chunks)

        transcript_segments = []
        for i, transcript_section in enumerate(transcript_chunks):
            print(f"Processing Transcript Segment ({i+1}/{len(transcript_chunks)})")
            response = chatgpt_json(instructions=instructions, content=transcript_section, response_format=Transcriptions)
            transcript_segments.extend(response['transcriptions'])

    else:
        # Full raw transcript can be processed by OpenAI Chat Completions API
        with open('./instructions.txt', 'r') as file:
            instructions = file.read()

        response = chatgpt_json(instructions=instructions, content=raw_transcript, response_format=Transcriptions)
        transcript_segments = response['transcriptions']

    print(f"\nSTRUCTURED OUTPUT:")
    merged_transcriptions = merge_consecutive_speakers(transcript_segments=transcript_segments)
    pprint(merged_transcriptions)

    final_output = ''
    for section in merged_transcriptions:
        final_output += f'[{section["timestamp"]}] {section["speaker"]}: "{section["transcription"]}"\n\n'

    final_output = final_output.strip()
    print(f"\nFINAL OUTPUT:")
    print(final_output)
    return final_output


if __name__ == "__main__":
    AUDIO_FILE = './audio_files/test.mp3'

    split_points = get_split_points(mp3_path=AUDIO_FILE, max_file_size=10.0)
    print(split_points)

    if split_points:
        chunk_files = chunk_mp3_file(mp3_path=AUDIO_FILE, split_points=split_points)
        chunk_files = sorted(chunk_files, key=lambda x: int(re.findall(r'\d+', x)[0]))
        raw_transcript = combine_transcription_chunks(chunk_files=chunk_files)

    else:
        raw_transcript = combine_transcription_chunks(chunk_files=[AUDIO_FILE])

    final_output = process_raw_transcript(raw_transcript=raw_transcript)
            
