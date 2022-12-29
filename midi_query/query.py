import mido
from mido import second2tick
from mingus.containers import Note
from mingus.core import chords
from mingus.core.keys import get_notes

from midi_query.midi_info import MidiInfo

REQUIRED_NOTE_MATCH_PER_BAR = 3


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


def find_clips(target_key: str, target_progression: str, midi_info: MidiInfo):
    bars_of_messages = group_messages_by_bar(midi_info.get_merged_track(), midi_info.get_ticks_in_track(), midi_info.get_ticks_per_beat())

    bars_of_notes = convert_messages_to_notes(bars_of_messages)
    print('bars_of_notes: ' + str(bars_of_notes))

    match = find_matches(target_progression, target_key, bars_of_notes)
    print('has_match: ' + str(match))

    return match


def add_numbers(a, b):
    return a + b


def main():
    # PARAMS TO BE PASSED BY CLI
    target_key = 'G'
    target_progression = ['Cmaj7', 'Emin7', 'Emin7', 'Cmaj7']

    midi_info = MidiInfo('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

    find_clips(target_key, target_progression, midi_info)


if __name__ == "__main__":
    main()
