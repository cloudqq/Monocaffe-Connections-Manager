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
Script to add new connections to mcm
'''

from optparse import OptionParser
from mcm.common.connections import *
from mcm.common.utils import *

if __name__ == '__main__':
    parser = OptionParser(usage="%prog -a ALIAS -t [SSH|TELNET|FTP|RDP|VNC] -g GROUP -u USER -p PASSWORD -P PORT -H HOST -o OPTIONS -d DESCRIPTION\nexample:\n %prog -a test -g test_grp -o \"-X -L\"", version="%prog 0.9")
    parser.add_option("-a", "--alias", action="store", dest="alias", help="Alias of the new connection")
    parser.add_option("-t", "--type", action="store", dest="type", help="Type of the new connection [SSH|TELNET|FTP|RDP|VNC]")
    parser.add_option("-g", "--group", action="store", dest="group", help="Group for the new connection [OPTIONAL]")
    parser.add_option("-u", "--user", action="store", dest="user", help="Username for the connection [OPTIONAL]")
    parser.add_option("-p", "--password", action="store", dest="password", help="Password for the connection [OPTIONAL]")
    parser.add_option("-P", "--port", action="store", dest="port", help="Port to connect to. Uses defaults ports. [OPTIONAL]")
    parser.add_option("-H", "--host", action="store", dest="host", help="Hostname or IP Address [OPTIONAL]")
    parser.add_option("-o", "--options", action="store", dest="options", help="Custom options as they would be used with the client [OPTIONAL]")
    parser.add_option("-d", "--desc", action="store", dest="description", help="Description of the connection [OPTIONAL]")

    (options, args) = parser.parse_args()

    dao = Dao()
    connections = dao.read_xml()
    if connections != None:
        if connections.has_key(options.alias):
            raise AttributeError("This alias is already used. Try with another one")

    cx = connections_factory(get_last_id(connections), options.type, options.user, options.host, options.alias, options.password, options.port, options.group, options.options, options.description)
    connections[options.alias] = cx

    print("saved")
    print(cx)

    dao.save_to_xml(connections.values())
    exit(0)

