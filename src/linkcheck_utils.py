import logging, sys
from datetime import datetime
from time import perf_counter
from urllib.parse import urlsplit

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

    def check_for_bad_data(self, this_link, parent_local, any_link_local, done_links_glob_sing=[]):
        has_bad_data = lc_utils().ck_bad_data(this_link)  #check for bad data
        link_eq_parent = bool(this_link == parent_local)
        good_suffix = lc_utils().has_correct_suffix(this_link)  #check suffix
        in_any_local = bool(this_link in [i[0] for i in any_link_local])
        done_links_glob_sing.append(this_link)  ## add to main done list
        return has_bad_data, link_eq_parent, good_suffix, in_any_local, done_links_glob_sing

    def add_to_any_base(self, this_link, parent_local, base_links_glob2=[]): #Adding this base link to base glob
        _IN_BASE_GLOB = bool(this_link in [i[0] for i in base_links_glob2])
        if not _IN_BASE_GLOB:  # if not already in this
            base_links_glob2.append((this_link, parent_local))
            #self.logger.debug("Adding this base link to base glob: " + this_link)
        return base_links_glob2

    def add_to_any(self, this_link, parent_local, any_link_glob2=[]): #Adding this base link to any glob
        in_any_glob = bool(this_link in [i[0] for i in self.any_link_glob2])
        if not in_any_glob:
            any_link_glob2.append((this_link, parent_local))
        return any_link_glob2




    def reset_timer(self, name, tstart):
        print(name, perf_counter() - tstart)
        tstart = perf_counter()
        return tstart

    @staticmethod
    def split_url(url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url

    @staticmethod
    def has_correct_suffix(link):
        goods = ['html',  'htm',  '/', 'php', 'asp', 'pl', 'com', 'net', 'org', 'css', 'py', 'rb', 'js'
            'jsp','shtml', 'cgi', 'txt']
        for g in goods:
            if link.endswith(g):
                return True
        return False

    @staticmethod
    def ck_base(this_link, thebase_part, base_links_local=[]):
        _IS_BASE = bool(thebase_part in this_link)
        in_base_local = bool(this_link in [i for i in base_links_local])
        return _IS_BASE, in_base_local

    @staticmethod
    def divide_url(parent_local):
        thebase_part_local = None
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            print(e)
        return thebase_part_local

    @staticmethod
    def print_errs(errlinks=[]):
        fin_list = []
        answer_string, e = '', ''
        if errlinks:
            errs = list(set(errlinks))
            er_len = len(errs)
            print("\nTotal errors: ", er_len)
            print("-------------- Here are the errors ------------- :")
            errs2 = sorted(errs, key=lambda x: x[0])  # sort on first
            for e in errs2:
                p0 = "BAD LINK: "
                p1 = " REASON: "
                p2 = " REFERRING PAGE: "
                st0,st1,st2 = str(e[0]),str(e[1]),str(e[2])
                answer_string = '\n' + p0 + st0 + p1 + st1 + p2 + st2 + '\n\n'
                fin_list.append(answer_string)
        return fin_list
