
from urllib.parse import urlparse
from requests_html import HTMLSession
from random import random
from time import perf_counter
from config import conf_debug
import requests
import cfscrape


class LinkCheckLib(object):

    def __init__(self):
        base_only_plain_repeat_tup = []
        self.base_only_plain_repeat_tup = base_only_plain_repeat_tup
        self.MAIN_DICT = dict()
        rand = str(random())[2:]
        self.rand = rand

        self.ORIGNAME = "ORIG" + rand
        self.ORIGNAMEwww = "ORIGwww" + rand
        self.BASENAME = "BASE" + rand
        self.BASENAMEwww = "BASEwww" + rand
        self.rerr = "rerr_" + rand
        self.redirs = "redirs_" + rand
        self.rdonesingles = "rdone_" + rand
        self.rothers = "rothers_" + rand
        self.rbase = "rbase_" + rand

        err_links = []   # final error links found
        redir_list = []   # final error links found
        done_ln_glob_singles = []
        other_links_gl = []  #list of tups
        base_lnks_g = []  #list of tups
        # redirecterrs_dat = []

        self.tlds_list = []
        self.MAIN_DICT.update({self.ORIGNAME: "init"})
        self.MAIN_DICT.update({self.ORIGNAMEwww: "init"})
        self.MAIN_DICT.update({self.BASENAME: "init"})
        self.MAIN_DICT.update({self.BASENAMEwww: "init"})
        self.MAIN_DICT.update({self.rerr: err_links})
        self.MAIN_DICT.update({self.redirs: redir_list})
        self.MAIN_DICT.update({self.rdonesingles: done_ln_glob_singles})
        self.MAIN_DICT.update({self.rothers: other_links_gl})
        self.MAIN_DICT.update({self.rbase: base_lnks_g})
        # self.MAIN_DICT.update({self.redirecterrs: redirecterrs_dat})
        self.load_tlds()

        self.myprint("self.ORIGNAME: " + self.ORIGNAME)
        self.myprint("self.ORIGNAMEwww: " + self.ORIGNAMEwww)
        self.myprint("name of err list: " + self.rerr)
        self.myprint("name of redirs list: " + self.redirs)

    #-----------------------------------------------------------------------------
    def myprint(self, print_str ):
        if conf_debug:
            print(print_str)

    # -----------------------------------------------------------------------------

    def load_tlds(self):
        filehandle = open('tlds-alpha-by-domain.txt', 'r')
        for line in filehandle:
            current_place = line[:-1]
            self.tlds_list.append((current_place.lower()))
        filehandle.close()

    #-----------------------------------------------------------------------------

    def rem_base_dupes(self, tlinks_tups):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        for link in tlinks_tups:
            if link[0] in done_ln_gl_sing:
                tlinks_tups.remove(link)
        return tlinks_tups
    #-----------------------------------------------------------------------------

    def ret_bool_ifin_other_glob(self, this_link):
        other_link_gl = self.MAIN_DICT.get(self.rothers)
        return bool(this_link in [i[0] for i in other_link_gl])

    #-----------------------------------------------------------------------------
     
    def ret_bool_ifin_DONE_singles(self, this_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        return bool(this_link in done_ln_gl_sing)
    #-----------------------------------------------------------------------------

    @classmethod
    def ret_bool_if_in_OTHER_loc(cls, this_lin, other_link_loc):
        return bool(this_lin in [i[0] for i in other_link_loc])  # is it local?
    #-----------------------------------------------------------------------------


    def ret_bool_if_in_BASE_glob(self, this_lin):
        base_lnks_g = self.MAIN_DICT.get(self.rbase)
        return bool(this_lin in [i[0] for i in base_lnks_g])  # is it local?

    # -----------------------------------------------------------------------------

    def return_errors(self):
        self.myprint("in return_errors()")
        finlist = []
        err_links = self.MAIN_DICT.get(self.rerr)

        if err_links:
            answer_string, loc_e, a_finlist = '', '', []
            try:
                if err_links:
                    errs = list(set(err_links))
                    err_links.clear()
                    #er_len = len(errs)
                    #nstring = '\n' + "Total errors: " + str(er_len) + " Here are the errors ---:"
                    #self.myprint(nstring)

                    errs1 = list(set(errs))
                    errs2 = sorted(errs1, key=lambda x: x[0])  # sort on first
                    errs3 = set(errs2)
                    errs1.clear()
                    errs2.clear()

                    for loc_e in errs3:
                        an0, an1, an2 = loc_e[0], str(loc_e[1]), loc_e[2]

                        answer_string = [an0, an1, an2]
                        finlist.append(answer_string)

                    # err_links.clear()
                else:
                    finlist = [answer_string]
            except Exception as loc_e:
                self.myprint('Exception print_errs: ' + str(loc_e))

        self.myprint("len of finlist: " + str(len(finlist)))
        return finlist

        # -----------------------------------------------------------------------------

    def return_redirs(self):
        self.myprint("in return_redirs()")
        finlistr = []
        rerrlinks = self.MAIN_DICT.get(self.redirs)

        if rerrlinks:
            answer_string, loc_e  = '', ''
            try:
                if rerrlinks:
                    errs = list(set(rerrlinks))
                    rerrlinks.clear()
                    errs1 = list(set(errs))
                    errs2 = sorted(errs1, key=lambda x: x[0])  # sort on first
                    errs3 = set(errs2)
                    errs1.clear()
                    errs2.clear()

                    for loc_e in errs3:
                        an0, an1, an2 = loc_e[0], str(loc_e[1]), loc_e[2]

                        answer_string = [an0, an1, an2]
                        finlistr.append(answer_string)

                    # err_links.clear()
                else:
                    finlistr = [answer_string]
            except Exception as loc_e:
                self.myprint('Exception print_errs: ' + str(loc_e))

        self.myprint("len of finlist: " + str(len(finlistr)))
        return finlistr

    # -----------------------------------------------------------------------------
    def make_www_url(self, tlink):  # is it THE parent? part of the main website?
        lens = 0
        scheme_len = 0
        schemef = urlparse(tlink).scheme
        if schemef:
            scheme_len = len(schemef)
        netl = urlparse(tlink).netloc
        if tlink[:4] == 'www.':
            return tlink
        if "www." in netl:
            return tlink
        else:
            link_back = tlink[scheme_len:]
            link_www = "www." + link_back
            full_link = schemef + link_www
            return full_link


#------------------------------------------------------------------------------------------
    def isTHEparent(self, main_link):  # is it THE parent? part of the main website?
        schemeonly = None
        lens=0
        #self.myprint("in isTHEparent 1 -----mainlink--------------- 7" + main_link)

        try:
            urlpar = urlparse(main_link)
            #self.myprint("-------------------- 5 " )
            try:
                schemeonly = urlpar.scheme
                if schemeonly:
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


                # if parsed.scheme != '':   main_link = parsed.netloc

            t_parent = self.MAIN_DICT.get(self.BASENAME)
            par_locwww = self.MAIN_DICT.get(self.BASENAMEwww)
            if mainew in t_parent:
                return True
            elif mainew in par_locwww:
                return True
            else:
                return False  # is it the parent?
        except Exception as e:
            print("-------------------------------------------------except in isTHEparent-------------------------------------------------")
            print(str(e))

    # -----------------------------------------------------------------------
    def ret_bool_if_same_as_orig_url(self, inlink):
        is_same_link = False
        orig = self.MAIN_DICT.get(self.ORIGNAME)
        origwww = self.MAIN_DICT.get(self.ORIGNAMEwww)

        pf = urlparse(inlink)

        rebuild = pf.netloc + pf.path + pf.params + pf.query

        if (rebuild == orig) or (rebuild == origwww):
            is_same_link = True

        return is_same_link

    # -----------------------------------------------------------------------

    def ret_bool_if_BASE(self, in_link):
        this_link = in_link
        _IS_BASE = False

        one = 'http://'
        two = 'https:/'
        link_sub = in_link[0:7]
        if (link_sub==one) or (link_sub==two):
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

        except Exception as e:
            self.myprint("Exception ck_base: " + str(e))
        return _IS_BASE

    #-----------------------------------------------------------------------

    def do_get_request(self, a_link, p_link):

        # scraper = cfscrape.create_scraper(delay=30)  # returns a CloudflareScraper instance
        # # Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
        # print("SCRAPING---------!!!")
        # try:
        #     scp = scraper.get(a_link)
        #     print()      # => "<!DOCTYPE html><html><head>..."
        # except Exception as e:
        #     self.myprint("Exception ck_base: " + str(e))


        self.myprint("do_response link is " + a_link + " parent: " + p_link)

        done_ln_glob_singles = self.MAIN_DICT.get(self.rdonesingles)
        other_lin_loc = self.MAIN_DICT.get(self.rothers)
        t_err = 0
        code = None
        the_big_response = None
        try:
            self.myprint("do_response 2")
            if not (( a_link in done_ln_glob_singles) and (a_link not in other_lin_loc)):
                session = HTMLSession()
                self.myprint("do_response 3")
                # ---------------------------------------------------------session.get--------------
                the_big_response = session.get(a_link)
                # ----------------------------------------------------------session.get-------------
                session.close()
                self.myprint("do_response 3.3")
                self.check_redirs(the_big_response, a_link, p_link)  ##----------CHECK REDIRS ----------!!!!@@!!
                self.MAIN_DICT.get(self.rdonesingles).append(a_link)  # add this link to done list
                self.myprint("do_response 4")


                if the_big_response is not None:
                    code = the_big_response.status_code
                    self.myprint("LINK: in do_response: " + a_link + "  status code: " + str(code))
                    # ---------------------------------------------------new-----------
                    # ---------------------------------------------------new-----------

# ---------------------------------------------------301-----------

                    if code == 301:
                        if self.ret_bool_if_BASE(p_link):
                            self.add_err_to_errlinks(a_link, code, p_link)  ## if there's an error
                        return the_big_response  # no error - lets leave

                    elif code in [200, 302]:
                        return the_big_response  # no error - lets leave

                    elif code is not None:
                        self.add_err_to_errlinks(a_link, code, p_link)  ## if there's an error

                    else:  #no code but still and error
                        self.MAIN_DICT.get(self.rerr).append((a_link, 000, p_link))  ## we had some kind of error

        except Exception as e:
            self.myprint("GOT AN EXCEPTION inside do_response: " + str(e))
            self.handle_exc(a_link, e, p_link)

        return the_big_response

    #----------------------------------------------------------------------get_links-
    def check_redirs(self, r, given, parent):
        histz_stat = 0
        print("-------------------------------@@@@@@@@@ Inside check_redirs   - given url: ", given)
        parentbase = urlparse(parent).netloc
        givenbase = urlparse(given).netloc
        is_this_on_base = self.ret_bool_if_BASE(parent)
        if not is_this_on_base:
            return

        newname = r.url
        histlen = len(r.history)
        if histlen > 0:
            print("------------------redir hist len: " + str(histlen))

            try:
                histz = r.history[0]
            #print("------------------histz hist len: " )
                histz_stat = histz.status_code
            except Exception as e:
                print("GOT AN EXCEPTION inside check_redirs: " + str(e))

        print("histz_stat: ", histz_stat)
        if histz_stat == 301:
            newnamebase = urlparse(newname).netloc
            mainnew = (givenbase, parentbase, newnamebase)
            big_redirs = self.MAIN_DICT.get(self.redirs)
            big_redirs.append(mainnew)
            self.MAIN_DICT.update({self.redirs: big_redirs})
            print()


    #-----------------------------------------------------------------------------

    def ck_bad_data(self, dlink):
        #self.myprint("!!!!!=============inside ck_bad_data. val of link: " + dlink)
        bad_counter = 0
        mylist = ['#', 'tel:+', '[[']
        try:
            for item in mylist:
                if item in dlink:
                    bad_counter += 1
        except Exception as e:
            self.myprint("Exception ck_bad_data: " + str(e))

        ckme = dlink[7:30]
        if ("pinterest.com" or "facebook.com" or "twitter.com") in ckme:
            if len(dlink) > 50:
                bad_counter += 1

        good_suffix = self.has_correct_suffix(dlink)  # check suffix
        #self.myprint("!inside ck_bad_data: " + str(good_or_bad) + ' ' + str(good_suffix))
        return bad_counter, good_suffix

    #-----------------------------------------------------------------------------
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
                self.myprint("appending to others: " + tlink)
                self.MAIN_DICT.get(self.rothers).append((tlink, parent_local))  # add if not there

        except Exception as e:
            self.myprint("exception in add_others: " + str(e))

    #-----------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    def do_head_request(self, lin_and_par_tup):
        print()
        print('-- in do_head_request() ')
        if not lin_and_par_tup:    #nothing correct passed in
            return

        print("here is the tuple  in do_head_request(): " + str(lin_and_par_tup) )
        rdone_singles = self.MAIN_DICT.get(self.rdonesingles)
        if lin_and_par_tup[0] in rdone_singles:
            print('!!!!!============================found dupe in do_head_request() - skipping. ')
            return

        parent = "empty"
        head_response = None
        link_to_ck, parent = lin_and_par_tup[0], lin_and_par_tup[1]

        self.myprint("trying THIS_LN: " + link_to_ck + " parent: " + parent + " in do_head_request")

        try:
 #--------------- simple request of head only -------------------------------!!-------
            head_response = requests.head(link_to_ck)
 # --------------- simple request of head only -----------------------------!!!---------

            self.MAIN_DICT.get(self.rdonesingles).append(link_to_ck)  # record we did this one
            head_stat = head_response.status_code
            self.myprint("do_head_request is : " + str(head_stat))
            if head_stat == 404:
                scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
                print("Trying Cloudflare unit ---------!!!")
                scp = scraper.get(link_to_ck)
                head_stat = scp.status_code

        except Exception as e:
            self.myprint("Exception inside do_head_request. " + str(e))
            self.handle_exc(link_to_ck, e, parent)
            return

        try:
            if head_stat < 301:
                return
            elif head_stat > 300:
                if head_stat == 301:  # perm redirect
                    follow_url = head_response._next.url  # only for 301 errs
                    self.MAIN_DICT.get(self.redirs).append((link_to_ck, parent, follow_url))
                    return
                elif head_stat in [400, 404, 408, 409, 410]:
                    self.add_err_to_errlinks(link_to_ck, head_stat, parent)
                else:
                    return

            # else:   # no status means no regular result
            #     self.add_err_to_errlinks(link_to_ck, 000 , parent)

        except Exception as e:
            self.myprint("Exception inside do_head_request 2: " + str(e))


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

    def handle_exc(self, tlink, tException, plink):
        the_err = str(tException)
        self.myprint('!!!!! Inside handle_exc. Error------------------> ' + str(tException))
        the_err_str = the_err[:72]
        badlist = ["Document is empty","object has no attribute","ConnectionResetError","RemoteDisconnected"]

        for i in badlist:
            if i in the_err:  # for mp3 and similar files
                return

        err_links = self.MAIN_DICT.get(self.rerr)
        if tlink not in err_links:
            # self.MAIN_DICT.get(self.rerr).append((tlink, the_err_str, plink))
            err_links.append((tlink, the_err_str, plink))
            self.MAIN_DICT.update({self.rerr: err_links})

    #-----------------------------------------------------------------------------

    def add_err_to_errlinks(self, t_link, er_code_int, tpar):
        try:
            err_codes = [000, 400, 404, 408, 409]
            if (er_code_int in err_codes) and (t_link not in self.MAIN_DICT.get(self.rerr)):
                self.myprint("adding error in ck_status_code " + t_link  + "  " + str(er_code_int)  + "  " + tpar)
                self.MAIN_DICT.get(self.rerr).append((t_link, er_code_int, tpar))
#####------ 301:
#--------------------------------------------------
            elif er_code_int == 301:
                if self.ret_bool_if_BASE(tpar):
                    self.MAIN_DICT.get(self.redir).append((t_link, er_code_int, tpar, 'None'))
                    self.myprint("-- Adding redir in ck_status_code:  " + t_link + "  " + str(er_code_int) + "  " +  tpar)

        except Exception as e:
            self.myprint("Exception in ck_status_code: " + str(e))

    #-----------------------------------------------------------------------------

    
    @classmethod
    def mk_link_w_scheme(cls, addy):
        if (addy[0:8] == 'https://') or (addy[0:7]== 'http://'):
            return addy
        else:
            return 'https://' + addy

    #-----------------------------------------------------------------------------
    def reset_timer( self, name, tstart):
        self.myprint(name + str( perf_counter() - tstart))
        tstart = perf_counter()
        return tstart
