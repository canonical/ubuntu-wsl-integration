import sys
from configparser import ConfigParser

from .i18n import translation

_ = translation.gettext


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def config_name_extractor(config_name):
    config_name_set = config_name.split(".")
    # it should always be three level: the type, the section, and the config.
    if len(config_name_set) == 3:
        return config_name_set[0], config_name_set[1], config_name_set[2]
    elif len(config_name_set) == 2:  # if type is missing, guess
        if config_name_set[0] in ("Ubuntu", "WSL") and config_name_set[1] == "*":  # top level wild card
            return config_name_set[0], config_name_set[1], ""
        else:  # other cases
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


def query_yes_no(question, default="yes", assume_yes=False):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    Adopted from https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(_("invalid default answer: '{name}'").format(name=default))

    while True:
        sys.stdout.write(question + prompt)
        if assume_yes:
            choice = "y"
        else:
            choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(_("Please respond with 'yes' or 'no' "
                               "(or 'y' or 'n').\n"))
