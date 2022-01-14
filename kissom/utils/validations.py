from kissom.appExceptions import ObjectAttributeValueException

_allowedValuesStr = "allowedValues"


def validateAttributeValues(obj: dict, config: list):
    for _col in config:
        if "obj" in _col:
            _attName = _col["obj"]["name"]
            if (_attName in obj) and (_allowedValuesStr in _col["obj"]):
                if obj[_attName] not in _col["obj"][_allowedValuesStr]:
                    raise ObjectAttributeValueException(
                        attributeName=_attName,
                        attributeValue=obj[_attName],
                        allowedValues=_col["obj"][_allowedValuesStr],
                    )
