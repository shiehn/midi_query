import unittest

from midi_query.extractor import Extractor
from midi_query.midi_info import MidiInfo


def get_percent_diff(current: int, previous: int) -> float:
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


class TestExtractor(unittest.TestCase):

    def test_extract_on_beat(self):
        midi_info = MidiInfo('test_assets/split_test_beat_one_three.MID')
        self.assertTrue(midi_info.load_status())

        extractor = Extractor(midi_info)
        midi_clip = extractor.extract(0, 4)

        #midi_clip.midi_file.save('extract3.mid')

        diff = get_percent_diff(midi_clip.track_length_in_ticks, (midi_info.track_length_in_ticks / 2))

        self.assertTrue(diff < 5)

    def test_extract_on_beat(self):
        midi_info = MidiInfo('test_assets/split_test_beat_two_four.MID')
        self.assertTrue(midi_info.load_status())

        extractor = Extractor(midi_info)
        midi_clip = extractor.extract(0, 4)

        #midi_clip.midi_file.save('extract2.mid')

        diff = get_percent_diff(midi_clip.track_length_in_ticks, (midi_info.track_length_in_ticks / 2))

        self.assertTrue(diff < 5)
