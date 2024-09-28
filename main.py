import tkinter as tk
import pygame
import threading

from fretboard import highlight_notes
from fretboard_panel import create_fretboard_panel
from metronome_panel import create_metronome_panel
from random_note_panel import create_random_note_panel
from metronome import start_metronome, stop_metronome

# Initialize the Tkinter window
root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 1000
window_height = 700
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

root.focus_force()

# Variables to track interval checkbox states
checkbox_states = {'root': 1, 'M3': 0, 'P5': 0, 'M7': 0}

# Create an event to synchronize metronome ticks with random note generation
tick_event = threading.Event()

def highlight_callback(note):
    """Highlight notes on the fretboard based on the intervals selected."""
    highlight_notes(canvas, note, checkbox_states)

# Create the fretboard panel
canvas = create_fretboard_panel(root, window_width, row=0, highlight_callback=highlight_callback, checkbox_states=checkbox_states)

# Create the random note practice panel and pass the highlight function, sync with tick_event
random_note_slider = create_random_note_panel(root, window_width, row=1, highlight_notes=lambda note: highlight_notes(canvas, note, checkbox_states), tick_event=tick_event)

# Create the metronome panel and sync with tick_event
bpm_slider = create_metronome_panel(root, window_width, row=2, tick_event=tick_event)

root.mainloop()

pygame.mixer.quit()