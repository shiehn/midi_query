import unittest

from midi_query.midi_info import MidiInfo


class TestMidiInfo(unittest.TestCase):

    def test_load(self):
        midi_info = MidiInfo('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        self.assertTrue(midi_info.load_status())

    def test_get_merged_track(self):
        midi_info = MidiInfo('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        merged_track = midi_info.get_merged_track()

        self.assertTrue(merged_track is not None)
