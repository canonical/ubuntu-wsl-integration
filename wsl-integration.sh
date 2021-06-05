#!/bin/bash

set -eu

CUR_CONF_LOC=/etc/default/ubuntu-wsl/ubuntu-wsl.conf
[ -f "/etc/ubuntu-wsl.conf" ] && CUR_CONF_LOC=/etc/ubuntu-wsl.conf

__ubuntu_wsl_conf_handling() {
    section=""
    while IFS='=' read var val
    do
        if [[ $var =~ ^\;.*$ ]] || [[ $var =~ ^\#.*$ ]]
        then
            continue
        elif [[ $var =~ ^\[.*\]$ ]]
        then
            section="$(echo $var | tr -d '\[\]' | tr '[:lower:]' '[:upper:]')"
        elif [[ -n "$val" ]]
        then
            var="$(echo $var | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')"
            val="$(echo $val | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')"
            declare -r -g UBUNTU_WSL_${section}_${var}=${val}
        fi
    done < $CUR_CONF_LOC
}

__ubuntu_wsl_sane_variables() {
    VARIABLE=UBUNTU_WSL_$1
    if [ ! -v ${VARIABLE} ]; then
        echo "UBUNTU_WSL_${1} is not set, check /etc/ubuntu-wsl.conf for updates"
        declare -r -g UBUNTU_WSL_${1}=${2}
    fi
}

[ -f "$CUR_CONF_LOC" ] && __ubuntu_wsl_conf_handling
unset CUR_CONF_LOC

# check UBUNTU_WSL_ variables
# if not set, set default ones
__ubuntu_wsl_sane_variables "GUI_FOLLOWWINTHEME" "false"
__ubuntu_wsl_sane_variables "GUI_THEME" "default"
__ubuntu_wsl_sane_variables "INTEROP_GUIINTEGRATION" "false"
__ubuntu_wsl_sane_variables "INTEROP_AUDIOINTEGRATION" "false"
__ubuntu_wsl_sane_variables "INTEROP_ADVANCEDIPDETECTION" "false"
__ubuntu_wsl_sane_variables "MOTD_WSLNEWSENABLED" "true"

if [ "$WAYLAND_DISPLAY" = "wayland-0" ]; then
    if type gsettings > /dev/null 2>&1; then
        if [ "$UBUNTU_WSL_GUI_FOLLOWWINTHEME" = "true" ]; then
            TMP_THEME=$(wslsys -t -s)
            gsettings set org.gnome.desktop.interface gtk-theme "Yaru-$TMP_THEME"
        elif [ "$UBUNTU_WSL_GUI_THEME" = "default" ]; then
          gsettings set org.gnome.desktop.interface gtk-theme "Yaru"
        else
          gsettings set org.gnome.desktop.interface gtk-theme "Yaru-$UBUNTU_WSL_GUI_THEME"
        fi
    fi
# the... like, the real detection part
elif [ "$UBUNTU_WSL_INTEROP_GUIINTEGRATION" = "true" ] || [ "$UBUNTU_WSL_INTEROP_AUDIOINTEGRATION" = "true" ]; then
    if type pactl > /dev/null 2>&1 || type xvinfo > /dev/null 2>&1; then
        # detect WSL host
        # WSL2
        if [ "$(wslsys -V -s)" = "2" ]; then
            if [ "$UBUNTU_WSL_INTEROP_ADVANCEDIPDETECTION" = "true" ] && grep enabled /proc/sys/fs/binfmt_misc/WSLInterop >/dev/null; then
                WSL_HOST_LINE="$(powershell.exe -noprofile -noninteractive -Command Get-WmiObject -class win32_NetworkAdapterConfiguration | grep -n -m 1 "DefaultIPGateway.*: {[0-9a-z]" | cut -d : -f 1)"
                WSL_HOST="$(powershell.exe -noprofile -noninteractive -Command Get-WmiObject -class win32_NetworkAdapterConfiguration | sed $(( WSL_HOST_LINE - 2 ))','$(( WSL_HOST_LINE + 4 ))'!d' | grep IPAddress | grep -E -o "([0-9]{1,3}[\.]){3}[0-9]{1,3}" | head -1)"
                unset WSL_HOST_LINE
                WSL_HOST_X_TIMEOUT=0.2
                WSL_HOST_PA_TIMEOUT=0.3
            else
                WSL_HOST="$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null)"
                WSL_HOST_X_TIMEOUT=0.2
                WSL_HOST_PA_TIMEOUT=0.3
            fi
        # WSL1
        else
            WSL_HOST="${WSL_HOST:-localhost}"
            WSL_HOST_X_TIMEOUT=0.6
            WSL_HOST_PA_TIMEOUT=0.8
        fi

        # set DISPLAY if there is an X11 server running and integration is enabled
        if [ "$UBUNTU_WSL_INTEROP_GUIINTEGRATION" = "true" ] && type xvinfo > /dev/null 2>&1 && env DISPLAY="${WSL_HOST}:0" timeout "$WSL_HOST_X_TIMEOUT" xvinfo > /dev/null 2>&1; then
            export DISPLAY="${WSL_HOST}:0"
            export LIBGL_ALWAYS_INDIRECT=1
            win_sys_scaling=$(wslsys -S -s)
            export GDK_SCALE=$win_sys_scaling
            export QT_SCALE_FACTOR=$win_sys_scaling
        fi
        
        # set up audio if pulse server is reachable only via tcp
        if [ "$UBUNTU_WSL_INTEROP_AUDIOINTEGRATION" = "true" ] && type pactl > /dev/null 2>&1 \
        && (! timeout "$WSL_HOST_PA_TIMEOUT" pactl info > /dev/null 2>&1 || timeout "$WSL_HOST_PA_TIMEOUT" pactl info 2> /dev/null | grep -q 'Default Sink: auto_null' ) \
        && env PULSE_SERVER="tcp:${WSL_HOST}" timeout "$WSL_HOST_PA_TIMEOUT" pactl stat > /dev/null 2>&1; then
            export PULSE_SERVER="tcp:${WSL_HOST}"
        fi
        
        unset WSL_HOST
        unset WSL_HOST_X_TIMEOUT
        unset WSL_HOST_PA_TIMEOUT
    fi
fi

set +eu
