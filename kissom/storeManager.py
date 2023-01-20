import logging
from kissom.storeAdapter import StoreAdapter
from kissom.utils.sequences import assignNextValue
from kissom.utils.storeConfig import (
    loadConfigFile,
    saveConfigFile,
    deriveObjNames,
    getConfigFieldNames,
    getPrimaryKeyFieldNames,
)
from kissom.utils.sql import convertConditionsToDbNames
from kissom.utils.names import getFqn
from kissom.utils.validations import validateAttributeValues
from kissom.appExceptions import (
    ObjectNotProvidedException,
    TableNameNotDefinedException,
    PrimaryKeyNotProvidedException,
    InvalidRequestException,
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
        loggerName: str = "kissom",
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

    def closeConnection(self):
        """closes the connection if open"""
        self.logger.debug("Closing Connection")
        self.adapter.closeConnection()

    def commitTransaction(self):
        """commits any records in connection"""
        self.logger.debug("Committing Transaction")
        self.adapter.commit()

    def rollbackTransaction(self):
        """aborts or rolls back any records modified in the connection"""
        self.logger.debug("Rolling Back Transaction")
        self.adapter.rollback()

    def getConfig(self, tableNames: list, configFN: str = None):
        """returns the configuration for the tables specified from the store adapter"""
        self.logger.debug("Getting Table Definitions From Store For '{}'".format(tableNames))
        _cfg = {}
        for fqtn in tableNames:
            _fqtn = getFqn(fullyQualifiedName=fqtn, defaultSchema=self.adapter.getDefaultSchemaName())
            _cfg[_fqtn] = self.adapter.getDefinition(tableName=_fqtn)
        return _cfg

    def getObjectKeys(self, fqtn: str):
        """
        returns the object (dict) keys expected for the table name provided;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema;\n
        """
        _cfg = self._getConfig(fqtn=fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_cfg, logName=self.logger.name)
        return _objKeys

    def getTransactionCursor(self):
        """returns a transaction cursor, if supported, from the store adapter;\n'None' if not supported"""
        return self.adapter.getTransactionCursor()

    def insert(self, obj: dict, fqtn: str = None, sequenceName: str = None, transaction=None):
        """
        inserts an object into the object store;\n
        obj: dict, the object to insert;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        sequenceName: str, name of the sequence to get an id from, if provided, overrides the default value;\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _fqtn = obj.get("__fqtn__", fqtn)
        _tblCfg = self._getConfig(fqtn=_fqtn)
        self._validateIsTable(fqtn=_fqtn)
        assignNextValue(
            obj=obj,
            config=_tblCfg,
            adapter=self.adapter,
            sequenceName=sequenceName,
            xaction=transaction,
            loggerName=self.logger.name,
        )
        validateAttributeValues(obj=obj, config=_tblCfg)
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
        self._validateIsTable(fqtn=_fqtn)
        validateAttributeValues(obj=obj, config=_tblCfg)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        _dbPKeys, _objPKeys = getPrimaryKeyFieldNames(config=_tblCfg)
        conditions = self._getPkConditions(
            obj=obj, config=_tblCfg, conditions=conditions, usePrimaryKeys=usePrimaryKeys
        )
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.update(
            fqtn=_fqtn,
            dbKeys=_dbKeys,
            objKeys=_objKeys,
            objPrimaryKeys=_objPKeys,
            obj=obj,
            conditions=conditions,
            xaction=transaction,
        )

    def replace(
        self, obj: dict, fqtn: str = None, conditions: dict = None, usePrimaryKeys: bool = True, transaction=None
    ):
        """
        replaces an object in the object store;\n
        obj: dict, the object values to update, this can be a partial object, but it will update all the fields in the table adding nulls where necessary;\n
        fqtn: str, fully-qualified table name, in the format 'schema.table', only providing the table name assumes the default schema, if not provided, the fqtn must be provided in the obj with the key '__fqtn__';\n
        conditions: dict, the 'where' clause in the following formats:\n
        Simple: {"fieldName":"firstName","fieldValue":"Johnny"};\n
        Complex: {"operator":"OR","conditions":[{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Johnny","comparer":"="},{"fieldName":"lastName","fieldValue":"Appleseed"}]},{"operator":"AND","conditions":[{"fieldName":"firstName","fieldValue":"Patrick"},{"fieldName":"lastName","fieldValue":"Putnum"}]}]};\n
        usePrimaryKeys: bool, if no conditions are provided, the primary keys of the object are used to define the conditions to update;\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _fqtn = obj.get("__fqtn__", fqtn)
        _tblCfg = self._getConfig(fqtn=_fqtn)
        self._validateIsTable(fqtn=_fqtn)
        validateAttributeValues(obj=obj, config=_tblCfg)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        _dbPKeys, _objPKeys = getPrimaryKeyFieldNames(config=_tblCfg)
        conditions = self._getPkConditions(
            obj=obj, config=_tblCfg, conditions=conditions, usePrimaryKeys=usePrimaryKeys
        )
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.replace(
            fqtn=_fqtn,
            dbKeys=_dbKeys,
            objKeys=_objKeys,
            objPrimaryKeys=_objPKeys,
            obj=obj,
            conditions=conditions,
            xaction=transaction,
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
        self._validateIsTable(fqtn=_fqtn)
        _dbKeys, _objKeys = getConfigFieldNames(config=_tblCfg)
        _dbPKeys, _objPKeys = getPrimaryKeyFieldNames(config=_tblCfg)
        conditions = self._getPkConditions(
            obj=obj, config=_tblCfg, conditions=conditions, usePrimaryKeys=usePrimaryKeys
        )
        convertConditionsToDbNames(conditionTree=conditions, dbKeys=_dbKeys, objKeys=_objKeys)
        return self.adapter.delete(
            fqtn=_fqtn, dbKeys=_dbPKeys, objKeys=_objPKeys, conditions=conditions, xaction=transaction
        )

    def nextSequenceValue(self, sequenceName: str, transaction=None):
        """
        returns the next value of the sequence specified;\n
        sequenceName: str, the name of the sequence object to pull the next value from;\n
        transaction: store transaction cursor, if supported, if not provided, the store adapter auto-commits
        """
        _sequenceName = getFqn(fullyQualifiedName=sequenceName, defaultSchema=self.adapter.getDefaultSchemaName())
        return self.adapter.next(sequenceName=_sequenceName, xaction=transaction)

    def _getConfig(self, fqtn: str):
        if not fqtn:
            raise TableNameNotDefinedException()
        _fqtn = getFqn(fullyQualifiedName=fqtn, defaultSchema=self.adapter.getDefaultSchemaName())
        if not self.config:
            self.config = loadConfigFile(filename=self.configFileName)
        if _fqtn in self.config:
            return self.config[_fqtn]
        dbDef = self.adapter.getDefinition(tableName=_fqtn)
        self.config[_fqtn] = {"isTable": dbDef["isTable"], "columns": list({"db": x} for x in dbDef["columns"])}
        deriveObjNames(config=self.config[_fqtn], logName=self.logger.name)
        saveConfigFile(filename=self.configFileName, config=self.config)
        return self.config[_fqtn]

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

    def _validateIsTable(self, fqtn: str, config: dict):
        if not config.get("isTable", False):
            raise InvalidRequestException("{} Is Not A Table, You Can't Modify It's Contents".format(fqtn))
