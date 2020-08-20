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

        to_validate = ""
        assert type(self.default_type) in (str, dict), _("Bad 'default_type' passed. "
                                                         "It should be either 'str' or 'dict'.")
        if type(self.default_type) == str:
            to_validate = self.default_type
        else:
            to_validate = self.default_type[config_section][config_setting]

        assert to_validate in ("bool", "pass", "mount"), _("Unknown type to be validated.")
        if to_validate == "bool":
            return input_con in ("true", "false"), _("Input should be either 'true' or 'false'")
        elif to_validate == "path":
            return re.fullmatch(r"(/[^/ ]*)+/?", input_con) is not None, _("Input should be a valid UNIX path")
        elif to_validate == "mount":
            # Not validating this one for now;
            # This is mostly because it is very poorly documented by Microsoft
            # and it is really hard to check which can be passed and which can't.
            return True, ""



    def list(self, is_default=False):
        if is_default:
            self._get_default()
        for section in self.config.sections():
            for config_item in self.config[section]:
                print(self.inst_type + "." + section + "." + config_item + ": " +
                      self.config[section][config_item])

    def show(self, config_section, config_setting, is_short=False, is_default=False):
        if is_default:
            self._get_default()
        show_str = ""
        if not is_short:
            show_str = self.inst_type + "." + config_section + "." + config_setting + ": "
        print(show_str + self.config[config_section][config_setting])

    def update(self, config_section, config_setting, config_value):
        try:
            self.config[config_section][config_setting] = config_value
            with open(self.user_conf, 'w') as configfile:
                self.config.write(configfile)
                print(_("OK."))
        except IOError:
            exit(_("IOError: There is a Error whe trying to Read/Write the file."
                   "You need to have root privileges to use this function. Exiting."))

    def reset(self, config_section, config_setting):
        try:
            self.config[config_section][config_setting] = self.default_conf[config_section][config_setting]
            with open(self.user_conf, 'w') as configfile:
                self.config.write(configfile)
                print(_("OK."))
        except IOError:
            exit(_("IOError: There is a Error whe trying to Read/Write the file."
                   "You need to have root privileges to use this function. Exiting."))

    def reset_all(self):
        try:
            self._get_default()
            with open(self.user_conf, 'w') as configfile:
                self.config.write(configfile)
                print(_("OK."))
        except IOError:
            exit(_("IOError: There is a Error whe trying to Read/Write the file."
                   "You need to have root privileges to use this function. Exiting."))


class UbuntuWSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "Ubuntu", default_ubuntu_wsl_conf_file, default_ubuntu_wsl_conf_type, "/etc/ubuntu-wsl.conf")


class WSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "WSL", default_wsl_conf_file, default_wsl_conf_type, "/etc/wsl.conf")
