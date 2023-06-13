from os import name
import json
import unittest
from kissom.utils.validations import validateAttributeValues, _allowedValuesStr
from kissom.appExceptions import ObjectAttributeValueException


class TestUtilValidations(unittest.TestCase):
    def test_a_none(self):
        _object = {"name": "John"}
        _config = [{"obj": {"name": "status"}}]
        validateAttributeValues(obj=_object, config=_config)
        self.assertTrue(True)

    def test_b_noneDefined(self):
        _object = {"name": "John", "status": "active"}
        _config = [{"obj": {"name": "status"}}]
        validateAttributeValues(obj=_object, config=_config)
        self.assertTrue(True)

    def test_c_definedValid(self):
        _object = {"name": "John", "status": "active"}
        _config = [{"obj": {"name": "status", _allowedValuesStr: ["active", "inactive"]}}]
        validateAttributeValues(obj=_object, config=_config)
        self.assertTrue(True)

    def test_c_definedInvalid(self):
        _object = {"name": "John", "status": "locked"}
        _config = [{"obj": {"name": "status", _allowedValuesStr: ["active", "inactive"]}}]
        self.assertRaises(ObjectAttributeValueException, validateAttributeValues, _object, _config)
