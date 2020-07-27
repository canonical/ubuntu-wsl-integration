from configparser import ConfigParser


def config_name_extractor(config_name):
    config_name_set = config_name.split(".")
    # it should always be three level: the type, the section, and the config.
    if len(config_name_set) == 3:
        return config_name_set[0], config_name_set[1], config_name_set[2]
    elif len(config_name_set) == 2:  # if type is missing, guess which one it is from
        type_name = "Ubuntu" if config_name_set[0] in (
            "Motd", "Interop") else "WSL"
        return type_name, config_name_set[0], config_name_set[1]
    else:  # invaild name, return nothing
        return "", "", ""


def get_ubuntu_wsl_conf_defaults():
    config = ConfigParser()
    config.BasicInterpolcation = None
    config.read("/etc/default/ubuntu-wsl/ubuntu-wsl.conf")
    the_conf_dict = {}
    for section in config.sections():
        the_conf_dict[section] = {}
        for key, val in config.items(section):
            the_conf_dict[section][key] = val
    return the_conf_dict
