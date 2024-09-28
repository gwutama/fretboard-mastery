import tkinter as tk
import random
import threading
import time

chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
random_note_running = False

def display_random_note(note_label, highlight_notes):
    """Generates and displays a random note, and highlights it on the fretboard."""
    random_note = random.choice(chromatic_scale)
    note_label.config(text=random_note)  # Update label with random note
    highlight_notes(random_note)  # Highlight the matching notes on the fretboard

def random_note_task(interval_slider, note_label, highlight_notes):
    """Task to display a random note at selected intervals."""
    global random_note_running
    while random_note_running:
        display_random_note(note_label, highlight_notes)  # Show a new random note
        interval = interval_slider.get()  # Get interval from the slider
        time.sleep(interval)

def start_random_note_practice(interval_slider, note_label, highlight_notes):
    """Starts the random note practice in a separate thread."""
    global random_note_running
    if not random_note_running:
        random_note_running = True
        threading.Thread(target=random_note_task, args=(interval_slider, note_label, highlight_notes), daemon=True).start()

def stop_random_note_practice():
    """Stops the random note practice."""
    global random_note_running
    random_note_running = False

def create_random_note_panel(root, window_width, row, highlight_notes):
    """Creates the Random Note Practice panel."""
    random_note_frame = tk.LabelFrame(root, text="Random Note Generator", padx=10, pady=10, width=window_width - 40)
    random_note_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

    interval_label = tk.Label(random_note_frame, text="Interval (secs):", anchor="w", width=15)
    interval_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    interval_slider = tk.Scale(random_note_frame, from_=5, to=60, orient=tk.HORIZONTAL, length=300)
    interval_slider.set(5)  # Default value set to 10 seconds
    interval_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    # Center the note label using grid and set its text color to blue
    note_label = tk.Label(random_note_frame, text="Note", font=("Arial", 50, "bold"), fg="red")
    note_label.grid(row=1, column=0, columnspan=4, padx=5, pady=20, sticky="nsew")

    start_button = tk.Button(random_note_frame, text="Start", command=lambda: start_random_note_practice(interval_slider, note_label, highlight_notes))
    start_button.grid(row=0, column=2, padx=(5, 2), pady=5, sticky='e')

    stop_button = tk.Button(random_note_frame, text="Stop", command=stop_random_note_practice)
    stop_button.grid(row=0, column=3, padx=(2, 5), pady=5, sticky='w')

    # Configure column stretching to center the note label
    random_note_frame.grid_columnconfigure(0, weight=1)
    random_note_frame.grid_columnconfigure(1, weight=1)
    random_note_frame.grid_columnconfigure(2, weight=0)
    random_note_frame.grid_columnconfigure(3, weight=0)

    return interval_slider