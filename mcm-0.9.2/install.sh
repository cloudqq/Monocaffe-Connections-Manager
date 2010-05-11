#!/bin/sh
#
# Install Script for Monocaffe Connections Manager
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
mcm_shell="/usr/share/apps/mcm/bin/mcm"

echo "1/3 Copying files to ${install_dir}"
mkdir ${install_dir} 2>/dev/null
cp -R * ${install_dir} 2>/dev/null

echo "2/3 Creating symlinks"
ln -s ${mcm_shell}  /usr/bin/mcm
ln -s ${mcm_shell}  /usr/bin/mcm-gtk

echo "3/3 Creating menu-entry for Monocaffe Connections Manager"
cp /usr/share/apps/mcm/gtk/mcm_icon.xpm /usr/share/pixmaps/mcm.xpm
cp /usr/share/apps/mcm/gtk/mcm.desktop /usr/share/applications/

echo "Done. Monocaffe Connections Manager is ready"
echo "Type mcm on a console or run mcm-gtk from the GNOME Menu"

exit 0
