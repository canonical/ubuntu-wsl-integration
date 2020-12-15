#    ubuntuwslctl.loader - loaders for conf
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
import os
import re
from configparser import ConfigParser

from .default import (
     default_ubuntu_wsl_conf_file,
     default_ubuntu_wsl_conf_type,
     default_wsl_conf_file,
     default_wsl_conf_type)
from .i18n import translation

_ = translation.gettext


class ConfigEditor:
    def __init__(self, inst_type, default_conf, default_type, user_conf):
        self.inst_type = inst_type
        self.default_conf = default_conf
        self.default_type = default_type
        self.user_conf = user_conf

        self.config = ConfigParser()
        self.config.BasicInterpolcation = None
        self.config.read_dict(default_conf)

        if os.path.exists(self.user_conf):
            self.config.read(self.user_conf)

    def _get_default(self):
        for section in self.config.sections():
            self.config.remove_section(section)
        self.config.read_dict(self.default_conf)

    def _type_validation(self, config_section, config_setting, input_con):
        assert type(self.default_type) in (str, dict), _("Bad 'default_type' passed. "
                                                         "It should be either 'str' or 'dict'.")
        if type(self.default_type) == str:
            to_validate = self.default_type
        else:
            default_type_tmp = self.default_type
            to_validate = default_type_tmp[config_section][config_setting]

        assert to_validate in ("bool", "pass", "mount"), _("Unknown type to be validated.")
        if to_validate == "bool":
            return input_con in ("true", "false"), _("Input should be either 'true' or 'false'")
        elif to_validate == "path":
            return re.fullmatch(r"(/[^/ ]*)+/?", input_con) is not None, _("Input should be a valid UNIX path")
        elif to_validate == "mount":
            # Not validating this one for now;
            # This is mostly because documentations about DrvFS is very limited
            # and it is really hard to check which can be passed and which can't.
            return True, ""

        return False, "Something went wrong, but how do you even get here?"

    def show(self, config_section, config_setting, is_short=False, is_default=False):
        if is_default:
            self._get_default()
        show_str = ""
        if not is_short:
            show_str = self.inst_type + "." + config_section + "." + config_setting + ": "
        print(show_str + self.config[config_section][config_setting])

    def show_list(self, config_section, is_short=False, is_default=False):
        for config_item in self.config[config_section]:
            self.show(config_section, config_item, is_short, is_default)

    def list(self, is_default=False, is_short=False):
        for section in self.config.sections():
            self.show_list(section, is_short, is_default)

    def update(self, config_section, config_setting, config_value):
        assert_check, assert_warn = self._type_validation(config_section, config_setting, config_value)
        assert assert_check, assert_warn
        self.config[config_section][config_setting] = config_value
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print(_("OK.\n"))

    def reset(self, config_section, config_setting):
        self.config[config_section][config_setting] = self.default_conf[config_section][config_setting]
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print(_("OK.\n"))

    def reset_all(self):
        self._get_default()
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print(_("OK.\n"))


class UbuntuWSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "ubuntu", default_ubuntu_wsl_conf_file, default_ubuntu_wsl_conf_type, "/etc/ubuntu-wsl.conf")


class WSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "wsl", default_wsl_conf_file, default_wsl_conf_type, "/etc/wsl.conf")
