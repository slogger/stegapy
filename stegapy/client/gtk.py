#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""GUI GTK+3 client for audio-steganography

Copyright 2014 Maxim Syrykh
"""

from gi.repository import Gtk, GObject
from stegapy.parsers.extra_file import ExtraFile
from stegapy.models.container import BaseContainer
from stegapy.errors import ContainerError
from stegapy import config


class Window(Gtk.Window):
    '''Main window'''
    def __init__(self):
        # Set title
        Gtk.Window.__init__(self, title="Steganography tool")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # HIDE SECTION

        hide_options = Gtk.ListBox()
        hide_options.set_selection_mode(Gtk.SelectionMode.NONE)

        # render container formats
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Container format", xalign=0)
        format_store = Gtk.ListStore(str)
        for f in config['formats']:
            format_store.append([f])
        combo = Gtk.ComboBox.new_with_model(format_store)
        combo.connect("changed", self.on_format_changed)
        combo.set_active(0)
        combo.set_size_request(130, 25)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.props.valign = Gtk.Align.CENTER
        combo.add_attribute(renderer_text, "text", 0)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)
        hide_options.add(row)

        # Choose container file button
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Choose container", xalign=0)
        sub_title = Gtk.Label("Requires WAV files", xalign=0)
        child_vbox.pack_start(title, True, True, 0)
        child_vbox.pack_start(sub_title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Choose file")
        choose_file_btn.connect("clicked", self.on_wav_choosed, sub_title)
        choose_file_btn.set_size_request(130, 25)
        hbox.pack_start(choose_file_btn, False, True, 0)
        hide_options.add(row)

        # Steganography method switch
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Steganography method", xalign=0)
        steganomethod_store = Gtk.ListStore(str)
        for steganomethod in config['steganomethods']:
            steganomethod_store.append([steganomethod])
        combo = Gtk.ComboBox.new_with_model(steganomethod_store)
        combo.connect("changed", self.on_steganomethod_changed)
        combo.set_size_request(130, 25)
        combo.set_active(0)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)
        hide_options.add(row)

        # Choose message file button
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Choose message", xalign=0)
        sub_title = Gtk.Label("Requires any files", xalign=0)
        child_vbox.pack_start(title, True, True, 0)
        child_vbox.pack_start(sub_title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Choose file")
        choose_file_btn.connect("clicked", self.on_msg_choosed, sub_title)
        choose_file_btn.set_size_request(130, 25)
        hbox.pack_start(choose_file_btn, False, True, 0)
        hide_options.add(row)

        # Start hiding
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Hide message", xalign=0)
        child_vbox.pack_start(title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Hide")
        choose_file_btn.connect("clicked", self.on_hide)
        choose_file_btn.set_size_request(130, 25)
        hbox.pack_start(choose_file_btn, False, True, 0)
        hide_options.add(row)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        stack.add_titled(hide_options, "hide", "Hide")

        ## UNHIDE SECTION

        unhide_options = Gtk.ListBox()
        unhide_options.set_selection_mode(Gtk.SelectionMode.NONE)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Container format", xalign=0)
        format_store = Gtk.ListStore(str)
        for f in config['formats']:
            format_store.append([f])
        combo = Gtk.ComboBox.new_with_model(format_store)
        combo.connect("changed", self.on_format_changed)
        combo.set_active(0)
        combo.set_size_request(130, 25)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.props.valign = Gtk.Align.CENTER
        combo.add_attribute(renderer_text, "text", 0)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        unhide_options.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Choose container", xalign=0)
        sub_title = Gtk.Label("Requires WAV files", xalign=0)
        child_vbox.pack_start(title, True, True, 0)
        child_vbox.pack_start(sub_title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Choose file")
        choose_file_btn.connect("clicked", self.on_wav_choosed, sub_title)
        choose_file_btn.set_size_request(130, 25)
        hbox.pack_start(choose_file_btn, False, True, 0)

        unhide_options.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        label = Gtk.Label("Steganography method", xalign=0)
        steganomethod_store = Gtk.ListStore(str)
        for steganomethod in config['steganomethods']:
            steganomethod_store.append([steganomethod])
        combo = Gtk.ComboBox.new_with_model(steganomethod_store)
        combo.connect("changed", self.on_steganomethod_changed)
        combo.set_size_request(130, 25)
        combo.set_active(0)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        unhide_options.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Unhide message", xalign=0)
        child_vbox.pack_start(title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Unhide")
        choose_file_btn.connect("clicked", self.on_unhide)
        choose_file_btn.set_size_request(130, 25)
        hbox.pack_start(choose_file_btn, False, True, 0)

        unhide_options.add(row)

        stack.add_titled(unhide_options, "unhide", "Unhide")

        ## INFO SECTION

        info_options = Gtk.ListBox()
        info_options.set_selection_mode(Gtk.SelectionMode.NONE)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        child_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(child_vbox, True, True, 0)

        title = Gtk.Label("Choose container", xalign=0)
        sub_title = Gtk.Label("Requires WAV files", xalign=0)
        child_vbox.pack_start(title, True, True, 0)
        child_vbox.pack_start(sub_title, True, True, 0)

        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER

        choose_file_btn = Gtk.Button("Choose container")
        choose_file_btn.connect("clicked", self.on_show_info)
        hbox.pack_start(choose_file_btn, False, True, 0)

        info_options.add(row)

        stack.add_titled(info_options, "info", "Info")

        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)

        vbox.pack_start(stack_switcher, True, True, 0)
        vbox.pack_start(stack, True, True, 0)

    def on_steganomethod_changed(self, combo):
        """Changed tool for steganography"""
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            stehanomethod = model[tree_iter][0]
            _stegtool = __import__("stegapy.steganography.%s" %
                                   (stehanomethod),
                                   fromlist=[stehanomethod])
            self.stegtool = getattr(_stegtool, stehanomethod)

    def on_format_changed(self, combo):
        """Changed libs for container"""
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            container_format = model[tree_iter][0]
            _parser = __import__("stegapy.parsers.%s" % (container_format),
                                 fromlist=[container_format])
            self.Container = getattr(_parser, container_format)

    def on_wav_choosed(self, widget, title):
        """Open dialog to choose container"""
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_wav_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.original = self.Container(dialog.get_filename())
                if len(dialog.get_filename()) > 17:
                    title.set_text('...%s' % (dialog.get_filename()[-20:]))
                else:
                    title.set_text(dialog.get_filename())
                dialog.destroy()
            except ContainerError as e:
                dialog.destroy()
                self.push_message(str(e))
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            self.push_message("Please, choose container file")

    def on_msg_choosed(self, widget, title):
        """Open dialog to choose message"""
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_any_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            try:
                self.message = ExtraFile(dialog.get_filename())
                if len(dialog.get_filename()) > 17:
                    title.set_text('...%s' % (dialog.get_filename()[-20:]))
                else:
                    title.set_text(dialog.get_filename())
            except PermissionError:
                self.push_message("Permission denied")
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            self.push_message("Please, choose message file")

    def on_hide(self, widget):
        """Hide information"""
        if hasattr(self, "original") and hasattr(self, "message"):
            dialog = Gtk.FileChooserDialog("Please, save a file", self,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE,
                                            Gtk.ResponseType.OK))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                filename = dialog.get_filename()
                dialog.destroy()
                # progressbar = ProgressBarWindow()
                # self.push_message("Please walt", 'Work on!')
                try:
                    output_data = self.stegtool(self.original).encode(self.message)
                    opres = self.Container(filename, read=False).write(output_data)
                    if opres == 'OK':
                        self.push_message("Success hide", opres)
                except Exception:
                    self.push_message("Something go wrong")
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.push_message("Please, save file")
        else:
            self.push_message("You should choose container and message files")

    def on_unhide(self, widget):
        """Unhide information"""
        if hasattr(self, "original"):
            # self.push_message("Please walt", "Start unhiding!")
            dialog = Gtk.FileChooserDialog("Please save a file", self,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL,
                                            Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE,
                                            Gtk.ResponseType.OK))
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                # TODO: add progress bar
                filename = dialog.get_filename()
                dialog.destroy()
                try:
                    hide_content = self.stegtool(self.original).decode()
                    if len(hide_content) != 0:
                        opcode = BaseContainer(filename).write(hide_content)
                        if opcode == 'OK':
                            self.push_message("Success unhide", "OK")
                        else:
                            self.push_message("Something go wrong")
                    else:
                        self.push_message('Message not found')
                except ContainerError as e:
                    self.push_message(str(e))
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                self.push_message("Please, save file")
        else:
            self.push_message("You should choose container file")

    def on_show_info(self, widget):
        """Diving into container and show info about his"""
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_wav_filters(dialog)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            params = self.Container(dialog.get_filename(),
                                    valid=False).get_params()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()
            self.push_message("Please, choose file")

        dialog.destroy()
        info = InfoDialog(self, params)
        show_info_dialog = info.run()
        info.destroy()

    def push_message(self, message, title="Warning"):
        """Show message box"""
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, title)
        dialog.format_secondary_text(
            message)
        dialog.run()
        # Это надо что-бы оно закрывалось
        dialog.destroy()

    def add_wav_filters(self, dialog):
        """Filter wav files"""
        filter_wav = Gtk.FileFilter()
        filter_wav.set_name("WAV files")
        filter_wav.add_mime_type("audio/wav")
        dialog.add_filter(filter_wav)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def add_any_filters(self, dialog):
        """Filter any files"""
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


class InfoDialog(Gtk.Dialog):
    """Create dialog with table, show container params"""
    def __init__(self, parent, raw_param):
        Gtk.Dialog.__init__(self, "Dive into WAV", parent, 0,
                            (Gtk.STOCK_CLOSE, Gtk.ResponseType.OK))

        liststore = Gtk.ListStore(str, str)
        for param, value in raw_param.items():
            liststore.append([param, str(value)])

        treeview = Gtk.TreeView(model=liststore)

        renderer_text = Gtk.CellRendererText()
        column_params = Gtk.TreeViewColumn("Key", renderer_text, text=0)
        treeview.append_column(column_params)

        renderer_value = Gtk.CellRendererText()

        column_value = Gtk.TreeViewColumn("Value", renderer_value, text=1)
        treeview.append_column(column_value)

        box = self.get_content_area()
        box.add(treeview)
        self.show_all()
