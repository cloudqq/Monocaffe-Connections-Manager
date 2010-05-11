#!/bin/bash
#
# Creates the Structure for a deb

rm -rf /tmp/pack
mkdir -p /tmp/pack/usr/share/apps/mcm
mkdir -p /tmp/pack/DEBIAN
cp -R ../* /tmp/pack/usr/share/apps/mcm
cp debian/* /tmp/pack/DEBIAN/

cd /tmp/
dpkg -b pack mcm-0.9.2_all.deb
