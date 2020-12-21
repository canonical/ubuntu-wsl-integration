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

class FileHandler:

    def __init__(self, ubuntu, wsl, file_format, action):
        self.UbuntuConf = ubuntu
        self.WSLConf = wsl
        self.format = file_format
        self.action = action
        self.parsed_config = {}
        self.parsed_default_config = {}

        self._init_config()

    def _init_config(self):
        ubuntu_tmp = (self.UbuntuConf.get_config())._sections
        wsl_tmp = (self.WSLConf.get_config())._sections
        self.parsed_config = {"ubuntu": ubuntu_tmp, "wsl": wsl_tmp}

        ubuntu_tmp_1 = (self.UbuntuConf.get_config(is_default=True))._sections
        wsl_tmp_1 = (self.WSLConf.get_config(is_default=True))._sections
        self.parsed_default_config = {"ubuntu": ubuntu_tmp_1, "wsl": wsl_tmp_1}
        print(self.parsed_config)
        print(self.parsed_default_config)







