import pygame.mixer
import threading
import time

# Initialize pygame for sound playback
pygame.mixer.init()
tick_sound = pygame.mixer.Sound("sounds/drumstick.wav")
metronome_running = False

def play_tick():
    """Plays the tick sound using pygame.mixer."""
    tick_sound.play()

def metronome(bpm_slider, tick_event):
    """Runs the metronome in a loop with an interval based on BPM, synchronizes with random note generator."""
    global metronome_running
    while metronome_running:
        bpm = bpm_slider.get()  # Get BPM from the slider
        interval = 60.0 / bpm
        play_tick()  # Play tick sound
        tick_event.set()  # Set the event to signal the random note generator
        time.sleep(interval)  # Wait for the next tick

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