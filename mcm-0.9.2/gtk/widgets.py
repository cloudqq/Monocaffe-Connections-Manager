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

import gtk
import gtk.glade
import pygtk
pygtk.require("2.0")

from mcm.common.connections import *
from mcm.common.utils import *
from mcm.common.configurations import McmConfig
import mcm.common.constants

'''
Dialogs for Monocaffe Connections Manager
'''


class UtilityDialogs(object):
    """
    Class that defines the methods used to display MessageDialog dialogs
    to the user
    """

    def __init__(self):
        pass

    def show_question_dialog(self, title, message):
        """Display a Warning Dialog and return the response to the caller"""
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_OK_CANCEL, title)
        dialog.format_secondary_text(message)
        response = dialog.run()
        dialog.destroy()
        return response

    def show_error_dialog(self, title, message):
        """Display an error dialog to the user"""
        self.show_common_dialog(title, message, gtk.MESSAGE_ERROR)

    def show_info_dialog(self, title, message):
        """Display an error dialog to the user"""
        self.show_common_dialog(title, message, gtk.MESSAGE_INFO)

    def show_common_dialog(self, title, message, icon):
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, icon, gtk.BUTTONS_OK, title)
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


class AddConnectionDialog(object):

    def __init__(self, id, aliases, groups, types):
        """I need a list with the aliases so I can validate the name"""
        self.response = gtk.RESPONSE_CANCEL
        self.new_connection = None
        self.error = None
        self.xml = gtk.glade.XML(constants.glade_file, 'dialog_add')
        self.aliases = aliases
        self.id = id
        self.widgets = {
                        'dlg': self.xml.get_widget('dialog_add'),
                        'types_combobox': self.xml.get_widget('types_combobox'),
                        'group_combobox': self.xml.get_widget('group_combobox'),
                        'user_entry1': self.xml.get_widget('user_entry1'),
                        'host_entry1': self.xml.get_widget('host_entry1'),
                        'port_entry1': self.xml.get_widget('port_entry1'),
                        'options_entry1': self.xml.get_widget('options_entry1'),
                        'description_entry1': self.xml.get_widget('description_entry1'),
                        'password_entry1': self.xml.get_widget('password_entry1'),
                        'alias_entry1': self.xml.get_widget('alias_entry1'),
                        }
        events = {
                        'response': self.cancel_event,
                        'on_button_cancel_clicked': self.cancel_event,
                        'on_button_save_clicked': self.save_event,
                        'on_alias_entry1_changed': self.validate_alias,
                        'on_types_combobox_changed': self.insert_default_options,
                }
        # Glade3 changes the behaviour of the comboboxentry widget.
        g_entry = self.widgets['group_combobox'].get_child()
        self.widgets['group_entry1'] = g_entry
        self.xml.signal_autoconnect(events)
        self.init_combos(groups, types)

    def run(self):
        dlg = self.widgets['dlg']
        dlg.run()
        dlg.destroy()

    def init_combos(self, groups, types):
        cb_groups = self.widgets['group_combobox']
        cb_types = self.widgets['types_combobox']
        for i in groups:
            cb_groups.append_text(i)

        for i in types:
            cb_types.append_text(i)

    def insert_default_options(self, widget):
        type = widget.get_active_text()
        conf = McmConfig()
        config = ""
        if type == 'SSH':
            not_used, config = conf.get_ssh_conf()
        elif type == 'VNC':
            not_used, config = conf.get_vnc_conf()
        elif type == 'RDP':
            not_used, config = conf.get_rdp_conf()
        elif type == 'TELNET':
            not_used, config = conf.get_telnet_conf()
        elif type == 'FTP':
            not_used, config = conf.get_ftp_conf()

        opts_entry = self.widgets['options_entry1']
        opts_entry.set_text(config)

    def cancel_event(self, widget):
        pass

    def save_event(self, widget):
        if self.error == None:
            self.response = gtk.RESPONSE_OK
            cx_type = self.widgets['types_combobox'].get_active_text()
            cx_group = self.widgets['group_entry1'].get_text()
            cx_user = self.widgets['user_entry1'].get_text()
            cx_host = self.widgets['host_entry1'].get_text()
            cx_alias = self.widgets['alias_entry1'].get_text()
            cx_port = self.widgets['port_entry1'].get_text()
            cx_desc = self.widgets['description_entry1'].get_text()
            cx_pass = self.widgets['password_entry1'].get_text()
            cx_options = self.widgets['options_entry1'].get_text()
            self.new_connection = connections_factory(self.id, cx_type, cx_user, cx_host, cx_alias, cx_pass, cx_port, cx_group, cx_options, cx_desc)

    def validate_alias(self, widget):
        alias = widget.get_text()
        entry = self.widgets['alias_entry1']
        if alias in self.aliases:
            self.error = constants.alias_error
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFADAD"))
            widget.set_tooltip_text(self.error)
        else:
            self.error = None
            widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("#FFFFFF"))
            widget.set_tooltip_text(constants.alias_tooltip)

    def validate_port(self, widget):
        pass


