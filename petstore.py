#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
import time
import ujson as json
import requests
import random, string
from args import get_args
from jinja2 import Environment, PackageLoader

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

def getprox():


    now = int(time.time())
    try:
        with open("actions.json") as actions:
            data = json.load(actions)
            checkedtime = data['proxfetchtimestamp']
    except IOError:
        data = {'proxfetchtimestamp': now - 86400}
        with open('actions.json', 'w') as outfile:
            json.dump(data, outfile)
        checkedtime = now - 86400
    if now - checkedtime >= 86400:
        log.info('Getting todays proxies')
        prox = requests.get(args.papi, timeout=5)
        file = open('proxynew.txt', "w+")
        file.write(prox.text)
        file.close()
        data = {'proxfetchtimestamp': now}
        with open('actions.json', 'w+') as outfile:
            json.dump(data, outfile)
    else:
        log.info('You have already fetched proxies today. Skipping')


def appendprox():
    log.info('Adding known good proxies')
    potato = open('temp.txt', 'a')
    prox = open('proxynew.txt', 'r')
    outfile = open("good.txt", "r+")
    for line in outfile:
        potato.write(line)
    for line in prox:
        potato.write(line)
    potato.write('\n')
    potato.close()
    outfile.close()

    log.info('Checking for duplicates')
    outfile = open("good.txt", "w")
    lines_seen = set()  # holds lines already seen
    for line in open("temp.txt", "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    os.remove('temp.txt')

def runchecks():
    log.info('Starting prox checks')
    os.system('python checker/start.py -t 3 -r 40 -f good.txt -o '
                     'checked/rmgood.txt -er -r 2 -mc 600 -bs 600 -m http')

    os.system('python checker/start.py -f good.txt -r 40 --kinancity -bs 600 '
                     '-o checked/kinangood.txt -er -r 2 -t 3 -mc 600 -m http')

    os.system('python checker/start.py -f good.txt -r 40 --clean -bs 600 -t 3 '
                     '-o checked/freshgood.txt -er -t 3 -r 2 -mc 600 -m http')
    log.info('Updating good.txt')

    infile = open("checked/freshgood.txt", "r")
    outfile = open("good.txt", "w+")
    outfile.writelines(infile)
    infile.close()
    outfile.close()

def addtemplates():
    if args.rmdirs is not None:
        log.info('replacing RM format proxies')
        for dir in args.rmdirs:
            infile = open("checked/freshgood.txt", "r")
            outfile = open(dir, "w+")
            outfile.writelines(infile)
            infile.close()
            outfile.close()


    if args.kinandir:
        log.info('Making kinan config from template')
        kinan = open("checked/kinangood.txt", "r")
        for line in kinan:
            proxies = line

        temp = Environment(
            loader=PackageLoader('petstore', 'templates')).get_template(
            'config.properties')
        rendered = temp.render(prox=proxies)
        outfile = open(args.kinandir, "w+")
        outfile.writelines(rendered)
        outfile.close()
        kinan.close()

    if args.kinanuser:
        log.info('Making kinan start script')
        rand = ''.join(random.choice(string.ascii_letters) for x in range(4))
        user = args.kinanuser + rand

        if args.kinanstartdir:
            temp = Environment(
                loader=PackageLoader('petstore', 'templates')).get_template(
                'start.sh')
            rendered = temp.render(user=user)
            outfile = open(args.kinanstartdir, "w+")
            outfile.writelines(rendered)
            outfile.close()

        else:
            log.info('Kinan user configured, but no directory for start.sh')



if __name__ == '__main__':
    #getprox()
    appendprox()
    runchecks()
    addtemplates()
