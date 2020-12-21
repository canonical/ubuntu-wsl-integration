#    ubuntuwslctl.main - main commandline application
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

import sys
from argparse import ArgumentParser, RawTextHelpFormatter

from ubuntuwslctl.utils.helper import config_name_extractor, query_yes_no, bcolors
from ubuntuwslctl.utils.i18n import translation
from ubuntuwslctl.core.editor import UbuntuWSLConfigEditor, WSLConfigEditor

_ = translation.gettext


class Application:
    def __init__(self):
        self.ubuntu_conf = UbuntuWSLConfigEditor()
        self.wsl_conf = WSLConfigEditor()
        self.parser = ArgumentParser(
            formatter_class=RawTextHelpFormatter,
            description=_("ubuntuwsl is a tool for help manage your settings for Ubuntu WSL."),
            epilog=_("Note: \"Super Experimental\" means it is WIP and not working. "
                     "\"Experimental\" means it is WIP but most of the part is working."
                     "\n\nThis cli has the ability to make a joke."))
        self._init_parser()
        self._args = self.parser.parse_args()

    def run(self):
        try:
            self._args.func()
        except KeyError:
            print(bcolors.FAIL + _("KeyError: ") + bcolors.ENDC +
                  _("Unknown key name `{name}` passed. Aborting.").format(name=self._args.name))
            sys.exit(1)
        except AssertionError as e:
            print(bcolors.FAIL + _("ValidationError: ") + bcolors.ENDC +
                  _("{error}. Aborting.").format(error=e))
            sys.exit(1)
        except IOError:
            print(bcolors.FAIL + _("IOError: ") + bcolors.ENDC +
                  _("There is an error whe trying to read/write the conf file. "
                    "You need to have root privileges to perform such action. Aborting."))
            sys.exit(1)
        except Exception:
            print(bcolors.FAIL + _("ERROR:") + bcolors.ENDC +
                  _("Something happened during the execution. Following are the details:").format(name=self._args.name))
            raise
            sys.exit(1)

    def _init_parser(self):
        self.parser.add_argument(
            '--version', action='version', version="ubuntuwsl 0.20.1")
        self.parser.set_defaults(func=self.do_help)
        self.parser.add_argument(
            "-y", "--yes", action="store_true",
            help=_("When passed, always assume yes."), required=False)
        # self.parser.add_argument(
        #     "-c", "--config", type=str, choices=["ubuntu", "wsl", "both"], default="both",
        #     help=_("When passed, handling ubuntu-wsl.conf only."), required=False)
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
            help=(
                "The name of the command to output help for")
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
            help=_("Show the default configuration settings instead of current "
                   "user-defined ones."))
        show_cmd.set_defaults(func=self.do_show)

        ls_cmd = commands.add_parser(
            "list", aliases=["ls"],
            description=_("List all configurations."),
            help=_("List all configuration settings from ubuntu-wsl.conf and wsl.conf."))
        ls_cmd.add_argument(
            "-d", "--default", action="store_true",
            help=_("Show the default configuration settings instead of current "
                   "user-defined ones."))
        ls_cmd.set_defaults(func=self.do_list)

        ui_cmd = commands.add_parser(
            "visual", aliases=["ui", "tui"],
            description=_("Display a friendly text-based user interface. (Super Experimental)"),
            help=_("Display a WIP friendly text-based user interface. (Super Experimental)"))
        ui_cmd.set_defaults(func=self.do_ui)

        export_cmd = commands.add_parser(
            "export", aliases=["out"],
            description=_("Export the settings (Super Experimental)"),
            help=_("Export settings as a json string (Super Experimental)"))
        export_cmd.add_argument(
            "file",
            help=_("the name of the file to export."))
        export_cmd.set_defaults(func=self.do_export)

        import_cmd = commands.add_parser(
            "import", aliases=["in"],
            description=_("Import settings (Super Experimental)"),
            help=_("Import settings from a json file (Super Experimental)"))
        import_cmd.set_defaults(func=self.do_import)

        joke_cmd = commands.add_parser("joke")
        joke_cmd.set_defaults(func=self.do_joke)

    def _select_config(self, type_input):
        type_input = type_input.lower()
        if type_input == "ubuntu":
            return self.ubuntu_conf
        elif type_input == "wsl":
            return self.wsl_conf
        else:
            raise ValueError(_("Invalid config name. Please check again."))

    def do_help(self):
        if 'cmd' in self._args and self._args.cmd is not None:
            self.parser.parse_args([self._args.cmd, '-h'])
        else:
            self.parser.parse_args(['-h'])

    def do_list(self):
        self.ubuntu_conf.list(self._args.default)
        self.wsl_conf.list(self._args.default)

    def do_reset(self):
        print(bcolors.WARNING + _("WARNING: ") + bcolors.ENDC +
              _("you need to restart Ubuntu distribution to take effect."))
        assume_yes = 'yes' in self._args and self._args.yes
        if 'name' in self._args and self._args.name is not None:
            config_type, config_section, config_setting = config_name_extractor(self._args.name)
            if query_yes_no(_("You are trying to reset `{name}`."
                              "Do you still want to proceed?").format(name=self._args.name),
                            default="no", assume_yes=assume_yes):
                self._select_config(config_type) \
                    .reset(config_section, config_setting)
        else:
            if query_yes_no(_("You are trying to reset all settings, "
                              "including ubuntu-wsl.conf and wsl.conf. "
                              "Do you still want to proceed?"), default="no", assume_yes=assume_yes):
                self._select_config("Ubuntu").reset_all()
                self._select_config("WSL").reset_all()

    def do_show(self):
        config_type, config_section, config_setting = config_name_extractor(self._args.name)
        if config_section == "*":  # top level wild card display
            self._select_config(config_type).list(self._args.default, is_short=self._args.short)
        elif config_setting == "*": # second level wild card display
            self._select_config(config_type).show_list(config_section, self._args.short, self._args.default)
        else:
            self._select_config(config_type) \
                .show(config_section, config_setting, self._args.short, self._args.default)

    def do_update(self):
        print(bcolors.WARNING + _("WARNING: ") + bcolors.ENDC +
              _("you need to restart Ubuntu distribution to take effect."))
        config_type, config_section, config_setting = config_name_extractor(self._args.name)
        self._select_config(config_type) \
            .update(config_section, config_setting, self._args.value)

    def do_ui(self):
        from ubuntuwslctl.tui import tui_main
        tui_main(self.ubuntu_conf, self.wsl_conf)

    def do_export(self):
        from ubuntuwslctl.core.generator import SuperHandler
        SuperHandler(self.ubuntu_conf, self.wsl_conf, self._args.file, 'json').export_file()

    def do_import(self):
        pass

    def do_joke(self):
        import base64
        joke = b'CuKghOKghOKghOKghOKghOKghOKghOKghOKghOKiuOKjhOKjr+Kiv+Khn+KggeKjgOKgtOKgiOKggeKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKgiOKgsuKjhOKghOKiv+Kjv+KhpuKghOKjgOKghOKghOKghOKghArioITioITioITioITioITioITioITioITioITioITio7/io7/io6/io6TioJ7ioIHioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioIjioLvio67io7/io7/io7vioKXioKTioITioITioIQK4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qC44qO/4qGf4qCb4qCB4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCI4qC74qO/4qOe4qKm4qCE4qCE4qCE4qCECuKghOKghOKghOKghOKghOKghOKihOKjgOKjgOKjtOKjv+Kjv+KghuKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKgmOKjv+KhhOKggeKghOKghOKghArioITioITioITioITioITioITioITioLniopvio7/io7/ioIbioITioITioITioITiorDio6Tio6TiooDio4DioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioKDior/ioYfioITioITioITioIQK4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qG84qK74qO/4qO+4qCE4qCE4qCE4qKA4qO84qO/4qO/4qOn4qGf4qCB4qGA4qKA4qGi4qKk4qO24qOO4qOA4qGA4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qO84qCB4qCE4qCE4qCE4qCECuKghOKghOKghOKghOKghOKghOKghOKghOKghOKguOKjn+Kjv+KghOKghOKigeKjpuKjgOKgiOKgu+KjvuKjtOKjv+Kjn+KjvOKjt+KjpuKjveKjv+Kjv+Kjv+Kjt+KghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKigOKggeKigOKhoOKghOKghOKghArioITioITioITioITioITioITioITioITioITiooDio7HioZnioITioITioITiooXioLbioojio7bio7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/io7/ioITioITioITioITioITioITioITioITioITioITioITioITioYvioIHioITioITioITioIQK4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCI4qCJ4qCB4qCH4qCE4qCE4qCE4qK44qO/4qO/4qO/4qG/4qC/4qC/4qC/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCb4qKG4qCE4qCE4qCE4qCECuKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKiv+Kjv+Kjt+KjpuKhgOKjoOKjv+Kjv+Kjv+Kjv+Kjv+Kgn+KjveKjv+Khn+KghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKgoOKghOKghOKghOKghOKghOKghArioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioIjior/io7/io7/io7/io7/iob3ioLfioJvioJvioIvioqDio7/io7/ioYfioITioITioITioITioITioITioITioITioITioITioITioITiooHioYDio4DioITioITioIQK4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCI4qC74qO/4qO/4qOm4qKA4qOk4qO24qG24qO24qO84qO/4qO/4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCi4qGA4qCE4qCE4qCECuKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKgiOKiv+Kjv+KjluKjv+Kjn+Kjv+Kjv+Kjv+Kjv+Kgh+KghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKgiOKgu+KjpuKghOKghArioITioITioITio6Dio6Tio7bio7bioYDioITioITioITioITioITioITioITioITioITioITioITioITioITioJnio7/io63io4nio4nio7Tio7/iob/ioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioJHioIQK4qCE4qCE4qOA4qO/4qO/4qG/4qCL4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCY4qC/4qC/4qC/4qCb4qCB4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCD4qCE4qCECuKigOKjvuKjv+Kjv+Kgi+KghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKhgOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKhhuKghOKghArio7/io7fioJ/ioIHioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioJjio6TioYDioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioIQK4qGu4qCB4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qOP4qG34qKA4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCECuKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKjgOKjvOKjv+Kjt+Kjv+KjpeKhhOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghArioITioITioITioITioITioITioITioITioITioITio4Dio6Dio6Tio7bio7bio77io7/io7/io7/io7/io7/io7/io7/io7/io7fio6DioYDioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioITioIQK4qCE4qCE4qCE4qCE4qCE4qOA4qOk4qO04qO24qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qO/4qG74qOc4qO34qO94qO34qO/4qOm4qGA4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCE4qCECuKghOKghOKghOKjoOKjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kin+Kjr+KjvuKjv+Kjv+Kjv+Kjv+Kjv+Kjv+Kjv+KjpuKhgOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghOKghAouLllvdSBhcmUgZXhwZWN0aW5nIGEgam9rZSwgYnV0IGl0IHdhcyBtZSwgRGlvIS4uCg=='

        print(base64.b64decode(joke).decode("utf-8"))


def main():
    main_app = Application()
    main_app.run()


if __name__ == '__main__':
    sys.exit(main())
