#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os, sys
import errno
import subprocess
from args import get_args

# create logger

log = logging.getLogger('Poracle')
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(module)s]' +
                              '[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


args = get_args()

def petstore():

    log.info('Started doing things!')



if __name__ == '__main__':
    petstore()