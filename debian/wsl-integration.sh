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

[ -f "/etc/ubuntu-wsl.conf" ] && . /etc/ubuntu-wsl.conf

if [ "$UBUNTU_WSL_GUI_INTEGRATION" = "true" ] || [ "$UBUNTU_WSL_AUDIO_INTEGRATION" = "true" ] ; then
    if type pactl > /dev/null 2>&1 || type xvinfo > /dev/null 2>&1; then
        # detect WSL host
        if type systemd-detect-virt > /dev/null 2>&1 && test "$(systemd-detect-virt -c)" != wsl -a -e /etc/resolv.conf; then
            WSL_HOST="$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null)"
            WSL_HOST_X_TIMEOUT=0.2
            WSL_HOST_PA_TIMEOUT=0.3
        else
            WSL_HOST="${WSL_HOST:-localhost}"
            WSL_HOST_X_TIMEOUT=0.6
            WSL_HOST_PA_TIMEOUT=0.8
        fi

        # set DISPLAY if there is an X11 server running and integration is enabled
        if [ "$UBUNTU_WSL_GUI_INTEGRATION" = "true" ] && type xvinfo > /dev/null 2>&1 && env DISPLAY="${WSL_HOST}:0" timeout "$WSL_HOST_X_TIMEOUT" xvinfo > /dev/null 2>&1; then
            export DISPLAY="${WSL_HOST}:0"
            export LIBGL_ALWAYS_INDIRECT=1
            win_sys_scaling=$(wslsys -S -s)
            export GDK_SCALE=$win_sys_scaling
            export QT_SCALE_FACTOR=$win_sys_scaling
        fi
        
        # set up audio if pulse server is reachable only via tcp
        if [ "$UBUNTU_WSL_AUDIO_INTEGRATION" = "true" ] && type pactl > /dev/null 2>&1 \
        && (! timeout "$WSL_HOST_PA_TIMEOUT" pactl info > /dev/null 2>&1 || timeout "$WSL_HOST_PA_TIMEOUT" pactl info 2> /dev/null | grep -q 'Default Sink: auto_null' ) \
        && env PULSE_SERVER="tcp:${WSL_HOST}" timeout "$WSL_HOST_PA_TIMEOUT" pactl stat > /dev/null 2>&1; then
            export PULSE_SERVER="tcp:${WSL_HOST}"
        fi
        
        unset WSL_HOST
        unset WSL_HOST_X_TIMEOUT
        unset WSL_HOST_PA_TIMEOUT
    fi
fi
