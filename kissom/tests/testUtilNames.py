from os import name
import unittest
from kissom.utils.names import normalizeObjNameToStore, normalizeStoreNameToObj


class TestUtilNames(unittest.TestCase):
    def test_a_objToStoreSuccess(self):
        objName = "myName"
        storeName = normalizeObjNameToStore(name=objName)
        self.assertEqual(storeName, "my_name")

    def test_b_objToStoreSuccess(self):
        objName = "id"
        storeName = normalizeObjNameToStore(name=objName)
        self.assertEqual(storeName, "id")

    def test_c_storeToObjSuccess(self):
        storeName = "silly_name"
        objName = normalizeStoreNameToObj(name=storeName, toLower=False)
        self.assertEqual(objName, "sillyName")

    def test_d_storeToObjSuccess(self):
        storeName = "id"
        objName = normalizeStoreNameToObj(name=storeName, toLower=False)
        self.assertEqual(objName, "id")
