from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSqlDelete(unittest.TestCase):
    def test_a(self):
        tn = "test.table"
        dc = {"fieldName": "pk", "fieldValue": 1001}
        dKeys = ["full_name", "age", "home"]
        sql, tpl = deleteSql(tableName=tn, dbKeys=dKeys, conditionTree=dc)
        self.assertEqual(sql, "DELETE FROM test.table WHERE pk = %s RETURNING full_name, age, home")
        self.assertEqual(tpl, (1001,))

    def test_b(self):
        tn = "test.table"
        dc = {"fieldName": "pk", "fieldValue": 1001}
        dKeys = ["pk"]
        sql, tpl = deleteSql(tableName=tn, dbKeys=dKeys, conditionTree=dc)
        self.assertEqual(sql, "DELETE FROM test.table WHERE pk = %s RETURNING pk")
        self.assertEqual(tpl, (1001,))
