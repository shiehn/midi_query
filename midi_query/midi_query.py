import time
import mido
import rtmidi

drum_filter = ['drum',
               'drums',
               'bassdrum',
               'snare',
               'snaredrum',
               'piccolo',
               'shaker',
               'timpani',
               'timp',
               'hihat',
               'kick',
               'tambourin',
               'tambourine',
               'congas',
               'conga\'s'
               'ride',
               'crash',
               'tom',
               'claps',
               'clap',
               'handclaps',
               'cowbell',
               'bongo',
               'percussion',
               'perc',
               ]


def seconds_per_quarter_note(microseconds_per_quarter_note):
    return microseconds_per_quarter_note / 1000000.0


def get_tempo(midi_file):
    for track in midi_file.tracks:
        for msg in track:
            if msg.type == 'set_tempo':
                return msg.tempo
    else:
        # Default tempo.
        return 500000


def merge_tracks(tracks):
    printed_tracks = []
    for track in tracks:
        for msg in track:
            if msg.is_meta:
                if 'name' in msg.dict():
                    if msg.name not in printed_tracks:
                        printed_tracks.append(msg.name)
                        print('track_name:' + str(msg.name))

    return mido.merge_tracks(tracks)


def filter_drum_tracks(tracks):
    filtered_tracks = []

    track_count = 0
    for track in tracks:
        add_track = True
        for msg in track:
            if msg.is_meta:
                if 'name' in msg.dict():
                    track_name = msg.name.lower().strip()
                    if track_name in drum_filter:
                        print('FILTER TRACK: ' + str(msg.name))
                        add_track = False

                if 'channel' in msg.dict():
                    if msg.channel > 10:
                        # drop the drum track
                        add_track = False

        if add_track:
            filtered_tracks.append(track)

        track_count = track_count + 1

    return filtered_tracks

def print_midi_file_info(midi_file):

    print(
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    print('TEMPO: {}'.format(get_tempo(midi_file)))
    print('TEMPO: AS SEC: {}'.format(seconds_per_quarter_note(get_tempo(midi_file))))

    print('TRACK_COUNT: ' + str(len(midi_file.tracks)))
    num_of_tracks = len(midi_file.tracks)

    print('BEFORE MERGE msg_count: ' + str(len(midi_file.tracks[17])))

    filtered_tracks = filter_drum_tracks(midi_file.tracks)

    merged_track = merge_tracks(filtered_tracks)
    print('AFTER MERGE msg_count: ' + str(len(merged_track)))


    #for idx, msg in enumerate(merged_track):
    #
    #     if idx < 1000:
    # print('MSG:' + str(msg))
    # if 'channel' in msg.dict():
    #     if msg.channel > 10:
    #         # drop the drum track
    #         print('DROP:' + str(msg))
    #     else:
    #         print('msg.channel:' + str(msg.channel))

    # print('MERGED_TRACK_COUNT: ' + str(len(midi_file.tracks)))

    # print('TEMPO:' + str(mid.tempo))
    # get tempo in seconds
    # seconds_per_quarter_note = seconds_per_quarter_note(mid.tempos[0].tempo)

    # mid.tick2second()
    # for msg in midi_file:
    #     if msg.is_meta:
    #         print('META: ' + str(msg.tempo))
    # print('msg:' + str(msg))

    # for i, track in enumerate(mid.tracks):
    #     print('Track {}: {}'.format(i, track.name))
    # for msg in track:
    #     print(msg)
    #
    # for msg in midi_file.play():
    #     port.send(msg)

def main():
    print('dude')
    midi_file = mido.MidiFile('datasets/multi_track_pop.mid', clip=True)

    print_midi_file_info(midi_file)

if __name__ == "__main__":
    main()
