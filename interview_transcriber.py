import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import threading

from pydub import AudioSegment
import os
import re

from chatgpt import chatgpt, transcribe_audio, segment_by_speaker
from utils import mp4_to_mp3, get_split_points, chunk_mp3_file  # Import the utility functions

AUDIO_DIR = "./audio_files/"
CHUNKS_DIR = "./audio_files/audio_chunks/"

# Ensure the audio directories exist
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)

# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if file_path:
        selected_file_label.config(text=f"Selected: {os.path.basename(file_path)}")
        transcribe_button.config(state=tk.NORMAL)
        global VIDEO_FILE
        VIDEO_FILE = file_path

# Function to handle transcription process
# Function to handle transcription process
def transcribe_interview():
    def run_transcription():
        # Start progress bar
        progress.config(mode='indeterminate')
        progress.start()

        try:
            # Step 1: Update UI - Converting MP4 to MP3
            transcription_display.delete(1.0, tk.END)
            transcription_display.insert(tk.END, "Step 1: Converting video file to audio (MP3)...\n")
            transcription_display.update_idletasks()

            # Convert MP4 to MP3 and save it
            audio_file = os.path.join(AUDIO_DIR, "converted_audio.mp3")
            mp4_to_mp3(VIDEO_FILE, audio_file)

            # Step 2: Check if chunking is necessary
            transcription_display.insert(tk.END, "Step 2: Checking if chunking is required...\n")
            transcription_display.update_idletasks()

            # Get split points based on file size
            split_points = get_split_points(mp3_path=audio_file, max_file_size=10.0)

            if split_points:
                # Step 3: Chunking audio
                transcription_display.insert(tk.END, "Step 3: Audio file too large, chunking into smaller segments...\n")
                transcription_display.update_idletasks()

                # If the audio file is too large, chunk it into mp3 audio segments
                chunk_files = chunk_mp3_file(mp3_path=audio_file, split_points=split_points)
                chunk_files = sorted(chunk_files, key=lambda x: int(re.findall(r'\d+', x)[0]))

                # Step 4: Transcribing each chunk
                raw_transcripts = []
                for i, chunk_path in enumerate(chunk_files):
                    transcription_display.insert(tk.END, f"Step 4: Transcribing chunk {i+1}/{len(chunk_files)}...\n")
                    transcription_display.update_idletasks()
                    
                    raw_transcript = transcribe_audio(audio_file=chunk_path)
                    raw_transcripts.append(raw_transcript.strip())

                # Concatenate the transcripts
                raw_transcript = " ".join(raw_transcripts)
            else:
                # Step 3 (No chunking needed): Transcribing entire file
                transcription_display.insert(tk.END, "Step 3: Audio file is within max file size threshold. No segmenting required...\n")
                transcription_display.update_idletasks()

                transcription_display.insert(tk.END, "Step 4: Transcribing audio to text...\n")
                transcription_display.update_idletasks()
                raw_transcript = transcribe_audio(audio_file=audio_file)

            # Step 5: Segmenting transcript by speaker
            transcription_display.insert(tk.END, "Step 5: Segmenting transcript by speaker...\n")
            transcription_display.update_idletasks()

            # Segment the transcript by speaker
            speaker_segmented_transcript = segment_by_speaker(transcription=raw_transcript)

            # Step 6: Updating UI with transcription
            transcription_display.delete(1.0, tk.END)
            transcription_display.insert(tk.END, speaker_segmented_transcript)

            # Enable the save button after transcription is complete
            save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during transcription: {e}")
        finally:
            # Stop progress bar
            progress.stop()
            progress.config(mode='determinate', maximum=100, value=100)
            transcribe_button.config(state=tk.NORMAL)

    # Indicate that transcription is in progress
    transcription_display.delete(1.0, tk.END)
    transcription_display.insert(tk.END, "Starting transcription process...\n")
    transcription_display.update_idletasks()  # Force update of the UI
    transcribe_button.config(state=tk.DISABLED)  # Disable button during processing

    # Run transcription in a separate thread to prevent UI freezing
    transcription_thread = threading.Thread(target=run_transcription)
    transcription_thread.start()

# Function to save transcript to file
def save_transcript():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, 'w') as file:
            file.write(transcription_display.get(1.0, tk.END))
        messagebox.showinfo("File Saved", f"Transcript saved to {file_path} successfully.")

# Main application window
root = tk.Tk()
root.title("Video Transcription Tool")

# File selection frame
file_frame = tk.Frame(root)
file_frame.pack(pady=10)

select_button = tk.Button(file_frame, text="Select Video File", command=select_file)
select_button.pack(side=tk.LEFT, padx=5)

selected_file_label = tk.Label(file_frame, text="No file selected")
selected_file_label.pack(side=tk.LEFT)

# Transcription button
transcribe_button = tk.Button(root, text="TRANSCRIBE INTERVIEW", state=tk.DISABLED, command=transcribe_interview)
transcribe_button.pack(pady=10)

# Transcription display area
transcription_display = ScrolledText(root, wrap=tk.WORD, width=80, height=20)
transcription_display.pack(pady=10)

# Progress bar
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
progress.pack(pady=10)

# Save to file button
save_button = tk.Button(root, text="Save to File", state=tk.DISABLED, command=save_transcript)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
