import tkinter as tk
from tkinter import ttk
from chatgpt import chatgpt  # Import your chatgpt function
import threading

def send_prompt():
    """Function to handle sending the prompt and displaying the response."""
    prompt = prompt_text.get("1.0", tk.END).strip()  # Get all text from the text widget
    if prompt:
        progress_bar.start()  # Start the progress bar
        response_text.delete("1.0", tk.END)  # Clear previous response
        threading.Thread(target=process_prompt, args=(prompt,)).start()  # Run in a separate thread to avoid freezing the GUI

def process_prompt(prompt):
    """Function to process the prompt and update the UI with the response."""
    response = chatgpt(prompt)  # Call the chatgpt function
    response_text.insert(tk.END, response)  # Update the Text widget with the response
    progress_bar.stop()  # Stop the progress bar
    adjust_text_widget_height(response_text, response)  # Adjust text widget height to fit response

def adjust_text_widget_height(widget, text):
    """Adjust the height of the Text widget based on the content length."""
    line_count = text.count('\n') + 1  # Count the number of lines in the text
    widget.configure(height=min(max(line_count, 10), 30))  # Set a minimum of 10 lines and a maximum of 30 lines

def on_enter(event=None):
    """Function to handle the Enter key event."""
    send_prompt()

def copy_to_clipboard():
    """Function to copy the response text to the clipboard."""
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(response_text.get("1.0", tk.END).strip())  # Append the response text to the clipboard

# Create the main window
root = tk.Tk()
root.title("ChatGPT Query App")

# Set the default window size
root.geometry("700x600")

# Make the window resizable
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Create a frame for all the content with added padding
content_frame = tk.Frame(root, padx=15, pady=15)
content_frame.pack(fill=tk.BOTH, expand=True)

# Create a frame for the text box and button
input_frame = tk.Frame(content_frame)
input_frame.pack(fill=tk.X, padx=10, pady=10)

# Configure row and column weights for the frame to be responsive
input_frame.rowconfigure(0, weight=1)
input_frame.columnconfigure(0, weight=1)

# Create a Text widget for the prompt with a Scrollbar and a maximum height
prompt_text = tk.Text(input_frame, height=5, width=50, wrap=tk.WORD)
prompt_text.grid(row=0, column=0, sticky="nsew")

# Add a vertical scrollbar to the Text widget
prompt_scrollbar = tk.Scrollbar(input_frame, command=prompt_text.yview)
prompt_scrollbar.grid(row=0, column=1, sticky="ns")
prompt_text['yscrollcommand'] = prompt_scrollbar.set

# Allow the user to vertically resize the input Text widget, but not horizontally
input_frame.grid_propagate(True)

# Create a button to submit the prompt, placed below the prompt text box
submit_button = tk.Button(input_frame, text="Send", command=send_prompt)
submit_button.grid(row=1, column=0, pady=(5, 0))

# Create a Progressbar widget for showing progress
progress_bar = ttk.Progressbar(content_frame, mode='indeterminate')
progress_bar.pack(fill=tk.X, padx=10, pady=(10, 0))

# Create a Text widget to display the response
response_text = tk.Text(content_frame, height=10, width=50, wrap=tk.WORD)
response_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))

# Add a button to copy the response to the clipboard
copy_button = tk.Button(content_frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(padx=10, pady=(10, 0))

# Run the main loop
root.mainloop()