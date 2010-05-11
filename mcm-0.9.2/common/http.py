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

import threading
import BaseHTTPServer
import SimpleHTTPServer
import os

class McmHttpServerThread(threading.Thread):
    def __init__(self, path, port=8000):
        threading.Thread.__init__(self)
        self.path = path
        self.port = port
        self.running = False

    def run(self):
        self.running = True
        server_class = BaseHTTPServer.HTTPServer
        handler_class = SimpleHTTPServer.SimpleHTTPRequestHandler
        server_address = ('0.0.0.0', self.port)
        httpd = server_class(server_address, handler_class)
        os.chdir(self.path)
        while self.running:
            httpd.handle_request()

    def stop(self):
        self.running = False

if __name__ == '__main__':
    import time
    x = McmHttpServerThread("/tmp")
    x.start()
    i = 0
    while i < 10:
        print "Hola"
        time.sleep(2)
        i += 1
    x.stop()
