
from urllib.parse import urlparse
from requests_html import HTMLSession
from random import random
from time import perf_counter
from config import conf_debug
import requests



class LinkCheckLib(object):

    def __init__(self):
        self.MAIN_DICT = dict()
        rand = str(random())[2:]

        self.ORIGNAME = "ORIG" + rand
        self.ORIGNAMEwww = "ORIGwww" + rand
        self.BASENAME = "BURL" + rand
        self.BASENAMEwww = "BURLwww" + rand
        self.rerr = "rerr_" + rand
        self.rdonesingles = "rdone_" + rand
        self.rothers = "rothers_" + rand
        self.rbase = "rbase_" + rand
        self.redirecterrs = "redirecterrs" + rand

        err_links = []   # final error links found
        done_ln_glob_singles = []
        other_links_gl = []  #list of tups
        base_lnks_g = []  #list of tups
        redirecterrs_dat = []

        self.tlds_list = []
        self.MAIN_DICT.update({self.ORIGNAME: "init"})
        self.MAIN_DICT.update({self.ORIGNAMEwww: "init"})
        self.MAIN_DICT.update({self.BASENAME: "init"})
        self.MAIN_DICT.update({self.BASENAMEwww: "init"})
        self.MAIN_DICT.update({self.rerr: err_links})
        self.MAIN_DICT.update({self.rdonesingles: done_ln_glob_singles})
        self.MAIN_DICT.update({self.rothers: other_links_gl})
        self.MAIN_DICT.update({self.rbase: base_lnks_g})
        self.MAIN_DICT.update({self.redirecterrs: redirecterrs_dat})
        self.load_tlds()

        self.myprint("self.ORIGNAME: " + self.ORIGNAME)
        self.myprint("self.ORIGNAMEwww: " + self.ORIGNAMEwww)
        self.myprint("name of err list: " + self.rerr)

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
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if tlinks is None:
            tlinks = []
        for link in tlinks:
            if link in done_ln_gl_sing:
                tlinks.remove(link)
        return tlinks

    def rem_errs_tups(self, tlinks_tups=None):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if tlinks_tups is None:
            tlinks_tups = []
        for link in tlinks_tups:
            if link[0] in done_ln_gl_sing:
                tlinks_tups.remove(link)
        return tlinks_tups
    #-----------------------------------------------------------------------------

    def ck_other_ln_glob(self, this_link):
        other_link_glov = self.MAIN_DICT.get(self.rothers)
        return bool(this_link in [i[0] for i in other_link_glov])

    #-----------------------------------------------------------------------------
     
    def ck_if_in_done_singles_glob(self, this_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)

        return bool(this_link in done_ln_gl_sing)
    #-----------------------------------------------------------------------------

    @classmethod
    def ck_if_in_other_loc(cls, this_lin, other_link_loc):
        return bool(this_lin in [i[0] for i in other_link_loc])  # is it local?
    #-----------------------------------------------------------------------------


    def ck_if_in_base_glob(self, this_lin):
        base_lnks_g = self.MAIN_DICT.get(self.rbase)
        return bool(this_lin in [i[0] for i in base_lnks_g])  # is it local?

    # -----------------------------------------------------------------------------

    def return_errors(self):
        finlist = []
        err_links = self.MAIN_DICT.get(self.rerr)

        if err_links:
            answer_string, e, a_finlist = '', '', []
            try:
                if err_links:
                    errs = list(set(err_links))
                    err_links.clear()
                    er_len = len(errs)
                    nstring = '\n' + "Total errors: " + str(er_len) + " Here are the errors ---:"
                    #self.myprint(nstring)

                    errs1 = list(set(errs))

                    errs2 = sorted(errs1, key=lambda x: x[0])  # sort on first

                    errs3 = set(errs2)
                    err_links.clear()

                    for e in errs3:
                        an0, an1, an2 = str(e[0]), str(e[1]), str(e[2])

                        answer_string = [an0, an1, an2]
                        a_finlist.append(answer_string)
                        finlist = a_finlist.copy()
                        #self.myprint(str(answer_string))
                else:
                    finlist = [answer_string]
                    self.myprint("len of finlist: " + str(len(finlist)))
            except Exception as e:
                self.myprint('Exception print_errs: ' + str(e))

        return finlist


        # -----------------------------------------------------------------------------
    def mkwww(self, tlink):  # is it THE parent? part of the main website?
        lens = 0
        f = 0
        front = urlparse(tlink).scheme
        f = len(front)
        netl = urlparse(tlink).netloc
        if "www." in netl:
            return tlink
        else:
            newlink = tlink[f:]
            n2 = "www." + newlink
            best = front + n2
            return best





