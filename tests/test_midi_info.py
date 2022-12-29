import unittest

from midi_query.midi_info import MidiInfo


class TestMidiInfo(unittest.TestCase):

    def test_load(self):
        midi_info = MidiInfo('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        self.assertTrue(midi_info.load_status())
