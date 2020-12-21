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


class SuperHandler:
    """
    This class tries to handle everything Editor cannot handle.
    """
    def __init__(self, ubuntu, wsl, file_name, file_format):
        self.UbuntuConf = ubuntu
        self.WSLConf = wsl
        self.format = file_format
        self.name = file_name

        ubuntu_tmp = (self.UbuntuConf.get_config())._sections
        wsl_tmp = (self.WSLConf.get_config())._sections
        self.parsed_config = {"ubuntu": ubuntu_tmp, "wsl": wsl_tmp}

        ubuntu_tmp_1 = (self.UbuntuConf.get_config(is_default=True))._sections
        wsl_tmp_1 = (self.WSLConf.get_config(is_default=True))._sections
        self.parsed_default_config = {"ubuntu": ubuntu_tmp_1, "wsl": wsl_tmp_1}

    def get_config(self, is_default=False):
        return self.parsed_default_config if is_default else self.parsed_config

    def export_file(self, is_default=False):
        with open(self.name, 'w+') as f:
            if is_default:
                json.dump(self.parsed_default_config, f)
            else:
                json.dump(self.parsed_config, f)

    def import_file(self, is_default=False):
        pass