#------------------------------------------------------------------------------------------
    def isTHEparent(self, main_link):  # is it THE parent? part of the main website?
        schemeonly = ''
        lens=0
        #self.myprint("in isTHEparent 1")
        #self.myprint("-----mainlink--------------- 7" + main_link)

        try:
            urlpar = urlparse(main_link)
            #self.myprint("-------------------- 5 " )
            try:
                schemeonly = urlpar.scheme
                lens = len(schemeonly)
            except:
                schemeonly = ''
                lens = 0

            if lens:
                #self.myprint("-------------------- 4x ")
                frontlen = lens + 3
                mainew = main_link[frontlen:]
                #self.myprint("in isTHEparent ")
            else:
                #self.myprint("-------------------- 5x ")
                mainew = main_link
            #self.myprint("new mainew:  " + mainew)


                # if parsed.scheme != '':
                #     main_link = parsed.netloc

            par_loc = self.MAIN_DICT.get(self.BASENAME)
            #self.myprint("in isTHEparent ")
            par_locwww = self.MAIN_DICT.get(self.BASENAMEwww)
            #self.myprint("in isTHEparent ")
            if mainew in par_loc:
                return True
            elif mainew in par_locwww:
                return True
            else:
                return False  # is it the parent?
        except Exception as e:
            print("-------------------------------------------------except in isTHEparent-------------------------------------------------")
            print(str(e))
    # -----------------------------------------------------------------------
    def is_same_site_link(self, inlink):
        is_same_link = False
        orig = self.MAIN_DICT.get(self.ORIGNAME)
        origwww = self.MAIN_DICT.get(self.ORIGNAMEwww)

        pf = urlparse(inlink)

        rebuild = pf.netloc + pf.path + pf.params + pf.query

        if (rebuild == orig) or (rebuild == origwww):
            is_same_link = True

        return is_same_link

    # -----------------------------------------------------------------------

    def ck_for_base(self, in_link, base_links_local=None):

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
        self.myprint("do_response1 parent is " + p_link)

        r_errs = self.MAIN_DICT.get(self.rerr)

        # redirecterr = self.MAIN_DICT.get(self.redirecterrs)
        done_ln_glob_singles = self.MAIN_DICT.get(self.rdonesingles)
        other_lin_loc = self.MAIN_DICT.get(self.rothers)
        t_err = 0
        the_big_response = None
        try:
            #self.myprint("do_response 2")
            self.myprint("THIS_LN: " + str(a_link) + " parent: " + p_link)
            if a_link not in done_ln_glob_singles:
                #self.myprint("do_response 3")
                if a_link not in other_lin_loc:
                    #self.myprint("do_response 4")

                    session = HTMLSession()
                    # ---------------------------------------------------------session.get--------------
                    the_big_response = session.get(a_link)
                    # ----------------------------------------------------------session.get-------------
                    if the_big_response is not None:
                        self.myprint("THIS_LN: " + str(a_link) + " parent: " + p_link)
                        session.close()
                        done_ln_glob_singles.append(a_link)  ## add to main done list
                        self.MAIN_DICT.update({self.rdonesingles: done_ln_glob_singles})

                        code = the_big_response.status_code
                        self.ck_status_code(a_link, code, p_link)  ## if there's    an error
                        self.myprint("LINK: in do_response: " + a_link + "  status code: " + str(code))
                    else:
                        r_errs.append((a_link, 404, p_link))

                    self.MAIN_DICT.update({self.rerr: r_errs})

        except Exception as e:
            self.myprint("GOT AN EXCEPTION inside do_response: " + str(e))
            self.handle_exc(a_link, e, p_link)

        return the_big_response

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

            if answ is True or answ2 is True:
                final_answer = True
        except Exception as e:
            self.myprint("Exception in has_correct_suffix: " + str(e))
        return final_answer
    #-----------------------------------------------------------------------------
    def add_to_others_glob(self, tlink, parent_local):  # Adding this MAIN_DICT link to any glob
        self.myprint("----------------------------!!! !!!! in add_to_others_glob: ")
        is_par = self.isTHEparent(tlink)
        if is_par:
            return
        other_lns_gl = self.MAIN_DICT.get(self.rothers)

        try:
            glob_bool = bool(tlink in [i[0] for i in other_lns_gl])
            if not glob_bool:
                #self.myprint("appending to others: ")
                other_lns_gl.append((tlink, parent_local))  # add if not there

        except Exception as e:
            self.myprint("exception in add_others: " + str(e))

        self.MAIN_DICT.update({self.rothers: other_lns_gl})
        return

    #-----------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    def get_simple_response(self, lin_and_par_tup):

        rdone_sings = self.MAIN_DICT.get(self.rdonesingles)
        if lin_and_par_tup[0] in rdone_sings:
            print('!!!!!============================found dupe: ')
            return

        if not lin_and_par_tup:
            return

        parent = "empty"
        the_response_simple = None
        #self.myprint("inside get_simple_response: ")
        #print("here is the tuple : " + str(lin_and_par_tup) )
        link_to_ck, parent = lin_and_par_tup[0], lin_and_par_tup[1]

                #self.myprint("trying THIS_LN: " + link_to_ck + " parent: " + parent + " in get_simple_response")

        try:
            the_response_simple = requests.head(link_to_ck)

        except Exception as e:
            self.myprint("Exception inside get_simple_response: ")
            self.handle_exc(link_to_ck, e, parent)
            return

        try:
            if the_response_simple:
                self.myprint("THIS_LN: " + link_to_ck + " parent: " + parent )
                stat = the_response_simple.status_code
                rdone_sings.append(link_to_ck)
                #self.myprint("status: " + str(stat))
                self.ck_status_code(link_to_ck, stat, parent)

            self.MAIN_DICT.update({self.rdonesingles: rdone_sings})

        except Exception as e:
            self.myprint("Exception inside get_simple_response: " + str(e))


