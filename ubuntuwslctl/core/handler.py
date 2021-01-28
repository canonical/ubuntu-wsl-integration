#     ubuntuwslctl.core.generator
#     Copyright (C) 2020 Canonical Ltd.
#                   2020 Patrick Wu <patrick.wu@canonical.com>
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
import json
import time

from ubuntuwslctl.core.editor import UbuntuWSLConfigEditor, WSLConfigEditor


class SuperHandler:
    """
    The Core Handler.
    """

    def __init__(self):
        self.ubuntu_conf = UbuntuWSLConfigEditor()
        self.wsl_conf = WSLConfigEditor()

        ubuntu_tmp = (self.ubuntu_conf.get_config())._sections
        wsl_tmp = (self.wsl_conf.get_config())._sections
        self.parsed_config = {"ubuntu": ubuntu_tmp, "wsl": wsl_tmp}

    def _select_config(self, type_input):
        type_input = type_input.lower()
        if type_input == "ubuntu":
            return self.ubuntu_conf
        elif type_input == "wsl":
            return self.wsl_conf
        else:
            raise ValueError("Invalid config name. Please check again.")

    def get_config(self):
        return self.parsed_config

    def update(self, config_type, section, config, value):
        self._select_config(config_type).update(section, config, value)

    def reset(self, config_type, section, config):
        self._select_config(config_type).reset(section, config)

    def reset_all(self):
        self.ubuntu_conf.reset_all()
        self.wsl_conf.reset_all()

    def list_all(self, default):
        self.ubuntu_conf.list(default)
        self.wsl_conf.list(default)

    def export_file(self, name):
        t = time.gmtime(time.time())
        ts = "{}{:02d}{:02d}{:02d}{:02d}{:02d}UTC".format(t[0], t[1], t[2], t[3], t[4], t[5])
        self.parsed_config['time_exported'] = ts
        if name == "":
            name = "exported_settings_{}.json".format(ts)
        with open(name, 'w+') as f:
            json.dump(self.parsed_config, f)

        return name

    def import_file(self, name):
        with open(name, 'r+') as f:
            file = json.load(f)
            for i in ("ubuntu", "wsl"):
                conf_to_read = file[i]
                for j in conf_to_read.keys():
                    j_tmp = conf_to_read[j]
                    for k in j_tmp.keys():
                        self.update(i, j, k, j_tmp[k])
