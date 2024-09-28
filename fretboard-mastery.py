import tkinter as tk
import pygame.mixer
import threading
import time

pygame.mixer.init()
tick_sound = pygame.mixer.Sound("sounds/drumstick.wav")
metronome_running = False

# Notes for each string (standard tuning EADGBE), mirrored vertically
notes = ['E', 'B', 'G', 'D', 'A', 'E']  # High E string is now at the top, Low E is at the bottom

# All possible notes in a chromatic scale
chromatic_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def get_note_name(string_note, fret):
    """Returns the note name for a given string and fret."""
    start_index = chromatic_scale.index(string_note)
    return chromatic_scale[(start_index + fret) % len(chromatic_scale)]


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
    """Draws the fretboard with 22 frets, 6 strings, note names, and inlays."""
    left_padding = 30  # Add padding to the left for the 0th fret notes
    string_spacing = 30
    canvas_height = string_spacing * 6 + 40
    normal_fret_width = (canvas_width - left_padding) // 22
    first_fret_width = normal_fret_width + 5
    fret_line_top = 50
    fret_line_bottom = canvas_height - 20

    canvas.config(width=canvas_width, height=canvas_height)

    # Fret inlays on frets 5, 7, 9, 12, 15, 17
    inlay_frets = [4, 6, 8, 14, 16]
    inlay_color = "black"
    inlay_radius = 5

    # Position the inlays outside the frets (below the fretboard)
    y_inlay_position = fret_line_bottom + 17  # Position below the frets

    # Draw single dot inlays between frets
    for fret in inlay_frets:
        x = left_padding + (fret + 0.5) * normal_fret_width + first_fret_width - normal_fret_width
        canvas.create_oval(x - inlay_radius, y_inlay_position - inlay_radius, x + inlay_radius, y_inlay_position + inlay_radius,
                           fill=inlay_color, outline="")

    # Double inlays for fret 12 with horizontal arrangement
    x_12 = left_padding + (11 + 0.5) * normal_fret_width + first_fret_width - normal_fret_width
    double_inlay_offset = 8
    canvas.create_oval(x_12 - inlay_radius - double_inlay_offset, y_inlay_position - inlay_radius,
                       x_12 + inlay_radius - double_inlay_offset, y_inlay_position + inlay_radius, fill=inlay_color, outline="")
    canvas.create_oval(x_12 - inlay_radius + double_inlay_offset, y_inlay_position - inlay_radius,
                       x_12 + inlay_radius + double_inlay_offset, y_inlay_position + inlay_radius, fill=inlay_color, outline="")

    # Draw frets
    canvas.create_line(left_padding, fret_line_top, left_padding, fret_line_bottom, width=15)  # Thicker 0th fret
    canvas.create_line(left_padding + first_fret_width, fret_line_top, left_padding + first_fret_width, fret_line_bottom, width=2)
    for i in range(2, 23):
        x = left_padding + first_fret_width + (i - 1) * normal_fret_width
        canvas.create_line(x, fret_line_top, x, fret_line_bottom, width=2)

    # Draw strings over the frets and inlays
    for i in range(6):
        canvas.create_line(left_padding, 50 + i * string_spacing, canvas_width, 50 + i * string_spacing, width=2)

    # Draw note names, move one fret to the left for correct positioning
    note_radius = 12
    for string in range(6):
        base_note = notes[string]  # Now using the mirrored string order
        y_pos = 50 + string * string_spacing
        for fret in range(22):
            if fret == 0:
                # Shift fret 0 notes as if they're on a "negative 1" fret
                x_pos = left_padding + first_fret_width - normal_fret_width - 20  # Further left for -1 fret effect
            else:
                # Adjust x_pos for notes to be one fret left
                x_pos = left_padding + first_fret_width + (fret - 1.5) * normal_fret_width

            note_name = get_note_name(base_note, fret)

            # Assign a tag to each note (circle + text) for easy selection later
            note_tag = f"note_{note_name}"

            # Draw circle for the note
            note_circle = canvas.create_oval(x_pos - note_radius, y_pos - note_radius, x_pos + note_radius, y_pos + note_radius,
                                             fill="dark grey", outline="", tags=note_tag)
            # Draw the note name in white
            note_text = canvas.create_text(x_pos, y_pos, text=note_name, fill="white", font=("Arial", 10, "bold"), tags=note_tag)

            # Bind click event to highlight all matching notes
            canvas.tag_bind(note_tag, "<Button-1>", lambda event, note=note_name: highlight_notes(canvas, note))


def highlight_notes(canvas, note_to_highlight):
    """Highlights all notes that match the clicked note."""
    # Reset all note colors first
    for note in chromatic_scale:
        note_tag = f"note_{note}"
        # Reset both the circle fill and text color
        for item in canvas.find_withtag(note_tag):
            if canvas.type(item) == 'oval':
                canvas.itemconfig(item, fill="dark grey")  # Reset circle fill color
            elif canvas.type(item) == 'text':
                canvas.itemconfig(item, fill="white")  # Reset text color

    # Highlight matching notes
    note_tag = f"note_{note_to_highlight}"
    for item in canvas.find_withtag(note_tag):
        if canvas.type(item) == 'oval':
            canvas.itemconfig(item, fill="blue")  # Highlight circles
        elif canvas.type(item) == 'text':
            canvas.itemconfig(item, fill="white")  # Keep the text color white

    # Force UI update to immediately reflect changes
    canvas.update_idletasks()


def on_click(event):
    """Handles click events on the fretboard to print the corresponding note."""
    pass


root = tk.Tk()
root.title("Fretboard Mastery")

window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

# Focus the window when it starts
root.focus_force()

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