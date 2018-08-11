# python 3

from datetime import datetime
import logging
import sys

__all__ = ['home1', 'full_addy', 'lnfeed', 'ercodes', 'badlist',
           'the_logger','any_link_glob', 'base_links_glob', 'done_links_glob', 'err_links' ]

#home1   = 'cosmictoys.blogspot.com/'
home1   = 'repercussions.com/'
home1   = 'clarinetinstitute.com/'
home1   = 'alexforecast.blogspot.com/'
home1   = 'schorrmedia.com/'

full_addy = 'http://' + home1

lnfeed = '\n'
ercodes = [400, 404, 408, 409, 501, 502, 503]
badlist = ['#','com/#', '?', 'blogger.com', '/search', 'javascript:void(0)', 'widgetType','mailto:']
any_link_glob, base_links_glob, done_links_glob, err_links   = [], [], [], []

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
    lev = logging.getLogger().getEffectiveLevel()
    logger1.info('Completed configuring logger. Logging level is: '+ str(lev))
    return logger1


print("In " + str(super) + " __init__.py")
the_logger = setup_logger()


#driver = object# def start_driver():
#     tdriver = webdriver.Firefox()
#     print('Driver session id: ' + tdriver.session_id)
#     tdriver.implicitly_wait(10)
#     return tdriver
