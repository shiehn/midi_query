import unittest


from midi_query import query
from loader import Loader

class TestQuery(unittest.TestCase):

    def test_query_(self):

        target_key = 'G'
        target_progression = ['Cmaj7', 'Emin7', 'Emin7', 'Cmaj7']
        loader = Loader()
        midi_info = loader.read_midi_file('test_assets/cmaj7_em7_em7_cmaj7_bar5_key_g.MID')

        results = query.find_clips(target_key, target_progression, midi_info)

        self.assertEqual(results, [3, 4])
