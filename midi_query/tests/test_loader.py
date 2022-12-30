import unittest


from midi_query.loader import Loader
from midi_query.midi_info import MidiInfo


class TestLoader(unittest.TestCase):

    def test_load(self):
        loader = Loader()
        midi_info = loader.read_midi_file('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        self.assertTrue(midi_info.load_status())
