import tkinter as tk
from metronome import start_metronome, stop_metronome

def create_metronome_panel(root, window_width, row):
    """Creates the metronome panel and returns the slider widget."""
    metronome_frame = tk.LabelFrame(root, text="Metronome", padx=10, pady=10, width=window_width - 40)
    metronome_frame.grid(row=row, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

    # Set a fixed width for the label
    bpm_label = tk.Label(metronome_frame, text="BPM:", anchor="w", width=15)  # Approximate width for 100px
    bpm_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    bpm_slider = tk.Scale(metronome_frame, from_=40, to=240, orient=tk.HORIZONTAL, length=300)
    bpm_slider.set(120)
    bpm_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    # Reduced padx to bring buttons closer
    start_metronome_button = tk.Button(metronome_frame, text="Start", command=lambda: start_metronome(bpm_slider))
    start_metronome_button.grid(row=0, column=2, padx=(5, 2), pady=5, sticky='e')

    stop_metronome_button = tk.Button(metronome_frame, text="Stop", command=stop_metronome)
    stop_metronome_button.grid(row=0, column=3, padx=(2, 5), pady=5, sticky='w')

    # Configure column stretching for layout
    metronome_frame.grid_columnconfigure(0, weight=1)
    metronome_frame.grid_columnconfigure(1, weight=1)
    metronome_frame.grid_columnconfigure(2, weight=0)
    metronome_frame.grid_columnconfigure(3, weight=0)

    return bpm_slider