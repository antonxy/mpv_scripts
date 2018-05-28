#!/bin/sh
kill_child_processes() {
    isTopmost=$1
    curPid=$2
    childPids=`ps -o pid --no-headers --ppid ${curPid}`
    for childPid in $childPids
    do
        kill_child_processes 0 $childPid
    done
    if [ $isTopmost -eq 0 ]; then
        kill -9 $curPid 2> /dev/null
    fi
}

# Ctrl-C trap. Catches INT signal
trap "kill_child_processes 1 $$; exit 0" INT

# Create new fifo
rm mpvfifo
mkfifo mpvfifo

# Disable screen blanking
xset s off -dpms
# Inhibit standby
systemd-inhibit --what handle-lid-switch sleep infinity &

mpv black.png --pause --no-osc --osd-level=0 --fullscreen --keep-open=always --input-file=mpvfifo --cursor-autohide=always &
./video_control_csc.py > mpvfifo &
wait
