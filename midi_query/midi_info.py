from os import path

import mido
from mido import second2tick, MidiFile

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


class MidiInfo(object):
    def __init__(self, file_path: str = None, midi_file: MidiFile = None):
        if file_path is None and midi_file is None:
            raise ValueError('file_path or midi_file must be set')

        if file_path is not None:
            if path.isfile(file_path) is False:
                raise ValueError('file_path must be a valid file path')

        self.load_success = False
        self.file_path = file_path
        self.midi_file = midi_file
        self.merged_track = None
        self.ticks_per_beat = None
        self.track_length_in_ticks = None
        self.load()

    def get_ticks_in_track(self) -> int:
        return self.track_length_in_ticks

    def get_ticks_per_beat(self) -> int:
        return self.ticks_per_beat

    def get_merged_track(self):
        return self.merged_track

    def transpose_up(self, transpose_amount: int) -> bool:
        for msg in self.merged_track:
            if msg.type == 'note_on' or msg.type == 'note_off':
                new_note_value = msg.note + transpose_amount
                if new_note_value > 127:
                    return False

                msg.note = new_note_value

        return True

    def get_tempo(self, midi_file):
        for track in midi_file.tracks:
            for msg in track:
                if msg.type == 'set_tempo':
                    return msg.tempo
        else:
            # Default tempo.
            return 500000

    def seconds_per_quarter_note(self, microseconds_per_quarter_note):
        return microseconds_per_quarter_note / 1000000.0

    def micros_to_seconds(self, microseconds):
        return microseconds / 1000000.0

    def filter_drum_tracks(self, tracks):
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

    def merge_tracks(self, tracks):
        printed_tracks = []
        for track in tracks:
            for msg in track:
                if msg.is_meta:
                    if 'name' in msg.dict():
                        if msg.name not in printed_tracks:
                            printed_tracks.append(msg.name)
                            # print('track_name:' + str(msg.name))

        return mido.merge_tracks(tracks)

    def load(self):
        try:
            if self.midi_file is None:
                print('Loading midi file: ' + self.file_path)
                self.midi_file = mido.MidiFile(self.file_path, clip=True)

            self.ticks_per_beat = self.midi_file.ticks_per_beat

            print('MIDI_INFO: TYPE: ' + str(self.midi_file.type))

            print('MIDI_INFO: ticks_per_beat: ' + str(self.ticks_per_beat))

            tempo_in_ms = self.get_tempo(self.midi_file)
            print('MIDI_INFO: TEMPO MS: {}'.format(tempo_in_ms))
            print('MIDI_INFO: TEMPO: AS SEC: {}'.format(self.seconds_per_quarter_note(tempo_in_ms)))

            # print('MIDI_INFO: ORIGINAL TRACK COUNT: ' + str(len(self.midi_file.tracks)))

            # print('MIDI_INFO: self.midi_file: ' + str(self.midi_file))
            track_length = self.midi_file.length
            print('MIDI_INFO: track_length: ' + str(track_length))

            track_length_ticks = second2tick(track_length, self.ticks_per_beat, tempo_in_ms)
            print('MIDI_INFO: track_length_ticks: ' + str(track_length_ticks))

            self.track_length_in_ticks = track_length_ticks

            filtered_tracks = self.filter_drum_tracks(self.midi_file.tracks)

            self.merged_track = self.merge_tracks(filtered_tracks)

            self.load_success = True
        except Exception as e:
            print('Error loading midi file: ' + str(self.file_path))
            print('Error: ' + str(e))
            return

    def load_status(self) -> bool:
        return self.load_success and self.midi_file is not None and self.merged_track is not None
