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

def metronome(bpm_slider):
    """Runs the metronome in a loop with an interval based on BPM."""
    global metronome_running
    while metronome_running:
        bpm = bpm_slider.get()  # Get BPM from the slider
        interval = 60.0 / bpm
        print(f"Tick at {bpm} BPM")
        play_tick()
        time.sleep(interval)

def start_metronome(bpm_slider):
    """Starts the metronome in a separate thread."""
    global metronome_running
    if not metronome_running:
        metronome_running = True
        threading.Thread(target=metronome, args=(bpm_slider,), daemon=True).start()

def stop_metronome():
    """Stops the metronome."""
    global metronome_running
    metronome_running = False