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

            other_lk_loc, new_lnks_loc, base_lnks_loc_tup, response, ab_links = [], [], [], "0", []
            # #---------------  web response get here!!!!!!!!--------------------------------
            response, resp_err = self.do_response(mainlin, par_link)
            self.myprint("mainlin: " + mainlin  )
            self.myprint("Status code: " + str(response.status_code))

            if resp_err == 0:  ## 0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links: " + str(e))
                    return

                for the_link in new_lnks_loc:
                    issame = self.is_same_site_link(the_link)
                    if issame:
                        continue
                    base = self.getlinks_inside(the_link, par_link)
                             # self.MAIN_DICT.update({self.rdonesingles: done_ln_gl_sing})
                            # self.MAIN_DICT.update({self.rothers: other_lns_gl})
                    if base:
                        base_lnks_loc_tup.append((the_link, par_link))

            return list(set(base_lnks_loc_tup))
        else:
            return []

# #----------------------------------------------------------------------get_links-

    def getlinks_inside(self, the_link, par_link):
        done_already_singles_g = self.MAIN_DICT.get(self.rdonesingles)
        self.myprint("Starting parsing of: " + the_link + "\n")

        # issame = self.is_same_site_link(the_link)
        # if issame:
        #     return

        if the_link not in done_already_singles_g:  # if it hasn't been done yet
            self.myprint("in elif the_link")

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
                        return is_base

                else:
                    self.add_to_others_glob(the_link, par_link)  #does global too
                    self.myprint("!! added to others: " + the_link)


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
            base_only_plain_repeat_tup = self.get_links(link_w_scheme, link_w_scheme)  #first set of MAIN_DICT
            self.myprint("Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time
            if base_only_plain_repeat_tup:
                base_first_len = len(base_only_plain_repeat_tup)
                print("length base_only_plain_repeat: " + str(base_first_len))
                print("xxxxxxxxxxxxxxxxxx 1")
                new_base_tups = self.main_step_one_for_base(base_only_plain_repeat_tup, link_w_scheme)
                print("xxxxxxxxxxxxxxxx 2")

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

    def main_step_one_for_base(self, base_only_plain_repeat_tup2, link_w_scheme_here):
        self.myprint("In step_one")
        try:
            new_base_links_two, new_base_links_one_tups = [], base_only_plain_repeat_tup2
            repeats = 0

            base_len = len(base_only_plain_repeat_tup2)
            while base_len and repeats < 6:
                self.myprint("step_one 1xxx")
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink in new_base_links_one_tups[0]:
                    self.myprint("step_one 1aaaaa")
                    print("xxxxxxxxxxxxxxxxxx 3 about to check if parent-------------------------------------")
                    isparent_bool= self.isTHEparent(baselink)
                    print("xxxxxxxxxxxxxxxxxx 4")
                    self.myprint("isparent: " + str(isparent_bool))
                    self.myprint("step_one 0")
                    if not isparent_bool:
                        self.myprint("step_one 2")
                        self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                        new_base_links_tmp = self.get_links(baselink, link_w_scheme_here)  # first set of MAIN_DICT
                        self.myprint("step_one 3")
                        new_base_links_two = self.rem_errs(new_base_links_tmp)

                self.myprint("step_one 3")
                print("xxxxxxxxxxxxxxxxxx 5")

                base_len = len(new_base_links_two)
                self.myprint("five3")
                if base_len > 0:
                    base_glob_now = self.MAIN_DICT.get(self.rbase)
                    base_glob_now.append(new_base_links_two)
                    #self.MAIN_DICT.update({self.rbase:base_glob_now})
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside step_one-------------------------------------------: " + str(e))

        return new_base_links_one_tups

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
                        self.myprint("------------------------xxxxxxx")

                        alreadychecked.append(baselink)
                        base_glob_now.append(new_base_links_here)
                        the_len_b  = len(new_base_links_here)
                        self.myprint("------------------------xxxxxxxyyy")

            self.MAIN_DICT.update({self.rbase: base_glob_now})

        except Exception as e:
            self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def other_links_big_check(self):
        self.myprint("In other_links_big_check1")
        other_to_ck= self.MAIN_DICT.get(self.rothers)
        done_singles= self.MAIN_DICT.get(self.rdonesingles)

        self.myprint("done_singles: " + str(done_singles))
        self.myprint("other_to_ck: " + str(other_to_ck))
        self.myprint("-----------------------------------In other_links_big_check2")

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