import tkinter as tk
import pygame

from fretboard import highlight_notes
from fretboard_panel import create_fretboard_panel
from metronome_panel import create_metronome_panel
from random_note_panel import create_random_note_panel

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

def highlight_callback(note):
    """Highlight notes on the fretboard based on the intervals selected."""
    highlight_notes(canvas, note, checkbox_states)

# Create the fretboard panel and pass checkbox_states to track changes
canvas = create_fretboard_panel(root, window_width, row=0, highlight_callback=highlight_callback, checkbox_states=checkbox_states)

# Create the random note practice panel and pass the highlight function
create_random_note_panel(root, window_width, row=1, highlight_notes=lambda note: highlight_notes(canvas, note, checkbox_states))

# Create the metronome panel
create_metronome_panel(root, window_width, row=2)

root.mainloop()

pygame.mixer.quit()