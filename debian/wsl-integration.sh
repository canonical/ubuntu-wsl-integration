#!/bin/bash
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

[ -f "$CUR_CONF_LOC" ] && __ubuntu_wsl_conf_handling
unset CUR_CONF_LOC

# the... like, the real detection part
if [ "$UBUNTU_WSL_INTEROP_GUIINTEGRATION" = "true" ] || []; then
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