class ImportCsvDialog(object):

    def __init__(self):
        self.response = gtk.RESPONSE_CANCEL
        self.error = None
        self.uri = None
        self.xml = gtk.glade.XML(constants.glade_file, 'import_csv_dialog')
        self.widgets = {'dlg': self.xml.get_widget('import_csv_dialog')}

        events = {'on_filter_combo_changed': self.filter_event,
                  'on_open_button7_clicked': self.open_event,
                  'on_cancel_button6_clicked': self.cancel_event,
                }
        self.xml.signal_autoconnect(events)

    def get_response(self):
        return self.response

    def filter_event(self, widget):
        pass

    def open_event(self, widget):
        dlg = self.widgets['dlg']
        self.uri = dlg.get_filename()
        self.response = gtk.RESPONSE_OK

    def cancel_event(self, widget):
        self.response = gtk.RESPONSE_CANCEL

    def get_filename(self):
        return self.uri

    def run(self):
        dlg = self.widgets['dlg']
        dlg.run()
        dlg.destroy()


class ExportDialog(object):

    def __init__(self):
        self.response = gtk.RESPONSE_CANCEL
        self.error = None
        self.uri = None
        self.xml = gtk.glade.XML(constants.glade_file, 'export_filedialog')
        self.widgets = {'dlg': self.xml.get_widget('export_filedialog')}

        events = {
                    'on_button6_clicked': self.save_event,
                    'on_button7_clicked': self.cancel_event,
                }
        self.xml.signal_autoconnect(events)

    def get_response(self):
        return self.response

    def save_event(self, widget):
        dlg = self.widgets['dlg']
        self.uri = dlg.get_filename()
        self.response = gtk.RESPONSE_OK

    def cancel_event(self, widget):
        self.response = gtk.RESPONSE_CANCEL

    def get_filename(self):
        return self.uri

    def run(self):
        dlg = self.widgets['dlg']
        dlg.run()
        dlg.destroy()


class ImportProgressDialog(object):

    def __init__(self, cxs, connections):
        self.connections = connections
        self.xml = gtk.glade.XML(constants.glade_file, 'import_progress')
        self.results = self.xml.get_widget('import_result')
        self.dlg = self.xml.get_widget('import_progress')
        events = {
                    'on_ok_button6_clicked': self.close_event,
                    'on_import_progress_destroy': self.close_event,
                }
        self.xml.signal_autoconnect(events)
        for d in cxs:
            alias = d['alias'].strip()
            if len(d) != 10 or alias in self.connections:
                self.write_result(constants.import_not_saving % alias)
                continue
            cx = connections_factory(get_last_id(self.connections), d['type'], d['user'],
                                    d['host'], alias, d['password'], d['port'],
                                    d['group'], d['options'], d['description'])
            self.connections[alias] = cx
            self.write_result(constants.import_saving % cx)

    def run(self):
        self.dlg.run()

    def close_event(self, widget=None):
        self.dlg.destroy()

    def write_result(self, text):
        buffer = self.results.get_buffer()
        if buffer == None:
            buffer = gtk.TextBuffer()
            self.results.set_buffer(buffer)
        buffer.insert_at_cursor(text)


