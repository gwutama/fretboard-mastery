import tkinter as tk
from metronome import start_metronome, stop_metronome

def create_metronome_panel(root, window_width):
    """Creates the metronome panel and returns the slider widget."""
    metronome_frame = tk.LabelFrame(root, text="Metronome", padx=10, pady=10, width=window_width - 40)
    metronome_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

    bpm_label = tk.Label(metronome_frame, text="BPM:")
    bpm_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

    bpm_slider = tk.Scale(metronome_frame, from_=40, to=240, orient=tk.HORIZONTAL, length=300)
    bpm_slider.set(120)
    bpm_slider.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    start_metronome_button = tk.Button(metronome_frame, text="Start", command=lambda: start_metronome(bpm_slider))
    start_metronome_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    stop_metronome_button = tk.Button(metronome_frame, text="Stop", command=stop_metronome)
    stop_metronome_button.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    return bpm_slider