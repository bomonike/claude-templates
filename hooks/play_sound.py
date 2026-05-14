#!/Users/johndoe/.claude/hooks/.venv/bin/python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pygame",
#   "wave",
# ]
# ///
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

"""play_sound.py here.

# ONE-TIME setup:
   uv venv .venv                   # create folder .venv to import packages
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   uv lock --upgrade               # to latest version available publicly, including SHA-256 hashes
   uv sync                         # Install dependencies
#    uv add pygame.   # instead of pip install pygame
#    chmod +x play_sound.py
#
# ON EVERY RUN:
#    ./play_sound.py done.wav
"""
# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-05-14"
__commit_msg__ = "26-05-14 v001 [feat] new in @play_sound.py"
__repository__ = "https://github.com/wilsonmar/claude-templates/blob/main/hooks/play_sound.py"
__status__ = "WORKING: ruff check play_sound.py => All checks passed!"

import os
import sys
import time
import wave
import pygame


def detect_audio_params(file_path):
    """Detect frequency and channels from a WAV file. Returns defaults for non-WAV."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".wav":
        with wave.open(file_path, "rb") as wf:
            frequency = wf.getframerate()
            channels = wf.getnchannels()
            sample_width = wf.getsampwidth()  # bytes per sample
            size = -8 * sample_width  # negative = signed (e.g. -16 for 16-bit)
            # Scale buffer relative to sample rate for ~93ms of audio.
            buffer = max(512, 2 ** (frequency // 4096).bit_length() * 512)
            return frequency, size, channels, buffer
    # MP3 and other formats: use CD-quality defaults; pygame/SDL decodes internally.
    return 44100, -16, 2, 4096


def play_audio(file_path):
    """Play audio on macOS, using parameters detected from the file."""
    frequency, size, channels, buffer = detect_audio_params(file_path)

    pygame.mixer.init(frequency=frequency, size=size, channels=channels, buffer=buffer)
    pygame.mixer.music.set_volume(0.8)  # Set to 80% to avoid clipping peaks
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.wait(100)

if __name__ == "__main__":

    # Hello from the pygame community. https://www.pygame.org/contribute.html

    # print('\a ASCII ding')   # not loud at all

    # play sounds in ~/Music/Sounds copied from github.com/wilsonmar/python-samples/audio
    # disconnected.wav        error.wav               rimshot-joke-drum.wav   type.wav                warning.wav
    # done.wav                jeopardy-theme-song.mp3 sample-1mb.wav          wakeup.wav

    # POLICY: To avoid dependency errors, do not reach out of the folder containing this program.
    # POLICY: Play sounds from the Sounds folder in the same folder as this program.
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    SOUNDS_DIR = os.path.join(SCRIPT_DIR, "Sounds")
    DEFAULT_SOUND = "error.wav"

    # Create the Sounds directory if it doesn't exist.
    if not os.path.isdir(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR, exist_ok=True)
        print(f"Created missing sounds directory: {SOUNDS_DIR}")

    # POLICY: If a file_to_play specified by parameter is not found, play a default file.
    if len(sys.argv) > 2:
        # Loop to play each file specified:
        print("Usage: ./play_sound.py [file.wav or file.mp3]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        # If no directory component, prepend the default sounds directory
        if not os.path.dirname(arg):
            file_to_play = os.path.join(SOUNDS_DIR, arg)
        else:
            file_to_play = arg
    else:
        file_to_play = os.path.join(SOUNDS_DIR, DEFAULT_SOUND)
        print(f"No file specified, playing default: {file_to_play}")

    if not os.path.isfile(file_to_play):
        print(f"Error: Audio file not found: {file_to_play}", file=sys.stderr)
        print(f"Place .wav or .mp3 files in: {SOUNDS_DIR}", file=sys.stderr)
        sys.exit(1)

    try:
        # POLICY: Print the playback time.
        play_start = time.monotonic()
        play_audio(file_to_play)
        play_elapsed = time.monotonic() - play_start
        print(f"{os.path.basename(file_to_play)} {play_elapsed:.2f} seconds.")
    except pygame.error as e:
        print(f"Error: pygame failed to play audio: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error playing audio: {e}", file=sys.stderr)
        sys.exit(1)
