#!/bin/bash
#
# With all the .po files, generate the corresponding .mo files
#

for i in *.po; do
    echo "Generating file for language ${i%%.*}"
    msgfmt "${i}" -o "locale/${i%%.*}/LC_MESSAGES/mcm.mo"
done
