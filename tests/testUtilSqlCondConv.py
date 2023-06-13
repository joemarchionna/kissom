from os import name
import json
import unittest
from kissom.utils.sql import convertConditionsToDbNames


class TestUtilSqlCondConv(unittest.TestCase):
    def test_a_none(self):
        dbKeys = []
        objKeys = []
        conditions = None
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=dbKeys, objKeys=objKeys)
        self.assertIsNone(conditions)

    def test_b_empty(self):
        dbKeys = []
        objKeys = []
        conditions = {}
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=dbKeys, objKeys=objKeys)
        self.assertEqual(conditions, {})

    def test_c_simple(self):
        dbKeys = ["first_name"]
        objKeys = ["firstName"]
        with open("kissom/reference/conditions.json") as reader:
            conditions = json.load(reader)
        convertConditionsToDbNames(conditionTree=conditions[0], dbKeys=dbKeys, objKeys=objKeys)
        self.assertEqual(conditions[0]["fieldName"], "first_name")

    def test_d_compound(self):
        dbKeys = ["first_name", "last_name"]
        objKeys = ["firstName", "lastName"]
        with open("kissom/reference/conditions.json") as reader:
            conditions = json.load(reader)
        convertConditionsToDbNames(conditionTree=conditions[1], dbKeys=dbKeys, objKeys=objKeys)
        self.assertEqual(conditions[1]["conditions"][0]["conditions"][0]["fieldName"], "first_name")
        self.assertEqual(conditions[1]["conditions"][0]["conditions"][1]["fieldName"], "last_name")
        self.assertEqual(conditions[1]["conditions"][1]["conditions"][0]["fieldName"], "first_name")
        self.assertEqual(conditions[1]["conditions"][1]["conditions"][1]["fieldName"], "last_name")
