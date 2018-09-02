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
        console.setLevel(level=logging.INFO)

        logger.setLevel(level=logging.DEBUG)
        #logger.setLevel(level=logging.INFO)
        logger.addHandler(filehandle)
        logger.addHandler(console)                       ##logging.getLogger('').addHandler(console)  # add to root
        logger.info('Completed configuring logger. Logging level is: '+ str(logging.getLogger().getEffectiveLevel()))

        return logger

    @staticmethod
    def ck_bad_data(dlink):
        #print("!!!!!=============inside ckbaddata. val of link: ", dlink)
        end_val = 0
        mylist = ['#', 'tel:+']
        try:
            for i in mylist:
                if i in dlink:
                    end_val += 1
        except Exception as e: print("ck_bad_data: ", str(e))

        good_suf = lc_utils().has_correct_suffix(dlink)  # check suffix
        #print("!inside enval: ", end_val, good_suf)
        return end_val, good_suf

    @staticmethod
    def check_for_bad_data(alink, done_lnks_gl=None):
        try:
            if done_lnks_gl:
                done_lnks_gl.append(alink)  ## add to main done list
            else:
                done_lnks_gl = [alink]
        except Exception as e:
            print("check_for_bad_data: ", str(e))
        return done_lnks_gl

    @staticmethod
    def add_any_bse_g(zlink, parent_local, base_links_glob2=None): #Adding this base link to base glob
        try:
            if base_links_glob2:
                _IN_BASE_GLOB = bool(zlink in [i[0] for i in base_links_glob2])
                if not _IN_BASE_GLOB:  # if not already in this
                    base_links_glob2.append((zlink, parent_local))
                    #print("Adding this base link to base glob: " + zlink)
            else:
                base_links_glob2= [(zlink, parent_local)]

        except Exception as e:
            print("add_any_bse_g: ", str(e))
        return base_links_glob2

    @staticmethod
    def add_any(tlink, parent_local, any_link_loc=None, any_lnk_gl2=None): #Adding this base link to any glob
        try:
            if any_lnk_gl2:  # don't try without something there
                glob_bool = bool(tlink in [i[0] for i in any_lnk_gl2])
                if not glob_bool:
                    any_lnk_gl2.append((tlink, parent_local)) # add if not there
                    any_link_loc.append((tlink, parent_local))
            else:
                any_lnk_gl2 = [(tlink, parent_local)]  # make it if starting empty
                any_link_loc = [(tlink, parent_local)]
        except Exception as e:
            print("exception in add_any: ", str(e))
        return any_lnk_gl2, any_link_loc




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
        try:
            goods = ['html',  'htm',  '/', 'php', 'asp', 'pl', 'com', 'net', 'org', 'css', 'py', 'rb', 'js'
                'jsp','shtml', 'cgi', 'txt']
            for g in goods:
                if link.endswith(g):
                    return True
        except Exception as e:
            print("has_correct_suffix: ", str(e))
        return False

    @staticmethod
    def ck_base(this_link, thebase_part, base_links_local=None):
        _IS_BASE = False
        in_base_loc = False
        try:
            _IS_BASE = bool(thebase_part in this_link)
            if base_links_local:
                in_base_loc = bool(this_link in [i for i in base_links_local])
        except Exception as e:
            print("ck_base: ", str(e))
        return _IS_BASE, in_base_loc

    @staticmethod
    def divide_url(parent_local):
        thebase_part_local = None
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            print('divide_url: ', str(e))
            pass
        return thebase_part_local

    @staticmethod
    def print_errs(errlinks=None):
        if errlinks:
            answer_string, e, fin_list = '', '', []
            p0, p1, p2 = "BAD LINK: ", " REASON: ", " REFERRING PAGE: "
            try:
                if errlinks:
                    errs = list(set(errlinks))
                    er_len = len(errs)
                    print("\nTotal errors: ", er_len)
                    print("-------------- Here are the errors ------------- :")
                    errs2 = sorted(errs, key=lambda x: x[0])  # sort on first
                    for e in errs2:
                        st0,st1,st2 = str(e[0]),str(e[1]),str(e[2])
                        answer_string = p0 + st0 + p1 + st1 + p2 + st2 + '\n'
                        fin_list.append(answer_string)
                else:
                    fin_list = [answer_string]
            except Exception as e:
                print('print_errs: ', str(e))
            return fin_list
        else:
            return []
