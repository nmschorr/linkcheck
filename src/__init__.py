# python 3

from datetime import datetime
import logging
import sys

args_file = "E:/PycharmProjects/linkcheck/src/runargs.txt"

h4  = 'schorrmedia.com/'
h3    = 'repercussions.com/'
h2   = 'alexforecast.blogspot.com/'
h1   = 'azuresults.com/'
myargs = [h1, h2, h3]


# #home1   = 'cosmictoys.blogspot.com/'
# home1   = 'promatch.org/'
# home1   = 'clarinetinstitute.com/'
# home1   = 'repercussions.com/'

lnfeed = '\n'
any_link_glob, base_links_glob, done_links_glob_singles, err_links   = [], [], [], []
__all__ = ['args_file', 'lnfeed','the_logger','any_link_glob', 'base_links_glob', 'done_links_glob_singles', 'err_links']

def setup_logger():
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
    logger1.info('Completed configuring logger. Logging level is: '+ str(logging.getLogger().getEffectiveLevel()))
    return logger1


print("In " + str(super) + " __init__.py")
the_logger = setup_logger()

