import sys
import warnings
from argparse import ArgumentParser

from .helper import config_name_extractor, query_yes_no
from .i18n import translation
from .loader import UbuntuWSLConfigEditor, WSLConfigEditor

_ = translation.gettext


class Application:
    def __init__(self):
        self.ubuntu_conf = UbuntuWSLConfigEditor()
        self.wsl_conf = WSLConfigEditor()
        self.parser = ArgumentParser(
            description=_("ubuntuwsl is a tool for help manage your settings for Ubuntu WSL."))
        self._init_parser()
        self._args = self.parser.parse_args()
        self._args.func()

    def _init_parser(self):
        self.parser.add_argument(
            '--version', action='version', version="ubuntuwsl 0.13")
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
                "Change the value of one or more boot configuration "
                "settings. To reset the value of a setting to its "
                "default, simply omit the new value."),
            help=_("Change the state of one or more boot settings"))
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
            help=_("Change the state of one or more boot settings"))
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
            help=_("The name of the boot configuration to display")
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

    def _select_config(self, type_input):
        if type_input == "Ubuntu":
            return self.ubuntu_conf
        elif type_input == "WSL":
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
        assume_yes = 'yes' in self._args and self._args.yes
        if 'name' in self._args and self._args.name is not None:
            try:
                config_type, config_section, config_setting = config_name_extractor(self._args.name)
                if query_yes_no(_("You are trying to reset `{name}`."
                                  "Do you still want to proceed?").format(name=self._args.name),
                                default="no", assume_yes=assume_yes):
                    self._select_config(config_type) \
                        .reset(config_section, config_setting)
            except KeyError:
                print(_("ERROR: Unknown key name `{name}` passed. \n\nDetails:\n")
                          .format(name=self._args.name))
                raise
            except Exception:
                print(_("ERROR: Something happened.  \n\nDetails:\n")
                      .format(name=self._args.name))
                raise
        else:
            if query_yes_no(_("You are trying to reset all settings, "
                              "including ubuntu-wsl.conf and wsl.conf. "
                              "Do you still want to proceed?"), default="no", assume_yes=assume_yes):
                self._select_config("Ubuntu").reset_all()
                self._select_config("WSL").reset_all()

    def do_show(self):
        try:
            config_type, config_section, config_setting = config_name_extractor(self._args.name)
            self._select_config(config_type) \
                .show(config_section, config_setting, self._args.short, self._args.default)
        except KeyError:
            print(_("ERROR: Unknown key name `{name}` passed. \n\nDetails:\n")
                  .format(name=self._args.name))
            raise
        except Exception:
            print(_("ERROR: Something happened.  \n\nDetails:\n")
                  .format(name=self._args.name))
            raise

    def do_update(self):
        try:
            config_type, config_section, config_setting = config_name_extractor(self._args.name)
            self._select_config(config_type) \
                .update(config_section, config_setting, self._args.value)
        except KeyError:
            print(_("ERROR: Unknown key name `{name}` passed. \n\nDetails:\n")
                  .format(name=self._args.name))
            raise
        except Exception:
            print(_("ERROR: Something happened.  \n\nDetails:\n")
                  .format(name=self._args.name))
            raise


main = Application()
