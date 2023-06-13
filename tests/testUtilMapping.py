from os import name
import unittest
from kissom.utils.mapping import getDictFromTuple, getValueTuple


class TestUtilMapping(unittest.TestCase):
    def test_a_getDictFromTupleSuccess(self):
        tpl = (24, "billy", 92)
        recordKeys = ["id", "name", "age"]
        d = getDictFromTuple(values=tpl, keys=recordKeys)
        self.assertEqual(d, {"id": 24, "name": "billy", "age": 92})

    def test_b_getDictFromTupleSuccessNone(self):
        tpl = (24, "billy", None)
        recordKeys = ["id", "name", "age"]
        d = getDictFromTuple(values=tpl, keys=recordKeys)
        self.assertEqual(d, {"id": 24, "name": "billy", "age": None})

    def test_c_getDictFromTupleSuccessNoNone(self):
        tpl = (24, "billy", None)
        recordKeys = ["id", "name", "age"]
        d = getDictFromTuple(values=tpl, keys=recordKeys, includeNone=False)
        self.assertEqual(d, {"id": 24, "name": "billy"})

    def test_d_tupleSyntax(self):
        l = ["billy"]
        t = tuple(
            l,
        )
        self.assertEqual(t, ("billy",))
        self.assertEqual(t[0], "billy")

    def test_e_getValueTuple(self):
        record = {"id": 24, "name": "billy", "age": 92}
        recordKeys = ["name", "age"]
        vt = getValueTuple(record=record, keys=recordKeys)
        self.assertEqual(vt, ("billy", 92))

    def test_f_getValueTuple(self):
        record = {"id": 24, "name": "billy", "age": None}
        recordKeys = ["name", "age", "dob"]
        vt = getValueTuple(record=record, keys=recordKeys)
        self.assertEqual(vt, ("billy", None))

    def test_g_getValueTuple(self):
        record = {"id": 24, "name": "billy", "age": None}
        recordKeys = ["name", "age", "dob"]
        vt = getValueTuple(record=record, keys=recordKeys, includeIfNotPresent=True)
        self.assertEqual(vt, ("billy", None, None))
