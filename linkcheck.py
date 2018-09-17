# python 3
# Nancy Schorr, 2018
# this file is in active development
#from time import perf_counter
import requests_html as rt
from datetime import datetime


class linkcheck(object):
    def __init__(self):
        self.any_link_glob, self.base_lnks_g = [], []
        self.done_ln_gl_sing, self.err_links, self.link_count = [], [], 0
        #self.logger = lc().setup_logger()
        datet = datetime.now()
        self.myprint('In linkcheck: __init__New: ' + str(datet))
        self.tlds_list = self.load_tlds()

    def get_simple_response(self, lin_and_par_tup):
        er = "0"
        response = "0"
        link_to_ck, parent,  = lin_and_par_tup[0], lin_and_par_tup[1]
        self.link_count += 1
        self.myprint("Checking this link: " + link_to_ck)
        try:
            session = rt.HTMLSession()
            response = session.get(link_to_ck)
            er = self.ck_status_code(response, parent)
        except Exception as e:
            self.myprint("exception inside get_simple_response: " + str(e))
            if str(e).find("Document is empty"):   # for mp3 and similar files
                pass
            else:
                self.handle_exc(e, link_to_ck, parent)
    def add_any_bse_g(self, zlink, parent_local, base_links_glob2=0):  # Adding this base link to base glob
        if base_links_glob2 == 0:
            base_links_glob2 = []
        try:
            if base_links_glob2:
                _IN_BASE_GLOB = bool(zlink in [i[0] for i in base_links_glob2])
                if not _IN_BASE_GLOB:  # if not already in this
                    base_links_glob2.append((zlink, parent_local))
                    self.myprint("Adding this BASE LINK to base glob: " + zlink)
            else:
                base_links_glob2 = [(zlink, parent_local)]

        except Exception as e:
            self.myprint("Exception add_any_bse_g: " + str(e))
        return base_links_glob2

    def add_any(self, tlink, parent_local, any_link_loc=0):  # Adding this base link to any glob
        if any_link_loc == 0:
            any_link_loc = []
        try:
            if self.any_link_glob:  # don'w_thread try without something there
                glob_bool = bool(tlink in [i[0] for i in self.any_link_glob])
                if not glob_bool:
                    self.any_link_glob.append((tlink, parent_local))  # add if not there
                    any_link_loc.append((tlink, parent_local))
            else:
                self.any_link_glob = [(tlink, parent_local)]  # make it if starting empty
                any_link_loc = [(tlink, parent_local)]
        except Exception as e:
            self.myprint("exception in add_any: " + str(e))
        return any_link_loc

    def ck_base(self, this_link, thebase_part, base_links_local=0):
        if base_links_local == 0:
            base_links_local = []
        _IS_BASE = False
        dollar = False
        in_base_loc = False
        try:
            _IS_BASE = bool(thebase_part in this_link)

            if _IS_BASE:
                early_dollar = self.has_early_dollar(this_link, thebase_part)
                if early_dollar:
                    _IS_BASE = False  # base is embedded after something like twitter.com
                    return _IS_BASE, in_base_loc

            if base_links_local:
                in_base_loc = bool(this_link in [i for i in base_links_local])
        except Exception as e:
            self.myprint("Exception ck_base: " + str(e))
        return _IS_BASE, in_base_loc

    def print_errs(self, errlinks=0):
        if errlinks == 0:
            errlinks = []
        if errlinks:
            answer_string, e, fin_list = '', '', []
            p0, p1, p2 = "BAD LINK: ", " ERROR: ", " PARENT: "
            try:
                if errlinks:
                    errs = list(set(errlinks))
                    er_len = len(errs)
                    self.myprint("\nTotal errors: " + str(er_len))
                    self.myprint("-------------- Here are the errors ------------- :")
                    errs22 = sorted(errs, key=lambda x: x[0])  # sort on first
                    errs2 = set(errs22)
                    for e in errs2:
                        st0, st1, st2 = str(e[0]), str(e[1]), str(e[2])
                        an1 = p0 + st0
                        an2 = p1 + st1
                        an3 = st2

                        answer_string = [an1, an2, an3]
                        # answer_string = p0 + st0 + p1 + st1 + p2 + st2
                        fin_list.append(answer_string)
                        self.myprint(str(answer_string))
                else:
                    fin_list = [answer_string]
            except Exception as e:
                self.myprint('Exception print_errs: ' + str(e))
            return fin_list
        else:
            return []
    #-----------------------------------------------------------------------
    def do_response(self, a_link, p_link):
        t_err = 0
        #resp = rt.HTMLResponse
        resp = "0"
        try:
            self.myprint("-starting-get_home_links - just got this link: " + str(a_link))
            session = rt.HTMLSession()
            resp = session.get(a_link)
           # tp = isinstance(resp, 'HTMLResponse')
            tpp = type(resp)
            self.done_ln_gl_sing.append(a_link)  ## add to main done list
            t_err = self.ck_status_code(resp, a_link)  ## if there's    an error

        except Exception as e:
            if a_link not in self.err_links:
                self.err_links.append((a_link, str(e)[:42], p_link))
            self.myprint("GOT AN EXCEPTION inside do_response and added to errs: " + str(e))
            return resp, t_err
        return resp, t_err

    #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, _plin):
        has_bad, any_lnk_loc, new_lnks_loc, base_lnks_loc, response, ab_links = False,[], [], [], "0", []
        response, resp_err = self.do_response(mainlin, _plin)
        self.myprint("-------------INSIDE get_links! --------------: " + mainlin)

        try:
            if response.status_code:
                is_bool = True
                self.myprint("Status code: " + str(is_bool))
        except:
            self.myprint("Exception no valid response from: " + mainlin)
            return


        if resp_err == 0 and is_bool == True:  ## if there's an error  - 0 is good to continue
            try:
                ab_links = response.html.absolute_links
                new_lnks_loc = [ab for ab in ab_links]
            except Exception as e:
                self.myprint("exception inside get_links: " + str(e))

            self.myprint("got this far " + mainlin)
            for THIS_LN in new_lnks_loc:
                self.myprint("THIS_LN " + THIS_LN)
                if THIS_LN =='http://www.geocities.com/TheTropics/Coast/9678/':
                    print("here")
                    print("here")
                _IN_AN_LOC = self.ck_loc(THIS_LN, any_lnk_loc)
                if not _IN_AN_LOC and not self._DONE_YET(THIS_LN):    #NOT done yet  cg = check glob

                    try:
                        self.myprint("link: =============== " + THIS_LN)
                        self.myprint("new_lnks_loc === going to check bad data next: " + str(THIS_LN))
                        has_bad, good_suffix = self.ck_bad_data(THIS_LN)  # check for bad data
                        self.done_ln_gl_sing = self.check_for_bad_data(THIS_LN, self.done_ln_gl_sing)
                    except Exception as e:  self.handle_exc(e, THIS_LN, _plin)

                    try:
                        if self.ispar(THIS_LN, _plin) or has_bad:   pass
                        ##base_pt = divide_url(_plin)
                        _IS_BASE, in_base_local = self.ck_base(THIS_LN, self.divide_url(_plin), base_lnks_loc)

                        if _IS_BASE and good_suffix:  # IS base type
                            if not in_base_local:
                                base_lnks_loc.append(THIS_LN)


                            self.base_lnks_g = self.add_any_bse_g(THIS_LN, _plin, self.base_lnks_g)
                        else:                   #if not a home based link
                            if not self.ck_g(THIS_LN):  ## add bad suffix here too
                                any_lnk_loc = self.add_any(THIS_LN, _plin)  #does global too

                    except Exception as e:
                        self.handle_exc(e, THIS_LN, _plin)

        self.myprint('!! NEW----end get_home_links:---returning base_links_local: ' + str(base_lnks_loc))
        return list(set(base_lnks_loc))



    #############----------------------------------MAIN--------------------------
      #############----------------------------------MAIN-------------------------


    def main(self, a_site="a"):
        full_addy = self.ckaddymore(a_site)
        new_sorted, repeats, the_len = [], 0, 0
        self.myprint('\n\n------------------- STARTING OVER -----------------------')
        #tstart_main = perf_counter()
        self.myprint('In main() Getting first address: ' + full_addy)
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(full_addy, full_addy)  #first set of base
            self.myprint("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
            the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 6:
                repeats += 1
                self.myprint("repeats: " + str(repeats) + "-------------------!!In main loop ")
                for baselink in new_base_links_one:
                    new_base_links_two = self.get_links(baselink, full_addy)  # first set of base
                the_len = len(new_base_links_two)
                if the_len > 0:
                    new_base_links_one = new_base_links_two

        except Exception as e:
            self.myprint("Exception inside main_run: " + str(e))

        try:
            base_glob_now = self.base_lnks_g
            new_base_links_here, the_len_b = [], len(base_glob_now)
            while the_len_b and repeats < 6:

                repeats += 1
                self.myprint("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    base_lin = baselink[0]
                    parent_lin = baselink[1]
                    new_base_links_here = self.get_links(base_lin, parent_lin)  # first set of base
                the_len_b, base_glob_now = len(new_base_links_here), new_base_links_here

        except Exception as e:
            #self.handle_exc(e, base_lin, parent_lin)
            self.myprint("Exception after baselink in base_glob_now: " + str(e))


        tup = ()
        try:
            self.myprint("Step Two Done")
            any_link_to_check = list(self.any_link_glob)

            any_link_to_check = list(set(any_link_to_check))
            for tup in any_link_to_check:    #check non-base links
                self.get_simple_response(tup)
            for tup in self.base_lnks_g:
                self.get_simple_response(tup)

        except Exception as e:
            self.handle_exc(e, tup[0] ,tup[1])

        finlist = self.print_errs(self.err_links)
        #self.myprint("totalTime: " + str(perf_counter() - tstart_main))
        #self.myprint("Links checked: " + str(self.link_count))
        #x = len(self.done_ln_gl_sing)
        #self.myprint("errors: " + str(x))
        return finlist


if __name__ == "__main__":
    print("main")



