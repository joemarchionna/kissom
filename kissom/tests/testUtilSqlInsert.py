from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSqlInsert(unittest.TestCase):
    def test_a(self):
        tn = "test.table"
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        r = {"name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = insertSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r)
        self.assertEqual(
            sql, "INSERT INTO test.table (full_name, age, home) VALUES (%s, %s, %s) RETURNING full_name, age, home"
        )
        self.assertEqual(tpl, ("Johnny", 24, "Monroe"))

    def test_b(self):
        tn = "test.table"
        okeys = ["name", "hometown"]
        dKeys = ["full_name", "home"]
        r = {"name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = insertSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r)
        self.assertEqual(sql, "INSERT INTO test.table (full_name, home) VALUES (%s, %s) RETURNING full_name, home")
        self.assertEqual(tpl, ("Johnny", "Monroe"))
