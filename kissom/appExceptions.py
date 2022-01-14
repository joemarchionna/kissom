_tnExMsg = "A Fully-Qualified Table Name Must Be Supplied Either In The Object With The Key '__fqtn__' Or Defined In The Method Parameter 'fqtn' With The Format 'schema.table'"
_avExMsg = "Object Attribute '{}' As Value '{}' Is Not In Allowed Values List: {}"


class KissomException(Exception):
    pass


class TableNameNotDefinedException(KissomException):
    def __init__(self, *args: object) -> None:
        super().__init__(_tnExMsg, *args)


class TableNameDoesNotExistException(KissomException):
    def __init__(self, tablename: str, *args: object) -> None:
        _msg = "Table Name '{}' Does Not Exist In Database".format(tablename)
        super().__init__(_msg, *args)


class ObjectNotProvidedException(KissomException):
    pass


class PrimaryKeyNotProvidedException(KissomException):
    def __init__(self, keyName: str, *args) -> None:
        _msg = "Primary Key '{}' Was Not Provided In The Object, Can't Use Primary Keys As Conditions".format(keyName)
        super().__init__(_msg, *args)


class ObjectAttributeValueException(KissomException):
    def __init__(self, attributeName: str, attributeValue, allowedValues: list, *args: object) -> None:
        _msg = _avExMsg.format(attributeName, attributeValue, allowedValues)
        super().__init__(_msg, *args)
