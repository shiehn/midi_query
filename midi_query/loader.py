from midi_info import MidiInfo


class Loader(object):

    def read_midi_file(self, file_path: str) -> MidiInfo:
        midi_info = MidiInfo(file_path)
        return midi_info
