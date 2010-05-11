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
Configuration Loading for file ~/.mcm
'''

import ConfigParser
import os
import pango
import constants


class McmConfig(object):

    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.cfgfile = constants.conf_file
        self.config.read(self.cfgfile)

    def get_config(self, section):
        _config_dict = {}
        for option in self.config.options(section):
            _config_dict[option] = self.config.get(section, option)

        return _config_dict

    def get_connections_config(self):
        """Returns a dictionary with the configuration options"""
        return self.get_config('Clients')

    def get_console_config(self):
        return self.get_config('Console')

    def save_connections_config(self, configurations):
        self.save_config(configurations, 'Clients')

    def save_console_config(self, configurations):
        self.save_config(configurations, 'Console')

    def save_config(self, configurations, section):
        """Receives a dictionary with the options to be saved"""
        for k, v in configurations.items():
            self.config.set(section, k, v)
        self.config.write(open(self.cfgfile, 'w'))

    def get_ssh_conf(self):
        """Returns a tuple"""
        conf = self.get_connections_config()
        return (conf['ssh.client'], conf['ssh.default'])

    def get_vnc_conf(self):
        """Returns a tuple"""
        conf = self.get_connections_config()
        return (conf['vnc.client'], conf['vnc.default'])

    def get_rdp_conf(self):
        """Returns a tuple"""
        conf = self.get_connections_config()
        return (conf['rdp.client'], conf['rdp.default'])

    def get_telnet_conf(self):
        """Returns a tuple"""
        conf = self.get_connections_config()
        return (conf['telnet.client'], conf['telnet.default'])

    def get_ftp_conf(self):
        """Returns a tuple"""
        conf = self.get_connections_config()
        return (conf['ftp.client'], conf['ftp.default'])

    def get_bg_color(self):
        try:
            conf = self.get_console_config()
            return '#%s' % conf['bg.color']
        except KeyError:
            return '#000000000000'

    def get_fg_color(self):
        try:
            conf = self.get_console_config()
            return '#%s' % conf['fg.color']
        except KeyError:
            return '#3341ffff0000'

    def get_bg_image(self):
        conf = self.get_console_config()
        if os.path.isfile(conf['bg.image']) and \
        os.access(conf['bg.image'], os.R_OK):
            return conf['bg.image']
        else:
            return ""

    def get_bg_transparent(self):
        try:
            conf = self.get_console_config()
            return conf['bg.transparent'] == 'True'
        except KeyError:
            return False

    def get_bg_transparency(self):
        try:
            conf = self.get_console_config()
            return int(conf['bg.transparency'])
        except KeyError:
            return 0

    def get_font(self):
        try:
            conf = self.get_console_config()
            return pango.FontDescription(conf['font.type'])
        except KeyError:
            return pango.FontDescription("Monospace 10")

    def get_word_chars(self):
        try:
            conf = self.get_console_config()
            return conf['word.chars']
        except KeyError:
            return "-A-Za-z0-9,./?&#:_"

    def get_buffer_size(self):
        try:
            conf = self.get_console_config()
            size = int(conf['buffer.size'])
            if size:
                if size < 500:
                    return 500
                else:
                    return size
            else:
                return 500
        except KeyError:
            return 500
