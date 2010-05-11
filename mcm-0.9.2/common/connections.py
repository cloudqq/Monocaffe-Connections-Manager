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

import os
from configurations import McmConfig


class Connection(object):

    def __init__(self, id, user, host, alias, password, port, group=None, \
                options=None, description=None):
        self.id = id
        self.user = user
        self.host = host
        self.port = port
        self.group = group
        self.alias = alias
        self.password = password
        self.description = description
        self.options = options

    def cx_args(self, client, options, *args):
        """Creates a list containing all the arguments needed by subprocess"""
        _list = [self.command(client)]
        for option in options.split():
            _list.append(option)

        for arg in args:
            _list.append(arg)

        return _list

    def command(self, client):
        if os.path.exists(client) and os.access(client, os.X_OK):
            return client

    def print_connection(self, args):
        tstr = "Connecting: "
        for i in args:
            tstr += i + " "
        print tstr

    def get_type(self):
        return self.__class__.__name__.upper()

    def dialog_string(self):
        """Used to give a correct String for the dialog utility to show"""
        if self.get_type() == 'JBOSS':
            return "%s\thttp://%s:%s\t\t\t %s" % (self.get_type(), self.host, \
                                                self.port, self.description)
        elif self.get_type() == 'FTP':
            return "%s\tftp://%s@%s:%s\t\t %s" % (self.get_type(), self.user, \
                                    self.host, self.port, self.description)
        else:
            return "%s\t%s@%s:%s\t\t\t %s" % (self.get_type(), self.user, \
                                    self.host, self.port, self.description)

    def list_to_string(self, a_list):
        _str = ""
        for i in a_list:
            _str += " %s " % i
        _str += " ; exit\n "
        return _str

    def to_dict(self):
        return {'id': self.id, 'user': self.user, 'host': self.host,
                'port': self.port, 'alias': self.alias,
                'password': self.password,
                'description': self.description, 'options': self.options,
                'group': self.group}

    def to_list(self):
        return [self.alias, self.get_type(), self.id, self.host, self.port,
        self.user, self.password, self.options, self.group, self.description]

    def get_html_tr(self):
        cxs = [self.alias, self.get_type(), self.id, self.host, self.port,
        self.user, self.password, self.options, self.group, self.description]
        tr = "<tr>"
        for cx in cxs:
            tr += "<td>%s</td>" % cx
        tr += "</tr>"
        return tr

    def __str__(self):
        return "%s %s %s@%s:%s" % (self.get_type(), self.alias,
        self.user, self.host, self.port)


class Ssh(Connection):

    def hostname(self):
        return "%s@%s" % (self.user, self.host)

    def conn_args(self):
        conf = McmConfig()
        self.client, not_used = conf.get_ssh_conf()
        return self.cx_args(self.client, self.hostname(), "-p", self.port, self.options)

    def gtk_cmd(self):
        a_list = self.conn_args()
        return self.list_to_string(a_list)


class Vnc(Connection):

    def vnchost(self):
        return "%s:%s" % (self.host, self.port)

    def conn_args(self):
        conf = McmConfig()
        self.client, not_used = conf.get_vnc_conf()
        return self.cx_args(self.client, self.options, self.vnchost())

    def gtk_cmd(self):
        a_list = self.conn_args()
        return self.list_to_string(a_list)


class Rdp(Connection):

    def conn_args(self):
        conf = McmConfig()
        self.client, not_used = conf.get_rdp_conf()
        return self.cx_args(self.client, self.options, self.host)

    def gtk_cmd(self):
        a_list = self.conn_args()
        return self.list_to_string(a_list)


class Telnet(Connection):

    def conn_args(self):
        conf = McmConfig()
        self.client, not_used = conf.get_telnet_conf()
        return self.cx_args(self.client, self.options, self.host, self.port)

    def gtk_cmd(self):
        a_list = self.conn_args()
        return self.list_to_string(a_list)


class Ftp(Connection):

    def conn_args(self):
        conf = McmConfig()
        self.client, not_used = conf.get_ftp_conf()
        return self.cx_args(self.client, self.options, '-u',
        self.user, '-p', self.port, self.host)

    def gtk_cmd(self):
        a_list = self.conn_args()
        return self.list_to_string(a_list)


def connections_factory(cx_id, cx_type, cx_user, cx_host, cx_alias,
cx_password, cx_port, cx_group, cx_options, cx_desc):
    try:
        if not cx_alias:
            raise AttributeError("Bad format. Alias is not optional")

        cx = None
        if cx_type == 'SSH':
            cx = Ssh(cx_id, cx_user, cx_host, cx_alias, cx_password,
                    cx_port, cx_group, cx_options, cx_desc)

        elif cx_type == 'VNC':
            cx = Vnc(cx_id, cx_user, cx_host, cx_alias, cx_password,
                    cx_port, cx_group, cx_options, cx_desc)

        elif cx_type == 'RDP':
            cx = Rdp(cx_id, cx_user, cx_host, cx_alias, cx_password,
                    cx_port, cx_group, cx_options, cx_desc)

        elif cx_type == 'TELNET':
            cx = Telnet(cx_id, cx_user, cx_host, cx_alias, cx_password,
                        cx_port, cx_group, cx_options, cx_desc)

        elif cx_type == 'FTP':
            cx = Ftp(cx_id, cx_user, cx_host, cx_alias, cx_password,
                    cx_port, cx_group, cx_options, cx_desc)

        else:
            raise AttributeError("Unkown Connection Type: %s" % cx_type)

        return cx

    except TypeError, err:
        print(err)
        exit(1)


def groups(connections):
    groups = []
    for cx in connections.values():
        if cx.group not in groups:
            groups.append(cx.group)
    return groups


def types(connections):
    return ['SSH', 'VNC', 'RDP', 'TELNET', 'FTP']
