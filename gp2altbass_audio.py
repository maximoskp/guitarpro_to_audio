import guitarpro as gp
import mido
import subprocess
import os
import re
import librosa
import soundfile
import json

# global audio output variables
sample_rate = 8000
audio_data_format = 'PCM_16'
# alteration characteristics
alterations_for_piece = 10
alteration_semitones = [12, 7, 3, 6]
how_many_notes_per_alteration = 10

# 149KB
gp_files_path = os.getcwd() + '/files/gp/'
# 347KB
midi_files_path = os.getcwd() + '/files/midi_alt_bass/'
# 1.61GB (44100-32) - 71MB (8000-16)
audio_files_path = os.getcwd() + '/files/audio_alt_bass/'

# make sure hidden files are not included
gp_files_list = [f for f in os.listdir(gp_files_path) if not f.startswith('.')]

# for MuseScore conversion
# https://ourcodeworld.com/articles/read/1171/how-to-convert-any-guitar-pro-tab-file-gp-gp3-gp5-gpx-to-midi-from-the-command-line-using-musescore-3
# e.g., for windows
# c:\Program Files\MuseScore 3\bin\MuseScore3.exe
# for Mac
# converter_script = '/Applications/MuseScore\ 4.app/Contents/MacOS/mscore'
# for Linux
converter_script = '/usr/bin/mscore'

def get_track_info_from_gp_file(f):
    song = gp.parse(f)
    info_dictionary = {}
    for i, t in enumerate(song.tracks):
        info_dictionary[ 'track_' + str(i) ] = {}
        info_dictionary[ 'track_' + str(i) ]['type'] = None
        if t.isPercussionTrack:
            info_dictionary[ 'track_' + str(i) ]['type'] = 'percussion'
        else:
            # get number of strings and tuning
            if len(t.strings) == 6:
                if t.strings[0].value >= 59:
                    info_dictionary[ 'track_' + str(i) ]['type'] = 'guitar'
                else:
                    info_dictionary[ 'track_' + str(i) ]['type'] = 'bass'
            else:
                if t.strings[0].value < 59:
                    info_dictionary[ 'track_' + str(i) ]['type'] = 'bass'
                else:
                    info_dictionary[ 'track_' + str(i) ]['type'] = 'other'
    return info_dictionary
# end get_track_info_from_gp_file

def alter_track(t, s, n):
    # t: track to alter
    # s: list of semitones to use randomly during alterations
    # n: how many notes to alter for piece
    return 0, 0

for f in gp_files_list:
    # get list of instruments in gp file
    info_dictionary = get_track_info_from_gp_file(gp_files_path + f)
    gp_final_name = f.replace('\'', '')
    os.rename( gp_files_path + f, gp_files_path + gp_final_name )
    gp_esc = re.escape(gp_final_name.replace('\'', ''))
    # make folder for midi files
    midi_song_files_path = midi_files_path + gp_final_name.replace('.', '_').replace(' ', '_') + '/'
    os.makedirs(midi_song_files_path, exist_ok=True)
    # gp to mid
    midi_final_name = gp_final_name + '.mid'
    midi_esc = gp_esc + '.mid'
    subprocess.Popen(converter_script + ' ' + gp_files_path + gp_esc + ' -o ' + midi_song_files_path + midi_esc, shell=True).wait()
    # midi to separate tracks
    song = mido.MidiFile(midi_song_files_path + midi_final_name)
    # mid to wav - mixdown
    audio_song_files_path = audio_files_path + gp_final_name.replace('.', '_').replace(' ', '_') + '/'
    os.makedirs(audio_song_files_path, exist_ok=True)
    with open(audio_song_files_path + 'info.json', 'w') as fp:
        json.dump(info_dictionary, fp)
    # audio_final_name = midi_final_name + '.wav'
    # audio_esc = midi_esc + '.wav'
    # save original track
    audio_final_name = 'mix.wav'
    audio_esc = 'mix.wav'
    subprocess.Popen(converter_script + ' ' + midi_song_files_path + midi_esc + ' -o ' + audio_song_files_path + audio_esc, shell=True).wait()
    # convert to lighter format
    audio_hi_fi = librosa.load(audio_song_files_path + audio_final_name, sr=sample_rate, mono=True)
    soundfile.write( audio_song_files_path + audio_final_name , audio_hi_fi[0] , sample_rate , audio_data_format )
    # mid to wav - for altered bass versions
    for alt_i in range(alterations_for_piece):
        # initialize empty altered song
        tmp_song = mido.MidiFile()
        # add tracks to song and change bass track
        for i, track in enumerate(song.tracks):
            tmp_track_name = info_dictionary['track_' + str(i)]['type']
            if tmp_track_name == 'bass':
                alt_semitones, alt_timestamps = alter_track(track, alteration_semitones, how_many_notes_per_alteration)
            tmp_song.tracks.append(track)
            '''
            tmp_track_name = track.name.replace('\'', '')
            tmp_track_name = track.name.replace('.', '_')
            tmp_track_name = track.name.replace(' ', '_')
            if tmp_track_name == '':
                tmp_track_name = 'unk'
            '''
        tmp_track_full_path = midi_song_files_path + 'alt_' + str(i) + '_' + midi_final_name + '.mid'
        tmp_song.save( tmp_track_full_path )
        audio_final_name = 'alt_' + str(i) + '_' + midi_final_name + '.wav'
        subprocess.Popen(converter_script + ' ' + tmp_track_full_path + ' -o ' + audio_song_files_path + audio_final_name, shell=True).wait()
        audio_hi_fi = librosa.load(audio_song_files_path + audio_final_name, sr=sample_rate, mono=True)
        soundfile.write( audio_song_files_path + audio_final_name , audio_hi_fi[0] , sample_rate , audio_data_format )
    