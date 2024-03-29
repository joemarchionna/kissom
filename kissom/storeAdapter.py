import logging


class StoreAdapter(object):
    def __init__(self, logName: str = None):
        self.logger = logging.getLogger(logName)

    def getDefinition(self, tableName: str):
        pass

    def getTransactionCursor(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def openConnection(self):
        pass

    def closeConnection(self):
        pass

    def getDefaultSchemaName(self):
        pass

    def insert(self, fqtn: str, dbKeys: list, objKeys: list, obj: dict, xaction=None):
        pass

    def select(self, fqtn: str, dbKeys: list, objKeys: list, conditions: dict):
        pass

    def update(
        self, fqtn: str, dbKeys: list, objKeys: list, objPrimaryKeys: list, obj: dict, conditions: dict, xaction=None
    ):
        pass

    def replace(
        self, fqtn: str, dbKeys: list, objKeys: list, objPrimaryKeys: list, obj: dict, conditions: dict, xaction=None
    ):
        pass

    def delete(self, fqtn: str, dbKeys: list, objKeys: list, conditions: dict, xaction=None):
        pass

    def next(self, sequenceName: str, xaction=None):
        pass
