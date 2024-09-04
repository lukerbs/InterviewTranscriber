import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading

from pydub import AudioSegment
import os
import re

from chatgpt import chatgpt, transcribe_audio, segment_by_speaker

# Function to handle file selection
def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if file_path:
        selected_file_label.config(text=f"Selected: {os.path.basename(file_path)}")
        transcribe_button.config(state=tk.NORMAL)
        global AUDIO_FILE
        AUDIO_FILE = file_path

# Function to handle transcription process
def transcribe_interview():
    def run_transcription():
        # Convert the video file to audio (mp3) here if necessary
        # Assuming AUDIO_FILE is already an audio file for simplicity

        raw_transcript = transcribe_audio(audio_file=AUDIO_FILE)
        speaker_segmented_transcript = segment_by_speaker(transcription=raw_transcript)

        # Update UI with transcription
        transcription_display.delete(1.0, tk.END)
        transcription_display.insert(tk.END, speaker_segmented_transcript)

        # Enable the save button after transcription is complete
        save_button.config(state=tk.NORMAL)
        messagebox.showinfo("Transcription Complete", "The transcription has been completed.")

    # Indicate that transcription is in progress
    transcription_display.delete(1.0, tk.END)
    transcription_display.insert(tk.END, "Transcription in progress... Please wait.")
    transcribe_button.config(state=tk.DISABLED)

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

# Save to file button
save_button = tk.Button(root, text="Save to File", state=tk.DISABLED, command=save_transcript)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
