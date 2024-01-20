import mido
import json
import numpy as np
from copy import deepcopy

def get_song_tempo(s):
    # returns a list of the tempi found
    tempi_musec = []
    # get tempo
    for track in s.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                tempi_musec.append( msg.tempo )
    # if no tempo found, get default mido tempo
    if len(tempi_musec) == 0:
        # default mido tempo, in microseconds per tick
        tempi_musec = [500000]
    return tempi_musec
# end get_song_tempo

# get note ons/offs
def get_noteOnOffs_from_midi_track(s, info_dictionary, tempo, track_name='bass'):
    # s: mido song
    # info_dictionary
    # track_name: string of track name
    track_of_interest = None
    for i_track, track in enumerate(s.tracks):
        tmp_track_name = info_dictionary['track_' + str(i_track)]['type']
        if tmp_track_name == track_name:
            track_of_interest = deepcopy(track)
            note_ons = -1*np.ones(127).astype(int)
            note_ons_offs = []
            note_on_num = 0
            cummulative_time = 0
            # count how many notes in the bass channel
            for i_message, message in enumerate(track):
                cummulative_time += message.time
                if message.type == 'note_on':
                    if message.velocity > 0:
                        # keep the index that triggered the note on
                        note_ons[message.note] = note_on_num
                        tmp_note_obj = {
                            'on_idx': i_message,
                            'off_idx': -1,
                            'pitch': message.note,
                            'alteration': -1,
                            'time_on': mido.tick2second( cummulative_time, s.ticks_per_beat, tempo ),
                            'time_off': -1
                        }
                        note_ons_offs.append( tmp_note_obj )
                        note_on_num += 1
                    else:
                        if note_ons[message.note] > -1:
                            note_ons_offs[ note_ons[message.note] ]['off_idx'] = i_message
                            note_ons_offs[ note_ons[message.note] ]['time_off'] = mido.tick2second( cummulative_time, s.ticks_per_beat, tempo )
                            note_ons[message.note] = -1
                        else:
                            print('ERROR: note off without previous note one')
    return note_ons_offs, track_of_interest
# get_noteOnOffs_from_midi_track

def alter_notes(song, info_dictionary, n=10, s=[12, 7, 3, 6], track_name='bass'):
    # song: mido song
    # info_dictionary: created during original piece midi2audio run
    # n: number of alterations
    # s: semitones available
    # get tempo
    tempi_musec = get_song_tempo(song)
    # we don't want multiple tempi
    if len( tempi_musec ) > 1:
        print('ERROR: multiple tempi, skipping file')
        tempo_musec = 500000
    else:
        tempo_musec = tempi_musec[0]
        # for sanity check
        # tempo_bpm = mido.bpm2tempo(tempo_musec)
    # get_noteOnOffs_from_midi_track
    noteOnOffs, track_of_interest = get_noteOnOffs_from_midi_track(song, info_dictionary, tempo_musec, 'bass')
    # select alterations at random
    random_idxs = np.random.permutation(len(noteOnOffs))[:n]
    # keep only altered noteOnOffs for saving
    alteredNoteOnOffs = []
    # perform alterations
    for i in random_idxs:
        alteration = s[ np.random.randint( len(s) ) ]
        noteOnOffs[i]['alteration'] = alteration
        noteOnOffs[i]['pitch'] += alteration
        track_of_interest[noteOnOffs[i]['on_idx']].note = noteOnOffs[i]['pitch']
        track_of_interest[noteOnOffs[i]['off_idx']].note = noteOnOffs[i]['pitch']
        alteredNoteOnOffs.append( noteOnOffs[i] )
    # reassemble song with altered track
    # initialize empty altered song
    tmp_song = mido.MidiFile()
    for i_track, track in enumerate(song.tracks):
        tmp_track_name = info_dictionary['track_' + str(i_track)]['type']
        if tmp_track_name == track_name:
            tmp_song.tracks.append( track_of_interest )
        else:
            tmp_song.tracks.append(track)
    return tmp_song, alteredNoteOnOffs
# end alter_notes