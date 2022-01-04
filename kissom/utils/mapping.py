def getDictFromTuple(values: tuple, keys: list, includeNone: bool = True):
    """returns a dict based on the tuple values and assigns the values to the keys provided\n
    for instance, values=(1, "bill", 5} and keys=["id", "name", "age"] returns {"id": 1, "name": "bill", "age": 5}
    """
    _obj = {}
    for _i in range(len(values)):
        if includeNone or (values[_i] is not None):
            _obj[keys[_i]] = values[_i]
    return _obj


def _addValue(valueList: list, record: dict, keyName: str, includeNone: bool):
    if includeNone or (keyName in record):
        valueList.append(record.get(keyName, None))
    return valueList


def getValueTuple(record: dict, keys: list, includeIfNotPresent=False):
    """returns a tuple of values from the record provided of only the keys specified that are in the record\n
    for instance, record={"id":1, "name":"bill", "age":5} and keys=["name","age"] returns ("bill", 5)
    """
    _vals = []
    for _k in keys:
        _addValue(valueList=_vals, record=record, keyName=_k, includeNone=includeIfNotPresent)
    return tuple(
        _vals,
    )
