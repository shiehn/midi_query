import unittest


from midi_query import query
from loader import Loader
#from config import REQUIRED_NOTE_MATCH_PER_BAR, MAX_NONE_CHORD_TONES_PER_BAR

class TestQuery(unittest.TestCase):

    # def test_query_(self):
    #
    #     target_key = 'G'
    #     target_progression = ['Cmaj7', 'Emin7', 'Emin7', 'Cmaj7']
    #     loader = Loader()
    #     midi_info = loader.read_midi_file('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')
    #
    #     results = query.find_clips(target_key, target_progression, midi_info, 2, 2)
    #
    #     self.assertEqual(results, [4])

    def test_query_transpose(self):

        target_key = 'A'
        target_progression = ['Dmaj7', 'F#min7', 'F#min7', 'Dmaj7']
        loader = Loader()
        midi_info = loader.read_midi_file('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        midi_info.transpose_up(2)

        results = query.find_clips(target_key, target_progression, midi_info, 2, 2)

        self.assertEqual(results, [4])
