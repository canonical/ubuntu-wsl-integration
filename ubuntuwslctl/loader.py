import os
from configparser import ConfigParser

from .default import default_ubuntu_wsl_conf_file, default_wsl_conf_file


class ConfigEditor:
    def __init__(self, inst_type, default_conf, user_conf):
        self.inst_type = inst_type
        self.default_conf = default_conf
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

    def list(self, is_default=False):
        if is_default:
            self._get_default()
        for section in self.config.sections():
            for configitem in self.config[section]:
                print(self.inst_type + "." + section + "." + configitem + ": " +
                      self.config[section][configitem])

    def show(self, config_section, config_setting, isShort=False, isDefault=False):
        if isDefault:
            self._get_default()
        show_str = ""
        if not (isShort):
            show_str = self.inst_type + "." + config_section + "." + config_setting + ": "
        print(show_str + self.config[config_section][config_setting])

    def update(self, config_section, config_setting, config_value):
        self.config[config_section][config_setting] = config_value
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print("OK.")

    def reset(self, config_section, config_setting):
        self.config[config_section][config_setting] = self.default_conf[config_section][config_setting]
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print("OK.")

    def resetall(self):
        self._get_default()
        with open(self.user_conf, 'w') as configfile:
            self.config.write(configfile)
            print("OK.")


class UbuntuWSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "Ubuntu", default_ubuntu_wsl_conf_file, "/etc/ubuntu-wsl.conf")


class WSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "WSL", default_wsl_conf_file, "/etc/wsl.conf")
