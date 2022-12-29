import time
import mido
import mingus
from mido import tick2second, MidiFile, second2tick
from mingus.containers import Note
from mingus.core import chords
from mingus.core.keys import get_notes

REQUIRED_NOTE_MATCH_PER_BAR = 3

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


def micros_to_seconds(microseconds):
    return microseconds / 1000000.0


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


def get_last_note_start_time(midi_track):
    final_note_start = 0.0
    for msg in midi_track:
        if msg.type == 'note_on':
            final_note_start = msg.time

    return final_note_start


def group_messages_by_bar(track, track_length_ticks, ticks_per_beat):
    bars = []

    bar_length_ticks = ticks_per_beat * 4
    print('bar_length_ticks: ' + str(bar_length_ticks))

    num_of_bars = int(track_length_ticks / bar_length_ticks)

    print('num_of_bars: ' + str(num_of_bars))

    for bar_idx in range(num_of_bars):
        bar = []
        start_time = bar_idx * bar_length_ticks
        end_time = start_time + bar_length_ticks

        current_time = 0.0
        for msg in track:
            if 'time' in msg.dict():
                current_time = current_time + msg.time

                if msg.type == 'note_on':
                    if current_time >= start_time and current_time < end_time:
                        bar.append(msg)

        bars.append(bar)

    return bars


def convert_messages_to_notes(bars_of_messages):
    bars_of_notes = []
    for bar in bars_of_messages:
        notes = []
        for msg in bar:
            if msg.type == 'note_on':
                note = Note(msg.note)
                notes.append(note)
        bars_of_notes.append(notes)

    return bars_of_notes


def find_matches(target_progression, target_key, bars_of_notes):
    match_indexes = []
    bars_idx = 0

    while bars_idx < len(bars_of_notes) - len(target_progression):
        notes_not_in_chord = []
        is_match = True

        for prog_idx, prog_chord in enumerate(target_progression):
            note_chord_matches = []

            # print('COMPARE PROG_IDX: ' + str(prog_idx) + ' to BAR_IDX: ' + str(bars_idx + prog_idx))
            notes_in_prog_chord = chords.from_shorthand(prog_chord)
            notes_at_bar_idx = []
            for note in bars_of_notes[bars_idx + prog_idx]:
                notes_at_bar_idx.append(note.name)

            # print('NOTES_IN_PROG_CHORD: ' + str(notes_in_prog_chord))
            # print('NOTES_IN_BAR_IDX_CHORD: ' + str(notes_at_bar_idx))

            for note in bars_of_notes[bars_idx + prog_idx]:
                name = note.name
                if name in notes_in_prog_chord:
                    if name not in note_chord_matches:
                        note_chord_matches.append(name)
                else:
                    if name not in notes_not_in_chord:
                        notes_not_in_chord.append(name)

            if len(note_chord_matches) < REQUIRED_NOTE_MATCH_PER_BAR:
                is_match = False

            print('MATCH STATUS: ' + str(is_match))

        if is_match:
            print('ADDING MATCH INDEX: ' + str(bars_idx))
            print('EXTRA NOTES: ' + str(notes_not_in_chord))
            scale = get_notes(target_key)
            print('TARGET SCALE: ' + str(scale))
            scale_match = True
            for note in notes_not_in_chord:
                if note not in scale:
                    scale_match = False

            print('SCALE_MATCH: ' + str(scale_match))

            if scale_match:
                match_indexes.append(bars_idx)

        bars_idx = bars_idx + 1

    return match_indexes


def print_midi_file_info(midi_file):
    target_key = 'G'
    target_progression = ['Cmaj7', 'Emin7', 'Emin7', 'Cmaj7']
    midi_file = mido.MidiFile('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID', clip=True)

    ticks_per_beat = midi_file.ticks_per_beat
    print('ticks_per_beat: ' + str(ticks_per_beat))

    print(
        'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

    tempo_in_ms = get_tempo(midi_file)
    print('TEMPO MS: {}'.format(get_tempo(midi_file)))
    print('TEMPO: AS SEC: {}'.format(seconds_per_quarter_note(get_tempo(midi_file))))

    print('TRACK_COUNT: ' + str(len(midi_file.tracks)))
    num_of_tracks = len(midi_file.tracks)

    track_length = midi_file.length
    print('track_length: ' + str(track_length))

    track_length_ticks = second2tick(track_length, ticks_per_beat, tempo_in_ms)
    print('track_length_ticks: ' + str(track_length_ticks))

    filtered_tracks = filter_drum_tracks(midi_file.tracks)

    merged_track = merge_tracks(filtered_tracks)
    print('AFTER MERGE msg_count: ' + str(len(merged_track)))

    bars_of_messages = group_messages_by_bar(merged_track, track_length_ticks, ticks_per_beat)

    # print('bars_of_messages: ' + str(bars_of_messages))

    bars_of_notes = convert_messages_to_notes(bars_of_messages)
    print('bars_of_notes: ' + str(bars_of_notes))

    match = find_matches(target_progression, target_key, bars_of_notes)
    print('has_match: ' + str(match))


def main():
    midi_file = mido.MidiFile('datasets/multi_track_pop.mid', clip=True)

    print_midi_file_info(midi_file)


if __name__ == "__main__":
    main()
