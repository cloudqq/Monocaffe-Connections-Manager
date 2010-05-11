# - coding: utf-8 -
#
# Copyright (C) 2009 Alejandro Ayuso 
#
# This file is part of the Monocaffe Connection Manager
#
# Monocaffe Connection Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Monocaffe Connection Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the Monocaffe Connection Manager.  If not, see <http://www.gnu.org/licenses/>.
#

'''
This is the main script for mcm
'''
import os
import sys
import subprocess
import logging
from optparse import OptionParser

from tables import Table
from mcm.common.connections import *
from mcm.common.utils import *

class Mcm(object):
    def __init__(self):
        self.dialog_binary = '/usr/bin/dialog'
        self.dao = Dao()
        self.connections = self.dao.read_xml()

    def do_connect(self, connection):
        connection.print_connection(connection.conn_args())
        try:
            subprocess.call(connection.conn_args())
        except (KeyboardInterrupt, SystemExit):
            exit(0)

    def connect(self, alias):
        conn = self.connections[alias]
        self.do_connect(conn)

    def delete(self, alias):
        try:
            del self.connections[alias]
            self.save_and_exit()
        except KeyError:
            print("Unknown alias " + alias)

    def export_html(self, path):
        from mcm.common.export import Html
        html = Html(path, get_mcm_version(), self.dao.read_xml()) 
        html.export()

    def add(self, cxs=None):
        cx = None
        if cxs == None:
            try:
                print "Adding a new alias. Follow instructions"
                print "Type of server (ssh, vnc, rdp, telnet, ftp) [default: SSH]:"
                cx_type = raw_input()
                cx_type = cx_type.upper()
                if len(cx_type) <= 0:
                    cx_type = 'SSH'

                if cx_type != 'SSH' and cx_type != 'VNC' and cx_type != 'RDP' and cx_type != 'TELNET' and cx_type != 'FTP':
                    raise TypeError("Unknown server type: " + cx_type)

                print "Alias for this connection:"
                cx_alias = raw_input()
                if self.connections != None:
                    if self.connections.has_key(cx_alias):
                        raise TypeError("This alias is already used. Try with another one")
                    

                print "Hostname or IP Address:"
                cx_host = raw_input()

                print "Username:"
                cx_user = raw_input()

                print "Password:"
                cx_password = raw_input()

                print "Port:"
                cx_port = raw_input()

                print "Group:"
                cx_group = raw_input()
                if len(cx_group) <= 0:
                    cx_group = None

                print "Options:"
                cx_options = raw_input()

                print("Description:")
                cx_desc = raw_input()

                cx = connections_factory(get_last_id(self.connections), cx_type, cx_user, cx_host, cx_alias, cx_password, cx_port, cx_group, cx_options, cx_desc)
                self.connections[cx_alias] = cx
                print("saved")
                print(cx)

            except (KeyboardInterrupt, SystemExit):
                exit(1)
        else:
            for d in cxs: # d is a dict
                alias = d['alias'].strip()
                if len(d) != 10:
                    raise TypeError("Not a parseable Connection List")
                if self.connections.has_key(alias):
                    print "Not saving %s" % alias
                    continue
                cx = connections_factory(get_last_id(self.connections), d['type'], d['user'], d['host'], alias, d['password'], d['port'], d['group'], d['options'], d['description'])
                self.connections[alias] = cx
                print("saved")
                print(cx)
                
        self.save_and_exit()


    def list(self, alias=None):
        print "Usage: mcm [OPTIONS] [ALIAS]\n"
        t_headers = ['Alias', 'user', 'host', 'port']
        t_rows = []
        _ids = []
        for conn in self.connections.values():
            _ids.append(int(conn.id))
        
        _ids.sort()
        for _id in _ids:
            for conn in self.connections.values():
                if conn.id == str(_id):
                    t_rows.append((conn.alias, conn.user, conn.host, conn.port))

        table = Table(t_headers, t_rows)
        table.output()
        exit(0)

    def long_list(self):
        print '-'*80
        print "Full list of connections"
        (sshs, vncs, rdps, tels, ftps) = ([], [], [], [], [])
        for conn in self.connections.values():
            cx_type = conn.__class__.__name__.upper()
            if cx_type == 'SSH':
                sshs.append(conn)
            elif cx_type == 'VNC':
                vncs.append(conn)
            elif cx_type == 'RDP':
                rdps.append(conn)
            elif cx_type == 'TELNET':
                tels.append(conn)
            elif cx_type == 'FTP':
                ftps.append(conn)
            else:
                raise TypeError("Unknown Server Type: " + cx_type)

        self.long_print_conn("SSH", sshs)
        self.long_print_conn("VNC", vncs)
        self.long_print_conn("RDP", rdps)
        self.long_print_conn("TELNET", tels)
        self.long_print_conn("FTP", ftps)

        sys.exit(0)

    def show_menu(self):
        if os.path.exists(self.dialog_binary):
            alias = self.show_menu_dialog()
            self.connect(alias)
        else:
            self.list()

    def long_print_conn(self, type, connections):
        print '-'*80
        print type
        print '-'*80
        if len(connections) == 0:
            return
        t_headers = ['Alias', 'user', 'host', 'port', 'Password','Options', 'Description']
        t_rows = []
        for conn in connections:
            row = (conn.alias, conn.user, conn.host, conn.port, conn.password, conn.options, conn.description.strip())
            t_rows.append(row)

        table = Table(t_headers, t_rows)
        table.output()
    
    def show_menu_dialog(self):
        '''Show a dialog, catch its output and return it for do_connect'''
        menu_size = 20
        if len(self.connections) < menu_size:
            menu_size = str(len(self.connections))
        else:
            menu_size = str(menu_size)
        dialog = [
                self.dialog_binary, '--backtitle', 'Monocaffe Connections Manager ' + get_mcm_version(), '--clear', '--menu', '"Choose an Alias to connect to"', '0', '150', menu_size
                ]
        keys = self.connections.keys()
        keys.sort()
        for key in keys:
            conn = self.connections[key]
            dialog.append(key)
            dialog.append(conn.dialog_string())
        fhandlr = open('/tmp/mcm_ans', 'w+')
        try:
            #print dialog
            res = subprocess.call(dialog, stderr=fhandlr)
            if res == 1:
                raise SystemExit()
        except (KeyboardInterrupt, SystemExit):
            sys.exit(0)

        fhandlr.seek(0)
        aliases = fhandlr.readlines()
        fhandlr.close()
        return aliases[0]

    def save_and_exit(self):
        self.dao.save_to_xml(self.connections.values())
        exit(0)

    def import_csv(self, path):
        from mcm.common.utils import Csv
        _csv = Csv(path)
        cxs = _csv.do_import()
        self.add(cxs)

