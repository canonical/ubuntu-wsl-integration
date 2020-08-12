import sys
from argparse import ArgumentParser
from .loader import UbuntuWSLConfigEditor, WSLConfigEditor
from .helper import config_name_extractor, query_yes_no

class Application:

    def __init__(self):
        self.ubuntu_conf = UbuntuWSLConfigEditor()
        self.wsl_conf = WSLConfigEditor()
        self.parser = ArgumentParser(
            description="%(prog)s is a tool for help manage your settings for Ubuntu WSL.")
        self._init_parser()
        self._args = self.parser.parse_args()
        self._args.func()

    def _init_parser(self):
        self.parser.add_argument(
            '--version', action='version', version="%(prog)s 0.5")
        self.parser.set_defaults(func=self.do_help)
        commands = self.parser.add_subparsers(title=("commands"))

        help_cmd = commands.add_parser(
            "help", aliases=["?"],
            description=(
                "With no arguments, displays the list of ubuntuwslctl "
                "commands. If a command name is given, displays the "
                "description and options for the named command. "),
            help=("Displays help about the specified command"))
        help_cmd.add_argument(
            "cmd", metavar="command", nargs='?',
            help=(
                "The name of the command to output help for")
        )
        help_cmd.set_defaults(func=self.do_help)

        update_cmd = commands.add_parser(
            "update", aliases=["up"],
            description=(
                "Change the value of one or more boot configuration "
                "settings. To reset the value of a setting to its "
                "default, simply omit the new value."),
            help=("Change the state of one or more boot settings"))
        update_cmd.add_argument(
            "name",
            help=("The name of the configuration to be updated")
        )
        update_cmd.add_argument(
            "value",
            help=("The value you want to set for this configuration")
        )
        update_cmd.set_defaults(func=self.do_update)

        reset_cmd = commands.add_parser(
            "reset", aliases=["rs", "rm"],
            description=(
                "Reset(remove) the value of one configuration "
                "settings."),
            help=("Change the state of one or more boot settings"))
        reset_cmd.add_argument(
            "name",
            help=("The name of the configuration to be reset")
        )
        reset_cmd.set_defaults(func=self.do_reset)

        show_cmd = commands.add_parser(
            "show", aliases=["cat"],
            description=(
                "Display the specified stored configuration."),
            help=("Show the specified stored configuration"))
        show_cmd.add_argument(
            "name",
            help=("The name of the boot configuration to display")
        )
        show_cmd.add_argument(
            "-s", "--short", action="store_true",
            help=("When enabled, only value will be displayed."))
        show_cmd.add_argument(
            "-d", "--default", action="store_true",
            help=("Show the default configuration settings instead of current "
                  "user-defined ones."))
        show_cmd.set_defaults(func=self.do_show)

        ls_cmd = commands.add_parser(
            "list", aliases=["ls"],
            description=("List all configurations."),
            help=("List all configuration settings from ubuntu-wsl.conf and wsl.conf."))
        ls_cmd.add_argument(
            "-d", "--default", action="store_true",
            help=("Show the default configuration settings instead of current "
                  "user-defined ones."))
        ls_cmd.set_defaults(func=self.do_list)

    def _select_config(self, type_input):
        if type_input == "Ubuntu":
            return self.ubuntu_conf
        elif type_input == "WSL":
            return self.wsl_conf
        else:
            raise ValueError("Invalid config name. Please check again.")

    def do_help(self):
        if 'cmd' in self._args and self._args.cmd is not None:
            self.parser.parse_args([self._args.cmd, '-h'])
        else:
            self.parser.parse_args(['-h'])

    def do_list(self):
        self.ubuntu_conf.list(self._args.default)
        self.wsl_conf.list(self._args.default)

    def do_reset(self):
        if 'name' in self._args and self._args.name is not None:
            if query_yes_no(("You are trying to reset all settings, "
                             "including ubuntu-wsl.conf and wsl.conf. "
                             "Do you still want to proceed?"), default="no"):
                self._select_config("Ubuntu").resetall()
                self._select_config("WSL").resetall()
        else:
            try:
                config_type, config_section, config_setting = config_name_extractor(self._args.name)
                if query_yes_no(("You are trying to reset "+self._args.name+". "
                                 "Do you still want to proceed?"), default="no"):
                    self._select_config(config_type).reset(config_section, config_setting)
            except KeyError:
                print(("ERROR: Unknown keyname `{name}` passed.").format(name=self._args.name))
                sys.exit(1)

    def do_show(self):
        try:
            config_type, config_section, config_setting = config_name_extractor(self._args.name)
            self._select_config(config_type).show(config_section, config_setting, self._args.short, self._args.default)
        except KeyError:
            print(("ERROR: Unknown keyname `{name}` passed.").format(name=self._args.name))
            sys.exit(1)

    def do_update(self):
        try:
            config_type, config_section, config_setting = config_name_extractor(self._args.name)
            self._select_config(config_type).update(config_section, config_setting, self._args.value)
        except KeyError:
            print("ERROR: Unknown keyname `" + self._args.value + "` passed.")
            sys.exit(1)


main = Application()
