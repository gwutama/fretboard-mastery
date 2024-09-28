import tkinter as tk
import pygame
from fretboard import draw_fretboard, highlight_notes
from metronome_panel import create_metronome_panel
from random_note_panel import create_random_note_panel

root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 1000
window_height = 600
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

# Focus the window when it starts
root.focus_force()

# Draw the fretboard
canvas_width = int(window_width * 0.9)
canvas = tk.Canvas(root, width=canvas_width, height=250)
canvas.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
draw_fretboard(canvas, canvas_width)

# Create the metronome panel
create_metronome_panel(root, window_width, row=2)

# Create the random note practice panel and pass the highlight_notes function
create_random_note_panel(root, window_width, row=1, highlight_notes=lambda note: highlight_notes(canvas, note))

root.mainloop()

pygame.mixer.quit()