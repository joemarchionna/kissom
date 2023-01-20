def convert(config: dict):
    cfg = {"__version__": 2}
    for k in config.keys():
        kstr = str(k)
        cfg[kstr]["isTable"] = True
        cfg[kstr]["columns"] = config[k]
    return cfg
