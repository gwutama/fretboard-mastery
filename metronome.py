import os
import pygame.mixer
import threading
import time

basedir = os.path.dirname(__file__)

# Initialize pygame for sound playback
pygame.mixer.init()
tick_sound = pygame.mixer.Sound(os.path.join(basedir, "sounds", "drumstick.wav"))
metronome_running = False


def play_tick():
    """Plays the tick sound using pygame.mixer."""
    tick_sound.play()


def metronome(bpm_slider, tick_event):
    """Runs the metronome in a loop with an interval based on BPM, synchronizes with random note generator."""
    global metronome_running
    next_tick_time = time.time()  # Initialize the time for the next tick

    while metronome_running:
        bpm = bpm_slider.get()  # Get BPM from the slider
        interval = 60.0 / bpm  # Calculate the interval in seconds per beat (tick)

        current_time = time.time()

        # Check if it's time to play the next tick
        if current_time >= next_tick_time:
            play_tick()  # Play tick sound
            tick_event.set()  # Signal the random note generator
            next_tick_time += interval  # Calculate the time for the next tick

        # Small sleep to prevent high CPU usage
        time.sleep(0.001)


def start_metronome(bpm_slider, tick_event):
    """Starts the metronome in a separate thread, synchronized with the random note generator."""
    global metronome_running
    if not metronome_running:
        metronome_running = True
        threading.Thread(target=metronome, args=(bpm_slider, tick_event), daemon=True).start()


def stop_metronome():
    """Stops the metronome."""
    global metronome_running
    metronome_running = False