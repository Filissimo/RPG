import unittest
from unittest.mock import patch

from RPG.database_backed.db_operator import Updates


class TestUpdates(unittest.TestCase):
    @patch('pymongo.MongoClient')
    def test_get_stat_works_with_integers(self, mocked_pymongo):
        updates = Updates('test_character_type')
        updates.col = {'hp': {'current': 100}}
        expected_hp = 100
        actual_hp = updates.get_stat('hp', 'current')
        self.assertEqual(actual_hp, expected_hp)

    @patch('pymongo.MongoClient')
    def test_get_stat_works_with_strings(self, mocked_pymongo):
        updates = Updates('test_character_type')
        updates.col = {'hp': {'current': '100'}}
        expected_hp = '100'
        actual_hp = updates.get_stat('hp', 'current')
        self.assertEqual(actual_hp, expected_hp)

    @patch('pymongo.MongoClient')
    def test_set_stat_filled_value_sets_value(self, mocked_pymongo):
        updates = Updates('scrub')
        actual_query = updates.set_stat('hp', 'current', 100)
        expected_query = {'$set': {'hp.current': 100}}
        self.assertEqual(actual_query, expected_query)

    @patch('pymongo.MongoClient')
    def test_set_stat_none_value_sets_field(self, mocked_pymongo):
        updates = Updates('scrub')
        actual_query = updates.set_stat('hp', 'current', None)
        expected_query = {"$set": {'hp': 'current'}}
        self.assertEqual(actual_query, expected_query)
