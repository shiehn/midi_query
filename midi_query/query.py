import os
import pathlib
import uuid

from mingus.containers import Note
from mingus.core import chords
from mingus.core.keys import get_notes
import argparse

from midi_info import MidiInfo
from extractor import Extractor
from config import OUTPUT_DIR, DATASET_DIR, \
    MAX_FILES_TO_SEARCH, MAX_NONE_CHORD_TONES_PER_BAR, MIN_CHORD_TONES_PER_BAR, DATASET_START_OFFSET


def get_last_note_start_time(midi_track):
    final_note_start = 0.0
    for msg in midi_track:
        if msg.type == 'note_on':
            final_note_start = msg.time

    return final_note_start


def is_3_4_time(track) -> bool:
    for msg in track:
        if 'numerator' in msg.dict():
            if 3 % msg.numerator == 0:
                return True
        if 'denominator' in msg.dict():
            if 3 % msg.numerator == 0:
                return True

    return False


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


def find_matches(target_progression, target_key, bars_of_notes, max_passing_tones_per_bar: int = 1,
                 min_chord_tone_matches_per_bar: int = 2):
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

            if len(note_chord_matches) < min_chord_tone_matches_per_bar:
                print('FAILED: REQUIRED_NOTE_MATCH_PER_BAR: ' + str(min_chord_tone_matches_per_bar))
                is_match = False

            if len(notes_not_in_chord) > max_passing_tones_per_bar:
                print('FAILED: MAX_NONE_CHORD_TONES_PER_BAR: ' + str(len(notes_not_in_chord)))
                is_match = False

        if is_match:
            # print('ADDING MATCH INDEX: ' + str(bars_idx))
            # print('EXTRA NOTES: ' + str(notes_not_in_chord))
            scale = get_notes(target_key)
            # print('TARGET SCALE: ' + str(scale))
            scale_match = True
            for note in notes_not_in_chord:
                if note not in scale:
                    scale_match = False

            if scale_match:
                match_indexes.append(bars_idx)
            else:
                print('FAILED: SCALE_MATCH: ' + str(scale_match))

        bars_idx = bars_idx + 1

    return match_indexes


def find_clips(target_key: str, target_progression: str, midi_info: MidiInfo,
               max_passing_tones_per_bar: int = 1,
               min_chord_tone_matches_per_bar: int = 2):
    if is_3_4_time(midi_info.get_merged_track()):
        print('SKIPPING: NOT 4/4 TIME')
        return []

    if target_key is None:
        max_passing_tones_per_bar = 0

    bars_of_messages = group_messages_by_bar(midi_info.get_merged_track(), midi_info.get_ticks_in_track(),
                                             midi_info.get_ticks_per_beat())

    bars_of_notes = convert_messages_to_notes(bars_of_messages)

    match = find_matches(target_progression, target_key, bars_of_notes, max_passing_tones_per_bar,
                         min_chord_tone_matches_per_bar)

    return match


def add_numbers(a, b):
    return a + b


def create_output_dir(target_progression, target_key) -> str:
    dir_name = 'key_' + target_key.upper() + '_chords_' + '_'.join(target_progression)
    output_path = os.path.join(OUTPUT_DIR, dir_name)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    return output_path


parser = argparse.ArgumentParser()
parser.add_argument("--chords", help="expects a comma separated list of chords ex. Cmaj7,Amin7,Fmaj7,Gdom7")
parser.add_argument("--key", help="expects major key ex. 'C'")

def main():
    args = parser.parse_args()

    target_key = 'c'
    if args.key is not None:
        target_key = args.key

    target_progression = []

    if args.chords is not None:
        target_progression = args.chords.split(',')

    if len(target_progression) != 4:
        print('MIDI Query expects 4 chords')
        return

    for chord in target_progression:
        notes_in_prog_chord = chords.from_shorthand(chord)
        if notes_in_prog_chord is None or len(notes_in_prog_chord) == 0:
            print('Unable to parse chord: ' + str(chord))
            return


    output_dir = create_output_dir(target_progression, target_key)

    file_count = 0
    iterate_count = 0
    error_count = 0
    extracted_count = 0
    output_files = []
    try:
        for root, d_names, f_names in os.walk(DATASET_DIR):
            for f in f_names:
                file_path = os.path.join(root, f)
                file_extension = pathlib.Path(file_path).suffix
                if file_extension == '.mid' or file_extension == '.midi' or file_extension == '.MID' or file_extension == '.MIDI':

                    if file_count > MAX_FILES_TO_SEARCH:
                        raise Exception('Max files reached')

                    iterate_count = iterate_count + 1
                    if iterate_count < DATASET_START_OFFSET:
                        print('ITERATE: ' + str(iterate_count) + ' SKIPPING: ' + file_path)
                        continue

                    file_count = file_count + 1
                    print('PROCESSING FILE: ' + str(file_count) + ' ' + file_path)

                    # print('FILE_PATH: ' + file_path)
                    info = MidiInfo(file_path=file_path)
                    if info.load_status() is False:
                        print('ERROR: LOADING-FILE: ' + file_path)
                        error_count = error_count + 1
                        continue

                    # for each file transpose it up 11 times
                    for i in range(0, 12):
                        print('TRANSPOSE UP: +' + str(i))
                        if info.transpose_up(i*1) is False:
                            continue

                        match_indexes = find_clips(target_key, target_progression, info, MAX_NONE_CHORD_TONES_PER_BAR, MIN_CHORD_TONES_PER_BAR)
                        if len(match_indexes) > 0:
                            # TODO check the file size
                            for match_idx in match_indexes:
                                extrack = Extractor(info)
                                midi_clip = extrack.extract(match_idx, len(target_progression))
                                output_file_path = os.path.join(output_dir, uuid.uuid4().hex + '.mid')
                                midi_clip.midi_file.save(output_file_path)
                                output_files.append(output_file_path)
                                extracted_count = extracted_count + 1

    except Exception as e:
        print('LOOP BREAK: ' + str(e))

    print('OUTPUT: FILE_COUNT: ' + str(file_count))
    print('OUTPUT: ERROR_COUNT: ' + str(error_count))
    print('OUTPUT: EXTRACTED_COUNT: ' + str(extracted_count))


if __name__ == "__main__":
    main()
