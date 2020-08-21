# This is the file that contains the default settings if reset
from .helper import get_ubuntu_wsl_conf_defaults

# these are the default settings in ubuntu-wsl.conf.
# default configuration of ubuntu_wsl.conf is stored in /etc/default/wslu/
default_ubuntu_wsl_conf_file = get_ubuntu_wsl_conf_defaults()
default_ubuntu_wsl_conf_type = "bool"

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
# type is flatten as case is not important for config items
default_wsl_conf_type = {'automount': {'enabled': 'bool',
                                       'mountfstab': 'bool',
                                       'root': 'path',
                                       'options': 'mount'},
                         'network': {'generatehosts': 'bool',
                                     'generateresolvconf': 'bool'},
                         'interop': {'enabled': 'bool',
                                     'appendwindowspath': 'bool'}}