if __name__ == '__main__':
    parser = OptionParser(usage="%prog [OPTIONS] [ALIAS]\nWith no options, prints the list of connections\nexample:\n  %prog foo\t\tConnects to server foo", version="%prog 0.9")
    parser.add_option("-a", "--add", action="store_true", dest="add", help="add a new connection")
    parser.add_option("-l", "--list", action="store_true", dest="list", help="complete list of connections with all data")
    parser.add_option("-d", "--delete", action="store", dest="alias", help="delete the given connection alias")
    parser.add_option("--html", action="store", dest="html", help="Export the connections to the given HTML file")
    parser.add_option("--csv", action="store", dest="csv", help="Import the connections from the given CSV file")

    (options, args) = parser.parse_args()

    # Start the logging stuff
    log_format = "%(asctime)s %(levelname)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format = log_format)

    #(export, drop) = os.path.split(os.getcwd())
    #(export, drop) = os.path.split(export)
    #sys.path.insert(0, export)

    mcmt = Mcm()

    if not options.list and not options.add and not options.alias and not options.html and not options.csv and len(args) < 1:
        mcmt.show_menu()

    # I want only one option at a time
    if options.add and (options.list or options.alias or options.html or options.csv):
        parser.error("Only one option at a time")

    if options.list and options.alias and options.html and options.csv:
        parser.error("Only one option at a time")

    if options.add:
        mcmt.add()

    if options.list:
        mcmt.long_list()

    if options.alias:
        mcmt.delete(options.alias)

    if options.html:
        mcmt.export_html(options.html)

    if options.csv:
        mcmt.import_csv(options.csv)

    if len(args) > 0:
        mcmt.connect(args[0])
