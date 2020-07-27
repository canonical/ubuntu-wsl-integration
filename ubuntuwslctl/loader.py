from configparser import ConfigParser
from default import default_ubuntu_wsl_conf_file, default_wsl_conf_file
import os
import sys


class ConfigEditor:
    def __load_defaults__(self):
        pass

    def __init__(self, type, default_conf, user_conf):
        self.config = ConfigParser()
        self.config.BasicInterpolcation = None
        self.default_conf = default_conf
        self.user_conf = user_conf
        self.config.read_dict(default_conf)
        if os.path.exists(self.user_conf):
            self.config.read(self.user_conf)
        self.type = type
        self.location = ""

    def list(self):
        for section in self.config.sections():
            for configitem in self.config[section]:
                print(self.type+"."+section+"."+configitem+": " +
                      self.config[section][configitem])

    def show(self, config_section, config_setting):
        print(self.type+"."+config_section+"."+config_setting+": " +
              self.config[config_section][config_setting])

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


class UbuntuWSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "Ubuntu", default_ubuntu_wsl_conf_file, "/etc/ubuntu-wsl.conf")


class WSLConfigEditor(ConfigEditor):
    def __init__(self):
        ConfigEditor.__init__(
            self, "WSL", default_wsl_conf_file, "/etc/wsl.conf")
