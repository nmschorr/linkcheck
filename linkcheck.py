# python 3
# Nancy Schorr, 2018
# this file is in active development
from time import perf_counter
import requests
from urllib.parse import urlparse
from linkchecklib import LinkCheckLib

class LinkCheck(LinkCheckLib):

    def __init__(self):
        super().__init__()

    #---------------------------------------------------------------------------------------
    def get_simple_response(self, lin_and_par_tup):
        self.myprint("inside get_simple_response: ")
        link_to_ck, parent = lin_and_par_tup[0], lin_and_par_tup[1]
        try:
            resp = requests.head(link_to_ck, timeout=7.0)
            self.myprint("THIS_LN: " + link_to_ck + " parent: " + parent + " in get_simple_response")
            stat = resp.status_code
            self.ck_status_code(link_to_ck, parent, stat)


        except Exception as e:
            self.myprint("Exception inside get_simple_response: ")
            a, b = self.handle_exc(e, link_to_ck, parent)
            return a, b

    #---------------------------------------------------------------------------------------
    def base_add_to_b_globs(self, zlink, parent_local):  # Adding this MAIN_DICT link to MAIN_DICT glob
        base_lnks_g = self.MAIN_DICT.get(self.rbase)

        try:
            if base_lnks_g:
                _IN_BASE_GLOB = bool(zlink in [i[0] for i in base_lnks_g])
                if not _IN_BASE_GLOB:  # if not already in this
                    base_lnks_g.append((zlink, parent_local))
                    self.myprint("Adding this BASE LINK to MAIN_DICT glob: " + zlink)

        except Exception as e:
            self.myprint("Exception base_add_to_b_globs: " + str(e))
        base_lnks_g2 = list(set(base_lnks_g))
        self.MAIN_DICT.update({self.rbase: base_lnks_g2})
    #---------------------------------------------------------------------------------------
    def add_to_others_glob(self, tlink, parent_local):  # Adding this MAIN_DICT link to any glob
        self.myprint("----------------------------!!! !!!! in add_to_others_glob: ")
        is_par = self.isTHEparent(tlink)
        if is_par:
            return
        other_lns_gl = self.MAIN_DICT.get(self.rothers)

        try:
            glob_bool = bool(tlink in [i[0] for i in other_lns_gl])
            if not glob_bool:
                self.myprint("appending to others: " )
                other_lns_gl.append((tlink, parent_local))  # add if not there

        except Exception as e:
            self.myprint("exception in add_others: " + str(e))

        self.MAIN_DICT.update({self.rothers: other_lns_gl})
        return


    # #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, par_link):
        self.myprint(" in get_links: " + mainlin)
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if mainlin not in done_ln_gl_sing:
            self.myprint(" in get_links:2 " + mainlin)

            other_lk_loc, new_lnks_loc, base_lnks_loc, response, ab_links = [], [], [], "0", []
            # #---------------  web response get here!!!!!!!!--------------------------------
            response, resp_err = self.do_response(mainlin, par_link)
            self.myprint("mainlin: " + response.mainlin  )
            self.myprint("Status code: " + str(response.status_code))

            try:
                if response.status_code != "0":
                    self.myprint("Status code: " + str(response.status_code))
                    e = self.MAIN_DICT.get(self.rerr)
                    e.append((mainlin, response.status_code, par_link))
                    self.MAIN_DICT.update({self.rerr: e})
            except Exception as e:
                self.myprint("Exception no valid response from: " + mainlin)
                return

            if resp_err == 0:  ## if there's an error  - 0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links: " + str(e))
                    return

                for the_link in new_lnks_loc:
                    b = self.findlink_place(the_link, par_link)
                             # self.MAIN_DICT.update({self.rdonesingles: done_ln_gl_sing})
                            # self.MAIN_DICT.update({self.rothers: other_lns_gl})
                    if b:
                        base_lnks_loc.append((the_link, par_link))

            return list(set(base_lnks_loc))
        else:
            return []

            # #----------------------------------------------------------------------get_links-

    def findlink_place(self, the_link, par_link):
        done_already_singles_g = self.MAIN_DICT.get(self.rdonesingles)
        self.myprint("Starting parsing of: " + the_link + "\n")
        other_lk_loc, new_lnks_loc, base_lnks_loc, ab_links = [], [], [], []

        issame = self.is_same_site_link(the_link)

        if issame:
            return

        elif the_link not in done_already_singles_g:  # if it hasn't been done yet
            self.myprint("in elif the_link")
            done_already_singles_g.append(the_link)
            #in_other_local = self.ck_if_in_other_loc(the_link, other_lk_loc)  #check again
            #if not in_other_local and not self._DONE_YET(the_link):    #NOT done yet  cg = check glob
            good_suffix = True
            is_base = False
            has_bad = False

            try:    #check for good suffix
                self.myprint("new_lnks_loc === going to check bad data next: " + the_link)
                has_bad, good_suffix = self.ck_bad_data(the_link)  # check for bad data
                if has_bad:
                    return

                is_base, notused = self.ck_for_base(the_link)
                in_base_glob  = self.ck_if_in_base_glob(the_link)

                print("answers: the_link, is_base, notused, in_base_glob: ", the_link, is_base, notused, in_base_glob)

                if is_base and good_suffix:  # IS MAIN_DICT type
                    if not in_base_glob:
                        self.myprint("!! adding to base: " + the_link)
                        rbas = self.MAIN_DICT.get(self.rbase)
                        rbas.append((the_link, par_link))
                        self.MAIN_DICT.update({self.rbase: rbas})
                        return the_link

                else:
                    self.add_to_others_glob(the_link, par_link)  #does global too
                    self.myprint("!! added to others: " + the_link)
                    return

            except Exception as e:
                self.handle_exc(e, the_link, par_link)
                return

        self.MAIN_DICT.update({self.rdonesingles: done_already_singles_g})


      #############----------------------------------MAIN-------------------------

    def main(self, msite="a.htm"):
        tstart = perf_counter()

        self.MAIN_DICT.update({ self.ORIGNAME: msite })
        w_site = self.mkwww(msite)
        self.MAIN_DICT.update({self.ORIGNAMEwww:w_site})

        link_w_scheme = LinkCheckLib.mk_link_w_scheme(msite)
        parsed = urlparse(link_w_scheme)
        base_parsed = str(parsed.netloc)
        base_parsed_www = 'www.' + base_parsed
        self.MAIN_DICT.update({ self.BASENAME: base_parsed })
        self.MAIN_DICT.update({ self.BASENAMEwww: base_parsed_www })
        self.myprint('In main() Getting first address: ' + link_w_scheme)
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(link_w_scheme, link_w_scheme)  #first set of MAIN_DICT
            self.myprint("Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time
            if base_only_plain_repeat:
                base_first_len = len(base_only_plain_repeat)
                print("length base_only_plain_repeat: " + str(base_first_len))
                self.step_one(base_only_plain_repeat, link_w_scheme)
                print("past next line")

        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        self.get_more_baselinks()
        self.other_links_big_check()

        finlist = self.return_errors()
        self.myprint("Errors: ")
        for i in finlist:
               print("err: " + i[0])
        print("totalTime: " + str(perf_counter() - tstart))
        return finlist

    #-------------------------------------------------------------------

    def step_one(self, base_only_plain_repeat_here, link_w_scheme_here):
        self.myprint("In step_one")
        self.myprint("step_one 0c")
        try:
            new_base_links_two, new_base_links_one = [], base_only_plain_repeat_here
            repeats = 0

            base_len = len(base_only_plain_repeat_here)
            while base_len and repeats < 6:
                self.myprint("step_one 1xxx")
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink in new_base_links_one:
                    self.myprint("step_one 1")
                    isparent= self.isTHEparent(baselink)
                    self.myprint("isparent: " + isparent)
                    self.myprint("step_one 0")
                    if not isparent:
                        self.myprint("step_one 2")
                        self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                        new_base_links_tmp = self.get_links(baselink, link_w_scheme_here)  # first set of MAIN_DICT
                        self.myprint("step_one 3")
                        new_base_links_two = self.rem_errs(new_base_links_tmp)
                self.myprint("step_one 3")

                base_len = len(new_base_links_two)
                self.myprint("five3")
                if base_len > 0:
                    new_base_links_one = new_base_links_two
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside step_one: " + str(e))

    #-------------------------------------------------------------------

    def get_more_baselinks(self):
        self.myprint("In get_more_baselinks")
        base_glob_now = self.MAIN_DICT.get(self.rbase)
        repeats = 0
        alreadychecked = []
        try:
            new_base_links_here, the_len_b = [], len(base_glob_now)
            while the_len_b and repeats < 6:

                repeats += 1
                self.myprint('\n' + "Repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    if baselink not in alreadychecked:
                        base_lin, BASE_URL = baselink[0], baselink[1]  # split

                        new_base_links_here = self.get_links(base_lin, BASE_URL)  # first set of MAIN_DICT


                        alreadychecked.append(baselink)
                        base_glob_now = base_glob_now.append(new_base_links_here)
                        the_len_b  = len(new_base_links_here)

            self.MAIN_DICT.update({self.rbase: base_glob_now})

        except Exception as e:
            self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def other_links_big_check(self):
        self.myprint("In other_links_big_check1")
        rothers= self.MAIN_DICT.get(self.rothers)
        done_singles= self.MAIN_DICT.get(self.rdonesingles)
        other_to_ck  =  list(set(rothers))
        self.myprint("rothers: " + str(rothers))
        self.myprint("done_singles: " + str(done_singles))
        self.myprint("other_to_ck: " + str(other_to_ck))
        self.myprint("Step Two Done. In other_links_big_check2")


        try:
            self.myprint("Step Two Done. In other_links_big_check3")

            if other_to_ck:
                self.myprint("Step Two Done. In other_links_big_check4")
                for tupy in other_to_ck:  # check non-MAIN_DICT links
                    self.myprint("Step Two Done. In other_links_big_check5")
                    done_singles.append(tupy[0])
                    self.get_simple_response(tupy)

                self.MAIN_DICT.update({self.rdonesingles: done_singles})

        except Exception as e:
            if tupy:
                a, b = self.handle_exc(e, tupy[0], tupy[1])
                return a, b
            else:
                self.myprint((str(e)))
                return
    #-------------------------------------------------------------------

k = "kaldu.com"
s = 'schorrmedia.com/m.html'
#s = 'schorrmedia.com'

if __name__ == "__main__":
    lc = LinkCheck()
    lc.main(s)