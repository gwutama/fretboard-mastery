import tkinter as tk
import pygame
from fretboard import draw_fretboard
from metronome_panel import create_metronome_panel

root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

# Focus the window when it starts
root.focus_force()

# Draw the fretboard
canvas_width = int(window_width * 0.9)
canvas = tk.Canvas(root, width=canvas_width, height=250)
canvas.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")
draw_fretboard(canvas, canvas_width)

create_metronome_panel(root, window_width)

root.mainloop()

pygame.mixer.quit()