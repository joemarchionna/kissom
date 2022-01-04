_tnExMsg = "A Fully-Qualified Table Name Must Be Supplied Either In The Object With The Key '__fqtn__' Or Defined In The Method Parameter 'fqtn' With The Format 'schema.table'"


class TableNameNotDefinedException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(_tnExMsg)


class TableNameDoesNotExistException(Exception):
    def __init__(self, tablename: str) -> None:
        _msg = "Table Name '{}' Does Not Exist In Database".format(tablename)
        super().__init__(_msg)


class ObjectNotProvidedException(Exception):
    pass


class PrimaryKeyNotProvidedException(Exception):
    def __init__(self, keyName: str) -> None:
        _msg = "Primary Key '{}' Was Not Provided In The Object, Can't Use Primary Keys As Conditions".format(keyName)
        super().__init__(_msg)
