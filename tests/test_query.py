import unittest

from midi_query import query


class TestQuery(unittest.TestCase):

    def test_query(self):

        result = query.add_numbers(1, 2)

        self.assertEqual(result, 3)
