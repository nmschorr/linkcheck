from datetime import datetime
import logging
from time import perf_counter
import sys

class lc_utils(object):

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
        return logger

    def ck_bad_data(self, link):
        end_val = 0
        mylist = ['#', 'tel:+']
        for i in mylist:
            if i in link:
                end_val += 1
        return end_val

    def reset_timer(self, name, tstart):
        print(name, perf_counter() - tstart)
        tstart = perf_counter()
        return tstart

    def ck_status_code(self, response, parent_local):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        # goodcodes = [200]
        temp_url = response.url
        print("testing this now: ", temp_url)

        if response.status_code in err_codes:
            self.err_links.append((response.url, response.status_code, parent_local))
            return 1
        else:
            return 0  # ok

    def split_url(self, url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url

    def has_correct_suffix(self, link):
        goods = ['html',  'htm',  '/', 'php', 'asp', 'pl', 'com', 'net', 'org', 'css', 'py', 'rb', 'js'
            'jsp','shtml', 'cgi', 'txt']
        for g in goods:
            if link.endswith(g):
                return True
        return False

