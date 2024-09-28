import tkinter as tk
from fretboard import draw_fretboard, highlight_notes

def on_checkbox_change(canvas, root_checkbox, m3_checkbox, p5_checkbox, m7_checkbox, checkbox_states):
    """Update the checkbox states and re-highlight the fretboard."""
    # Update checkbox_states
    checkbox_states['root'] = root_checkbox.get()
    checkbox_states['M3'] = m3_checkbox.get()
    checkbox_states['P5'] = p5_checkbox.get()
    checkbox_states['M7'] = m7_checkbox.get()

    # Get the currently highlighted note and reapply the highlights
    highlighted_note = canvas.getvar("highlighted_note") if canvas.getvar("highlighted_note") else None
    if highlighted_note:
        highlight_notes(canvas, highlighted_note, checkbox_states)

def create_fretboard_panel(root, window_width, row, highlight_callback, checkbox_states):
    """Creates the fretboard panel with checkboxes for note intervals."""
    fretboard_frame = tk.LabelFrame(root, text="Fretboard", padx=10, pady=10, width=window_width - 40)
    fretboard_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

    # Checkboxes for note intervals
    root_checkbox = tk.IntVar(value=checkbox_states['root'])
    m3_checkbox = tk.IntVar(value=checkbox_states['M3'])
    p5_checkbox = tk.IntVar(value=checkbox_states['P5'])
    m7_checkbox = tk.IntVar(value=checkbox_states['M7'])

    tk.Checkbutton(fretboard_frame, text="Root", variable=root_checkbox,
                   command=lambda: on_checkbox_change(canvas, root_checkbox, m3_checkbox, p5_checkbox, m7_checkbox, checkbox_states)).grid(row=1, column=0, padx=5, pady=5, sticky='w')
    tk.Checkbutton(fretboard_frame, text="M3", variable=m3_checkbox,
                   command=lambda: on_checkbox_change(canvas, root_checkbox, m3_checkbox, p5_checkbox, m7_checkbox, checkbox_states)).grid(row=1, column=1, padx=5, pady=5, sticky='w')
    tk.Checkbutton(fretboard_frame, text="P5", variable=p5_checkbox,
                   command=lambda: on_checkbox_change(canvas, root_checkbox, m3_checkbox, p5_checkbox, m7_checkbox, checkbox_states)).grid(row=1, column=2, padx=5, pady=5, sticky='w')
    tk.Checkbutton(fretboard_frame, text="M7", variable=m7_checkbox,
                   command=lambda: on_checkbox_change(canvas, root_checkbox, m3_checkbox, p5_checkbox, m7_checkbox, checkbox_states)).grid(row=1, column=3, padx=5, pady=5, sticky='w')

    # Create the fretboard canvas
    canvas_width = int(window_width * 0.9)
    canvas = tk.Canvas(fretboard_frame, width=canvas_width, height=250)
    canvas.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="w")

    # Draw the fretboard
    draw_fretboard(canvas, canvas_width, highlight_callback)

    return canvas