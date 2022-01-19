from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSqlSelect(unittest.TestCase):
    def test_a(self):
        tn = "test.table"
        dKeys = ["pk", "full_name", "age", "home"]
        sql, tpl = selectSql(tableName=tn, dbKeys=dKeys)
        self.assertEqual(sql, "SELECT pk, full_name, age, home FROM test.table")
        self.assertEqual(tpl, ())

    def test_b(self):
        tn = "test.table"
        dKeys = ["pk", "full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        sql, tpl = selectSql(tableName=tn, dbKeys=dKeys, conditionTree=ct)
        self.assertEqual(sql, "SELECT pk, full_name, age, home FROM test.table WHERE pk = %s")
        self.assertEqual(tpl, (1001,))
