# Ubuntu WSL Integration

This is Ubuntu WSL Integration (`ubuntu-wsl-integration`) for use with independently or with Ubuntu WSL Onboarding Experience (`ubuntu-wsl-oobe`).

This is proposed to ship with Ubuntu WSL metapackage in 20.10 under Ubuntu WSL meta-package (`ubuntu-wsl`).

This contains:

- Ubuntu WSL Integration script that can be used during startup or with `wslusc` utility in `wslu`;
- A cli for managing the integration.
- A Text-based UI for easier integration menagement.

## Usage


-y, --yes             When passed, always assume yes.
    update (up)         Change the state of a specific setting
    reset (rs, rm)      Reset(remove) the value of a specific setting
    show (cat)          Show the specified stored configuration
    list (ls)           List all configuration settings from ubuntu-wsl.conf and wsl.conf.
    visual (ui, tui)    Display a friendly text-based user interface. (Experimental)
    export (out)        Export settings as a json string (Experimental)
    import (in)         Import settings from a json file (Experimental)
    tricks              Tricks/workarounds on some issues we are unable to include in images. (Super Experimental)

## Bugs

Please report bugs to launchpad here: <https://bugs.launchpad.net/ubuntu-wsl-integration>

## License

GPLv3

