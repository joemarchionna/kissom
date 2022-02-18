def normalizeStoreNameToObj(name: str, removeChars: list = ["_", "-"], toLower: bool = False):
    _nn = ""
    capNext = False
    for c in name:
        if c in removeChars:
            capNext = True
        else:
            if capNext:
                _nn += c.upper()
                capNext = False
            else:
                _nn += c
    return _nn


def normalizeObjNameToStore(name: str, ignoreChars: str = "_-", delimiter: str = "_", toLower: bool = True):
    _nn = ""
    for c in name:
        if c not in ignoreChars:
            if c.isupper():
                _nn += delimiter
            _nn += c
    return _nn.lower() if toLower else _nn


def combineFQTN(schemaName: str, tableName: str):
    return "{}.{}".format(schemaName, tableName)


def splitFQTN(fullyQualifiedTableName: str, defaultSchema: str = "public"):
    if not fullyQualifiedTableName:
        return None, None
    if "." not in fullyQualifiedTableName:
        return defaultSchema, fullyQualifiedTableName
    _elements = fullyQualifiedTableName.split(".")
    return _elements[0], _elements[1]


def getFqn(fullyQualifiedName: str, defaultSchema: str = "public"):
    schema, table = splitFQTN(fullyQualifiedTableName=fullyQualifiedName, defaultSchema=defaultSchema)
    return combineFQTN(schemaName=schema, tableName=table)
