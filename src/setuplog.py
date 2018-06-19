# python 3
from datetime import datetime
import logging
import sys
from selenium import webdriver

class makelogger(object):

    def setup_logger(self):
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
            #logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger1 = logging.getLogger('mainlogger')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s: Msg: %(message)s: Function: %(funcName)s',
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
        logger1.addHandler(console)                       ##logging.getLogger('').addHandler(console)  # add to root
        lev = logging.getLogger().getEffectiveLevel()
        logger1.info('Completed configuring logger. Logging level is: '+ str(lev))
        return logger1

    @staticmethod
    def start_driver():
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        return driver

    def __init__(self):
        None