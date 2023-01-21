import json, pkgutil, logging


def getMajorVersion(logName: str = None) -> int:
    try:
        version = json.loads(pkgutil.get_data("kissom", "_metadata.json").decode())
        majorVersion = int(version["version"].split(".")[0])
        return majorVersion
    except Exception as err:
        logging.getLogger(logName).error("Failed To Get Major Version Of kissom package")
        return 1
