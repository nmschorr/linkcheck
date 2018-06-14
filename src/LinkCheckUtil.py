# python 3

import sys
# from requests import *
# from selenium import webdriver
from datetime import datetime
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

    #############---------------------------------------- end of def

def print_er(err):
    for er2 in err:
        print('error: ', er2)

    #############---------------------------------------- end of def

def writefirstset_tofile(firstSetLinks):
    timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
    basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
    filen1_h = open(basefile, 'w')  #
    for b in firstSetLinks:
        filen1_h.write(b[0] + lnfeed)
    filen1_h.close()

    #############---------------------------------------- end of def

def writebig(big_err_list_final):
    print("inside writebig")
    timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
    bigerr_file = 'E:\\pylogs\\BIG_errs' + timenow + '.txt'
    bigerr_h = open(bigerr_file, 'w')  #
    for b in big_err_list_final:
        bigerr_h.write(b + lnfeed)
    bigerr_h.close()
