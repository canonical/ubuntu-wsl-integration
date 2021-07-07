#    ubuntuwslctl.core.handler - core handler for all config
#    Copyright (C) 2021 Canonical Ltd.
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>

import json
import time

from ubuntuwslctl.core.editor import UbuntuWSLConfigEditor, WSLConfigEditor


class SuperHandler:
    """
    The Core Handler.
    """

    def __init__(self, dry_run):
        self.ubuntu_conf = UbuntuWSLConfigEditor(dry_run)
        self.wsl_conf = WSLConfigEditor(dry_run)

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

    def validate(self, config_type, section, config, value):
        return self._select_config(config_type).type_validation(section, config, value)

    def update(self, config_type, section, config, value):
        self._select_config(config_type).update(section, config, value)

    def show(self, config_type, section, config, is_short, is_default):
        if section == "*":  # top level wild card display
            self._select_config(config_type).list(is_short, is_default)
        elif config == "*": # second level wild card display
            self._select_config(config_type).show_list(section, is_short, is_default)
        else:
            self._select_config(config_type).show(section, config, is_short, is_default)

    def reset(self, config_type, section, config):
        self._select_config(config_type).reset(section, config)

    def reset_all(self):
        self.ubuntu_conf.reset_all()
        self.wsl_conf.reset_all()

    def list_all(self, default):
        self.ubuntu_conf.list(is_default=default)
        self.wsl_conf.list(is_default=default)

    def export_file(self, name):
        t = time.gmtime(time.time())
        ts = "{}{:02d}{:02d}{:02d}{:02d}{:02d}UTC".format(t[0], t[1], t[2], t[3], t[4], t[5])
        self.parsed_config['time_exported'] = ts
        if name == "":
            name = "exported_settings_{}.json".format(ts)
        with open(name, 'w+') as f:
            json.dump(self.parsed_config, f)

        del self.parsed_config['time_exported']
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
