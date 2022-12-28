import time
import mido
import rtmidi


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

def merge_tracks(midi_file):
    print('do it here')


def print_midi_file_info(midi_file):

    print('TEMPO: {}'.format(get_tempo(midi_file)))
    print('TEMPO: AS SEC: {}'.format(seconds_per_quarter_note(get_tempo(midi_file))))

    print('TRACK_COUNT: ' + str(len(midi_file.tracks)))
    num_of_tracks = len(midi_file.tracks)

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
    midi_file = mido.MidiFile('datasets/ballade1.mid', clip=True)

    print_midi_file_info(midi_file)


if __name__ == "__main__":
    main()
