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
        doespagematch = False
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdonesingles)
        if mainlin not in done_ln_gl_sing:
            self.myprint(" in get_links_for_one_pair " + mainlin)

            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------
            response = self.do_get_request(mainlin, par_link)
            # #---------------  web response get here!!!!!!!!------------------------web response get here!!!!!!!!--------




            if response.url == mainlin:
                doespagematch = True

            if doespagematch == False:
                isbase = self.ret_bool_if_BASE(response.url)
                if not isbase:
                    return     #don't bother checking with it's links since it's been redirected somewhere


            if response is not None:  ## GOOD!  0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))  #reduce dupes
                except Exception as e:
                    self.myprint("Exception inside get_links_for_one_pair: " + str(e))
                    return

                the_link: object
                for the_link in new_lnks_loc:
                    if self.ret_bool_if_same_as_orig_url(the_link):
                        continue

                    else:
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


      #############----------------------------------MAIN setup-------------------------
    def main_setup(self, msite):
        self.MAIN_DICT.update({ self.ORIGNAME: msite })
        msite_www = self.make_www_url(msite)
        self.MAIN_DICT.update({self.ORIGNAMEwww:msite_www})
        msite_www_w_scheme = LinkCheckLib.mk_link_w_scheme(msite_www)

        msite_w_scheme = LinkCheckLib.mk_link_w_scheme(msite)
        parsed = urlparse(msite_w_scheme)
        base_netloc = str(parsed.netloc)
        # base_netloc_www = 'www.' + base_netloc
        if base_netloc[:4]!= 'www.':
            base_netloc_www = 'www.' + base_netloc

        self.MAIN_DICT.update({ self.BASENAME: msite  })
        self.MAIN_DICT.update({ self.BASENAMEwww:msite_www })
        # self.MAIN_DICT.update({ self.BASENAME: base_netloc })
        # self.MAIN_DICT.update({ self.BASENAMEwww: base_netloc_www })

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
            self.myprint("In main(). Step One Done with get_links_for_one_pair. ")   ##first time:  HOME PAGE ONLY  ##first time

            self.main_one_loop_get_links()

        except Exception as e:
            self.myprint("Exception inside main: " + str(e))

        try:
            self.main_two_more_baselinks()
            self.main_three_run_head()

            finlist = self.return_errors()
            finlistr = self.return_redirs()
            print()
            self.myprint("Here are the broken links: ")
            for i in finlist:
                print("  Broken link: " + i[0] + " found on parent: " + str(i[2]) )

            print()
            self.myprint("Here are the redirect problems: ")
            for i in finlistr:
                print("  Redirected link: " + i[0]  + " found on parent: " + i[1] + " redirected to: " + i[2]  )

        except Exception as e:
            self.myprint("Exception inside main 1: " + str(e))

        ##redirrs = self.main_loop_redirs()
        print()
        print("TotalTime: " + str(perf_counter() - tstart))
        return finlist, finlistr

    #-------------------------------------------------------------------
    def main_one_loop_get_links(self):
        self.myprint("In main_one_loop_get_links")
        try:
            repeats, new_base_links_two_tup = 0, []

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
        self.myprint("In main_two_more_baselinks")
        base_glob_now_tup = self.MAIN_DICT.get(self.rbase)
        repeats = 0
        alreadychecked_tups = []
        if base_glob_now_tup:

            try:
                the_len_b = len(base_glob_now_tup)
                new_base_links_here = []
                while the_len_b and repeats < 6:

                    repeats += 1
                    self.myprint('\n' + "Repeats: " + str(repeats) + "-------------------!!In main loop main_two_more_baselinks.")
                    if base_glob_now_tup:

                        for baselink_tup in base_glob_now_tup:
                            if baselink_tup not in alreadychecked_tups:
                                self.get_links_for_one_pair(baselink_tup[0], baselink_tup[1])  # first set of MAIN_DICT
                                alreadychecked_tups.append(baselink_tup)

            except Exception as e:
                self.myprint("Exception after baselink in main_two_more_baselinks: " + str(e))

    #-------------------------------------------------------------------

    def main_three_run_head(self):
        self.myprint("-----------------------------------In main_three_run_head()")
        other_to_ck= self.MAIN_DICT.get(self.rothers)
        base_to_ck= self.MAIN_DICT.get(self.rbase)
        #tupy1 = (0,0)

        #self.myprint("done_singles: " + str(done_singles)+"other_to_ck: " + str(other_to_ck))
        #self.myprint("-----------------------------------In other_links_big_check2")

        try:
            if other_to_ck:
                for tupy1 in other_to_ck:  # check non-MAIN_DICT links
                    self.do_head_request(tupy1)

            if base_to_ck:
                for tupy2 in base_to_ck:  # check non-MAIN_DICT links
                    self.do_head_request(tupy2)

        except Exception as e:
                #self.handle_exc(tupy[0], e, tupy[1])
                self.myprint("Exception main_three_run_head: " + str(e))

    #-------------------------------------------------------------------

ka = "kaldu.com"
ss = 'schorrmedia.com'
nss = 'nancyschorr.com'
repers = 'repercussions.com'
ast = 'astrology1234.com'
aaa = 'calendarastrology.com'
stt = 'starpresence.net'
wb = 'www.workbridgeassociates.com/locations/silicon-valley'

if __name__ == "__main__":
    #None
    # lc = LinkCheck()
    lc = LinkCheck()
    lc.main(wb)





    # def main_loop_redirs(self):
    #     try:
    #         reds1 = self.MAIN_DICT.get(self.redir)
    #         reds = list(set(reds1))
    #         redlist = []
    #         for loc in reds:
    #             answer_string = [ loc[0], str(loc[1]), loc[2]]
    #             redlist.append(answer_string)
    #
    #         print()
    #         self.myprint("Here are the redirected links which should be fixed: ")
    #         for i in redlist:
    #             print("  broken link: " + i[0] + " found on parent: " + i[2])
    #     except Exception as e:
    #         self.myprint("Exception inside main_loop_redirs: " + str(e))
    #     return redlist


    # -------------------------------------------------------------------