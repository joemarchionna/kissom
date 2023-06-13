from os import name
import json
import unittest
from kissom.utils.sql import insertSql, updateSql, deleteSql, selectSql, getConditions


class TestUtilSqlUpdate(unittest.TestCase):
    def test_a(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = updateSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET full_name = %s, age = %s, home = %s WHERE pk = %s RETURNING full_name, age, home",
        )
        self.assertEqual(tpl, ("Johnny", 24, "Monroe", 1001))

    def test_b(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "hometown": "Monroe"}
        sql, tpl = updateSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(sql, "UPDATE test.table SET home = %s WHERE pk = %s RETURNING full_name, age, home")
        self.assertEqual(tpl, ("Monroe", 1001))

    def test_c(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["name", "age", "hometown"]
        dKeys = ["full_name", "age", "home"]
        ct = {
            "operator": "AND",
            "conditions": [{"fieldName": "org", "fieldValue": 199200}, {"fieldName": "pk", "fieldValue": 1001}],
        }
        r = {"coid": 199200, "id": 1001, "hometown": "Monroe"}
        sql, tpl = updateSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql, "UPDATE test.table SET home = %s WHERE (org = %s AND pk = %s) RETURNING full_name, age, home"
        )
        self.assertEqual(tpl, ("Monroe", 199200, 1001))

    def test_d(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["id", "parentId", "name", "age", "hometown", "status"]
        dKeys = ["id", "parent", "full_name", "age", "home", "status"]
        r = {"id": 2112, "status": "missing"}
        ct = {
            "operator": "OR",
            "conditions": [
                {"fieldName": "id", "fieldValue": r["id"]},
                {"fieldName": "parentId", "fieldValue": r["id"]},
            ],
        }
        sql, tpl = updateSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET status = %s WHERE (id = %s OR parentId = %s) RETURNING id, parent, full_name, age, home, status",
        )
        self.assertEqual(tpl, ("missing", 2112, 2112))
