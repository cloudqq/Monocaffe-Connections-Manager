#!/bin/sh
#
# Uninstall Script for Monocaffe Connections Manager
# Please run as root
#
# This script is based on the one of pyjama.
#

# Clever way of testing for root
userpriv=$(test -w \/ && echo "ok")
if [ -z $userpriv ]
    then echo "Please run this script as root / sudo"
    exit 1
fi

install_dir="/usr/share/apps/mcm"

echo "1/3 Removing from GNOME Menu"
rm -f /usr/share/pixmaps/mcm.xpm
rm -f /usr/share/applications/mcm.desktop

echo "2/3 Removing Symlinks"
rm -f /usr/bin/mcm
rm -f /usr/bin/mcm-gtk

echo "3/3 Removing mcm"
rm -rf ${install_dir}
