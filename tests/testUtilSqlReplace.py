import unittest
from kissom.utils.sql import replaceSql


class TestUtilSqlReplace(unittest.TestCase):
    def test_a(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["id", "name", "age", "hometown"]
        dKeys = ["pk", "full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "name": "Johnny", "age": 24, "hometown": "Monroe"}
        sql, tpl = replaceSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET full_name = %s, age = %s, home = %s WHERE pk = %s RETURNING pk, full_name, age, home",
        )
        self.assertEqual(tpl, ("Johnny", 24, "Monroe", 1001))

    def test_b(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["id", "name", "age", "hometown"]
        dKeys = ["pk", "full_name", "age", "home"]
        ct = {"fieldName": "pk", "fieldValue": 1001}
        r = {"id": 1001, "hometown": "Monroe"}
        sql, tpl = replaceSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET full_name = %s, age = %s, home = %s WHERE pk = %s RETURNING pk, full_name, age, home",
        )
        self.assertEqual(tpl, (None, None, "Monroe", 1001))

    def test_c(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["id", "name", "age", "hometown"]
        dKeys = ["pk", "full_name", "age", "home"]
        ct = {"fieldName": "age", "fieldValue": 50}
        r = {"id": 1001, "hometown": "Monroe"}
        sql, tpl = replaceSql(
            tableName=tn,
            objKeys=okeys,
            objPrimaryKeys=opkeys,
            dbKeys=dKeys,
            data=r,
            conditionTree=ct,
            setPrimaryKeys=True,
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET pk = %s, full_name = %s, age = %s, home = %s WHERE age = %s RETURNING pk, full_name, age, home",
        )
        self.assertEqual(tpl, (1001, None, None, "Monroe", 50))

    def test_d(self):
        tn = "test.table"
        opkeys = ["id"]
        okeys = ["id", "familyId", "name", "age", "hometown"]
        dKeys = ["pk", "family_id", "full_name", "age", "home"]
        ct = {
            "operator": "AND",
            "conditions": [{"fieldName": "family_id", "fieldValue": 199200}, {"fieldName": "pk", "fieldValue": 1001}],
        }
        r = {"familyId": 199200, "id": 1001, "hometown": "Monroe"}
        sql, tpl = replaceSql(
            tableName=tn, objKeys=okeys, objPrimaryKeys=opkeys, dbKeys=dKeys, data=r, conditionTree=ct
        )
        self.assertEqual(
            sql,
            "UPDATE test.table SET family_id = %s, full_name = %s, age = %s, home = %s WHERE (family_id = %s AND pk = %s) RETURNING pk, family_id, full_name, age, home",
        )
        self.assertEqual(tpl, (199200, None, None, "Monroe", 199200, 1001))
