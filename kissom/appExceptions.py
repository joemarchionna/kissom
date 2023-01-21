TABLE_NAME_NOT_DEFINED_MSG = "A Fully-Qualified Table Name Must Be Supplied Either In The Object With The Key '__fqtn__' Or Defined In The Method Parameter 'fqtn' With The Format 'schema.table'"
CATALOG_NAME_NOT_EXIST_MSG = "Catalog (Table/View/Materialized View) Name '{}' Does Not Exist In Database"
OBJECT_ATT_VALUE_MSG = "Object Attribute '{}' As Value '{}' Is Not In Allowed Values List: {}"


class KissomException(Exception):
    pass


class TableNameNotDefinedException(KissomException):
    def __init__(self, *args: object) -> None:
        super().__init__(TABLE_NAME_NOT_DEFINED_MSG, *args)


class TableNameDoesNotExistException(KissomException):
    def __init__(self, tablename: str, *args: object) -> None:
        _msg = (
            "This Exception Has Been Deprecated, Please Use 'CatalogNameDoesNotExistException'; "
            + CATALOG_NAME_NOT_EXIST_MSG
        )
        _msg = _msg.format(tablename)
        super().__init__(_msg, *args)


class CatalogNameDoesNotExistException(KissomException):
    def __init__(self, tablename: str, *args: object) -> None:
        _msg = CATALOG_NAME_NOT_EXIST_MSG.format(tablename)
        super().__init__(_msg, *args)


class ObjectNotProvidedException(KissomException):
    pass


class PrimaryKeyNotProvidedException(KissomException):
    def __init__(self, keyName: str, *args) -> None:
        _msg = "Primary Key '{}' Was Not Provided In The Object, Can't Use Primary Keys As Conditions".format(keyName)
        super().__init__(_msg, *args)


class ObjectAttributeValueException(KissomException):
    def __init__(self, attributeName: str, attributeValue, allowedValues: list, *args: object) -> None:
        _msg = OBJECT_ATT_VALUE_MSG.format(attributeName, attributeValue, allowedValues)
        super().__init__(_msg, *args)


class InvalidRequestException(KissomException):
    pass
