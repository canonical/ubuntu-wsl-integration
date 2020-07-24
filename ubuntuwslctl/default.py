# This is the file that contains the default settings if reset
from ubuntuwslctl.helper import get_ubuntu_wsl_conf_defaults


# these are the default settings in ubuntu-wsl.conf.
default_ubuntu_wsl_conf_file = get_ubuntu_wsl_conf_defaults()

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
