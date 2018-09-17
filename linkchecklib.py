from urllib.parse import urlsplit


class LinkCheckLib(object):

    def __init__(self):
        tlds_list = self.setup()
        self.tlds_list = tlds_list

    def setup(self):
        tlds_list = self.load_tlds()

    def ispar(self, thisln, par_loc):
        return bool(thisln == par_loc)  # is it the parent?

    
    def ck_g(self, this_link, any_link_glob):
        return bool(this_link in [i[0] for i in any_link_glob])

    
    def _DONE_YET(self, this_link, done_ln_gl_sing):
        return bool(this_link in done_ln_gl_sing)

    
    def ck_loc(self, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?

    
    def ck_bad_data(self, dlink):
        self.myprint("!!!!!=============inside ckbaddata. val of link: " + dlink)
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

    
    def check_for_bad_data(self, alink, done_lnks_gl=0):
        if done_lnks_gl == 0:
            done_lnks_gl = []
        self.myprint("!!!!!=============inside check_for_bad_data. val of link: " + alink)
        try:
            if done_lnks_gl:
                done_lnks_gl.append(alink)  ## add to main done list
            else:
                done_lnks_gl = [alink]
        except Exception as e:
            self.myprint("Exception check_for_bad_data: " + str(e))
        return done_lnks_gl

    
    def split_url(self, url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url

    
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
            pass

        return final_answer

    def myprint(print_str):
        _MYDEBUG = 1
        if _MYDEBUG:
            print(print_str)

    def load_tlds(self):
        tlds = []
        with open('tlds-alpha-by-domain.txt', 'r') as filehandle:
            for line in filehandle:
                currentPlace = line[:-1]
                tlds.append((currentPlace.lower()))
        return tlds

    def check_sufx(self,sufx):
        if sufx in self.tlds_list:
            return True
        else:
            return False

    def handle_exc( self, e, link, plink):
        #self.myprint(str(e))
        self.myprint('!!!!!!!! found error------------------\n' + str(e))
        if link not in self.err_links:
            self.err_links.append((link, str(e)[:42], plink))
        pass

    def ck_status_code(self,response, tpar):
        link = response.html.url
        err_codes = [400, 404, 408, 409]
        if response.status_code in err_codes:
            if link not in self.err_links:
                self.err_links.append((link, response.status_code, tpar))
            return 1
        else: return 0  # ok

    
    def ckaddymore(self,addy):
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

    
    def has_early_dollar( self,link, base_p):
        if "$" in link:
            if link.index("$") < link.index(base_p):    ## if $ before base link
                return True     ## it's before base link - not good
            else:
                return False     # there's a $ sign but it's ok
        else:
            return False

    def divide_url(self, parent_local):
        thebase_part_local = ""
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            self.myprint('Exception divide_url: ' + str(e))
            pass
        return thebase_part_local

    # def reset_timer( name, tstart):
    #     self.myprint(name, perf_counter() - tstart)
    #     #tstart = perf_counter()
    #     return tstart




