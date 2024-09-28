import tkinter as tk
import pygame.mixer
import threading
import time

# Initialize pygame for sound
pygame.mixer.init()

# Load the tick sound (replace with the correct path to your wav file)
tick_sound = pygame.mixer.Sound("sounds/drumstick.wav")

# Flag to control the metronome
metronome_running = False


def play_tick():
    """Play the tick sound using pygame.mixer."""
    tick_sound.play()


def metronome():
    """Simple metronome using threading."""
    global metronome_running
    while metronome_running:
        bpm = bpm_slider.get()  # Get BPM from slider
        interval = 60.0 / bpm
        print(f"Tick at {bpm} BPM")
        play_tick()  # Play the tick sound on each tick
        time.sleep(interval)


def start_metronome():
    """Start the metronome in a new thread."""
    global metronome_running
    if not metronome_running:  # Avoid starting multiple threads
        metronome_running = True
        threading.Thread(target=metronome, daemon=True).start()


def stop_metronome():
    """Stop the metronome."""
    global metronome_running
    metronome_running = False


# GUI Setup
def draw_fretboard(canvas, canvas_width):
    """Draws a simple fretboard with 22 frets."""
    fret_width = canvas_width // 22  # Make the frets fill the entire canvas width
    string_spacing = 30  # Spacing between strings
    num_frets = 22
    num_strings = 6
    canvas_height = string_spacing * num_strings + 50

    canvas.config(width=canvas_width, height=canvas_height)

    # Draw strings (6 strings)
    for i in range(num_strings):
        canvas.create_line(0, 50 + i * string_spacing, canvas_width, 50 + i * string_spacing, width=2)

    # Draw frets (22 frets)
    for i in range(num_frets + 1):  # Including the nut (fret 0)
        canvas.create_line(i * fret_width, 50, i * fret_width, canvas_height - 20, width=2)


def on_click(event):
    """Handle clicks on the fretboard."""
    fret_width = canvas.winfo_width() // 22
    string_spacing = 30
    fret = event.x // fret_width
    string = (event.y - 50) // string_spacing
    if 0 <= fret <= 21 and 0 <= string <= 5:
        note = 40 + fret + (5 - string) * 5  # Map fret/string to MIDI note
        print(f"Played note: {note}")  # Print the note for testing


# Initialize Tkinter window
root = tk.Tk()
root.title("Fretboard Mastery")

# Set fixed window size (e.g., 800px wide and 400px high)
window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)  # Disable window resizing

# Create the canvas for the fretboard and make it as wide as the window (no left padding)
canvas_width = window_width  # Make it exactly as wide as the window
canvas = tk.Canvas(root, width=canvas_width, height=250)
canvas.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")  # Left-justified with no padding

# Draw fretboard with 22 frets
draw_fretboard(canvas, canvas_width)

# Bind click event to play note
canvas.bind("<Button-1>", on_click)

# Create a labeled frame (group) for metronome
metronome_frame = tk.LabelFrame(root, text="Metronome", padx=10, pady=10, width=window_width - 40)
metronome_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

# UI Controls for BPM Slider (Horizontal Layout inside the metronome group)
bpm_label = tk.Label(metronome_frame, text="BPM:")
bpm_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Add a wider slider to adjust BPM (from 40 to 240 BPM)
bpm_slider = tk.Scale(metronome_frame, from_=40, to=240, orient=tk.HORIZONTAL, length=300)  # Make the slider wider
bpm_slider.set(120)  # Default value set to 120 BPM
bpm_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Add Start and Stop buttons
start_metronome_button = tk.Button(metronome_frame, text="Start", command=start_metronome)
start_metronome_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

stop_metronome_button = tk.Button(metronome_frame, text="Stop", command=stop_metronome)
stop_metronome_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

# Run the application
root.mainloop()

# Cleanup mixer
pygame.mixer.quit()