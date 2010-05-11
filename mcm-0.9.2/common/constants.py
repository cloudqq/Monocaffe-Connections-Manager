# - coding: utf-8 -
#
# Copyright (C) 2009 Alejandro Ayuso
#
# This file is part of the Monocaffe Connection Manager
#
# Monocaffe Connection Manager is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Monocaffe Connection Manager is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with the Monocaffe Connection Manager. If not, see
# <http://www.gnu.org/licenses/>.
#

'''
File that contains all constants so it's easier to reuse, change and translate
str values.
'''

import os
import sys
import gettext
import locale
from xdg.BaseDirectory import *

version = '0.9.2'
app_name = "Monocaffe Connections Manager"

home = os.getenv("HOME")
mcm_config_dir = os.path.join(xdg_config_home, 'mcm')
mcm_data_dir = os.path.join(xdg_data_home, 'mcm')
glade_home = os.path.realpath(os.path.dirname(sys.argv[0]))
glade_file = os.path.join(glade_home, "mcm.glade")
tips_glade_file = os.path.join(glade_home, "tips.glade")
icon_file = os.path.join(glade_home, "mcm_icon.png")
tips_file = os.path.join(mcm_data_dir, "tips.json")
conf_file = os.path.join(mcm_config_dir, "mcm.conf")
cxs_file = os.path.join(mcm_data_dir, "mcm.xml")

# New Glade Files for GtkBuilder
glade_home = os.path.join(glade_home, "glade")
glade_main = os.path.join(glade_home, "main.glade")
glade_about = os.path.join(glade_home, "about.glade")
glade_file_utils = os.path.join(glade_home, "file_utils_dialogs.glade")
glade_http = os.path.join(glade_home, "http.glade")
glade_preferences = os.path.join(glade_home, "preferences.glade")
glade_new_cx = os.path.join(glade_home, "new_connection.glade")

# ----------------------------------------------------------------------
# i18n stuff
# ----------------------------------------------------------------------

def get_languages():
    _langs = []
    lc, enc = locale.getdefaultlocale()
    if lc:
        _langs = [lc]

    language = os.environ.get('LANG', None)
    if language:
        _langs += language.split(":")

    _langs += ["en", "es"]
    return _langs

l = "%s/../i18n/locale/"
local_path = l % os.path.realpath(os.path.dirname(sys.argv[0]))
gettext.install('mcm', local_path)
gettext.bindtextdomain('mcm', local_path)
gettext.textdomain('mcm')
langs = get_languages()

lang = gettext.translation('mcm', local_path, languages=langs, fallback=True)
_ = lang.ugettext

# ----------------------------------------------------------------------
# i18n stuff
# ----------------------------------------------------------------------

window_title = "Monocaffe Connections Manager - %s"

send_world = _("Send to the World")
google_docs_disclaimer = _("""If you select the option to send \
to the world, your tip will be sent to a Google Docs Spreadsheet \
using an online form. No personal information is sent, only \
the one you fill on the previous dialog.\n\nThis Form is \
online, and the results spreadsheet is public for everyone \
to see. Check the documentation for the links.\n\nIf you \
still feel the need to check on this go to the \
file \"common/utils.py\" and there is a class \
called \"GoogleForm\" where all this process happens.""")

io_error = _("Can\'t Access file %s")

google_docs_url = "http://spreadsheets.google.com/formResponse?\
formkey=dHV3bXRRZDQybnBwUktiX05YOExWWUE6MA&amp;theme=0AX42CRMsm\
RFbUy1iY2E5ZGYyZi1iZTJhLTQ2ODUtYWZmNS04ZWFiZTRkNzk4NjA&amp;ifq"
google_search_url = "http://www.google.com/search?q=%s"
mcm_help_url = "http://sites.google.com/site/monocaffe/home/mcm/help"
tips_url = "http://launchpad.net/mcm/trunk/mcm/+download/tips.json"

tip_error = _("Not a Tip Object")

deleting_connection_warning = _("Deleting Connection %s")
are_you_sure = _("Are you sure?")

tabs_switch_keys = "<Alt>%d"
tab_close_keys = "<Shift><Ctrl>w"
terminal_copy_keys = "<Shift><Ctrl>c"
terminal_paste_keys = "<Shift><Ctrl>v"
terminal_home_keys = "<Shift><Ctrl>T"
hide_connections_keys = "F2"

copy = _("Copy")
paste = _("Paste")
google_search = _("Google Search")
set_title = _("Set as Title")

press_enter_to_save = _("Press Enter to Save changes")

export_csv = _("Export to CSV done")
export_html = _("Export to HTML done")
saved_file = _("Saved file %s")

update_tips_error_1 = _("Unable to update tips file")
update_tips_error_2 = _("An error ocurred, please check \
                    the log files for more information")
update_tips_success_1 = _("Tips Update Success")
update_tips_success_2 = _("The tips file has been updated \
    succesfully using %s. A backup file has been created.")

alias_error = _("This alias is already used")
alias_tooltip = _("The alias for the new connection. Must be unique.")

import_not_saving = _("Not saving %s\n")
import_saving = _("Saved %s\n")
cluster_checkbox_tooltip = _("Set For Clustered Commands")

quit_warning = _("Quitting Monocaffe Connections Manager")
