from kissom.versioning.converters.toV02 import convert as convertToV02
from kissom.versioning import getMajorVersion

_convertingMap = {"toV2": convertToV02}


def convert(config: dict, logName: str = None):
    libVersion = getMajorVersion(logName)
    curVersion = config.get("__version__", 1)
    if curVersion >= libVersion:
        return config, False
    cfg = dict(config)
    upgraded = False
    for i in range(curVersion, libVersion):
        upgradeKey = "toV{}".format(i + 1)
        upgradeMethod = _convertingMap.get(upgradeKey, None)
        if upgradeMethod:
            cfg = upgradeMethod(config=cfg, logName=logName)
            upgraded = True
    return cfg, upgraded
