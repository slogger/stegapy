#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""CLI client for audio-steganography

Copyright 2014-2015 Maxim Syrykh
"""

import argparse
from stegapy import config
from stegapy.models.container import BaseContainer
from stegapy.parsers.extra_file import ExtraFile
from stegapy.errors import InputError


def gui_mode(args):
    from gi.repository import Gtk, GObject
    from stegapy.client.gtk import Window
    win = Window()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


def hide_mode(args):
    try:
        _parser = __import__("stegapy.parsers.%s" % args.format,
                             fromlist=[args.format])
        Container = getattr(_parser, args.format)
        _stegtool = __import__("stegapy.steganography.%s" % args.method,
                               fromlist=[args.method])
        stegtool = getattr(_stegtool, args.method)
    except ImportError as e:
        exit("Module %s not found" % e.args[0][16:])

    source = Container(args.source)
    message = ExtraFile(args.message)
    output_data = stegtool(source).encode(message)
    output_file = Container(args.destination,
                            read=False,
                            valid=False).write(output_data)


def unhide_mode(args):
    try:
        _parser = __import__("stegapy.parsers.%s" % args.format,
                             fromlist=[args.format])
        Container = getattr(_parser, args.format)
        _stegtool = __import__("stegapy.steganography.%s" % args.method,
                               fromlist=[args.method])
        stegtool = getattr(_stegtool, args.method)
    except ImportError as e:
        exit("Module %s not found" % e.args[0][16:])

    input_data = Container(args.source)
    hide_content = stegtool(input_data).decode()
    output_file = BaseContainer(args.destination).write(hide_content)


# Run the script.
if __name__ == '__main__':
    # Parsing arguments
    parser = argparse.ArgumentParser(
        prog='stegapy.client.cli',
        description='',
        epilog='Copyright 2014-2015 {}'.format(config['__author__']))

    subparser = parser.add_subparsers(title="Work mode")

    gui = subparser.add_parser("gui", help="launch GTK3+ Gui")
    gui.set_defaults(func=gui_mode)

    hide = subparser.add_parser("hide")
    hide.add_argument('source',
                      help='path to container file')

    hide.add_argument('message',
                      help='message file')

    hide.add_argument('destination',
                      help='output file')

    hide.add_argument('--method', '-m',
                      choices=config['steganomethods'],
                      default='LSB',
                      help='Steganography method')

    hide.add_argument('--format', '-f',
                      choices=config['formats'],
                      default='WAV',
                      help='Choice format')
    hide.set_defaults(func=hide_mode)

    unhide = subparser.add_parser("unhide")
    unhide.add_argument('source',
                        help='Path to container file')

    unhide.add_argument('destination',
                        help='output file')

    unhide.add_argument('--method', '-m',
                        choices=config['steganomethods'],
                        default='LSB',
                        help='Steganography method')

    unhide.add_argument('--format', '-f',
                        choices=config['formats'],
                        default='WAV',
                        help='Choice format')
    unhide.set_defaults(func=unhide_mode)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.parse_args(['-h'])
