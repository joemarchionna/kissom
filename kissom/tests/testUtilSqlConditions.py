from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSqlConditions(unittest.TestCase):
    def test_a_none(self):
        conditions = None
        sql, vals = getConditions(conditionTree=conditions)
        self.assertEqual(sql, "")
        self.assertEqual(vals, [])

    def test_b_empty(self):
        conditions = {}
        sql, vals = getConditions(conditionTree=conditions)
        self.assertEqual(sql, "")
        self.assertEqual(vals, [])

    def test_c_simple(self):
        with open("kissom/reference/conditions.json") as reader:
            conditions = json.load(reader)
        sql, vals = getConditions(conditionTree=conditions[0])
        self.assertEqual(sql, "firstName = %s")
        self.assertEqual(vals, ["Johnny"])

    def test_d_compound(self):
        with open("kissom/reference/conditions.json") as reader:
            conditions = json.load(reader)
        sql, vals = getConditions(conditionTree=conditions[1])
        self.assertEqual(sql, "((firstName = %s AND lastName = %s) OR (firstName = %s AND lastName = %s))")
        self.assertEqual(vals, ["Johnny", "Appleseed", "Patrick", "Putnum"])
