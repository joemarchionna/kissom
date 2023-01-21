import os
import json
import pathlib
import logging
from kissom.utils.names import normalizeStoreNameToObj
from kissom.versioning.storeConfig import convert
from kissom.versioning import getMajorVersion


def loadConfigFile(filename: str, logName: str = None):
    _logger = logging.getLogger(logName)
    _logger.debug("Loading Configuration File '{}'".format(filename))
    _cfg = {"__version__": getMajorVersion(logName)}
    if filename and os.path.exists(path=filename):
        with open(file=filename) as reader:
            _cfg = json.load(reader)
            _cfg, upgraded = convert(config=_cfg, logName=logName)
            if upgraded:
                saveConfigFile(filename, _cfg, logName)
    return _cfg


def saveConfigFile(filename: str, config: dict, logName: str = None):
    _logger = logging.getLogger(logName)
    _logger.debug("Saving Configuration File '{}'".format(filename))
    # split the fully qualified file name into directory and filename then create directory
    _dir, _fn = os.path.split(filename)
    pathlib.Path(_dir).mkdir(parents=True, exist_ok=True)
    # write out the file
    with open(file=filename, mode="w") as _writer:
        json.dump(obj=config, fp=_writer, indent=4)


def deriveObjNames(config: list, logName: str = None):
    _logger = logging.getLogger(logName)
    _logger.debug("Deriving Object Field Names From Database Column Names: {}".format(config))
    for _col in config["columns"]:
        objName = normalizeStoreNameToObj(name=_col["db"]["name"])
        _col["obj"] = {"name": objName, "type": _col["db"]["type"]}


def getConfigFieldNames(config: list, logName: str = None):
    _logger = logging.getLogger(logName)
    _logger.debug("Getting Database and Object Keys From {}".format(config))
    _dbKeys = []
    _objKeys = []
    for _c in config["columns"]:
        _logger.debug("Column Config: {}".format(_c))
        _dbKeys.append(_c["db"]["name"])
        _objKeys.append(_c["obj"]["name"])
    return _dbKeys, _objKeys


def getPrimaryKeyFieldNames(config: list, logName: str = None):
    _logger = logging.getLogger(logName)
    _logger.debug("Getting Database and Object Primary Keys")
    _dbKeys = []
    _objKeys = []
    for _c in config["columns"]:
        if _c["db"].get("isPrimaryKey", False):
            _dbKeys.append(_c["db"]["name"])
            _objKeys.append(_c["obj"]["name"])
    return _dbKeys, _objKeys


def createColumnDict(
    index,
    name: str,
    type: str,
    default=None,
    isNullable: bool = True,
    isUpdatable: bool = False,
    isPrimaryKey: bool = False,
):
    columnDef = {
        "index": index,
        "name": name,
        "type": type,
        "default": default,
        "isNullable": isNullable,
        "isUpdatable": isUpdatable,
        "isPrimaryKey": isPrimaryKey,
    }
    return columnDef
