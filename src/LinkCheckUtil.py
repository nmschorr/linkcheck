# python 3

from datetime import datetime
from src.config import *
import logging
import sys

    #############---------------------------------------- end of def

class linkckutil(object):

    def remcruft(self, localink, mlist):
        res = 'good'
        for i in mlist:
            if i in localink:
                res = 'bad'
        #res = list(filter(lambda x: x in locallink, mlist))
        return res   # good or bad for now

        #############---------------------------------------- end of def

    def print_er(self, err):
        for er2 in err:
            print('error: ', er2)

        #############---------------------------------------- end of def

    def writefirstset_tofile(self, firstSetLinks):
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
        filen1_h = open(basefile, 'w')  #
        for b in firstSetLinks:
            filen1_h.write(b[0] + lnfeed)
        filen1_h.close()

        #############---------------------------------------- end of def

    def writebig(self, big_err_list_final):
        print("inside writebig")
        timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
        bigerr_file = 'E:\\pylogs\\BIG_errs' + timenow + '.txt'
        bigerr_h = open(bigerr_file, 'w')  #
        for b in big_err_list_final:
            bigerr_h.write(b + lnfeed)
        bigerr_h.close()

    #############---------------------------------------- end of def

    #############---------------------------------------- end of def
    def setuplogger(self):

        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger1 = logging.getLogger('__name__')
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: Message: %(message)s: Function: %(funcName)s',
            datefmt='%m%d%y-%H.%M%S')
        fname = 'E:\\pylogs\\Logger-' + timestp + '.log'
        filehandle = logging.FileHandler(fname)
        filehandle.setFormatter(formatter)
        filehandle.setLevel(level=logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level=logging.DEBUG)


        logger1.setLevel(level=logging.DEBUG)
        logger1.addHandler(filehandle)
        logger1.addHandler(console)
        ##logging.getLogger('').addHandler(console)  # add to root

        lev = logging.getLogger().getEffectiveLevel()
        logger1.info('Completed configuring logger. Logging level is: '+ str(lev))
        return logger1

    def __init__(self, adict):
        self.__dict__.update(adict)   #globals
        #_logger = self.setuplogger()

    #def main(self):




