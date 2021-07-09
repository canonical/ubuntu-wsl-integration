# Contributing

## Setup

1. install the dependency:
```
# apt install -y debhelper \
dh-python \
python3 \
python3-autopep8 \
python3-flake8 \
python3-urwid \
python3-distutils \
python3-setuptools \
gettext
```
2. clone the repository:
```
$ git clone https://github.com/canonical/ubuntu-wsl-integration
```

3. Executing local development code:

Under the root folder, you can execute the command using the following:
```
PYTHONPATH=$(pwd) python3 -m ubuntuwslctl.main --dev-mode <command>
```

## Style & Linting

This Project uses **PEP8** style.
`flake8` and `autopep8` are used to perform linting and auto linting correspondingly. No additional rules are currently required.

### `default.json`

`default.json` is the file that store the definitions for `ubuntu-wsl.conf` and `wsl.conf` for both `ubuntu-wsl-oobe` and `ubuntu-wsl-integration`.

It should be generally looks like the following:

```json
{
    "wsl": { // file level
        "_friendly_name": "WSL Settings", 
        "_file_location": "/etc/wsl.conf",
        "automount": { // config section level
            "_friendly_name": "Auto-Mount",
            "enabled": { //config item level
                "_friendly_name": "Enabled",
                "_api_name": "automount",
                "default": "true",
                "type": "bool",
                "tip": "Whether the Auto-Mount freature is enabled. This feature allows you to mount Windows drive in WSL."
            },
            ...
```

File level is the configuration file general definitions like `wsl` and `ubuntu`. It consists of `_friendly_name` (The friendly name for the configuration),  `_file_location` (the configuration file location) and all the config section level definitions.

Config section level is the config section definitions inside of a certain configuration file. It consists of `_friendly_name` (The friendly name for the configuration section) and all the config item level definitions.

Config item level is the config section definitions inside of a config section. It consists of `_friendly_name` (The friendly name for the configuration section), `_api_name` (The name that is used in Ubuntu WSL OOBE experience for API Access), `default` (The default value for the item), `type` (The default type of the item), and `tip` (The small piece of guide that is being used in the tui/gui tooltip)