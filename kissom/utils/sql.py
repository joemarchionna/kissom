def addParam(baseLength: int, sqlBase, sqlToAdd, separator: str = ", "):
    """concatenates text with separator if the text length is longer than specified"""
    if len(sqlBase) > baseLength:
        sqlBase += separator
    return sqlBase + sqlToAdd


def insertSql(tableName: str, objKeys: list, dbKeys: list, data: dict):
    _fields = ""
    _values = ""
    _valList = []
    for i in range(len(objKeys)):
        if objKeys[i] in data:
            _fields = addParam(baseLength=0, sqlBase=_fields, sqlToAdd=dbKeys[i])
            _values = addParam(baseLength=0, sqlBase=_values, sqlToAdd="%s")
            _valList.append(data[objKeys[i]])
    _sql = "INSERT INTO {fqtn} ({fields}) VALUES ({values})".format(fqtn=tableName, fields=_fields, values=_values)
    _sql += _getReturning(keys=dbKeys)
    _valtpl = tuple(
        _valList,
    )
    return _sql, _valtpl


def updateSql(tableName: str, objKeys: list, dbKeys: list, data: dict, conditionTree: dict):
    _sql = "UPDATE {fqtn} SET ".format(fqtn=tableName)
    _baseLength = len(_sql)
    _sqlVals = []
    for i in range(len(objKeys)):
        if objKeys[i] in data:
            _sql = addParam(baseLength=_baseLength, sqlBase=_sql, sqlToAdd="{field} = %s".format(field=dbKeys[i]))
            _sqlVals.append(data[objKeys[i]])
    _sqlP, _valuesP = getWhereConditions(conditionTree=conditionTree)
    _sql = _sql + _sqlP + _getReturning(keys=dbKeys)
    _sqlVals.extend(_valuesP)
    _values = tuple(
        _sqlVals,
    )
    return _sql, _values


def deleteSql(tableName: str, dbKeys: list, conditionTree: dict):
    _sql = "DELETE FROM {fqtn}".format(fqtn=tableName)
    _sqlVals = []
    _sqlP, _valuesP = getWhereConditions(conditionTree=conditionTree)
    _sql = _sql + _sqlP + _getReturning(keys=dbKeys)
    _sqlVals.extend(_valuesP)
    _values = tuple(
        _sqlVals,
    )
    return _sql, _values


def selectSql(tableName: str, dbKeys: list, conditionTree: dict = None):
    _sql = "SELECT "
    _sqlVals = []
    _baseLength = len(_sql)
    for _i in range(len(dbKeys)):
        _sql = addParam(baseLength=_baseLength, sqlBase=_sql, sqlToAdd=dbKeys[_i])
    _sql += " FROM {}".format(tableName)
    _sqlP, _valuesP = getWhereConditions(conditionTree=conditionTree)
    _sql += _sqlP
    _sqlVals.extend(_valuesP)
    _values = tuple(
        _sqlVals,
    )
    return _sql, _values


def _getReturning(keys: list):
    _sql = ""
    if keys:
        _sql = " RETURNING "
        _baseLength = len(_sql)
        for _k in keys:
            _sql = addParam(baseLength=_baseLength, sqlBase=_sql, sqlToAdd=_k)
    return _sql


def getWhereConditions(conditionTree: dict):
    if not conditionTree:
        return "", []
    _sql, _vals = getConditions(conditionTree=conditionTree)
    _sql = " WHERE " + _sql
    return _sql, _vals


def getConditions(conditionTree: dict):
    _sql = ""
    _values = []
    if conditionTree and ("operator" in conditionTree) and ("conditions" in conditionTree):
        if len(conditionTree["conditions"]) > 1:
            _sql += "("
        _baseLength = len(_sql)
        for c in conditionTree["conditions"]:
            _sqlP, _valuesP = getConditions(conditionTree=c)
            _sql = addParam(
                baseLength=_baseLength,
                sqlBase=_sql,
                sqlToAdd=_sqlP,
                separator=" {} ".format(conditionTree["operator"]),
            )
            _values.extend(_valuesP)
        if len(conditionTree["conditions"]) > 1:
            _sql += ")"
    elif conditionTree and ("fieldName" in conditionTree) and ("fieldValue" in conditionTree):
        _sql = "{fieldName} {comparer} %s".format(
            fieldName=conditionTree["fieldName"], comparer=conditionTree.get("comparer", "=")
        )
        _values.append(conditionTree["fieldValue"])
    return _sql, _values


def convertConditionsToDbNames(conditionTree: dict, dbKeys: list, objKeys: list):
    if conditionTree and ("conditions" in conditionTree):
        for c in conditionTree["conditions"]:
            convertConditionsToDbNames(conditionTree=c, dbKeys=dbKeys, objKeys=objKeys)
    elif conditionTree and ("fieldName" in conditionTree):
        _idx = objKeys.index(conditionTree["fieldName"])
        conditionTree["fieldName"] = dbKeys[_idx]
