#!/usr/bin/python
# -*- coding: utf-8 -*-
import configargparse
import os
import sys


def get_args():

    configfile = []
    if '-cf' not in sys.argv and '--config' not in sys.argv:
        configfile = [os.getenv('CONFIG', os.path.join(
            os.path.dirname(__file__), 'config/config.ini'))]
    parser = configargparse.ArgParser(
        default_config_files=configfile)

    parser.add_argument(
        '--papi',
        default=False
        )
    parser.add_argument(
        '--rmdir',
        default=False
        )
    parser.add_argument(
        '--corsdir',
        required=True
        )
    parser.add_argument(
        '--kinandir',
        required=True
        )