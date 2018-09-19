from urllib.parse import urlsplit
from requests_html import HTMLSession

any_link_glob=[]
done_ln_gl_sing = []
_MYDEBUG = 1

class LinkCheckLib(object):
    ###from config import any_link_glob, err_links, _MYDEBUG

    def __init__(self):
        #print("yes")
        err_links = []
        self.err_links = err_links
        tlds_list = []
        self.tlds_list = tlds_list
        self.done_ln_gl_sing = done_ln_gl_sing
        self.any_link_glob = any_link_glob


    @classmethod
    def ispar(cls, thisln, par_loc):
        return bool(thisln == par_loc)  # is it the parent?

    def write_some_contents(self, contnt, nme):
        fname = str(nme) + ".log"
        wf = open(fname, "w")
        for i in contnt:
            wf.write(i)
            wf.close()


    def ck_g(self, this_link):
        global any_link_glob
        return bool(this_link in [i[0] for i in any_link_glob])

     
     
    def _DONE_YET(self, this_link):
        global done_ln_gl_sing
        return bool(this_link in done_ln_gl_sing)

    @classmethod
    def ck_loc(cls, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?
    #-----------------------------------------------------------------------------

    
    def print_errs(self):

        if self.err_links == 0:
            self.err_links = []
        if self.err_links:
            answer_string, e, fin_list = '', '', []
            try:
                if self.err_links:
                    errs = list(set(self.err_links))
                    er_len = len(errs)
                    nstring = "\nTotal errors: " + str(er_len) + " Here are the errors ---:"
                    self.myprint(nstring)
                    errs22 = sorted(errs, key=lambda x: x[0])  # sort on first
                    errs2 = set(errs22)
                    for e in errs2:
                        an0, an1, an2 = str(e[0]), str(e[1]), str(e[2])

                        answer_string = [an0, an1, an2]
                        fin_list.append(answer_string)
                        self.myprint(str(answer_string))
                else:
                    fin_list = [answer_string]
            except Exception as e:
                self.myprint('Exception print_errs: ' + str(e))
            return fin_list
        else:
            return []

    # -----------------------------------------------------------------------
    @classmethod
    def ck_base(cls, this_link, thebase_part, base_links_local=0):
        if base_links_local == 0:
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
        global done_ln_gl_sing
        t_err = 0
        #resp = rt.HTMLResponse
        resp = "0"
        try:
            self.myprint("-starting-get_home_links - just got this link: " + str(a_link))
            session = HTMLSession()
            resp = session.get(a_link)
            done_ln_gl_sing.append(a_link)  ## add to main done list
            t_err = self.ck_status_code(resp, a_link)  ## if there's    an error
            session.close()

        except Exception as e:
            if a_link not in self.err_links:
                self.err_links.append((a_link, str(e)[:42], p_link))
            self.myprint("GOT AN EXCEPTION inside do_response and added to errs: " + str(e))
            return resp, t_err
        return resp, t_err

    #----------------------------------------------------------------------get_links-

    def ck_bad_data(self, dlink):
        #self.myprint("!!!!!=============inside ckbaddata. val of link: " + dlink)
        end_val = 0
        mylist = ['#', 'tel:+']
        try:
            for i in mylist:
                if i in dlink:
                    end_val += 1
        except Exception as e:
            self.myprint("Exception ck_bad_data: " + str(e))

        good_suf = self.has_correct_suffix(dlink)  # check suffix
        self.myprint("!inside enval: " + str(end_val) + ' ' + str(good_suf))
        return end_val, good_suf

    #-----------------------------------------------------------------------------

    #def check_for_bad_data(cls, alink, done_lnks_gl=0):
    def check_for_bad_data(self, alink):
        global done_ln_gl_sing
        
        if self.done_ln_gl_sing == 0:
            done_ln_gl_sing = []
            self.myprint("!!!!!=============inside check_for_bad_data. val of link: " + alink)
        try:
            if done_ln_gl_sing:
                done_ln_gl_sing.append(alink)  ## add to main done list
                
            else:
                done_ln_gl_sing = [alink]
        except Exception as e:
            self.myprint("Exception check_for_bad_data: " + str(e))


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
            self.myprint("Exception in has_correct_suffix: " + str(e))
        return final_answer

    def myprint(self, print_str):
        global _MYDEBUG
        if _MYDEBUG:
            print(print_str)

    @classmethod
    def myprinter(cls, print_str):
        global _MYDEBUG
        if _MYDEBUG:
            print(print_str)

    def load_tlds(self):
        with open('tlds-alpha-by-domain.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                self.tlds_list.append((currentPlace.lower()))

    def check_sufx(self, sufx):
        low_sufx = str(sufx).lower()
        if low_sufx in self.tlds_list:
            return True
        else:
            return False

    def handle_exc( self, e, link, plink):
        self.myprint('!!!!!!!! found error------------------\n' + str(e))
        tempstr = str(e)
        if "Document is empty" in str(e):  # for mp3 and similar files
            None
        elif link not in self.err_links:
            self.err_links.append((link, str(e)[:42], plink))


    def ck_status_code(self, response, tpar):
        tlink = response.html.url
        err_codes = [400, 404, 408, 409]
        if response.status_code in err_codes:
            if tlink not in self.err_links:
                self.err_links.append((tlink, response.status_code, tpar))
            return 1
        else: return 0  # ok

    
    @classmethod
    def ckaddymore(cls, addy):
        one = 'http://'
        two = 'https://'
        needprefix = True
        if addy[0:7]==one:
            needprefix = False
        if addy[0:8] == 'https://':
            needprefix = False
        if needprefix:
            full_addy = 'http://' + addy
        else:
            full_addy = addy
        return full_addy

    
    @classmethod
    def has_early_dollar( cls, clink, base_p):
        bp = clink.index(base_p)
        if "$" or "?" or "#" in clink:
            if (clink.index("$") < bp) or (clink.index("?") < bp) or (clink.index("#") < bp):
                ## if $ or # or ? before base link
                return True     ## it's before base link - not good
            else:
                return False     # there's a $ sign but it's ok
        else:
            return False

    @classmethod
    def divide_url(cls, parent_local):
        thebase_part_local = ""
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            cls.myprinter('Exception divide_url: ' + str(e))

        return thebase_part_local

    # def reset_timer( name, tstart):
    #     self.myprint(name, perf_counter() - tstart)
    #     #tstart = perf_counter()
    #     return tstart
