#    ubuntuwslctl.tircks - tricks for quick addressing WSL issues
#    Copyright (C) 2021 Canonical Ltd.
#    Copyright (C) 2021 Patrick Wu
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
import os

class Tricks:

    def __init__(self, name):
        self.name = name

    def tricks_gh6044(self):
        """
        Tricks for https://github.com/Microsoft/WSL/issues/6044
        Prevetning the use of `nftables` on Ubuntu WSL
        """
        if os.path.exists("/etc/fstab"):
            os.mknod("/etc/fstab")
        os.system("update-alternatives --set iptables /usr/sbin/iptables-legacy")
        os.system("update-alternatives --set ip6tables /usr/sbin/ip6tables-legacy")

    def do(self):
        t_f = f"tricks_{self.name}"
        if hasattr(self, t_f) and callable(func := getattr(self, t_f)):
            func()

