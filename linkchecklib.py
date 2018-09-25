
from urllib.parse import urlsplit
from requests_html import HTMLSession
#import logging


_MYDEBUG = 0


class mem(object):
    err_links = None
    done_ln_gl_sing = None
    any_link_glob = None
    base_lnks_g = None

    def __init__(self):
        err_links = []
        done_ln_gl_sing = []
        any_link_glob = []
        base_lnks_g = []

class LinkCheckLib(object):

    def __init__(self):
        memg = mem()
        #memg.__init__()
        self.memg = memg
        tlds_list = []

        self.memg.err_links = memg.err_links
        self.memg.done_ln_gl_sing = memg.done_ln_gl_sing
        self.memg.any_link_glob = memg.any_link_glob
        self.memg.base_lnks_g = memg.base_lnks_g
        self.tlds_list = tlds_list


    #-----------------------------------------------------------------------------

    @classmethod
    def ispar(cls, thisln, par_loc):   # is it a parent? part of the main website?
        if par_loc in thisln:
            return True
        else:
            return False # is it the parent?

    #-----------------------------------------------------------------------------
    @staticmethod
    def write_some_contents(contnt, nme):
        fname = str(nme) + ".log"
        wf = open(fname, "w")
        for i in contnt:
            wf.write(i)
            wf.close()
    #-----------------------------------------------------------------------------


    def ck_g(self, this_link):
        return bool(this_link in [i[0] for i in self.memg.any_link_glob])

    #-----------------------------------------------------------------------------

     
    def _DONE_YET(self, this_link):
        return bool(this_link in self.memg.done_ln_gl_sing)
    #-----------------------------------------------------------------------------

    @classmethod
    def ck_loc(cls, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?
    #-----------------------------------------------------------------------------

    
    def return_errors(self):

        finlist = []
        if self.memg.err_links is None:
            self.memg.err_links = []
        if self.memg.err_links:
            answer_string, e, fin_list = '', '', []
            try:
                if self.memg.err_links:
                    errs = list(set(self.memg.err_links))
                    self.memg.err_links.clear()
                    er_len = len(errs)
                    nstring = "\nTotal errors: " + str(er_len) + " Here are the errors ---:"
                    LinkCheckLib.myprint(nstring)
                    errs22 = sorted(errs, key=lambda x: x[0])  # sort on first
                    errs.clear()

                    errs2 = set(errs22)
                    errs22.clear()
                    self.memg.err_links.clear()
                    for e in errs2:
                        an0, an1, an2 = str(e[0]), str(e[1]), str(e[2])

                        answer_string = [an0, an1, an2]
                        fin_list.append(answer_string)
                        finlist = fin_list.copy()
                        LinkCheckLib.myprint(str(answer_string))
                else:
                    fin_list = [answer_string]
                    finlist = fin_list.copy()
                    print("len of finlist: ", str(len(finlist)))
                    del fin_list
                errs2.clear()
            except Exception as e:
                LinkCheckLib.myprint('Exception print_errs: ' + str(e))
            return finlist
        else:
            return []

    # -----------------------------------------------------------------------
    @classmethod
    def ck_base(cls, this_link, thebase_part, base_links_local=None):
        if base_links_local is None:
            base_links_local = []
        _IS_BASE = False
        in_base_loc = False
        try:
            _IS_BASE = bool(thebase_part in this_link)

            if _IS_BASE:
                early_dollar = cls.has_early_dollar(this_link, thebase_part)
                if early_dollar:
                    _IS_BASE = False  # base is embedded after something like twitter.com
                    return _IS_BASE, in_base_loc

            if base_links_local:
                in_base_loc = bool(this_link in [i for i in base_links_local])
        except Exception as e:
            print("Exception ck_base: " + str(e))
        return _IS_BASE, in_base_loc
    #-----------------------------------------------------------------------

    def do_response(self, a_link, p_link):
        t_err = 0
        resp = "0"
        try:
            if a_link not in self.memg.done_ln_gl_sing:
                LinkCheckLib.myprint("-starting-get_home_links - just got this link: " + str(a_link))
                self.memg.done_ln_gl_sing.append(a_link)  ## add to main done list
                session = HTMLSession()
                resp = session.get(a_link)
                t_err = self.ck_status_code(resp, a_link)  ## if there's    an error
                session.close()

        except Exception as e:
            self.handle_exc(e, a_link, p_link)
            LinkCheckLib.myprint("GOT AN EXCEPTION inside do_response")
            return resp, t_err
        return resp, t_err

    #----------------------------------------------------------------------get_links-

    def ck_bad_data(self, dlink):
        LinkCheckLib.myprint("!!!!!=============inside ck_bad_data. val of link: " + dlink)
        good_or_bad = 0
        mylist = ['#', 'tel:+']
        try:
            for item in mylist:
                if item in dlink:
                    good_or_bad += 1
        except Exception as e:
            LinkCheckLib.myprint("Exception ck_bad_data: " + str(e))

        good_suffix = self.has_correct_suffix(dlink)  # check suffix
        LinkCheckLib.myprint("!inside ck_bad_data: " + str(good_or_bad) + ' ' + str(good_suffix))
        return good_or_bad, good_suffix

    # #-----------------------------------------------------------------------------

    # def check_for_bad_data(self, alink):
    #     print("")
    #     return
    #-----------------------------------------------------------------------------

    def has_correct_suffix(self, link):
        answ, answ2, final_answer = False, False, False

        try:
            answ = self.check_sufx(link)
            goods = ['html', 'htm', '/', 'php', 'asp', 'pl', 'com', 'net', 'org',
                     'css', 'py', 'rb', 'js','jsp', 'shtml',
                     'cgi', 'txt', 'edu', 'gov']
            for g in goods:
                if link.endswith(g):
                    answ2 = True
            if answ == True or answ2 == True:
                final_answer = True
        except Exception as e:
            LinkCheckLib.myprint("Exception in has_correct_suffix: " + str(e))
        return final_answer
    #-----------------------------------------------------------------------------

    @staticmethod
    def myprint(print_str):
        global _MYDEBUG
        if not _MYDEBUG:
            print(print_str)
            #logging.info(print_str)
        else:
            #logging.debug(print_str)
            print(print_str)


    #-----------------------------------------------------------------------------

    # @classmethod
    # def myprinter(cls, print_str):
    #     global _MYDEBUG
    #     if not _MYDEBUG:
    #         logging.info(print_str)
    #     else:
    #         logging.debug(print_str)

    #-----------------------------------------------------------------------------

    def load_tlds(self):
        with open('tlds-alpha-by-domain.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                self.tlds_list.append((currentPlace.lower()))
    #-----------------------------------------------------------------------------

    def check_sufx(self, sufx):
        low_sufx = str(sufx).lower()
        if low_sufx in self.tlds_list:
            return True
        else:
            return False
    #-----------------------------------------------------------------------------

    def handle_exc( self, e, link, plink):
        tempstr = str(e)
        LinkCheckLib.myprint('!!!!! Inside handle_exc. Error------------------\n' + tempstr)
        if "Document is empty" in tempstr:  # for mp3 and similar files
            return
        if "object has no attribute" in tempstr:  # for mp3 and similar files
            return
        elif link not in self.memg.err_links:
            self.memg.err_links.append((link, tempstr[:42], plink))
    #-----------------------------------------------------------------------------


    def ck_status_code(self, response, tpar):
        try:
            tlink = response.html.url
            err_codes = [400, 404, 408, 409]
            if response.status_code in err_codes:
                if tlink not in self.memg.err_links:
                    self.memg.err_links.append((tlink, response.status_code, tpar))
                return 1
            else: return 0  # ok
        except Exception as e:
            LinkCheckLib.myprint("Exception in ck_status_code: " + str(e))

    #-----------------------------------------------------------------------------

    
    @classmethod
    def ckaddymore(cls, addy):
        one = 'http://'
        two = 'https://'
        needprefix = True
        if addy[0:7]==one:
            needprefix = False
        if addy[0:8] == two:
            needprefix = False
        if needprefix:
            full_addy = one + addy
        else:
            full_addy = addy
        return full_addy
    #-----------------------------------------------------------------------------

    
    @classmethod
    def has_early_dollar( cls, clink, base_p):
        print("in hasearlydollar: ", clink, " ", base_p)
        bp = clink.index(base_p)
        if "$" or "?" or "#" in clink:
            if (clink.index("$") < bp) or (clink.index("?") < bp) or (clink.index("#") < bp):
                ## if $ or # or ? before base link
                return True     ## it's before base link - not good
            else:
                return False     # there's a $ sign but it's ok
        else:
            return False
    #-----------------------------------------------------------------------------

    @classmethod
    def divide_url(cls, parent_local):
        thebase_part_local = ""
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            LinkCheckLib.myprint('Exception divide_url: ' + str(e))

        return thebase_part_local

    # def reset_timer( name, tstart):
    #     LinkCheckLib.myprint(name, perf_counter() - tstart)
    #     #tstart = perf_counter()
    #     return tstart
