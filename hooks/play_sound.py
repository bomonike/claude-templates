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

# Called from ~/.claude/settings.local.json for local execution.

# ONE-TIME setup:
   git clone https://github.com/bomoniki/claude-templates --depth 1
   cd claude-templates; cp hooks ~/.claude

   uv venv .venv                   # create folder .venv to import packages
   source .venv/bin/activate       # on macOS & Linux
        # ./scripts/activate       # PowerShell only
        # ./scripts/activate.bat   # Windows CMD only
   uv lock --upgrade               # to latest ver avail., including SHA-256 hashes
   uv sync                         # Install dependencies
#    uv add pygame.   # instead of pip install pygame
#    chmod +x play_sound.py
#
# ON EVERY RUN:
#    ./play_sound.py done.wav
#    ./play_sound.py --verbose done.wav
"""
# POLICY: Dunder (double-underline) variables readable from CLI outside Python
__commit_date__ = "2026-05-14"
__commit_msg__ = "26-05-14 v001 [feat] argparse in @play_sound.py"
__repository__ = "https://github.com/wilsonmar/claude-templates/blob/main/hooks/play_sound.py"
__status__ = "WORKING: ruff check play_sound.py => All checks passed!"

import argparse
import os
import sys
import time
import wave

# POLICY: Stop Pygame hello message being displayed when it initializes:
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


def detect_audio_params(file_path) -> tuple[int, int, int, int]:
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
    return frequency, size, channels, buffer


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for audio playback."""
    parser = argparse.ArgumentParser(
        description="Play an audio file from the local Sounds folder or a provided path."
    )
    parser.add_argument(
        "audio_file",
        nargs="?",
        help="Audio file name in the Sounds folder, or an explicit file path.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Show playback time and audio metadata after playback (default: disabled).",
    )
    return parser.parse_args()


if __name__ == "__main__":

    # Hello from the pygame community. https://www.pygame.org/contribute.html

    # print('\a ASCII ding')   # not loud at all

    # play sounds in Sounds folder copied from github.com/wilsonmar/python-samples/audio

    # POLICY: To avoid dependency errors, do not reach out of the folder containing this program.
    # POLICY: Play sounds from the Sounds folder in the same folder as this program.
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    SOUNDS_DIR = os.path.join(SCRIPT_DIR, "Sounds")
    DEFAULT_SOUND = "error.wav"
    args = parse_args()

    # Create the Sounds directory if it doesn't exist.
    if not os.path.isdir(SOUNDS_DIR):
        os.makedirs(SOUNDS_DIR, exist_ok=True)
        print(f"Created missing sounds directory: {SOUNDS_DIR}")

    # POLICY: If a file_to_play specified by parameter is not found, play a default file.
    if args.audio_file:
        arg = args.audio_file
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
        # POLICY: Print the playback time and audio metadata.
        play_start = time.monotonic()
        frequency, size, channels, buffer = play_audio(file_to_play)
        play_elapsed = time.monotonic() - play_start
        if args.verbose:
            print(
                f"{os.path.basename(file_to_play)} {play_elapsed:.2f} secs, "
                f"{frequency} Hz, {size} size, {channels} channel(s), {buffer} bytes."
            )
    except pygame.error as e:
        print(f"Error: pygame failed to play audio: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Unexpected error playing audio: {e}", file=sys.stderr)
        sys.exit(1)

"""
disconnected.wav 1.45 secs, 11025 Hz, -8 size, 1 channels, 2048 bytes.
done.wav 0.52 secs, 11025 Hz, -8 size, 1 channels, 2048 bytes.
error.wav 0.73 secs, 22050 Hz, -8 size, 1 channels, 4096 bytes.
jeopardy-theme-song.mp3 33.41 secs, 44100 Hz, -16 size, 2 channels, 4096 bytes.rimshot-joke-drum.wav 2.19 secs, 44100 Hz, -16 size, 2 channels, 8192 bytes.
type.wav 0.31 secs, 11025 Hz, -8 size, 1 channels, 2048 bytes.
warning.wav 0.72 secs, 22050 Hz, -8 size, 1 channels, 4096 bytes.
sample-1mb.wav - file does not start with RIFF id
wakeup.wav 4.04 secs, 22050 Hz, -8 size, 1 channels, 4096 bytes.
"""
