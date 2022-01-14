import logging
from kissom.utils.storeConfig import getPrimaryKeyFieldNames
from kissom.storeAdapter import StoreAdapter
import logging


def assignNextValue(obj: dict, config: dict, adapter: StoreAdapter, sequenceName: str, xaction, loggerName: str):
    logger = logging.getLogger(loggerName)
    if sequenceName:
        logger.debug("Getting Next Sequence Id From '{}'".format(sequenceName))
        nextId = adapter.next(sequenceName=sequenceName, xaction=xaction)
        pkDb, pkObj = getPrimaryKeyFieldNames(config=config, logName=loggerName)
        obj[pkObj[0]] = nextId
    logger.debug("No Sequence Specified")
    return
