#    ubuntuwslctl.default - storing default values
#    Copyright (C) 2021 Canonical Ltd.
#
#    Authors: Patrick Wu <patrick.wu@canonical.com>

## Tooltip and Name definition ##

conf_def = {
    'wsl': {
        '_friendly_name': 'WSL Settings',
        '_file_location': '/etc/wsl.conf',
        'automount': {
            '_friendly_name': 'Auto-Mount',
            'enabled': {
                '_friendly_name': 'Enabled',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether the Auto-Mount freature is enabled. This feature allows you to mount Windows drive in WSL.'
            },
            'mountfstab': {
                '_friendly_name': 'Mount `/etc/fstab`',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether `/etc/fstab` will be mounted. The configuration file `/etc/fstab` contains the necessary '
                       'information to automate the process of mounting partitions. '
            },
            'root': {
                '_friendly_name': 'Auto-Mount Location',
                'default': '/mnt/',
                'type': 'path',
                'tip': 'This is the location where the Windows Drive will be auto-mounting to. It is `/mnt/` by default.'
            },
            'options': {
                '_friendly_name': 'Auto-Mount Option',
                'default': '',
                'type': 'mount',
                'tip': 'This is the options you want to pass when the Windows Drive  auto-mounting. Please refer to '
                       '<https://docs.microsoft.com/en-us/windows/wsl/wsl-config#mount-options> For the detailed input.'
            },
        },
        'network': {
            '_friendly_name': 'Network',
            'generatehosts': {
                '_friendly_name': 'Generate /etc/hosts',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether generate /etc/hosts at each startup.'
            },
            'generateresolvconf': {
                '_friendly_name': 'Generate /etc/resolv.conf',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether generate /etc/resolv.conf at each startup.'
            },
        },
        'interop': {
            '_friendly_name': 'Interoperability',
            'enabled': {
                '_friendly_name': 'Enabled',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether the interoperability is enabled.'
            },
            'appendwindowspath': {
                '_friendly_name': 'Append Windows Path',
                'default': 'true',
                'type': 'bool',
                'tip': 'Whether Windows Path will be append in the PATH environment variable in WSL.'
            },
        }
    },
    'ubuntu': {
        '_friendly_name': 'Ubuntu Settings',
        '_file_location': '/etc/ubuntu-wsl.conf',
        'GUI': {
            '_friendly_name': 'GUI (WSLg)',
            'theme': {
                '_friendly_name': 'GUI Theme',
                'default': 'default',
                'type': 'theme',
                'tip': 'This option changes the Ubuntu theme. You can choose from `default`, `dark` or `light`. By '
                       'default it is `default`. '
            },
            'followwintheme': {
                '_friendly_name': 'Follow Windows Theme',
                'default': 'false',
                'type': 'bool',
                'tip': 'This option manages whether the Ubuntu theme follows the WSindows theme; that is, when Windows '
                       'uses dark theme, Ubuntu also uses dark theme. Requires WSL interoperability enabled. '
            }
        },
        'Interop': {
            '_friendly_name': 'Interoperability',
            'guiintegration': {
                '_friendly_name': 'Legacy GUI Integration',
                'default': 'false',
                'type': 'bool',
                'tip': 'This option enables the Legacy GUI Integration on Windows 10. Requires a Third-party X Server.'
            },
            'audiointegration': {
                '_friendly_name': 'Legacy Audio Integration',
                'default': 'false',
                'type': 'bool',
                'tip': 'This option enables the Legacy Audio Integration on Windows 10. Requires PulseAudio for '
                       'Windows Installed. '
            },
            'advancedipdetection': {
                '_friendly_name': 'Advanced IP Detection',
                'default': 'false',
                'type': 'bool',
                'tip': 'This option enables advanced detection of IP by Windows IPv4 Address which is more reliable to '
                       'use with WSL2. Requires WSL interoperability enabled. '
            },
        },
        'Motd': {
            '_friendly_name': 'Message Of The Day (MOTD)',
            'wslnewsenabled': {
                '_friendly_name': 'WSL News',
                'default': 'true',
                'type': 'bool',
                'tip': 'This options allows you to control your MOTD News. Toggling it on allows you to see the MOTD.'
            },
        }
    }
}
