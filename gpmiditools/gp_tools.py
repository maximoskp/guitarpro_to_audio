import guitarpro as gp

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