class PreferencesDialog(object):

    def __init__(self):
        self.response = gtk.RESPONSE_CANCEL
        self.xml = gtk.glade.XML(constants.glade_file, 'dialog_preferences')
        self.dlg = self.xml.get_widget('dialog_preferences')
        self.widgets = {
            # Consoles
            'fg_colorbutton': self.xml.get_widget('font-colorbutton'),
            'fontbutton': self.xml.get_widget('fontbutton'),
            'buffer_hscale': self.xml.get_widget('buffer-hscale'),
            'chk_bg_transparent': self.xml.get_widget('chk_bg_transparent'),
            'transparency_hscale': self.xml.get_widget('transparency-hscale'),
            'bgimage_filechooserbutton': self.xml.get_widget('bgimage-filechooserbutton'),
            'bg_colorbutton': self.xml.get_widget('bg-colorbutton'),
            'clear_bg': self.xml.get_widget('clear_image_button'),
            # Connections
            'ssh_options_entry': self.xml.get_widget('ssh_default_options_entry'),
            'vnc_options_entry': self.xml.get_widget('vnc_default_options_entry'),
            'rdp_options_entry': self.xml.get_widget('rdp_default_options_entry'),
            'telnet_options_entry': self.xml.get_widget('telnet_default_options_entry'),
            'ftp_options_entry': self.xml.get_widget('ftp_default_options_entry'),
            'ssh_entry': self.xml.get_widget('ssh_client_entry'),
            'vnc_entry': self.xml.get_widget('vnc_client_entry'),
            'rdp_entry': self.xml.get_widget('rdp_client_entry'),
            'telnet_entry': self.xml.get_widget('telnet_client_entry'),
            'ftp_entry': self.xml.get_widget('ftp_client_entry'),
            'console_char_entry': self.xml.get_widget('console_char_entry')}

        events = {
            'on_dialog_preferences_close': self.close_event,
            'on_pref_cancel_button_clicked': self.close_event,
            'on_pref_appy_button_clicked': self.apply_event,
            'on_clear_image_button_clicked': self.clear_event,
            'on_chk_bg_transparent_toggled': self.toggle_transparency_event}
        self.xml.signal_autoconnect(events)
        self.fill_entries()
        self.fill_console()

    def close_event(self, widget):
        self.dlg.destroy()

    def apply_event(self, widget):
        self.save_connections_config()
        self.save_console_config()
        self.close_event(None)
        self.response = gtk.RESPONSE_OK

    def clear_event(self, widget):
        '''Set the bg image to None'''
        bg_but = self.widgets['bgimage_filechooserbutton']
        bg_but.set_filename("None")

    def toggle_transparency_event(self, widget):
        bg_button = self.widgets['bgimage_filechooserbutton']
        bg_clear = self.widgets['clear_bg']
        bg_color = self.widgets['bg_colorbutton']
        if widget.get_active():
            bg_button.set_sensitive(False)
            bg_clear.set_sensitive(False)
            bg_color.set_sensitive(False)
        else:
            bg_button.set_sensitive(True)
            bg_clear.set_sensitive(True)
            bg_color.set_sensitive(True)

    def fill_entries(self):
        conf = McmConfig()
        #SSH
        client, options = conf.get_ssh_conf()
        e1 = self.widgets['ssh_entry']
        e2 = self.widgets['ssh_options_entry']
        e1.set_text(client)
        e2.set_text(options)
        #VNC
        client, options = conf.get_vnc_conf()
        e1 = self.widgets['vnc_entry']
        e2 = self.widgets['vnc_options_entry']
        e1.set_text(client)
        e2.set_text(options)
        #Telnet
        client, options = conf.get_telnet_conf()
        e1 = self.widgets['telnet_entry']
        e2 = self.widgets['telnet_options_entry']
        e1.set_text(client)
        e2.set_text(options)
        #FTP
        client, options = conf.get_ftp_conf()
        e1 = self.widgets['ftp_entry']
        e2 = self.widgets['ftp_options_entry']
        e1.set_text(client)
        e2.set_text(options)
        #RDP
        client, options = conf.get_rdp_conf()
        e1 = self.widgets['rdp_entry']
        e2 = self.widgets['rdp_options_entry']
        e1.set_text(client)
        e2.set_text(options)

    def fill_console(self):
        conf = McmConfig()
        widget = self.widgets['fg_colorbutton']
        widget.set_color(gtk.gdk.color_parse(conf.get_fg_color()))
        widget = self.widgets['fontbutton']
        pango_font = conf.get_font()
        widget.set_font_name(pango_font.to_string())
        widget = self.widgets['chk_bg_transparent']
        widget.set_active(conf.get_bg_transparent())
        widget.toggled()
        widget = self.widgets['transparency_hscale']
        widget.set_value(conf.get_bg_transparency())
        widget = self.widgets['bgimage_filechooserbutton']
        widget.set_filename(conf.get_bg_image())
        widget = self.widgets['bg_colorbutton']
        widget.set_color(gtk.gdk.color_parse(conf.get_bg_color()))
        widget = self.widgets['console_char_entry']
        widget.set_text(conf.get_word_chars())
        widget = self.widgets['buffer_hscale']
        widget.set_value(conf.get_buffer_size())

    def save_connections_config(self):
        conf = McmConfig()
        cfg = conf.get_connections_config()
        #SSH
        cfg['ssh.client'] = self.widgets['ssh_entry'].get_text()
        cfg['ssh.default'] = self.widgets['ssh_options_entry'].get_text()
        #VNC
        cfg['vnc.client'] = self.widgets['vnc_entry'].get_text()
        cfg['vnc.default'] = self.widgets['vnc_options_entry'].get_text()
        #RDP
        cfg['rdp.client'] = self.widgets['rdp_entry'].get_text()
        cfg['rdp.default'] = self.widgets['rdp_options_entry'].get_text()
        #TELNET
        cfg['telnet.client'] = self.widgets['telnet_entry'].get_text()
        cfg['telnet.default'] = self.widgets['telnet_options_entry'].get_text()
        #FTP
        cfg['ftp.client'] = self.widgets['ftp_entry'].get_text()
        cfg['ftp.default'] = self.widgets['ftp_options_entry'].get_text()
        conf.save_connections_config(cfg)

    def save_console_config(self):
        conf = McmConfig()
        cfg = conf.get_console_config()

        color = self.widgets['fg_colorbutton'].get_color()
        cfg['fg.color'] = color.to_string().strip("#")
        color = self.widgets['bg_colorbutton'].get_color()
        cfg['bg.color'] = color.to_string().strip("#")

        fname = self.widgets['bgimage_filechooserbutton'].get_filename()
        if fname == None:
            fname = "None"
        cfg['bg.image'] = fname

        active = self.widgets['chk_bg_transparent'].get_active()
        cfg['bg.transparent'] = str(active)

        value = self.widgets['transparency_hscale'].get_value()
        value = int(value)
        cfg['bg.transparency'] = str(value)

        value = self.widgets['buffer_hscale'].get_value()
        value = int(value)
        cfg['buffer.size'] = str(value)

        font = self.widgets['fontbutton'].get_font_name()
        cfg['font.type'] = font

        cfg['word.chars'] = self.widgets['console_char_entry'].get_text()
        conf.save_console_config(cfg)

    def get_font(self):
        return self.widgets['fontbutton'].get_font_name()

    def get_fg_color(self):
        return self.widgets['fg_colorbutton'].get_color()

    def get_bg_color(self):
        return self.widgets['bg_colorbutton'].get_color()

    def get_transparency(self):
        return (self.widgets['chk_bg_transparent'].get_active(), self.widgets['transparency_hscale'].get_value())

    def get_bg_image(self):
        return self.widgets['bgimage_filechooserbutton'].get_filename()

    def run(self):
        self.dlg.run()


