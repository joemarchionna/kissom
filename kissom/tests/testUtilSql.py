from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSql(unittest.TestCase):
    def test_a_insert(self):
        tn = "test.table"
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        r = {"name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = insertSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r)
        self.assertEqual(
            sql, "INSERT INTO test.table (full_name, age, home) VALUES (%s, %s, %s) RETURNING full_name, age, home"
        )
        self.assertEqual(tpl, ("Johnny", 24, "Monroe"))

    def test_b_insert(self):
        tn = "test.table"
        okeys = ["name", "hometown"]
        dKeys = ["full_name", "home"]
        r = {"name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = insertSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r)
        self.assertEqual(sql, "INSERT INTO test.table (full_name, home) VALUES (%s, %s) RETURNING full_name, home")
        self.assertEqual(tpl, ("Johnny", "Monroe"))

    def test_c_update(self):
        tn = "test.table"
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = updateSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r, conditionTree=ct)
        self.assertEqual(
            sql,
            "UPDATE test.table SET full_name = %s, age = %s, home = %s WHERE pk = %s RETURNING full_name, age, home",
        )
        self.assertEqual(tpl, ("Johnny", 24, "Monroe", 1001))

    def test_d_update(self):
        tn = "test.table"
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "hometown": "Monroe"}
        sql, tpl = updateSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r, conditionTree=ct)
        self.assertEqual(sql, "UPDATE test.table SET home = %s WHERE pk = %s RETURNING full_name, age, home")
        self.assertEqual(tpl, ("Monroe", 1001))

    def test_e_update(self):
        tn = "test.table"
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {
            "operator": "AND",
            "conditions": [{"fieldName": "org", "fieldValue": 199200}, {"fieldName": "pk", "fieldValue": 1001}],
        }
        r = {"coid": 199200, "id": 1001, "hometown": "Monroe"}
        sql, tpl = updateSql(tableName=tn, objKeys=okeys, dbKeys=dKeys, data=r, conditionTree=ct)
        self.assertEqual(
            sql, "UPDATE test.table SET home = %s WHERE (org = %s AND pk = %s) RETURNING full_name, age, home"
        )
        self.assertEqual(tpl, ("Monroe", 199200, 1001))

    def test_f_delete(self):
        tn = "test.table"
        dc = {"fieldName": "pk", "fieldValue": 1001}
        dKeys = ["full_name", "age", "home"]
        sql, tpl = deleteSql(tableName=tn, dbKeys=dKeys, conditionTree=dc)
        self.assertEqual(sql, "DELETE FROM test.table WHERE pk = %s RETURNING full_name, age, home")
        self.assertEqual(tpl, (1001,))

    def test_g_delete(self):
        tn = "test.table"
        dc = {"fieldName": "pk", "fieldValue": 1001}
        dKeys = ["pk"]
        sql, tpl = deleteSql(tableName=tn, dbKeys=dKeys, conditionTree=dc)
        self.assertEqual(sql, "DELETE FROM test.table WHERE pk = %s RETURNING pk")
        self.assertEqual(tpl, (1001,))

    def test_h_select(self):
        tn = "test.table"
        dKeys = ["pk", "full_name", "age", "home"]
        sql, tpl = selectSql(tableName=tn, dbKeys=dKeys)
        self.assertEqual(sql, "SELECT pk, full_name, age, home FROM test.table")
        self.assertEqual(tpl, ())

    def test_i_select(self):
        tn = "test.table"
        dKeys = ["pk", "full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        sql, tpl = selectSql(tableName=tn, dbKeys=dKeys, conditionTree=ct)
        self.assertEqual(sql, "SELECT pk, full_name, age, home FROM test.table WHERE pk = %s")
        self.assertEqual(tpl, (1001,))
