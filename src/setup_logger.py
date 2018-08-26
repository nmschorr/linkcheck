from datetime import datetime
import logging
from logging import getLogger
import sys

class this_logger(object):

    def setup_logger(self):
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
            #logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger = logging.getLogger('mainlogger')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s: Msg: %(message)s: Function: %(funcName)s',
                                      datefmt='%m%d%y-%H.%M%S')
        fname = 'E:\\pylogs\\Logger-' + timestp + '.log'
        filehandle = logging.FileHandler(fname)
        filehandle.setFormatter(formatter)
        filehandle.setLevel(level=logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level=logging.DEBUG)

        logger.setLevel(level=logging.DEBUG)
        logger.addHandler(filehandle)
        logger.addHandler(console)                       ##logging.getLogger('').addHandler(console)  # add to root
        logger.info('Completed configuring logger. Logging level is: '+ str(logging.getLogger().getEffectiveLevel()))
