#    ubuntuwslctl.helper - helpers for the cli
#    Copyright (C) 2020 Canonical Ltd.
#    Copyright (C) 2020 Patrick Wu
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This package is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  On Debian systems, the complete text of the GNU General
#  Public License version 3 can be found in "/usr/share/common-licenses/GPL-3".
import sys
from configparser import ConfigParser

from ubuntuwslctl.utils.i18n import translation

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
        if config_name_set[0] in ("ubuntu", "wsl") and config_name_set[1] == "*":  # top level wild card
            return config_name_set[0], config_name_set[1], ""
        else:  # other cases
            type_name = "ubuntu" if config_name_set[0] in (
                "Motd", "Interop") else "wsl"
            return type_name, config_name_set[0], config_name_set[1]
    else:  # invaild name, return nothing
        return "", "", ""


def str2bool(s):
    return s.lower() in ("yes", "y", "1", "true", "t")


def bool2str(b):
    return "true" if b else "false"


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
            if assume_yes:
                sys.stdout.write("\n")

