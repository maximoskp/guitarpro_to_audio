import mido
import json
import numpy as np

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
def get_noteOnOffs_from_midi_track(s, info_dictionary, track_name='bass'):
    # s: mido song
    # info_dictionary
    # track_name: string of track name
    for i_track, track in enumerate(s.tracks):
        tmp_track_name = info_dictionary['track_' + str(i_track)]['type']
        if tmp_track_name == track_name:
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
    return note_ons_offs
# get_noteOnOffs_from_midi_track

