import configparser
import os
import sys

class ConfigEditor:
    def __load_settings__(self):
        pass

    def __init__(self, type):
        self.config = configparser.ConfigParser()
        self.config.BasicInterpolcation = None
        self.__load_settings__()
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

    def add(self, config_section, config_setting, config_value):
        self.config[config_section][config_setting] = config_value
        with open(self.location, 'w') as configfile:
            self.config.write(configfile)
            print("OK.")


class UbuntuWSLConfigEditor(ConfigEditor):
    def __load_settings__(self):
        self.location = "/etc/ubuntu-wsl.conf" if os.path.exists(
            "/etc/ubuntu-wsl.conf") else "/etc/default/ubuntu-wsl/ubuntu-wsl.conf"
        self.config.read(self.location)

    def __init__(self):
        ConfigEditor.__init__(self, "Ubuntu")


class WSLConfigEditor(ConfigEditor):
    def __load_settings__(self):
        """
        This is for wsl.conf only.
        This won't help set all global settings in .wslconfig on the Windows side.
        """
        # these are the public default configuration for wsl.conf.
        # this won't cover all hidden configurations.
        default_wsl_conf_file = {'automount': {'enabled': 'true',
                                               'mountFsTab': 'true',
                                               'root': '/mnt/',
                                               'options': ''},
                                 'network': {'generateHosts': 'true',
                                             'generateResolvConf': 'true'},
                                 'interop': {'enabled': 'true',
                                             'appendWindowsPath': 'true'}}
        self.config.read_dict(default_wsl_conf_file)
        self.location = "/etc/wsl.conf"
        if os.path.exists(self.location):
            self.config.read(self.location)


    def __init__(self):
        ConfigEditor.__init__(self, "WSL")
