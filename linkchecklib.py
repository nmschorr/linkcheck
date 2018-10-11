
from urllib.parse import urlparse
from requests_html import HTMLSession
from random import random
from time import perf_counter
from config import conf_debug

class LinkCheckLib(object):

    def __init__(self):
        MAIN_DICT = dict()
        self.MAIN_DICT = MAIN_DICT
        rand = str(random())

        BASENAME = "BURL" + rand
        BASENAMEwww = "BURLwww" + rand
        re = "re_" + rand
        rd = "rd_" + rand
        ra = "ra_" + rand
        rb = "rb_" + rand
        redirs = "redirs" + rand
        self.redirs = redirs
        self.BASENAME = BASENAME
        self.BASENAMEwww = BASENAMEwww
        self.re = re
        self.rd = rd
        self.ra = ra
        self.rb = rb
        self.rb = rb

        err_links = []
        done_ln_gl_sing = []
        any_link_glob = []
        base_lnks_g = []
        BN = "empty"
        BNwww = "empty"
        redirs_dat = []

        self.tlds_list = []
        self.MAIN_DICT.update({BASENAME: BN})
        self.MAIN_DICT.update({BASENAMEwww: BNwww})
        self.MAIN_DICT.update({re: err_links})
        self.MAIN_DICT.update({rd: done_ln_gl_sing})
        self.MAIN_DICT.update({ra: any_link_glob})
        self.MAIN_DICT.update({rb: base_lnks_g})
        self.MAIN_DICT.update({redirs: redirs_dat})
        self.load_tlds()

    #-----------------------------------------------------------------------------
    def myprint(self, print_str, mdebug=0 ):
        mdebug = conf_debug
        if mdebug:
            print(print_str)

    #-----------------------------------------------------------------------------

    def ck_g(self, this_link):
        ra = self.ra
        any_link_glob = self.MAIN_DICT.get(self.ra)
        return bool(this_link in [i[0] for i in any_link_glob])

    #-----------------------------------------------------------------------------
     
    def _DONE_YET(self, this_link):
        rd = self.rd
        done_ln_gl_sing = self.MAIN_DICT.get(self.rd)

        return bool(this_link in done_ln_gl_sing)
    #-----------------------------------------------------------------------------

    @classmethod
    def ck_loc(cls, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?
    #-----------------------------------------------------------------------------

    
    def return_errors(self):

        finlist = []
        re = self.re
        err_links = self.MAIN_DICT.get(re)
        
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
        redirs = self.redirs
        rederdat = self.MAIN_DICT.get(redirs)
        done_ln_gl_sing = self.MAIN_DICT.get(self.rd)
        t_err = 0
        resp = None
        try:
            if a_link not in done_ln_gl_sing:
                #self.myprint("Starting-get_home_links - just got this link: " + str(a_link))
                done_ln_gl_sing.append(a_link)  ## add to main done list

                session = HTMLSession()
                resp = session.get(a_link, timeout=7.0)
                session.close()

                code = resp.status_code
                t_err = self.ck_status_code(a_link, p_link, code)  ## if there's    an error
                self.myprint("LINK: in do_response: " + a_link + "  status code: " + str(code))

                if code == 301:
                    rederdat.append(a_link)  # no need to recheck because it's automatic

        except Exception as e:
            self.myprint("GOT AN EXCEPTION inside do_response ")
            self.myprint(str(e))
            self.handle_exc(e, a_link, p_link)
            pass
        self.MAIN_DICT.update({redirs: rederdat})
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

    def load_tlds(self):
        filehandle = open('tlds-alpha-by-domain.txt', 'r')
        for line in filehandle:
            current_place = line[:-1]
            self.tlds_list.append((current_place.lower()))
        filehandle.close()
    #-----------------------------------------------------------------------------

    def ck_tld_sufx(self, alink):
        tlink = alink.lower()
        the_suf = tlink.split(".")[-1]
        if the_suf[-1] == '/':
            the_suf = the_suf[0:-1]

        if the_suf in self.tlds_list:
            return True
        else:
            return False
    #-----------------------------------------------------------------------------

    def handle_exc( self, e, link, plink):
        re = self.re
        err_links = self.MAIN_DICT.get(re)

        tempstr = str(e)
        self.myprint('!!!!! Inside handle_exc. Error------------------> ' + tempstr)

        badlist = ["Document is empty","object has no attribute","ConnectionResetError","RemoteDisconnected"]

        for i in badlist:
            if i in tempstr:  # for mp3 and similar files
                return

        if link not in err_links:
            err_links.append((link, tempstr[:72], plink))
            self.MAIN_DICT.update({re:err_links})

    #-----------------------------------------------------------------------------

    def ck_status_code(self, t_link, tpar, st_code):
        re = self.re
        err_links = self.MAIN_DICT.get(re)
        try:
            err_codes = [400, 404, 408, 409]
            if st_code in err_codes:
                if t_link not in err_links:
                    err_links.append((t_link, st_code, tpar))
                    self.MAIN_DICT.update({re: err_links})
                return 1
            else:
                return 0  # ok
        except Exception as e:
            self.myprint("Exception in ck_status_code: " + str(e))
            pass

    #-----------------------------------------------------------------------------

    
    @classmethod
    def ckaddymore(cls, addy):
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
