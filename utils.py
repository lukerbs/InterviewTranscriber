import os
from pydub import AudioSegment, silence

def get_audio_duration(mp3_path:str):
    audio = AudioSegment.from_mp3(mp3_path)
    # convert milliseconds to seconds
    length_in_seconds = len(audio) / 1000.0
    length_in_seconds = round(length_in_seconds, 2)
    print(f"Length of the MP3 file: {length_in_seconds} seconds")
    return length_in_seconds


def downsample_audio(audio_segment, target_sample_rate=16000):
    # Change the frame rate (sample rate)
    audio_segment = audio_segment.set_frame_rate(target_sample_rate)
    
    # You can also reduce the number of channels or sample width if needed
    audio_segment = audio_segment.set_channels(1)  # Convert to mono
    audio_segment = audio_segment.set_sample_width(1)  # Reduce sample width (8-bit audio)
    return audio_segment

def get_sample_rate(path):
    # Gets the sample rate of an audio or video file in kHz
    audio = AudioSegment.from_file(path)
    sample_rate_hz = audio.frame_rate
    print(f"Sample Rate: {sample_rate_hz} Hz")
    return sample_rate_hz

def mp4_to_mp3(mp4_path, mp3_path, sample_rate=None):
    """
    Converts an MP4 file to MP3 audio with an optional sample rate.

    Args:
        mp4_path (str): Path to the MP4 file.
        mp3_path (str): Destination path to save the MP3 file.
        sample_rate (int, optional): Desired sample rate for the MP3 file. Defaults to None (original sample rate).

    Returns:
        None: Returns None.
    """
    print(f"Converting '{mp4_path}' to MP3...")
    # Load the MP4 file
    audio = AudioSegment.from_file(mp4_path, format="mp4")
    if sample_rate:
        # Set the sample rate if provided
        print(f'Downsampled audio to: {sample_rate} Hz')
        audio = audio.set_frame_rate(sample_rate)

    # Export the MP3
    audio.export(mp3_path, format="mp3")
    print(f"Successfully converted to: {mp3_path}")
    return None

def get_silence_timestamps(mp3_path, silence_threshold=-40, min_silence_duration=1000, midpoint=True, downsample=True):
    """Finds timestamps in an MP3 conversation where there are pauses longer than a second.

    Args:
        mp3_path (str): Path to MP3 file
        silence_threshold (int, optional): The threshold for detecting silence (in dBFS)
        min_silence_duration (int, optional): Minimum duration of silence (in ms).
        midpoint (bool): Return list of midpoints between start and end times of silences

    Returns:
        list[float]: List of timestamps of silences longer than 1 second (timestamp at middle of silence)
    """
    print(f"Retrieving timestamps (seconds) for audio silences / pauses > 1 second...")
    def get_midpoint(start_end: tuple):
        midpoint = min(start_end) + ((max(start_end) - min(start_end)) / 2)
        return round(midpoint, 2)
    
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_path)

    if downsample:
        audio = downsample_audio(audio_segment=audio)

    # Detect silent parts in the audio
    pauses = silence.detect_silence(audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold)

    # Convert the pause timestamps from milliseconds to seconds and return
    pause_times = [(start / 1000, end / 1000) for start, end in pauses]
    if midpoint:
        # Return pause times as mid points between start and end times of silences
        pause_times = [get_midpoint(pause) for pause in pause_times]

    print(f"Silence Timestamps: {pause_times}")
    return pause_times


def get_file_size(path):
    """Returns the size of a file in MB

    Args:
        path (str): Path to the file

    Returns:
        float: Size of the file in MB
    """
    print(f"Getting size of file: '{path}'.")
    # Get file size in bytes
    file_size_bytes = os.path.getsize(path)
    file_size_mb = file_size_bytes / (1024 * 1024)
    print(f"File size: {file_size_mb:.2f} MB")
    return file_size_mb


def get_split_points(mp3_path: str, max_file_size:float=10.0):
    """This function splits an audio file into chunks based on a max file size (MB)

    Args:
        mp3_path (str): Path to mp3 file
        max_file_size (float, optional): Max size of mp3 chunks in MB. Defaults to 10.0.

    Returns:
        list: list of timestamps
    """
    file_size_mb = get_file_size(path=mp3_path)
    if file_size_mb > max_file_size:
        print(f"MP3 file '{mp3_path}' ({file_size_mb} MB) exceeds max file size of {max_file_size} MB.")

        num_splits = int((file_size_mb / max_file_size)) - 1
        if num_splits == 0:
            num_splits = 1

        audio_duration_seconds = get_audio_duration(mp3_path=mp3_path)
        num_chunks = num_splits + 1
        chunk_length = audio_duration_seconds / num_chunks

        time_point = 0
        split_points = []
        while len(split_points) < num_splits:
            time_point += chunk_length
            split_points.append(time_point)
        
        # Get list of all pause / silence timestamps in audio greater than 1 second
        silence_timestamps = get_silence_timestamps(mp3_path=mp3_path)

        approximate_split_points = []
        for time_point in split_points:
            nearest_silence_point = min(silence_timestamps, key=lambda x: abs(x - time_point))
            approximate_split_points.append(nearest_silence_point)
            
        
        print(f'Silence Split Points: {approximate_split_points}')
        return approximate_split_points
    
    else:
        print(f"Audio file does not exceed max file size ({max_file_size} MB). No chunking required.")
        return None
    
def chunk_mp3_file(mp3_path: str, split_points: list[float]):
    """This function chunks an MP3 file into smaller mp3 chunks based on a list of points to split the file. 


    Args:
        mp3_path (str): Path to the original MP3 file.
        split_points (list[float]): List of numbers representing the times (in seconds) where the audio file should be split.
    """
    AUDIO_CHUNKS_PATH = f'{os.path.dirname(__file__)}/audio_files/audio_chunks'
    chunk_files = os.listdir(AUDIO_CHUNKS_PATH)

    num_chunks = len(split_points) + 1
    print(f"Splitting audio file into {num_chunks} mp3 chunks...")

    # Remove any existing MP3 chunk files from previous runs. 
    old_mp3_chunks = [file for file in chunk_files if '.mp3' in file.lower()]
    if old_mp3_chunks:
        for file in old_mp3_chunks:
            os.remove(f"{AUDIO_CHUNKS_PATH}/{file}")
        print(f"Deleted {len(old_mp3_chunks)} audio chunk file(s) from '{AUDIO_CHUNKS_PATH}/' directory.")

    # Load audio
    audio = AudioSegment.from_mp3(mp3_path)
    # Convert split points from seconds to milliseconds
    split_points_ms = [int(point * 1000) for point in split_points]
    
    # Add the start and end points to split points list
    split_points_ms = [0] + split_points_ms + [len(audio)]
    
    # Iterate through the split points and create chunks
    print(f"Saving {num_chunks} file chunks to '{AUDIO_CHUNKS_PATH}/'.")
    saved_chunks = []
    for i in range(len(split_points_ms) - 1):
        start = split_points_ms[i]
        end = split_points_ms[i + 1]
        chunk = audio[start:end]
        
        # Save the chunk as an MP3 file
        chunk_filename = os.path.join(AUDIO_CHUNKS_PATH, f"chunk_{i+1}.mp3")
        chunk.export(chunk_filename, format="mp3")
        saved_chunks.append(chunk_filename)
    
    print(f"Audio file has been split into {len(split_points_ms)-1} chunks.")
    return saved_chunks


    


    
