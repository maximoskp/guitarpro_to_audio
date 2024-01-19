import os

os.makedirs('files', exist_ok=True)
# put gp files here:
os.makedirs('files/gp', exist_ok=True)
# midi files from gp are stored here:
os.makedirs('files/midi', exist_ok=True)
# audio files from midi are stored here:
os.makedirs('files/audio', exist_ok=True)

# altered bass folders
# this simulation creates random changes in the bass in the midi file
# the original version along with the altered versions are stored as audio
# the changes are stored in a csv (type of change and time of change)
# midi files from gp are stored here:
os.makedirs('files/midi_alt_bass', exist_ok=True)
# audio files from midi are stored here:
os.makedirs('files/audio_alt_bass', exist_ok=True)