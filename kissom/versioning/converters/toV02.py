def convert(config: dict, logName: str):
    cfg = {"__version__": 2}
    for k in config.keys():
        kstr = str(k)
        cfg[kstr] = {"isTable": True, "columns": config[k]}
    return cfg
