# python 3

import sys
# from requests import *
# from selenium import webdriver
# from datetime import datetime
from src.config import *
import logging
import logging.handlers
from colorama import Fore

#############---------------------------------------- end of def

def remcruft(localink, mlist):
    res = 'good'
    for i in mlist:
        if i in localink:
            res = 'bad'
    #res = list(filter(lambda x: x in locallink, mlist))
    return res   # good or bad for now


def print_er(e):
    for er2 in e:
        print('error: ', er2)

def logr():
    logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logr = logging.getLogger('logr')
    formatter = logging.Formatter(
        '%(asctime)s-%(name)s-%(levelname)s: Message: %(message)s: Function: %(funcName)s',
        datefmt='%m%d%y-%H.%M%S')
    filehandle = logging.FileHandler(finame)
    filehandle.setFormatter(formatter)
    filehandle.setLevel(level=logging.DEBUG)

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    console.setLevel(level=logging.DEBUG)

    logr.setLevel(level=logging.DEBUG)
    logr.addHandler(filehandle)
    logr.addHandler(console)
    logging.getLogger('').addHandler(console)  # add to root
    logr.info('Completed configuring logger ')
    lev = logging.getLogger().getEffectiveLevel()
    print("\nLogging level is: ", lev)
    return logr