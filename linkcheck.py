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

    def get_links_for_one_pair(self, mainlin, par_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if mainlin not in done_ln_gl_sing:
            self.myprint(" in get_links_for_one_pair " + mainlin)

            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------
            response = self.do_response(mainlin, par_link)
            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------

            if response is not None:  ## GOOD!  0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links_for_one_pair: " + str(e))
                    return

                for the_link in new_lnks_loc:
                    if self.ret_bool_if_same_as_orig_url(the_link):
                        continue
                    self.push_links_Base_or_Other(the_link, par_link)

# #----------------------------------------------------------------------get_links-

    def push_links_Base_or_Other(self, the_link, par_link):
        self.myprint("Starting getlinks_base_ck_two for: " + the_link)
        inbase_bool = self.ret_bool_if_in_BASE_glob(the_link)
        if inbase_bool:
            #self.myprint("================== found inbase_bool dupe")
            return

        try:    #check for good suffix
            self.myprint("new_lnks_loc === going to check bad data next: " + the_link)
            has_bad, good_suffix = self.ck_bad_data(the_link)  # check for bad data
            if has_bad:
                return

            is_base = self.ret_bool_if_BASE(the_link)

            if is_base and good_suffix:  # IS MAIN_DICT type
                self.myprint("!! adding to base: " + the_link + " " +  par_link)
                self.MAIN_DICT.get(self.rbase).append((the_link, par_link))
                self.base_only_plain_repeat_tup.append((the_link, par_link))

            else:  ## will accept base with bad suffix
                self.add_to_others_glob(the_link, par_link)  #does global too

        except Exception as e:
            self.handle_exc(the_link, e, par_link)


      #############----------------------------------MAIN-------------------------
    def main_setup(self, msite):
        self.MAIN_DICT.update({ self.ORIGNAME: msite })
        w_site = self.make_www_url(msite)
        self.MAIN_DICT.update({self.ORIGNAMEwww:w_site})

        msite_w_scheme = LinkCheckLib.mk_link_w_scheme(msite)
        parsed = urlparse(msite_w_scheme)
        base_netloc = str(parsed.netloc)
        base_netloc_www = 'www.' + base_netloc
        self.MAIN_DICT.update({ self.BASENAME: base_netloc })
        self.MAIN_DICT.update({ self.BASENAMEwww: base_netloc_www })
        self.myprint('In main_setup() Getting first address: ' + msite_w_scheme)
        return msite_w_scheme



      #############----------------------------------MAIN-------------------------

    def main(self, msite="a.htm"):
        finlist = None
        tstart = perf_counter()
        link_w_scheme = self.main_setup(msite)
        try:
            #############---------step ONE:
            self.get_links_for_one_pair(link_w_scheme, link_w_scheme)  #first set of MAIN_DICT
            self.myprint("In main(). Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time
            self.main_loop_get_links()

        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        try:
            self.main_two_more_baselinks()
            self.main_run_simple()

            finlist = self.return_errors()
            for i in finlist:
                print("broken link: " + i[0] + " found on parent: " + i[2])
        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        print("totalTime: " + str(perf_counter() - tstart))
        return finlist

    #-------------------------------------------------------------------

    def main_loop_get_links(self):
        self.myprint("In main_loop_get_links")
        try:
            repeats = 0
            new_base_links_two_tup = []
            base_len = len(self.base_only_plain_repeat_tup)
            while base_len and repeats < 6:
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink, parent in self.base_only_plain_repeat_tup[0], self.base_only_plain_repeat_tup[1]:
                    isparent_bool= self.isTHEparent(baselink)
                    if not isparent_bool:
                        self.get_links_for_one_pair(baselink, parent)  # first set of MAIN_DICT

                if new_base_links_two_tup:
                    self.MAIN_DICT.get(self.rbase).append(new_base_links_two_tup)
                    #self.MAIN_DICT.update({self.rbase:base_glob_now})
                    self.myprint("!! new_base_links_two_tup: " + new_base_links_two_tup )
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside step_one-------------------------------------------: " + str(e))

    #-------------------------------------------------------------------

    def main_two_more_baselinks(self):
        self.myprint("In get_more_baselinks")
        base_glob_now_tup = self.MAIN_DICT.get(self.rbase)
        the_len_b = 0
        repeats = 0
        alreadychecked_tups = []
        if base_glob_now_tup:

            try:
                the_len_b = len(base_glob_now_tup)
                new_base_links_here = []
                while the_len_b and repeats < 6:

                    repeats += 1
                    self.myprint('\n' + "Repeats: " + str(repeats) + "-------------------!!In main loop")
                    if base_glob_now_tup:

                        for baselink_tup in base_glob_now_tup:
                            if baselink_tup not in alreadychecked_tups:
                                self.get_links_for_one_pair(baselink_tup[0], baselink_tup[1])  # first set of MAIN_DICT
                                alreadychecked_tups.append(baselink_tup)

                        #self.myprint("adding to rbase: " + (str(base_glob_now)))
                        #self.MAIN_DICT.update({self.rbase: base_glob_now})

            except Exception as e:
                self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def main_run_simple(self):
        self.myprint("-----------------------------------In main_run_simple()")
        other_to_ck= self.MAIN_DICT.get(self.rothers)
        base_to_ck= self.MAIN_DICT.get(self.rbase)
        tupy = (0,0)

        #self.myprint("done_singles: " + str(done_singles)+"other_to_ck: " + str(other_to_ck))
        #self.myprint("-----------------------------------In other_links_big_check2")

        try:
            if other_to_ck:
                for tupy in other_to_ck:  # check non-MAIN_DICT links
                    self.get_simple_response(tupy)

            if base_to_ck:
                for tupy in base_to_ck:  # check non-MAIN_DICT links
                    self.get_simple_response(tupy)

        except Exception as e:
                self.handle_exc(tupy[0], e, tupy[1])

    #-------------------------------------------------------------------

k = "kaldu.com"
s = 'schorrmedia.com/m.html'
#s = 'schorrmedia.com'
r = 'repercussions.com'
a = 'astrology1234.com'

if __name__ == "__main__":
    lc = LinkCheck()
    lc.main(s)