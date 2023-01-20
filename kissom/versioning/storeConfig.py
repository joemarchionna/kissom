import json, pkgutil
from kissom.versioning.converters.toV02 import convert as convertToV02


_convertingMap = {"toV2": convertToV02}


def _getMajorVersion() -> int:
    version = json.loads(pkgutil.get_data("kissom", "_metadata.json").decode())
    majorVersion = int(version["version"].split(".")[0])
    return majorVersion


def convert(config: dict):
    libVersion = _getMajorVersion()
    curVersion = config.get("__version__", 1)
    if curVersion >= libVersion:
        return config, False
    cfg = dict(config)
    upgraded = False
    for i in range(curVersion, libVersion):
        upgradeKey = "toV{}".format(i + 1)
        upgradeMethod = _convertingMap.get(upgradeKey, None)
        if upgradeMethod:
            cfg = upgradeMethod(config=cfg)
            upgraded = True
    return cfg, upgraded
