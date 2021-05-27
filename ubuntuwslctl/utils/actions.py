#    ubuntuwslctl.actions - tricks for quick addressing WSL issues
#    Copyright (C) 2021 Canonical Ltd.
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>

import os


class Tricks:
    @staticmethod
    def __cmd_p(cmd):
        print(">>", cmd)
        os.system(cmd)

    """ BEGIN OF TRICKS """

    def tricks_gui_enhancement(self, help=False):
        if help:
            return "native GUI Improvements"
        glist = ["xclip","gnome-themes-standard","gtk2-engines-murrine","dbus","dbus-x11",
                 "mesa-utils","libqt5core5a","binutils","libnss3","libegl1-mesa", "yaru-theme-gtk", "yaru-theme-icon"]
        g_str = "apt install -y " + " ".join(glist)
        self.__cmd_p(g_str)
        self.__cmd_p("gsettings set org.gnome.desktop.interface gtk-theme 'Yaru'")
        self.__cmd_p("gsettings set org.gnome.desktop.interface icon-theme 'Yaru'")
        self.__cmd_p("gsettings set org.gnome.desktop.interface cursor-theme 'Yaru'")
        self.__cmd_p("gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'")

    tricks_gui = tricks_gui_enhancement

    def tricks_gh6044(self, help=False):
        """
        Tricks for https://github.com/Microsoft/WSL/issues/6044
        use legacy `iptables` instead of `nftables` on Ubuntu
        """
        if help:
            return "use legacy `iptables` instead of `nftables` on Ubuntu"
        self.__cmd_p("update-alternatives --verbose --set iptables /usr/sbin/iptables-legacy")
        self.__cmd_p("update-alternatives --verbose --set ip6tables /usr/sbin/ip6tables-legacy")

    tricks_nftables = tricks_native_docker = tricks_gh6044

    """ END OF TRICKS """

    def do(self, name):
        t_f = f"tricks_{name}"
        if hasattr(self, t_f) and callable(func := getattr(self, t_f)):
            func()
        else:
            print("Invalid Name: ", name)

    def list(self):
        for func in dir(self):
            if callable(cfunc := getattr(self, func)) and func.startswith("tricks_"):
                print("{}: {}".format(func[7:], cfunc(help=True)))
