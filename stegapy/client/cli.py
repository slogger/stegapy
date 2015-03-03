#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""CLI client for audio-steganography

Copyright 2014 Maxim Syrykh
"""

import argparse
from stegapy.models.container import BaseContainer
from stegapy.parsers.extra_file import ExtraFile
from stegapy.errors import InputError
import stegapy.config as config


def parse_args():
    """Parsing cli-arguments"""
    parser = argparse.ArgumentParser(
        prog='stegapy.client.cli',
        description='',
        epilog='Copyright 2014 Maxim Syrykh')

    parser.add_argument('format',
                        choices=config.formats,
                        default='WAV',
                        help='container format')

    # parser.add_argument('mode',
    #                     choices=['hide', 'unhide'],
    #                     help='work mode')

    parser.add_argument('input',
                        help='path to container file')

    parser.add_argument('method',
                        choices=config.steganomethods,
                        default='LSB',
                        help='steganography method')


    subparsers = parser.add_subparsers(help='sub-command help', dest='mode')

    subparsers_hide = subparsers.add_parser('hide',
                                            help='Hiding work mode')

    subparsers_hide.add_argument('message',
                                 default='',
                                 help='Message file')

    subparsers_unhide = subparsers.add_parser('unhide',
                                              help='Unhide work mode')


    parser.add_argument('output',
                        default='',
                        help='Output file')

    return parser.parse_args()


def main():
    '''Main logic block'''
    args = parse_args()
    # Import needs modules
    try:
        _parser = __import__("stegapy.parsers.%s" % args.format,
                             fromlist=[args.format])
        Container = getattr(_parser, args.format)
        _stegtool = __import__("stegapy.steganography.%s" % args.method,
                               fromlist=[args.method])
        stegtool = getattr(_stegtool, args.method)
    except ImportError as e:
        exit("Module %s not found" % e.args[0][16:])

    def hide(input_name, message, output_name):
        """Hide method"""
        input_data = Container(input_name)
        add_file = ExtraFile(message)
        output_data = stegtool(input_data).encode(add_file)
        output_file = Container(output_name, read=False, valid=False).write(output_data)

    def unhide(container_name, output_name):
        """Unhide method"""
        input_data = Container(container_name)
        print('START decoding')
        hide_content = stegtool(input_data).decode()
        print('START unhiding')
        output_file = BaseContainer(output_name).write(hide_content)
        print('yeee')

    # Run hide or unhide method
    if args.mode == 'hide':
        hide(args.input, args.message, args.output)
    else:
        unhide(args.input, args.output)

# Run the script.
if __name__ == '__main__':
    main()
    # print(parser.parse_args(['WAV', 'path', ]))
