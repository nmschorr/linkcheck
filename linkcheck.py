# python 3
# Nancy Schorr, 2018
# this file is in active development
from time import perf_counter
from urllib.parse import urlparse
from linkchecklib import LinkCheckLib

class LinkCheck(LinkCheckLib):
    base_only_plain_repeat_tup = []

    def __init__(self):
        super().__init__()
        base_only_plain_repeat_tup = []
        self.base_only_plain_repeat_tup = base_only_plain_repeat_tup


    # #----------------------------------------------------------------------get_links-

    def get_links_for_one_pair(self, mainlin, par_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if mainlin not in done_ln_gl_sing:
            self.myprint(" in get_links:2 " + mainlin)

            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------
            response, resp_err = self.do_response(mainlin, par_link)
            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------

            if response is not None:  ## GOOD!  0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links: " + str(e))
                    return

                for the_link in new_lnks_loc:
                    if self.is_same_site_link(the_link):
                        continue
                    self.getlinks_base_ck_two(the_link, par_link)

# #----------------------------------------------------------------------get_links-

    def getlinks_base_ck_two(self, the_link, par_link):
        rbas = self.MAIN_DICT.get(self.rbase)
        self.myprint("Starting parsing of: " + the_link + "\n")
        # for ttup in  self.base_only_plain_repeat_tup:
        #     the_link = ttup[0]
        #     par_link = ttup[1]

        try:    #check for good suffix
            self.myprint("new_lnks_loc === going to check bad data next: " + the_link)
            has_bad, good_suffix = self.ck_bad_data(the_link)  # check for bad data
            if has_bad:
                return

            is_base, notused = self.ck_for_base(the_link)

            print("answers: the_link, is_base, notused: ", the_link, str(is_base))
            print(" rbas: ",  rbas)

            if is_base and good_suffix:  # IS MAIN_DICT type
                inbase_bool = self.ck_if_in_base_glob(the_link)
                if not inbase_bool:
                    self.myprint("!! adding to base: " + the_link + " " +  par_link)
                    if (the_link, par_link):
                        rbas.append((the_link, par_link))
                        self.MAIN_DICT.update({self.rbase: rbas})
                        self.base_only_plain_repeat_tup.append((the_link, par_link))

            else:
                self.add_to_others_glob(the_link, par_link)  #does global too
                self.myprint("!! added to others: " + the_link)

        except Exception as e:
            self.handle_exc(e, the_link, par_link)


      #############----------------------------------MAIN-------------------------
    def main_setup(self, msite):
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
        tstart = perf_counter()
        link_w_scheme = self.main_setup(msite)
        try:
            #############---------step ONE:
            self.get_links_for_one_pair(link_w_scheme, link_w_scheme)  #first set of MAIN_DICT
            self.myprint("Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time
            self.main_loop_get_links(link_w_scheme)

        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        self.main_two_more_baselinks()
        self.main_run_simple()

        finlist = self.return_errors()
        self.myprint("Errors: ")
        for i in finlist:
               print("err: " + i[0] + " parent: " + i[1])
       # print("totalTime: " + str(perf_counter() - tstart))
        return finlist

    #-------------------------------------------------------------------

    def main_loop_get_links(self):
        self.myprint("In step_one")
        try:
            repeats = 0
            new_base_links_two_tup = []
            base_len = len(self.base_only_plain_repeat_tup)
            while base_len and repeats < 6:
                self.myprint("step_one 1xxx")
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink, parent in self.base_only_plain_repeat_tup[0], self.base_only_plain_repeat_tup[1]:
                    self.myprint("step_one 1aaaaa")
                    print("xxxxxxxxxxxxxxxxxx 3 about to check if parent-------------------------------------")
                    isparent_bool= self.isTHEparent(baselink)
                    #print("xxxxxxxxxxxxxxxxxx 4")
                    self.myprint("isparent: " + str(isparent_bool))
                    if not isparent_bool:
                        self.myprint("step_one 2")
                        self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
          #---------------------getlinks !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        new_base_links_tmp = self.get_links_for_one_pair(baselink, parent)  # first set of MAIN_DICT

                        self.myprint("step_one 3")
                        new_base_links_two_tup = self.rem_errs_tups(new_base_links_tmp)

                self.myprint("step_one 3")
                print("xxxxxxxxxxxxxxxxxx 5")

                self.myprint("five3")
                if new_base_links_two_tup:
                    base_glob_now = self.MAIN_DICT.get(self.rbase)
                    base_glob_now.append(new_base_links_two_tup)
                    self.myprint("!! new_base_links_two_tup: " + new_base_links_two_tup )
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside step_one-------------------------------------------: " + str(e))

    #-------------------------------------------------------------------

    def main_two_more_baselinks(self, first=0):
        self.myprint("In get_more_baselinks")
        base_glob_now = self.MAIN_DICT.get(self.rbase)
        the_len_b = 0
        repeats = 0
        alreadychecked = []
        if base_glob_now:

            try:
                the_len_b = len(base_glob_now)
                new_base_links_here = []
                while the_len_b and repeats < 6:

                    repeats += 1
                    self.myprint('\n' + "Repeats: " + str(repeats) + "-------------------!!In main loop")
                    if base_glob_now:

                        for baselink in base_glob_now:
                            if baselink not in alreadychecked:
                                base_lin, BASE_URL = baselink[0], baselink[1]  # split

                                new_base_links_here = self.get_links_for_one_pair(base_lin, BASE_URL)  # first set of MAIN_DICT
                                self.myprint("------------------------xxxxxxx")

                                alreadychecked.append(baselink)
                                if new_base_links_here:
                                    base_glob_now.append(new_base_links_here)
                                    the_len_b  = len(new_base_links_here)
                                else:
                                    the_len_b = 0
                                self.myprint("------------------------xxxxxxxyyy")

                        self.myprint("adding to rbase: " + base_glob_now)
                        self.MAIN_DICT.update({self.rbase: base_glob_now})

            except Exception as e:
                self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def main_run_simple(self):
        self.myprint("-----------------------------------In other_links_big_check2")
        other_to_ck= self.MAIN_DICT.get(self.rothers)
        done_singles= self.MAIN_DICT.get(self.rdonesingles)
        base_to_ck= self.MAIN_DICT.get(self.rbase)
        tupy = None

        self.myprint("done_singles: " + str(done_singles)+"other_to_ck: " + str(other_to_ck))
        #self.myprint("-----------------------------------In other_links_big_check2")

        try:
            if other_to_ck:
                for tupy in other_to_ck:  # check non-MAIN_DICT links
                    self.get_simple_response(tupy)

        except Exception as e:
            if tupy:
                self.handle_exc(e, tupy[0], tupy[1])
            else:
                self.myprint((str(e)))

        try:
            if base_to_ck:
                for tupy in base_to_ck:  # check non-MAIN_DICT links
                    self.get_simple_response(tupy)

        except Exception as e:
            if tupy:
                self.handle_exc(e, tupy[0], tupy[1])
            else:
                self.myprint((str(e)))
    #-------------------------------------------------------------------

k = "kaldu.com"
s = 'schorrmedia.com/m.html'
#s = 'schorrmedia.com'

if __name__ == "__main__":
    lc = LinkCheck()
    lc.main(s)