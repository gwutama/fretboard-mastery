import tkinter as tk
import pygame
from fretboard import draw_fretboard
from metronome_panel import create_metronome_panel
from random_note_panel import create_random_note_panel  # Import random note panel

root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 800
window_height = 600  # Adjust the window height to fit all panels
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

# Focus the window when it starts
root.focus_force()

# Draw the fretboard (row 0)
canvas_width = int(window_width * 0.9)
canvas = tk.Canvas(root, width=canvas_width, height=250)
canvas.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
draw_fretboard(canvas, canvas_width)

# Create the random note practice panel (row 1)
create_random_note_panel(root, window_width, row=1)

# Create the metronome panel (row 2)
create_metronome_panel(root, window_width, row=2)

root.mainloop()

pygame.mixer.quit()