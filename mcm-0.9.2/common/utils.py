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
This is the Class we use to access the persistence
file where connections get saved
'''

import os
import shutil
import xml
import csv
import json
import urllib
import urllib2
from xml.dom import minidom
from xml.dom.minidom import Document
from StringIO import StringIO
from datetime import date
from connections import *
import constants

def get_last_id(connections):
    a_list = []
    _max = 0
    try:
        for conn in connections.values():
            a_list.append(int(conn.id))
        _max = max(a_list)
    except ValueError:
        _max = 0
    _max += 1
    return str(_max)


class Dao(object):

    def __init__(self):
        self.xmlfile = constants.cxs_file

    def read_xml(self):
        dom = minidom.parse(self.xmlfile)
        root = dom.firstChild
        return self.parse_connections_from_xml(root)

    def save_to_xml(self, connections):
        doc = Document()
        mcm_node = doc.createElement('mcm')
        doc.appendChild(mcm_node)

        if connections is not None:
            cons_node = doc.createElement('connections')
            for cx in connections:
                cx_node = doc.createElement('connection')
                cx_node.setAttribute('protocol', cx.__class__.__name__.upper())
                for (k, v) in cx.to_dict().items():
                    cx_id = doc.createElement(k)
                    cx_id_val = doc.createTextNode(str(v))
                    cx_id.appendChild(cx_id_val)
                    cx_node.appendChild(cx_id)
                cons_node.appendChild(cx_node)

            mcm_node.appendChild(cons_node)
        xml_w = open(self.xmlfile, 'w')
        doc.writexml(xml_w, "  ", "  ", "\n", "UTF-8")
        xml_w.close()

    def parse_connections_from_xml(self, root):
        cons_nodes = root.getElementsByTagName('connection')
        connections = {}
        for node in cons_nodes:
            cx_type = node.getAttribute('protocol')
            cx_id = self.get_node_value_by_name(node, 'id')
            cx_alias = self.get_node_value_by_name(node, 'alias')
            cx_user = self.get_node_value_by_name(node, 'user')
            cx_host = self.get_node_value_by_name(node, 'host')
            cx_port = self.get_node_value_by_name(node, 'port')
            cx_group = self.get_node_value_by_name(node, 'group')
            cx_password = self.get_node_value_by_name(node, 'password')
            cx_description = self.get_node_value_by_name(node, 'description')
            cx_options = self.get_node_value_by_name(node, 'options')
            cx = connections_factory(cx_id, cx_type, cx_user, cx_host, cx_alias, cx_password, cx_port, cx_group, cx_options, cx_description)
            connections[cx_alias] = cx

        return connections

    def get_node_value_by_name(self, node, node_name):
        '''Many elements are unique, but don't use this one for elements that aren't unique'''
        node_list = node.getElementsByTagName(node_name)

        if len(node_list) == 0:
            return None

        node = node_list[0]
        return node.firstChild.nodeValue.strip()


class Csv(object):

    def __init__(self, path):
        if os.path.exists(path) and os.access(path, os.W_OK):
            self.path = path
        else:
            raise IOError(constants.io_error % path)

    def do_import(self, pattern="alias"):
        """Returns a list with a dict"""
        cxs = []
        hdr = []
        csvreader = csv.reader(open(self.path, 'rb'))
        # From the header in the CSV we first get the header and create a list with it
        # then using this list, we iterate over the other rows creating a dict using
        # the header values as the keys and the row values for the dict values
        # then we save this dict to a list and return it.
        for row in csvreader:
            # Check if the row is the header
            if row[0] == pattern:
                for i in row:
                    hdr.append(i)
            else:
                cx = {}
                for i in range(len(hdr)):
                    _str = row[i]
                    cx[hdr[i]] = _str.strip()
                cxs.append(cx)
        return cxs


class GoogleForm(object):

    def __init__(self):
        self.url = constants.google_docs_url

    def send(self, tip):
        values = {"entry.0.single": tip.section,
                    "entry.1.single": tip.subsection,
                    "entry.2.single": tip.name,
                    "entry.3.single": tip.value,
                    "pageNumber": "0",
                    "backupCache": ""}

        data = urllib.urlencode(values)
        req = urllib2.Request(self.url, data)
        response = urllib2.urlopen(req)
        page = response.read()
        # page is a str that if everything is ok is the "thanks!" html
        # which is 1234 characters long. Could be bigger, depending on the
        # language but I think that 2000 is a good value. The Form html, which
        # is returned if the request failed, is bigger than 6000 chars. So:
        if len(page) > 2000:
            return false
        return True


class Tip(object):
    """
    A tip belongs to a subsection, which belongs to a section.
    Each tip has a name or description and a value which is the
    command or whatever we want to use and an ID to help us
    find them.
    """

    def __init__(self, id, section, subsection, name, value):
        self.id = id # Not used for now
        self.section = section
        self.subsection = subsection
        self.name = name
        self.value = value

        # To make comparing faster
        self.uid = hash(name + value)

    def __str__(self):
        return "<Tip: %s @ %s:%s - %s: %s>" % (self.id, self.section, self.subsection, self.name, self.value)

    def __eq__(self, other):
        return self.uid == other.uid

    def __cmp__(self, other):
        return self.uid == other.uid

    def get_label(self):
        return "%s: %s" % (self.name, self.value)

    def get_breadcrumb_list(self):
        return [self.section, self.subsection, self.name]


class TipsEncoder(json.JSONEncoder):

    def default(self, clazz):
        if not isinstance(clazz, Tip):
            print constants.tip_error
            return
        else:
            return dict(section=clazz.section, subsection=clazz.subsection, name=clazz.name, value=clazz.value)


class TipsDecoder(json.JSONDecoder):
    """Returns a List of Tips from a JSON String"""

    def decode(self, json_str):
        tips_list = json.loads(json_str)
        tips = []
        i = 0
        for tip in tips_list:
            tip = Tip(i, tip['section'], tip['subsection'], tip['name'], tip['value'])
            tips.append(tip)
            i += 1

        return tips


class Tips(object):
    """
    An object to describe the Tips loaded from the JSON file.
    """

    def __init__(self):
        self.jsonfile = constants.tips_file
        self.list = None

    def read(self):
        """ Reads the tips file (JSON) and returns a List with all the Tip objects """
        if not self.list:
            file = open(self.jsonfile, 'r')
            self.list = json.load(file, cls=TipsDecoder)
            file.close
        return self.list

    def save(self, tips=None):
        """ Given a list of tips. Save them. If no list is provided, we use the one in the object. """
        if not tips:
            tips = self.list
        file = open(self.jsonfile, 'w')
        json.dump(tips, file, cls=TipsEncoder, encoding="utf-8", sort_keys=True, indent=4)
        file.close

    def dump(self, tips, filepath):
        """ Given a list of tips, save them to the specified file. Used to import from CSV """
        file = open(filepath, 'w')
        json.dump(tips, file, cls=TipsEncoder, encoding="utf-8", sort_keys=True, indent=4)
        file.close

    def update(self, filename=None):
        """Update the tips.json file, with the new tips from the given file or
        downloads the JSON file from Launchpad. The tips under the section 'MyTips'
        don't get updated or erased. A backup file is created.
        Returns a str with the update process we used. Or None if the update failed.
        """

        raw = None
        update_from = filename

        try:
            if not filename:
                sock = urllib.urlopen(constants.tips_url)
                raw = StringIO(sock.read())
                update_from = "web"
            else:
                raw = open(filename, 'r')

            # Backup the old file
            today = date.today()
            today = today.strftime("%d%m%y")
            shutil.copyfile(self.jsonfile, self.jsonfile + "_" + today + ".backup")

            my_tips_list = self.get_my_tips()
            new_tips_list = json.load(raw, cls=TipsDecoder)
            new_tips_list += my_tips_list
            unique_tips_list = list(set(new_tips_list)) # Eliminate Duplicates.

            self.list = unique_tips_list
            self.save()
            return update_from

        except Error, e:
            print "Failed to Update"
            print e
            return None

    def get_my_tips(self):
        my_tips = []
        for tip in self.list:
            if tip.section == 'MyTips':
                my_tips.append(tip)
        return my_tips

    def get_max_id(self):
        return len(self.list)

    def get_subsections(self):
        subsections = []
        for tip in self.list:
            subsections.append(tip.subsection)
        return set(subsections)

    def get_sections(self):
        sections = []
        for tip in self.list:
            sections.append(tip.section)
        return set(sections)


# Use this script to create a json file from a CSV file
#if __name__ == '__main__':
#    _csv = Csv('/tmp/tips.csv')
#    rawtips = _csv.do_import("Section")
#
#    print constants.home
#
#    tips = []
#    for rawtip in rawtips:
#        tip = Tip(0, rawtip['Section'], rawtip['Subsection'], rawtip['Title'], rawtip['Value'])
#        tips.append(tip)
#
#    _tips = Tips()
#    _tips.dump(tips, "/tmp/tips.json")
#    tips_list = _tips.read()
#    tips_list += tips
#    unique_list = list(set(tips_list))
#    print unique_list

