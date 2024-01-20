# guitarpro_to_audio

### gp2midi2audio.py
Converts guitar pro files in the files/gp directory (e.g., from the DadaGP dataset) to multitrack audio using python.

It first creats a separate midi file for each track from gp files usesing the executable from:

https://github.com/rageagainsthepc/GuitarPro-to-Midi 

and then it renders each midi file to audio command-line musescore to create multitrack renderings of GP files.

A json file is also generated that describes the category of the instrument in each track, including guitar, bass, drums, keyboards and other.

### gp2altbass_audio

Converts guitar pro files in the files/gp directory (e.g., from the DadaGP dataset) to multitrack audio using python.

While seperating the tracks, it identifies the bass track and performs multiple rounds of alterations in notes selected at random. It also records what type of alterations happened and the timestamp of the alteration. These data are stored in a csv file.

# How to run

1. First run ```make_folders_structure.py``` to create folders.

2. Then copy gp files with no subfolders in the ```/files/gp``` folder.

3. Define executable for musescore in ```gp2midi2audio.py``` or ```gp2altbass_audio.py``` and run this script.

The ```GuitarProToMidi``` executable might not work in a non-unix OS. Please consult the original github repo given above if things don't work out regarding this executable.