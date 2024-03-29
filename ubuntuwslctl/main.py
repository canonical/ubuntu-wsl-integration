#    ubuntuwslctl.main - main commandline application
#    Copyright (C) 2021 Canonical Ltd.
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>


import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from ubuntuwslctl.utils.helper import config_name_extractor, query_yes_no, \
    bcolors
from ubuntuwslctl.utils.i18n import translation
from ubuntuwslctl.core.handler import SuperHandler

_ = translation.gettext


class Application:
    def __init__(self):
        self.handler = SuperHandler()
        self.parser = ArgumentParser(
            formatter_class=RawTextHelpFormatter,
            description=_("ubuntuwsl is a tool for help manage your settings"
                          " for Ubuntu WSL."),
            epilog=_("Note: \"Super Experimental\" means it is WIP and not"
                     " working. \"Experimental\" means it is WIP but most "
                     "of the part is working."))
        self._init_parser()
        self._args = self.parser.parse_args()

    def run(self):
        try:
            self._args.func()
        except KeyError:
            print(bcolors.FAIL + _("KeyError: ") + bcolors.ENDC +
                  _("Unknown key name `{name}` passed. Aborting.")
                  .format(name=self._args.name))
            sys.exit(1)
        except AssertionError as e:
            print(bcolors.FAIL + _("ValidationError: ") + bcolors.ENDC +
                  _("{error}. Aborting.").format(error=e))
            sys.exit(1)
        except IOError:
            print(bcolors.FAIL + _("IOError: ") + bcolors.ENDC +
                  _("There is an error whe trying to read/write the conf file."
                    " You need to have root privileges to perform such action."
                    " Aborting."))
            sys.exit(1)
        except Exception:
            print(bcolors.FAIL + _("ERROR:") + bcolors.ENDC +
                  _("Something happened during the execution. Following are "
                  "the details:"))
            raise
            sys.exit(1)

    def _init_parser(self):
        self.parser.add_argument(
            '--version', action='version', version="ubuntuwsl 0.31.3")
        self.parser.set_defaults(func=self.do_help)
        self.parser.add_argument(
            "-y", "--yes", action="store_true",
            help=_("When passed, always assume yes."), required=False)
        # self.parser.add_argument(
        #     "-c", "--config", type=str, choices=["ubuntu", "wsl", "both"],
        #     default="both",
        #     help=_("When passed, handling ubuntu-wsl.conf only."),
        #     required=False)
        commands = self.parser.add_subparsers(title=_("commands"))

        help_cmd = commands.add_parser(
            "help", aliases=["?"],
            description=_(
                "With no arguments, displays the list of ubuntuwslctl "
                "commands. If a command name is given, displays the "
                "description and options for the named command. "),
            help=_("Displays help about the specified command"))
        help_cmd.add_argument(
            "cmd", metavar="command", nargs='?',
            help=("The name of the command to output help for")
        )
        help_cmd.set_defaults(func=self.do_help)

        update_cmd = commands.add_parser(
            "update", aliases=["up"],
            description=_(
                "Change the value of a WSL or Ubuntu configuration "
                "settings. "),
            help=_("Change the state of a specific setting"))
        update_cmd.add_argument(
            "name",
            help=_("The name of the configuration to be updated")
        )
        update_cmd.add_argument(
            "value",
            help=_("The value you want to set for this configuration")
        )
        update_cmd.set_defaults(func=self.do_update)

        reset_cmd = commands.add_parser(
            "reset", aliases=["rs", "rm"],
            description=_(
                "Reset(remove) the value of one configuration "
                "settings."),
            help=_("Reset(remove) the value of a specific setting")
        )
        reset_cmd.add_argument(
            "name",
            nargs="?",
            help=_("The name of the configuration to be reset")
        )
        reset_cmd.set_defaults(func=self.do_reset)

        show_cmd = commands.add_parser(
            "show", aliases=["cat"],
            description=_(
                "Display the specified stored configuration."),
            help=_("Show the specified stored configuration"))
        show_cmd.add_argument(
            "name",
            help=_("The name of the configurations")
        )
        show_cmd.add_argument(
            "-s", "--short", action="store_true",
            help=_("When enabled, only value will be displayed."))
        show_cmd.add_argument(
            "-d", "--default", action="store_true",
            help=_("Show the default configuration settings instead of current"
                   " user-defined ones."))
        show_cmd.set_defaults(func=self.do_show)

        ls_cmd = commands.add_parser(
            "list", aliases=["ls"],
            description=_("List all configurations."),
            help=_("List all configuration settings from ubuntu-wsl.conf and"
                   " wsl.conf."))
        ls_cmd.add_argument(
            "-d", "--default", action="store_true",
            help=_("Show the default configuration settings instead of current"
                   " user-defined ones."))
        ls_cmd.set_defaults(func=self.do_list)

        ui_cmd = commands.add_parser(
            "visual", aliases=["ui", "tui"],
            description=_("Display a friendly text-based user interface."
                          " (Experimental)"),
            help=_("Display a friendly text-based user interface."
                   " (Experimental)"))
        ui_cmd.set_defaults(func=self.do_ui)

        export_cmd = commands.add_parser(
            "export", aliases=["out"],
            description=_("Export the settings (Experimental)"),
            help=_("Export settings as a json string (Experimental)"))
        export_cmd.add_argument(
            "file", nargs="?", default="",
            help=_("the name of the file to export."))
        export_cmd.set_defaults(func=self.do_export)

        import_cmd = commands.add_parser(
            "import", aliases=["in"],
            description=_("Import settings (Experimental)"),
            help=_("Import settings from a json file (Experimental)"))
        import_cmd.add_argument(
            "file",
            help=_("the name of the file to export."))
        import_cmd.set_defaults(func=self.do_import)

        tricks_cmd = commands.add_parser(
            "tricks",
            description=_("Trigger Tricks/workarounds (Super Experimental)"),
            help=_("Tricks/workarounds on some issues we are unable to include"
                   " in images. (Super Experimental)"))
        tricks_cmd.add_argument(
            "name", nargs="?", default="",
            help=_("the name of the tricks/workarounds."))
        tricks_cmd.add_argument(
            "-l", "--list", action="store_true",
            help=_("Show the possible tricka."))
        tricks_cmd.set_defaults(func=self.do_tricks)

        fun_cmd = commands.add_parser("fun")
        fun_cmd.set_defaults(func=self.do_fun)

    def do_help(self):
        if 'cmd' in self._args and self._args.cmd is not None:
            self.parser.parse_args([self._args.cmd, '-h'])
        else:
            self.parser.parse_args(['-h'])

    def do_list(self):
        self.handler.list_all(self._args.default)

    def do_reset(self):
        print(bcolors.WARNING + _("WARNING: ") + bcolors.ENDC +
              _("you need to restart Ubuntu distribution to take effect."))
        assume_yes = 'yes' in self._args and self._args.yes
        if 'name' in self._args and self._args.name is not None:
            config_type, config_section, config_setting = config_name_extractor(
                self._args.name)
            if query_yes_no(_("You are trying to reset `{name}`."
                              "Do you still want to proceed?")
                            .format(name=self._args.name),
                            default="no", assume_yes=assume_yes):
                self.handler.reset(config_type, config_section, config_setting)
        else:
            if query_yes_no(_("You are trying to reset all settings, "
                              "including ubuntu-wsl.conf and wsl.conf. "
                              "Do you still want to proceed?"), default="no", assume_yes=assume_yes):
                self.handler.reset_all()

    def do_show(self):
        config_type, config_section, config_setting = config_name_extractor(
            self._args.name)
        self.handler.show(config_type, config_section,
                          config_setting, self._args.short, self._args.default)

    def do_update(self):
        print(bcolors.WARNING + _("WARNING: ") + bcolors.ENDC +
              _("you need to restart Ubuntu distribution to take effect."))
        config_type, config_section, config_setting = config_name_extractor(
            self._args.name)
        self.handler.update(config_type, config_section, config_setting,
                            self._args.value)

    def do_ui(self):
        from ubuntuwslctl.tui import Tui
        Tui(self.handler).run()

    def do_export(self):
        self.handler.export_file(self._args.file)

    def do_import(self):
        self.handler.import_file(self._args.file)

    def do_tricks(self):
        from ubuntuwslctl.utils.actions import Tricks
        tricks = Tricks()
        if self._args.list:
            tricks.list()
        else:
            tricks.do(self._args.name)

    @staticmethod
    def do_fun():
        # OwO no touchy
        import base64
        fun = b'44CA44CA44CA4oinX+KIpyAgICAgICAgZnVuPwrjgIDjgIAgKOOAgO+9pc+' \
              b'J772lKSAK44CAIO+8v3zjgIDiioPvvI8o77y/77y' \
              b'/XyAgCu+8j+OAgOKUlC0o77y/77y/77y/X++8jyAK77+j77+j77+j77+j77+' \
              b'j77+j77+jCiAgICAgICAgICAgICAgc2xlZXAgaXMgZnVuCuOAgO+8nOKMku+' \
              b'8j+ODvS3vvaRf77y/XwrvvI/vvJxfL++8v++8v++8v++8v' \
              b'++8jwrvv6Pvv6Pvv6Pvv6Pvv6Pvv6Pvv6M='
        print(base64.b64decode(fun).decode("utf-8"))


def main():
    main_app = Application()
    main_app.run()


if __name__ == '__main__':
    sys.exit(main())
