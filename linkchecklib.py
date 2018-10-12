
from urllib.parse import urlparse
from requests_html import HTMLSession
from random import random
from time import perf_counter
from config import conf_debug

class LinkCheckLib(object):

    def __init__(self):
        self.MAIN_DICT = dict()
        rand = str(random())[2:]

        self.BASENAME = "BURL" + rand
        self.BASENAMEwww = "BURLwww" + rand
        self.re = "re_" + rand
        self.rdone = "rdone_" + rand
        self.rany = "rany_" + rand
        self.rb = "rb_" + rand
        self.redirs = "redirs" + rand

        err_links = []   # final error links found
        done_ln_glob_singles = []
        any_link_glob = []
        base_lnks_g = []
        redirs_dat = []

        self.tlds_list = []
        self.MAIN_DICT.update({self.BASENAME: "init"})
        self.MAIN_DICT.update({self.BASENAMEwww: "init"})
        self.MAIN_DICT.update({self.re: err_links})
        self.MAIN_DICT.update({self.rdone: done_ln_glob_singles})
        self.MAIN_DICT.update({self.rany: any_link_glob})
        self.MAIN_DICT.update({self.rb: base_lnks_g})
        self.MAIN_DICT.update({self.redirs: redirs_dat})
        self.load_tlds()

        self.myprint("name of list: " + self.re)
        self.myprint("name of list: " + self.re)

    #-----------------------------------------------------------------------------
    def myprint(self, print_str ):
        mdebug = conf_debug
        if mdebug:
            print(print_str)

    # -----------------------------------------------------------------------------

    def load_tlds(self):
        filehandle = open('tlds-alpha-by-domain.txt', 'r')
        for line in filehandle:
            current_place = line[:-1]
            self.tlds_list.append((current_place.lower()))
        filehandle.close()

    #-----------------------------------------------------------------------------
    def rem_errs(self, tlinks=None):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdone)
        if tlinks is None:
            tlinks = []
        for link in tlinks:
            if link in done_ln_gl_sing:
                tlinks.remove(link)
        return tlinks

    #-----------------------------------------------------------------------------

    def ck_g(self, this_link):
        any_link_glob = self.MAIN_DICT.get(self.rany)
        return bool(this_link in [i[0] for i in any_link_glob])

    #-----------------------------------------------------------------------------
     
    def _DONE_YET(self, this_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdone)

        return bool(this_link in done_ln_gl_sing)
    #-----------------------------------------------------------------------------

    @classmethod
    def ck_loc(cls, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?
    #-----------------------------------------------------------------------------

    
    def return_errors(self):

        finlist = []
        err_links = self.MAIN_DICT.get(self.re)
        
        if err_links is None:
            err_links = []
        if err_links:
            answer_string, e, fin_list = '', '', []
            try:
                if err_links:
                    errs = list(set(err_links))
                    err_links.clear()
                    er_len = len(errs)
                    nstring = '\n' + "Total errors: " + str(er_len) + " Here are the errors ---:"
                    #self.myprint(nstring)
                    errs2 = sorted(errs, key=lambda x: x[0])  # sort on first

                    errs2 = set(errs2)
                    err_links.clear()
                    for e in errs2:
                        an0, an1, an2 = str(e[0]), str(e[1]), str(e[2])

                        answer_string = [an0, an1, an2]
                        fin_list.append(answer_string)
                        finlist = fin_list.copy()
                        #self.myprint(str(answer_string))
                else:
                    finlist = [answer_string]
                    self.myprint("len of finlist: " + str(len(finlist)))
            except Exception as e:
                self.myprint('Exception print_errs: ' + str(e))
            return finlist
        else:
            return []

        # -----------------------------------------------------------------------------

    def ispar(self, main_link):  # is it a parent? part of the main website?
        parsed = urlparse(main_link)
        if parsed.scheme != '':
            main_link = parsed.netloc

        par_loc = self.MAIN_DICT.get(self.BASENAME)
        par_locwww = self.MAIN_DICT.get(self.BASENAMEwww)
        if main_link == par_loc or main_link == par_locwww:
            return True
        else:
            return False  # is it the parent?
    # -----------------------------------------------------------------------
    def is_same_site_link(self, inlink):
        is_same_link = False
        par_loc = self.MAIN_DICT.get(self.BASENAME)
        par_locwww = self.MAIN_DICT.get(self.BASENAMEwww)

        (scheme, netloc, path, params, query, fragment) = urlparse(inlink)
        rebuild = netloc + path + params + query

        if (rebuild == par_loc) or (rebuild == par_locwww):
            is_same_link = True
            #self.myprint("--Is same: " + inlink + " found: " + par_loc + " and: " + par_locwww)

        return is_same_link

    # -----------------------------------------------------------------------

    def ck_base(self, in_link, base_links_local=None):

        this_link = in_link
        _IS_BASE = False
        in_base_loc = False

        one = 'http://'
        two = 'https:/'
        link_sub = in_link[0:7]
        if link_sub==one or link_sub==two:
           this_link = urlparse(in_link).netloc

        basepart = self.MAIN_DICT.get(self.BASENAME)
        basepartwww = self.MAIN_DICT.get(self.BASENAMEwww)

        this_sub = this_link[0:30]  # and this_link

        try:

            if this_link == basepart or this_link == basepartwww:
                _IS_BASE = True
                #self.myprint(  "--------------!!basepart or this_link == basepartwww!! _IS_BASE = True: " + this_link + " found : " + basepart + " in: " + this_link)
            elif this_sub == basepart[0:30] or this_sub == basepartwww[0:30]:
                _IS_BASE = True
                #self.myprint(  "--------------!!_IS_BASE = True " + this_link + " found : " + basepart + " in: " + this_link)
                if base_links_local:
                    in_base_loc = bool(this_link in [i for i in base_links_local])
                else:
                    self.myprint("did not find: " + this_link + " : " + basepart + " in: " + this_link)
        except Exception as e:
            self.myprint("Exception ck_base: " + str(e))
        return _IS_BASE, in_base_loc

    #-----------------------------------------------------------------------

    def do_response(self, a_link, p_link):
        rederdat = self.MAIN_DICT.get(self.redirs)
        done_ln_glob_singles = self.MAIN_DICT.get(self.rdone)
        any_link_gl = self.MAIN_DICT.get(self.rany)
        t_err = 0
        resp = None
        try:
            if a_link not in done_ln_glob_singles:
                if a_link not in any_link_gl:
                    done_ln_glob_singles.append(a_link)  ## add to main done list

                    session = HTMLSession()
                    resp = session.get(a_link, timeout=7.0)
                    self.myprint("THIS_LN: " + str(a_link) + " parent: " + p_link)
                    session.close()

                    code = resp.status_code
                    t_err = self.ck_status_code(a_link, p_link, code)  ## if there's    an error
                    self.myprint("LINK: in do_response: " + a_link + "  status code: " + str(code))

                    if code == 301:
                        rederdat.append(a_link)  # no need to recheck because it's automatic

        except Exception as e:
            self.myprint("GOT AN EXCEPTION inside do_response: " + str(e))
            self.handle_exc(e, a_link, p_link)
            pass
        self.MAIN_DICT.update({self.redirs: rederdat})
        return resp, t_err

    #----------------------------------------------------------------------get_links-

    def ck_bad_data(self, dlink):
        #self.myprint("!!!!!=============inside ck_bad_data. val of link: " + dlink)
        bad_counter = 0
        mylist = ['#', 'tel:+']
        try:
            for item in mylist:
                if item in dlink:
                    bad_counter += 1
        except Exception as e:
            self.myprint("Exception ck_bad_data: " + str(e))

        ckme = dlink[7:30]
        if "pinterest.com" in ckme:
            bad_counter += 1

        if "facebook.com" in ckme:
            if len(dlink) > 50:
                bad_counter += 1

        if "twitter.com" in ckme:
            if len(dlink) > 50:
                bad_counter += 1

        good_suffix = self.has_correct_suffix(dlink)  # check suffix
        #self.myprint("!inside ck_bad_data: " + str(good_or_bad) + ' ' + str(good_suffix))
        return bad_counter, good_suffix

    # #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------

    def has_correct_suffix(self, link):
        answ, answ2, final_answer = False, False, False

        try:
            answ = self.ck_tld_sufx(link)
            goods = ['html', 'htm', '/', 'php', 'asp', 'pl', 'com', 'net', 'org',
                     'css', 'py', 'rb', 'js','jsp', 'shtml',
                     'cgi', 'txt', 'edu', 'gov']
            for g in goods:      # in case tld list fails for some reason
                if link.endswith(g):
                    answ2 = True
            if answ == True or answ2 == True:
                final_answer = True
        except Exception as e:
            self.myprint("Exception in has_correct_suffix: " + str(e))
        return final_answer
    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------

    def ck_tld_sufx(self, alink):
        the_suf = alink.lower().split(".")[-1]
        if the_suf[-1] == '/':
            the_suf = the_suf[0:-1]

        if the_suf in self.tlds_list:
            return True
        else:
            return False
    #-----------------------------------------------------------------------------

    def handle_exc( self, e, link, plink):
        err_links = self.MAIN_DICT.get(self.re)

        the_err = str(e)
        self.myprint('!!!!! Inside handle_exc. Error------------------> ' + the_err)

        badlist = ["Document is empty","object has no attribute","ConnectionResetError","RemoteDisconnected"]

        for i in badlist:
            if i in the_err:  # for mp3 and similar files
                return

        if link not in err_links:
            err_links.append((link, the_err[:72], plink))
            self.MAIN_DICT.update({self.re:err_links})

    #-----------------------------------------------------------------------------

    def ck_status_code(self, t_link, tpar, st_code):
        err_links = self.MAIN_DICT.get(self.re)
        try:
            err_codes = [400, 404, 408, 409]
            if st_code in err_codes:
                if t_link not in err_links:
                    err_links.append((t_link, st_code, tpar))
                    self.MAIN_DICT.update({self.re: err_links})
                return 1
            else:
                return 0  # ok
        except Exception as e:
            self.myprint("Exception in ck_status_code: " + str(e))
            pass

    #-----------------------------------------------------------------------------

    
    @classmethod
    def mk_link_w_scheme(cls, addy):
        #LinkCheckLib.myprint(LinkCheckLib(), "--------testingprinting-----------!!!!!!")
        one = 'http://'
        two = 'https://'
        needprefix = True
        if addy[0:8] == two:
            needprefix = False
        elif addy[0:7]==one:
            needprefix = False

        if needprefix:
            full_addy = one + addy
        else:
            full_addy = addy
        return full_addy
    #-----------------------------------------------------------------------------


    #-----------------------------------------------------------------------------
    def reset_timer( self, name, tstart):
        self.myprint(name + str( perf_counter() - tstart))
        tstart = perf_counter()
        return tstart
