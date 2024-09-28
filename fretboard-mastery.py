import tkinter as tk
import pygame.mixer
import threading
import time

pygame.mixer.init()
tick_sound = pygame.mixer.Sound("sounds/drumstick.wav")
metronome_running = False


def play_tick():
    """Plays the tick sound using pygame.mixer."""
    tick_sound.play()


def metronome():
    """Runs the metronome in a loop with an interval based on BPM."""
    global metronome_running
    while metronome_running:
        bpm = bpm_slider.get()
        interval = 60.0 / bpm
        print(f"Tick at {bpm} BPM")
        play_tick()
        time.sleep(interval)


def start_metronome():
    """Starts the metronome in a separate thread."""
    global metronome_running
    if not metronome_running:
        metronome_running = True
        threading.Thread(target=metronome, daemon=True).start()


def stop_metronome():
    """Stops the metronome."""
    global metronome_running
    metronome_running = False


def draw_fretboard(canvas, canvas_width):
    """Draws the fretboard with 22 frets, 6 strings, and correct inlays."""
    string_spacing = 30
    canvas_height = string_spacing * 6 + 40

    # Adjusting fret sizes: The first fret is slightly larger to account for the thicker 0th fret
    normal_fret_width = canvas_width // 22
    first_fret_width = normal_fret_width + 5  # Increase the width of the first fret
    fret_line_top = 50  # Top y-coordinate for fret lines (aligned with the first string)
    fret_line_bottom = canvas_height - 20  # Bottom y-coordinate for fret lines (aligned with the last string)

    canvas.config(width=canvas_width, height=canvas_height)

    # Fret inlays on frets 5, 7, 9, 12, 15, 17 (corrected by subtracting 1)
    inlay_frets = [4, 6, 8, 14, 16]  # Subtracting 1 from each fret to correct the offset
    inlay_color = "light grey"
    inlay_radius = 5

    # Center y position for inlays
    y_center = (fret_line_top + fret_line_bottom) // 2

    # Draw single dot inlays first
    for fret in inlay_frets:
        x = (fret + 0.5) * normal_fret_width + first_fret_width - normal_fret_width
        canvas.create_oval(x - inlay_radius, y_center - inlay_radius, x + inlay_radius, y_center + inlay_radius,
                           fill=inlay_color, outline="")

    # Double inlays for fret 12 with wider separation
    x_12 = (11 + 0.5) * normal_fret_width + first_fret_width - normal_fret_width  # Adjusted for the first fret
    double_inlay_offset = 20  # Wider distance between the dots
    canvas.create_oval(x_12 - inlay_radius, y_center - double_inlay_offset, x_12 + inlay_radius,
                       y_center - double_inlay_offset + 2 * inlay_radius, fill=inlay_color, outline="")
    canvas.create_oval(x_12 - inlay_radius, y_center + double_inlay_offset - 2 * inlay_radius, x_12 + inlay_radius,
                       y_center + double_inlay_offset, fill=inlay_color, outline="")

    # Now draw the frets
    canvas.create_line(0, fret_line_top, 0, fret_line_bottom, width=15)  # Thicker 0th fret
    canvas.create_line(first_fret_width, fret_line_top, first_fret_width, fret_line_bottom, width=2)

    for i in range(2, 23):
        x = first_fret_width + (i - 1) * normal_fret_width
        canvas.create_line(x, fret_line_top, x, fret_line_bottom, width=2)

    # Draw the strings over the frets and inlays
    for i in range(6):
        canvas.create_line(0, 50 + i * string_spacing, canvas_width, 50 + i * string_spacing, width=2)


def on_click(event):
    """Handles click events on the fretboard to print the corresponding note."""
    pass


root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

# Reduce the width of the fretboard slightly (90% of window width)
canvas_width = int(window_width * 0.9)
canvas = tk.Canvas(root, width=canvas_width, height=250)
canvas.grid(row=0, column=0, columnspan=3, pady=10, sticky="w")

draw_fretboard(canvas, canvas_width)
canvas.bind("<Button-1>", on_click)

metronome_frame = tk.LabelFrame(root, text="Metronome", padx=10, pady=10, width=window_width - 40)
metronome_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

bpm_label = tk.Label(metronome_frame, text="BPM:")
bpm_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

bpm_slider = tk.Scale(metronome_frame, from_=40, to=240, orient=tk.HORIZONTAL, length=300)
bpm_slider.set(120)
bpm_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')

start_metronome_button = tk.Button(metronome_frame, text="Start", command=start_metronome)
start_metronome_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

stop_metronome_button = tk.Button(metronome_frame, text="Stop", command=stop_metronome)
stop_metronome_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

root.mainloop()

pygame.mixer.quit()