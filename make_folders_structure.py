import os

os.makedirs('files', exist_ok=True)
# put gp files here:
os.makedirs('files/gp', exist_ok=True)
# midi files from gp are stored here:
os.makedirs('files/midi', exist_ok=True)
# audio files from midi are stored here:
os.makedirs('files/audio', exist_ok=True)