class McmCheckbox(gtk.HBox):

    def __init__(self, title):
        gtk.HBox.__init__(self, False)
        self._label = gtk.Label(title)
        self._current_alias = title
        self.pack_start(self._label, True, True, 0)
        self._button = gtk.CheckButton()
        self._button.set_name("%s_button" % title)
        self._button.set_tooltip_text(constants.cluster_checkbox_tooltip)
        self.pack_start(self._button, False, False, 0)
        self.show_all()

    def get_active(self):
        return self._button.get_active()

    def set_title(self, title):
        self._label.set_text(title)

    def get_title(self):
        return self._label.get_text()

    def get_current_alias(self):
        return self._current_alias


class McmNewTipDialog(object):

    def __init__(self):
        self.response = gtk.RESPONSE_CANCEL
        self.new_tip = None
        self.error = None
        self.xml = gtk.glade.XML(constants.tips_glade_file, 'new_tips_dialog')
        self.widgets = {
                        'dlg': self.xml.get_widget('new_tips_dialog'),
                        'section_entry': self.xml.get_widget('section_entry'),
                        'subsection_entry': self.xml.get_widget('subsection_entry'),
                        'name_entry': self.xml.get_widget('name_entry'),
                        'value_entry': self.xml.get_widget('value_entry'),
                        'send_checkbox': self.xml.get_widget('send_checkbox'),
                        }
        events = {
                        'response': self.cancel_event,
                        'on_cancel_button_clicked': self.cancel_event,
                        'on_save_button_clicked': self.save_event,
                        'on_help_button_clicked': self.help_event,
                }
        self.xml.signal_autoconnect(events)
        self.dlg = self.widgets['dlg']

    def run(self):
        self.dlg.run()
        self.dlg.destroy()

    def cancel_event(self, widget):
        self.response = gtk.RESPONSE_CANCEL
        return True

    def save_event(self, widget):
        self.response = gtk.RESPONSE_OK
        section = self.widgets['section_entry'].get_text()
        subsection = self.widgets['subsection_entry'].get_text()
        name = self.widgets['name_entry'].get_text()
        value = self.widgets['value_entry'].get_text()
        send = self.widgets['send_checkbox'].get_active()

        # Shall I add a "Are you sure" dialog when sending to google docs?

        self.new_tip = Tip(0, section, subsection, name, value)
        if send:
            gform = GoogleForm()
            gform.send(self.new_tip)

        return True

    def help_event(self, widget):
        dlg = UtilityDialogs()
        response = dlg.show_info_dialog(constants.send_world, constants.google_docs_disclaimer)


