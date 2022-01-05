import logging
from kissom.storeAdapter import StoreAdapter
from kissom.utils.storeConfig import (
    loadConfigFile,
    saveConfigFile,
    deriveObjNames,
    getConfigFieldNames,
    getPrimaryKeyFieldNames,
)
from kissom.utils.sql import convertConditionsToDbNames
from kissom.appExceptions import (
    ObjectNotProvidedException,
    TableNameNotDefinedException,
    PrimaryKeyNotProvidedException,
)


class StoreManager(object):
    """
    manages access to a data store;\n
    adapter: kissom.StoreAdapter extended to provide generic access to the data store;\n
    loggerName: str, the logger name, optional;\n
    config: dict, the optional store configuration;\n
    configFN: str, path to the json configuration file;\n
    For configurations, the manager will evaluate config first, then if not provided, it will attempt to get the config at the configFN specified, if that does not exist, it will attempt to derive the config through the store adapter
    """

    def __init__(
        self,
        adapter: StoreAdapter,
        loggerName: str = None,
        config: dict = None,
        configFN: str = "local/storeConfig.json",
    ) -> None:
        super().__init__()
        self.adapter = adapter
        self.logger = logging.getLogger(loggerName)
        self.config = config
        self.configFileName = configFN

    def __enter__(self):
        self.logger.debug("Executing __enter__")
        return self

    def __exit__(self, type, value, traceback):
        self.logger.debug("Executing __exit__")
        self.adapter.closeConnection()

    def getConfig(self, tableNames: list, configFN: str = None):
        """returns the configuration for the tables specified from the store adapter"""
        self.logger.debug("Getting Table Definitions From Store For '{}'".format(tableNames))
        _cfg = {}
        for fqtn in tableNames:
            _cfg[fqtn] = self.adapter.getTableDefinition(tableName=fqtn)
        return _cfg

    def getTransactionCursor(self):
        """returns a transaction cursor, if supported, from the store adapter;\n'None' if not supported"""
        return self.adapter.getTransactionCursor()

    def insert(self, obj: dict, fqtn: str = None, transaction=None):
        """
        inserts an object into the object store;\n
        obj: dict, the object to insert;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _fqtn = obj.get("__fqtn__", fqtn)
        _tblCfg = self._getConfig(fqtn=_fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        return self.adapter.insert(fqtn=_fqtn, dbKeys=_dbKeys, objKeys=_objKeys, obj=obj, xaction=transaction)

    def select(self, fqtn: str, conditions: dict = None):
        """
        selects objects from the object store;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        conditions: dict, the 'where' clause in the following formats:\n
        Simple: {"fieldName":"firstName","fieldValue":"Johnny"}\n
        Complex: {"operator":"OR","conditions":[{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Johnny","comparer":"="},{"fieldName":"lastName","fieldValue":"Appleseed"}]},{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Patrick"},{"fieldName":"lastName","fieldValue":"Putnum"}]}]}
        """
        _tblCfg = self._getConfig(fqtn=fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.select(fqtn=fqtn, dbKeys=_dbKeys, objKeys=_objKeys, conditions=conditions)

    def update(
        self, obj: dict, fqtn: str = None, conditions: dict = None, usePrimaryKeys: bool = True, transaction=None
    ):
        """
        updates an object in the object store;\n
        obj: dict, the object values to update, this can be a partial object, it will only update the fields provided;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        conditions: dict, the 'where' clause in the following formats:\n
        Simple: {"fieldName":"firstName","fieldValue":"Johnny"};\n
        Complex: {"operator":"OR","conditions":[{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Johnny","comparer":"="},{"fieldName":"lastName","fieldValue":"Appleseed"}]},{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Patrick"},{"fieldName":"lastName","fieldValue":"Putnum"}]}]};\n
        usePrimaryKeys: bool, if no conditions are provided, the primary keys of the object are used to define the conditions to update;\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _fqtn = obj.get("__fqtn__", fqtn)
        _tblCfg = self._getConfig(fqtn=_fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        conditions = self._getPkConditions(
            obj=obj, config=_tblCfg, conditions=conditions, usePrimaryKeys=usePrimaryKeys
        )
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.update(
            fqtn=_fqtn, dbKeys=_dbKeys, objKeys=_objKeys, obj=obj, conditions=conditions, xaction=transaction
        )

    def delete(
        self,
        obj: dict = None,
        fqtn: str = None,
        conditions: dict = None,
        usePrimaryKeys: bool = True,
        transaction=None,
    ):
        """
        deletes an object from the object store;\n
        obj: dict, the object to delete, only required if using the primary keys to delete;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        conditions: dict, the 'where' clause in the following formats:\n
        Simple: {"fieldName":"firstName","fieldValue":"Johnny"};\n
        Complex: {"operator":"OR","conditions":[{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Johnny","comparer":"="},{"fieldName":"lastName","fieldValue":"Appleseed"}]},{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Patrick"},{"fieldName":"lastName","fieldValue":"Putnum"}]}]};\n
        usePrimaryKeys: bool, if no conditions are provided, the primary keys of the object are used to define the conditions to update;\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _fqtn = obj.get("__fqtn__", fqtn) if obj else fqtn
        _tblCfg = self._getConfig(fqtn=_fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        _dbPKeys, _objPKeys = getPrimaryKeyFieldNames(config=_tblCfg)
        conditions = self._getPkConditions(
            obj=obj, config=_tblCfg, conditions=conditions, usePrimaryKeys=usePrimaryKeys
        )
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.delete(
            fqtn=_fqtn, dbKeys=_dbPKeys, objKeys=_objPKeys, conditions=conditions, xaction=transaction
        )

    def _getConfig(self, fqtn: str):
        if not fqtn:
            raise TableNameNotDefinedException()
        if not self.config:
            self.config = loadConfigFile(filename=self.configFileName)
        if fqtn in self.config:
            return self.config[fqtn]
        dbColumns = self.adapter.getTableDefinition(tableName=fqtn)
        self.config[fqtn] = list({"db": x} for x in dbColumns)
        deriveObjNames(config=self.config[fqtn], logName=self.logger.name)
        saveConfigFile(filename=self.configFileName, config=self.config)
        return self.config[fqtn]

    def _getPkConditions(self, obj: dict, config, conditions: dict, usePrimaryKeys: bool):
        if (conditions is None) and usePrimaryKeys:
            if not obj:
                raise ObjectNotProvidedException()
            _dbPKeys, _objPKeys = getPrimaryKeyFieldNames(config=config)
            conditions = {"operator": "AND", "conditions": []}
            for i in range(len(_dbPKeys)):
                try:
                    conditions["conditions"].append({"fieldName": _objPKeys[i], "fieldValue": obj[_objPKeys[i]]})
                except KeyError as kerr:
                    raise PrimaryKeyNotProvidedException(keyName=_objPKeys[i])
        return conditions
