def config_name_extractor(config_name):
    config_name_set = config_name.split(".")
    if len(config_name_set) == 3: # it should always be three level: the type, the section, and the config.
        return config_name_set[0], config_name_set[1], config_name_set[2]
    elif len(config_name_set) == 2: # if type is missing, guess which one it is from
        type_name = "Ubuntu" if config_name_set[0] in ("Motd", "Interop") else "WSL"
        return type_name, config_name_set[0], config_name_set[1]
    else: # invaild name, return nothing
        return "", "", ""


