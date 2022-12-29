import mido


class MidiInfo(object):
    def __init__(self, file_path: str):
        self.load_success = False
        self.file_path = file_path
        self.midi_file = None
        self.load()

    def load(self):
        try:
            self.midi_file = mido.MidiFile(self.file_path, clip=True)
            self.load_success = True
        except:
            print('Error loading midi file: ' + self.file_path)
            return

    def load_status(self) -> bool:
        return self.load_success and self.midi_file is not None
