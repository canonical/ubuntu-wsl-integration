#    ubuntuwslctl.default - storing default values
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

from ubuntuwslctl.core.util import get_ubuntu_wsl_conf_defaults

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