#---------------------------------------------------------------------------------------

    def ck_tld_sufx(self, alink):
        the_suf = alink.lower().split(".")[-1]
        if the_suf[-1] == '/':
            the_suf = the_suf[0:-1]

        if the_suf in self.tlds_list:
            return True
        else:
            return False
    #-----------------------------------------------------------------------------

    def handle_exc( self, tlink, e, plink):
        err_links = self.MAIN_DICT.get(self.rerr)

        the_err = str(e)
        the_err_str = the_err[:72]
        self.myprint('!!!!! Inside handle_exc. Error------------------> ' + the_err)

        badlist = ["Document is empty","object has no attribute","ConnectionResetError","RemoteDisconnected"]

        for i in badlist:
            if i in the_err:  # for mp3 and similar files
                return

        if tlink not in err_links:
            err_links.append((tlink, the_err_str, plink))
            self.MAIN_DICT.update({self.rerr:err_links})

    #-----------------------------------------------------------------------------

    def ck_status_code(self, t_link, st_code_int, tpar):
        err_links = self.MAIN_DICT.get(self.rerr)
        try:
            err_codes = [400, 404, 408, 409]
            if st_code_int in err_codes:
                if t_link not in err_links:
                    #self.myprint("adding error in ck_status_code " + t_link + str(st_code_int) + tpar)
                    err_links.append((t_link, st_code_int, tpar))
                    self.MAIN_DICT.update({self.rerr: err_links})
                return 1
            else:
                return 0  # ok
        except Exception as e:
            self.myprint("Exception in ck_status_code: " + str(e))

    #-----------------------------------------------------------------------------

    
    @classmethod
    def mk_link_w_scheme(cls, addy):
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
    def reset_timer( self, name, tstart):
        self.myprint(name + str( perf_counter() - tstart))
        tstart = perf_counter()
        return tstart
