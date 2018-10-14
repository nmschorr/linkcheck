# python 3
# Nancy Schorr, 2018
# this file is in active development
from time import perf_counter
from urllib.parse import urlparse
from linkchecklib import LinkCheckLib

class LinkCheck(LinkCheckLib):

    def __init__(self):
        super().__init__()

    # #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, par_link):
        self.myprint(" in get_links: " + mainlin)
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if mainlin not in done_ln_gl_sing:
            self.myprint(" in get_links:2 " + mainlin)

            #other_lk_loc, new_lnks_loc, base_lnks_loc_tup, response, ab_links = [], [], [], "0", []
            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------
            response, resp_err = self.do_response(mainlin, par_link)
            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------

            if resp_err == 0:  ## GOOD!  0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links: " + str(e))
                    return

                for the_link in new_lnks_loc:
                    issame_url = self.is_same_site_link(the_link)
                    if issame_url:
                        continue
                    self.getlinks_base_ck_two(the_link, par_link)

        else:
            return

# #----------------------------------------------------------------------get_links-

    def getlinks_base_ck_two(self, the_link, par_link):
        rbas = self.MAIN_DICT.get(self.rbase)
        self.myprint("Starting parsing of: " + the_link + "\n")

        try:    #check for good suffix
            self.myprint("new_lnks_loc === going to check bad data next: " + the_link)
            has_bad, good_suffix = self.ck_bad_data(the_link)  # check for bad data
            if has_bad:
                return

            is_base, notused = self.ck_for_base(the_link)

            print("answers: the_link, is_base, notused, in_base_glob: ", the_link, is_base, notused, rbas)

            if is_base and good_suffix:  # IS MAIN_DICT type
                inbase_bool = self.ck_if_in_base_glob(the_link)
                if not inbase_bool:
                    self.myprint("!! adding to base: " + the_link)
                    rbas.append((the_link, par_link))
                    self.MAIN_DICT.update({self.rbase: rbas})

            else:
                self.add_to_others_glob(the_link, par_link)  #does global too
                self.myprint("!! added to others: " + the_link)

        except Exception as e:
            self.handle_exc(e, the_link, par_link)


      #############----------------------------------MAIN-------------------------
    def main_setup(self, msite):
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
        return link_w_scheme
      #############----------------------------------MAIN-------------------------

    def main(self, msite="a.htm"):
        link_w_scheme = self.main_setup(msite)
        try:
            #############---------step ONE:
            base_only_plain_repeat_tup = self.get_links(link_w_scheme, link_w_scheme)  #first set of MAIN_DICT
            self.myprint("Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time
            new_base_tups = self.main_loop(the_link, par_link)
            if base_only_plain_repeat_tup:
                base_first_len = len(base_only_plain_repeat_tup)
                print("length base_only_plain_repeat: " + str(base_first_len))
                print("xxxxxxxxxxxxxxxxxx 1")
                new_base_tups = self.main_loop(base_only_plain_repeat_tup, link_w_scheme)
                print("xxxxxxxxxxxxxxxx 2")

        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        self.main_two_more_baselinks()
        self.main_run_simple()

        finlist = self.return_errors()
        self.myprint("Errors: ")
        for i in finlist:
               print("err: " + i[0])
        print("totalTime: " + str(perf_counter() - tstart))
        return finlist

    #-------------------------------------------------------------------

    def main_loop(self, base_only_plain_repeat_tup2, link_w_scheme_here):
        self.myprint("In step_one")
        try:
            repeats = 0

            base_len = len(base_only_plain_repeat_tup2)
            while base_len and repeats < 6:
                self.myprint("step_one 1xxx")
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink in base_only_plain_repeat_tup2[0]:
                    self.myprint("step_one 1aaaaa")
                    print("xxxxxxxxxxxxxxxxxx 3 about to check if parent-------------------------------------")
                    isparent_bool= self.isTHEparent(baselink)
                    print("xxxxxxxxxxxxxxxxxx 4")
                    self.myprint("isparent: " + str(isparent_bool))
                    self.myprint("step_one 0")
                    if not isparent_bool:
                        self.myprint("step_one 2")
                        self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
          #---------------------getlinks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        new_base_links_tmp = self.get_links(baselink, link_w_scheme_here)  # first set of MAIN_DICT

                        self.myprint("step_one 3")
                        new_base_links_two = self.rem_errs_tups(new_base_links_tmp)

                self.myprint("step_one 3")
                print("xxxxxxxxxxxxxxxxxx 5")

                self.myprint("five3")
                if new_base_links_two:
                    base_glob_now = self.MAIN_DICT.get(self.rbase)
                    base_glob_now.append(new_base_links_two)
                    #self.MAIN_DICT.update({self.rbase:base_glob_now})
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside step_one-------------------------------------------: " + str(e))

    #-------------------------------------------------------------------

    def main_two_more_baselinks(self, first=0):
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
                        self.myprint("------------------------xxxxxxx")

                        alreadychecked.append(baselink)
                        base_glob_now.append(new_base_links_here)
                        the_len_b  = len(new_base_links_here)
                        self.myprint("------------------------xxxxxxxyyy")

            self.MAIN_DICT.update({self.rbase: base_glob_now})

        except Exception as e:
            self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def main_run_simple(self):
        self.myprint("-----------------------------------In other_links_big_check2")
        other_to_ck= self.MAIN_DICT.get(self.rothers)
        done_singles= self.MAIN_DICT.get(self.rdonesingles)

        self.myprint("done_singles: " + str(done_singles)+"other_to_ck: " + str(other_to_ck))
        #self.myprint("-----------------------------------In other_links_big_check2")

        try:
            if other_to_ck:

                for tupy in other_to_ck:  # check non-MAIN_DICT links
                    a, b = self.get_simple_response(tupy)


        except Exception as e:
            if tupy:
                a, b = self.handle_exc(e, tupy[0], tupy[1])
                return
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