class McmMenu(gtk.Menu):

    def __init__(self, label):
        gtk.Menu.__init__(self)
        self.label = label


class TipGtkMenuItem(gtk.MenuItem):

    def __init__(self, label, tip):
        gtk.MenuItem.__init__(self, label)
        self.tip = tip


class McmTipsWidget(object):

    def __init__(self, hbox):
        self.tips = Tips()
        self.tips_list = self.tips.read()
        self.hbox = hbox
        self.menu_bar = self.hbox.get_children()[0]
        self.tips_entry = self.hbox.get_children()[1]
        self.tips_entry.connect("icon-press", self.entry_icon_event)
        self.draw_menu_bar()

    def draw_menu_bar(self):
        root_menu_item = self.menu_bar.get_children()[0]
        sections_menu = gtk.Menu()
        root_menu_item.set_submenu(sections_menu)
        for sect in self.draw_sections():
            menu = sect.get_submenu()
            for subsect in self.draw_subsections(menu):
                menu.append(subsect)
                sub_menu = subsect.get_submenu()
                for tips in self.draw_tips_menu(menu, sub_menu):
                    sub_menu.append(tips)
            sections_menu.append(sect)

    def entry_icon_event(self, widget, icon, event):
        # Using 'event.button' I can know which mouse button was used
        if icon.value_name == "GTK_ENTRY_ICON_PRIMARY":
            print "To Console"
        elif icon.value_name == "GTK_ENTRY_ICON_SECONDARY":
            new_tip_dialog = McmNewTipDialog()
            new_tip_dialog.run()
            if new_tip_dialog.response == gtk.RESPONSE_OK:
                self.tips_list.append(new_tip_dialog.new_tip)
                self.draw_menu_bar()
                self.tips.save(self.tips_list)
        return True

    def draw_sections(self):
        sections = []
        menu_items = []
        for tip in self.tips_list:
            sections.append(tip.section)
        sections = set(sections)
        for section in sections:
            mi = gtk.MenuItem(section)
            me = McmMenu(section)
            mi.set_submenu(me)
            mi.show()
            menu_items.append(mi)
        return menu_items

    def draw_subsections(self, sections_menu):
        subsections = []
        menu_items = []
        label = sections_menu.label
        for tip in self.tips_list:
            if label == tip.section:
                subsections.append(tip.subsection)
        subsections = set(subsections)
        for subsection in subsections:
            mi = gtk.MenuItem(subsection)
            me = McmMenu(subsection)
            mi.set_submenu(me)
            mi.show()
            menu_items.append(mi)
        return menu_items

    def draw_tips_menu(self, sections_menu, subsections_menu):
        tips = []
        menu_items = []
        sect_label = sections_menu.label
        subsect_label = subsections_menu.label
        for tip in self.tips_list:
            if subsect_label == tip.subsection and sect_label == tip.section:
                tips.append(tip)
        for tip in tips:
            mi = TipGtkMenuItem(tip.name, tip)
            mi.connect("activate", self.item_event)
            mi.show()
            menu_items.append(mi)
        return menu_items

    def draw_breadcrumb(self, tip):
        items = self.menu_bar.get_children()
        if len(items) > 1:
            self.menu_bar.remove(items[1])
            self.menu_bar.remove(items[2])
            self.menu_bar.remove(items[3])

        mi_section = gtk.MenuItem(tip.section)
        mi_subsection = gtk.MenuItem(tip.subsection)
        mi_name = gtk.MenuItem(tip.name)

        mi_section.show()
        mi_subsection.show()
        mi_name.show()

        sect_menu = McmMenu(tip.section)
        subsect_menu = McmMenu(tip.subsection)
        name_menu = McmMenu(tip.name)

        for sect in self.draw_sections():
            menu = sect.get_submenu()
            for subsect in self.draw_subsections(menu):
                menu.append(subsect)
                sub_menu = subsect.get_submenu()
                for tips in self.draw_tips_menu(menu, sub_menu):
                    sub_menu.append(tips)
            sect_menu.append(sect)

        for subsect in self.draw_subsections(sect_menu):
            subsect_menu.append(subsect)
            sub_menu = subsect.get_submenu()
            for tips in self.draw_tips_menu(sect_menu, sub_menu):
                sub_menu.append(tips)

        for tips in self.draw_tips_menu(sect_menu, subsect_menu):
            name_menu.append(tips)

        mi_section.set_submenu(sect_menu)
        mi_subsection.set_submenu(subsect_menu)
        mi_name.set_submenu(name_menu)

        self.menu_bar.append(mi_section)
        self.menu_bar.append(mi_subsection)
        self.menu_bar.append(mi_name)

    def item_event(self, widget):
        self.draw_breadcrumb(widget.tip)
        self.tips_entry.set_text(widget.tip.value)

    def update(self, filename=None):
        response = self.tips.update(filename)
        self.tips_list = self.tips.read()
        self.draw_menu_bar()
        return response

class HttpServerDialog(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(constants.glade_http)
        self.dialog = builder.get_object("http_server_dialog")
        self.dialog.connect('on_http_server_connect_toggled', self.start_server)
        self.dialog.connect('on_http_server_disconnect_toggled', self.stop_server)
        #self.http_server = McmHttpServerThread

    def run(self):
        self.dialog.run()
        self.dialog.destroy()

    def start_server(self):
        pass

    def stop_server(self):
        pass
