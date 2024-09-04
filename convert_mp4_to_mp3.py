
# Put your folder path here
FOLDER_PATH = "/Users/jsandor/Downloads/f"  

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def convert_mp4_to_mp3(input_file):
    output_file = os.path.splitext(input_file)[0] + '.mp3'
    
    ffmpeg_command = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        '-acodec', 'libmp3lame',
        '-q:a', '2',
        output_file
    ]
    
    try:
        subprocess.run(ffmpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Converted: {input_file} -> {output_file}")
    except subprocess.CalledProcessError:
        print(f"Error converting: {input_file}")

def process_folder(folder_path):
    mp4_files = [f for f in os.listdir(folder_path) if f.endswith('.mp4')]
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(convert_mp4_to_mp3, os.path.join(folder_path, f)) for f in mp4_files]
        
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    if not os.path.isdir(FOLDER_PATH):
        print(f"Error: {FOLDER_PATH} is not a valid directory.")
    else:
        process_folder(FOLDER_PATH)


