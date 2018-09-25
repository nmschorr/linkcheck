# python 3
# Nancy Schorr, 2018
# this file is in active development
#from time import perf_counter
#import requests_html as rt

from linkchecklib import *
import requests




class LinkCheck(LinkCheckLib):

    def __init__(self):
        super().__init__()
        # done_ln_gl_sing = []
        # any_link_glob = []
        # base_lnks_g = []


    def get_simple_response(self, lin_and_par_tup):
        link_count, stat = 0, 0
        #er, response = "0", "0"
        link_to_ck, parent = lin_and_par_tup[0], lin_and_par_tup[1]
        link_count += 1
        LinkCheckLib.myprint("Checking this link: " + link_to_ck )
        try:
            stat = requests.get(link_to_ck).status_code
            self.ck_status_code_simple(link_to_ck, parent, stat)

        except Exception as e:
            #LinkCheckLib.myprint("Exception inside get_simple_response: " + str(e))
            self.handle_exc(e, link_to_ck, parent)


    #---------------------------------------------------------------------------------------
    def add_any_bse_g(self, zlink, parent_local):  # Adding this base link to base glob
        base_lnks_g = self.base.get(self.rb)

        if base_lnks_g is None:
            base_lnks_g = []
        try:
            if base_lnks_g:
                _IN_BASE_GLOB = bool(zlink in [i[0] for i in base_lnks_g])
                if not _IN_BASE_GLOB:  # if not already in this
                    base_lnks_g.append((zlink, parent_local))
                    LinkCheckLib.myprint("Adding this BASE LINK to base glob: " + zlink)
            else:
                base_lnks_g = [(zlink, parent_local)]

        except Exception as e:
            LinkCheckLib.myprint("Exception add_any_bse_g: " + str(e))

        self.base.update({self.rb: base_lnks_g})
    #---------------------------------------------------------------------------------------
    def add_any(self, tlink, parent_local, any_link_loc=None):  # Adding this base link to any glob
        any_link_glob = self.base.get(self.ra)
        if any_link_loc is None:
            any_link_loc = []
        try:
            if any_link_glob:  # don'w_thread try without something there
                glob_bool = bool(tlink in [i[0] for i in any_link_glob])
                if not glob_bool:
                    any_link_glob.append((tlink, parent_local))  # add if not there
                    any_link_loc.append((tlink, parent_local))
            else:
                any_link_glob.append((tlink, parent_local))  # make it if starting empty
                any_link_loc.append((tlink, parent_local))
            self.base.update({self.ra: any_link_glob})
        except Exception as e:
            LinkCheckLib.myprint("exception in add_any: " + str(e))

        return any_link_loc


    # #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, _plin):
        done_ln_gl_sing = self.base.get(self.rd)
        any_link_glob= self.base.get(self.ra)
        from time import sleep

        LinkCheckLib.myprint("-------------Starting get_links with: " + mainlin)
        has_bad, any_lnk_loc, new_lnks_loc, base_lnks_loc, response, ab_links = False,[], [], [], "0", []
        response, resp_err = self.do_response(mainlin, _plin)
        sleep(.05)
        is_bool = True
        good_suffix = True
        has_bad = False


        try:
            if response.status_code != "0":
                LinkCheckLib.myprint("Status code: " + str(response.status_code))
        except Exception as e:
            LinkCheckLib.myprint("Exception no valid response from: " + mainlin)
            #self.handle_exc(e, mainlin, _plin)
            return

        if resp_err == 0 and is_bool is True:  ## if there's an error  - 0 is good to continue
            try:
                ab_links = response.html.absolute_links
                new_lnks_loc = [ab for ab in ab_links]
            except Exception as e:
                LinkCheckLib.myprint("Exception inside get_links: " + str(e))
                return

            LinkCheckLib.myprint("Starting Main Check" + mainlin)
            for THIS_LN in new_lnks_loc:
                if THIS_LN not in done_ln_gl_sing:
                    LinkCheckLib.myprint("THIS_LN " + THIS_LN)
                    #_IS_PARENT = self.ispar(THIS_LN, _plin)

                    _IN_AN_LOC = self.ck_loc(THIS_LN, any_lnk_loc)
                    if not _IN_AN_LOC and not self._DONE_YET(THIS_LN):    #NOT done yet  cg = check glob

                        try:
                            LinkCheckLib.myprint("new_lnks_loc === going to check bad data next: " + str(THIS_LN))
                            has_bad, good_suffix = self.ck_bad_data(THIS_LN)  # check for bad data
                            #self.check_for_bad_data(THIS_LN)
                        except Exception as e:
                            self.handle_exc(e, THIS_LN, _plin)
                            continue

                        try:
                            if self.ispar(THIS_LN, _plin) or has_bad:
                                continue
                                baseurl = self.base.get(self.baseurl)

                            _IS_BASE, in_base_local = self.ck_base(THIS_LN, baseurl, base_lnks_loc)

                            if _IS_BASE and good_suffix:  # IS base type
                                if not in_base_local:
                                    base_lnks_loc.append(THIS_LN)

                                self.add_any_bse_g(THIS_LN, _plin)
                            else:                   #if not a home based link
                                if not self.ck_g(THIS_LN):  ## add bad suffix here too
                                    any_lnk_loc = self.add_any(THIS_LN, _plin)  #does global too
                                    continue

                        except Exception as e:
                            self.handle_exc(e, THIS_LN, _plin)
                            continue

            LinkCheckLib.myprint('---returning base_links_local: ' + str(base_lnks_loc))
            LinkCheckLib.myprint('!! NEW----end get_home_links \n\n')
            self.base.update({self.rd: done_ln_gl_sing})
            self.base.update({self.ra: any_link_glob})

            return list(set(base_lnks_loc))



    #############----------------------------------MAIN--------------------------
      #############----------------------------------MAIN-------------------------
    def rem_errs(self, tlinks=None):
        done_ln_gl_sing = self.base.get(self.rd)
        if tlinks is None:
            tlinks = []
        for link in tlinks:
            if link in done_ln_gl_sing:
                tlinks.remove(link)
        return tlinks



    def main(self, a_site="a.htm"):
        base_lnks_g = self.base.get(self.rb)
        any_link_glob= self.base.get(self.ra)

        baseurl = LinkCheckLib.divide_url(a_site)
        self.base.update({baseurl: baseurl})

        LinkCheckLib.myprint("Starting main with: " + a_site)
        base_only_plain_repeat = []
        new_base_links_one = []
        full_addy = self.ckaddymore(a_site)
        new_sorted, repeats, the_len = [], 0, 0
        #tstart_main = perf_counter()
        LinkCheckLib.myprint('In main() STARTING OVER Getting first address: ' + full_addy)
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(full_addy, full_addy)  #first set of base
            #LinkCheckLib.myprint("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
            if base_only_plain_repeat:
                the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 6:
                repeats += 1
                LinkCheckLib.myprint("repeats: " + str(repeats) + "-------------------!!In main loop ")
                for baselink in new_base_links_one:
                    new_base_links_tmp = self.get_links(baselink, full_addy)  # first set of base
                    new_base_links_two = self.rem_errs(new_base_links_tmp)

                the_len = len(new_base_links_two)
                if the_len > 0:
                    new_base_links_one = new_base_links_two

        except Exception as e:
            LinkCheckLib.myprint("Exception inside main_run: " + str(e))

        try:
            base_glob_now = base_lnks_g
            new_base_links_here, the_len_b = [], len(base_glob_now)
            while the_len_b and repeats < 6:

                repeats += 1
                #LinkCheckLib.myprint("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    base_lin, parent_lin = baselink[0], baselink[1]
                    new_base_links_here = self.get_links(base_lin, parent_lin)  # first set of base
                the_len_b, base_glob_now = len(new_base_links_here), new_base_links_here

        except Exception as e:
            LinkCheckLib.myprint("Exception after baselink in base_glob_now: " + str(e))

        tup = ()
        try:
            #LinkCheckLib.myprint("Step Two Done")
            any_link_to_check = []
            any_link_to_check = list(any_link_glob)

            any_link_to_check = list(set(any_link_to_check))
            for tup in any_link_to_check:    #check non-base links
                self.get_simple_response(tup)
            for tup in base_lnks_g:
                self.get_simple_response(tup)

        # except TypeError:
        #     print(str(TypeError))
        #     self.handle_exc(e, tup[0] ,tup[1])
        except IndexError:
            #print(str(IndexError))
            pass
        except Exception as e:
            #print(str(e))
            self.handle_exc(e, tup[0] ,tup[1])
            pass

        finlist = self.return_errors()
        #self.print_errs.del_finlist()
        #LinkCheckLib.myprint("totalTime: " + str(perf_counter() - tstart_main))
        #x = len(self.done_ln_gl_sing)
        #LinkCheckLib.myprint("errors: " + str(x))
        return finlist


# if __name__ == "__main__":
#     LinkCheck.main()



