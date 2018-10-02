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

    def get_simple_response(self, lin_and_par_tup):
        link_count, stat = 0, 0
        #er, response = "0", "0"
        link_to_ck, parent = lin_and_par_tup[0], lin_and_par_tup[1]
        link_count += 1
        self.myprint("Checking this link: " + link_to_ck )
        try:
            stat = requests.get(link_to_ck).status_code
            self.ck_status_code_simple(link_to_ck, parent, stat)
            self.myprint("-----status: " + str(stat) + "\n")

        except Exception as e:
            self.myprint("Exception inside get_simple_response: ")
            self.handle_exc(e, link_to_ck, parent)

    #---------------------------------------------------------------------------------------
    def add_any_bse_g(self, zlink, parent_local):  # Adding this MAIN_DICT link to MAIN_DICT glob
        rb = self.rb
        base_lnks_g = self.MAIN_DICT.get(rb)

        if base_lnks_g is None:
            base_lnks_g = []
        try:
            if base_lnks_g:
                _IN_BASE_GLOB = bool(zlink in [i[0] for i in base_lnks_g])
                if not _IN_BASE_GLOB:  # if not already in this
                    base_lnks_g.append((zlink, parent_local))
                    self.myprint("Adding this BASE LINK to MAIN_DICT glob: " + zlink)
            else:
                base_lnks_g = [(zlink, parent_local)]

        except Exception as e:
            self.myprint("Exception add_any_bse_g: " + str(e))

        self.MAIN_DICT.update({rb: base_lnks_g})
    #---------------------------------------------------------------------------------------
    def add_any(self, tlink, parent_local, any_link_loc=None):  # Adding this MAIN_DICT link to any glob
        ra = self.ra
        any_link_glob = self.MAIN_DICT.get(ra)
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
            self.MAIN_DICT.update({ra: any_link_glob})
        except Exception as e:
            self.myprint("exception in add_any: " + str(e))

        return any_link_loc


    # #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, par_link):
        _IS_BASE = False
        _IS_BASE2 = False
        ra = self.ra
        rd = self.rd
        done_ln_gl_sing = self.MAIN_DICT.get(rd)
        any_link_glob= self.MAIN_DICT.get(ra)
        from time import sleep
        self.myprint("\n\n------------ ")

        self.myprint("-------------Starting get_links with: " + mainlin)
        has_bad, any_lnk_loc, new_lnks_loc, base_lnks_loc, response, ab_links = False,[], [], [], "0", []
        response, resp_err = self.do_response(mainlin, par_link)



        sleep(.05)
        is_bool = True
        good_suffix = True
        has_bad = False
        is_same_link = False

        try:
            if response.status_code != "0":
                self.myprint("Status code: " + str(response.status_code))
        except Exception as e:
            self.myprint("Exception no valid response from: " + mainlin)
            #self.handle_exc(e, mainlin, par_link)
            return

        if resp_err == 0 and is_bool is True:  ## if there's an error  - 0 is good to continue
            try:
                ab_links = response.html.absolute_links
                new_lnks_loc = [ab for ab in ab_links]
            except Exception as e:
                self.myprint("Exception inside get_links: " + str(e))
                return

            self.myprint("Starting Main Check" + mainlin + "\n")
            for THIS_LN in new_lnks_loc:
                if THIS_LN not in done_ln_gl_sing:
                    self.myprint("THIS_LN " + THIS_LN)
                    _IS_BASE = self.ispar(THIS_LN)

                    _IN_AN_LOC = self.ck_loc(THIS_LN, any_lnk_loc)
                    if not _IN_AN_LOC and not self._DONE_YET(THIS_LN):    #NOT done yet  cg = check glob

                        try:
                            self.myprint("new_lnks_loc === going to check bad data next: " + str(THIS_LN))
                            has_bad, good_suffix = self.ck_bad_data(THIS_LN)  # check for bad data
                        except Exception as e:
                            self.handle_exc(e, THIS_LN, par_link)
                            continue

                        try:
                            issame = self.is_same_site_link(THIS_LN)
                            if issame:
                                continue

                        except Exception as e:
                            self.handle_exc(e, THIS_LN, par_link)
                            continue

                        try:
                            if has_bad:
                                continue

                            _IS_BASE2, in_base_local= self.ck_base(THIS_LN, base_lnks_loc)


                            if _IS_BASE2 and good_suffix:  # IS MAIN_DICT type
                                if not in_base_local:
                                    base_lnks_loc.append(THIS_LN)
                                self.add_any_bse_g(THIS_LN, par_link)
                            else:                   #if not a home based link
                                if not self.ck_g(THIS_LN):  ## add bad suffix here too
                                    any_lnk_loc = self.add_any(THIS_LN, par_link)  #does global too

                        except Exception as e:
                            self.handle_exc(e, THIS_LN, par_link)
                            continue

            self.myprint('---returning base_links_local: ' + str(base_lnks_loc))
            self.myprint('!! NEW----end get_home_links \n\n')
            self.MAIN_DICT.update({rd: done_ln_gl_sing})
            self.MAIN_DICT.update({ra: any_link_glob})
            self.myprint("- done with getlinks-----------\n \n")

            return list(set(base_lnks_loc))



    #############----------------------------------MAIN--------------------------
      #############----------------------------------MAIN-------------------------
    def rem_errs(self, tlinks=None):
        rd = self.rd
        done_ln_gl_sing = self.MAIN_DICT.get(rd)
        if tlinks is None:
            tlinks = []
        for link in tlinks:
            if link in done_ln_gl_sing:
                tlinks.remove(link)
        return tlinks



    def main(self, a_site="a.htm"):
        _IS_BASE2, _IS_BASE = False, False
        tstart = perf_counter()
        ra = self.ra
        rb = self.rb
        base_lnks_g = self.MAIN_DICT.get(rb)
        any_link_glob= self.MAIN_DICT.get(ra)

        asite=LinkCheckLib.ckaddymore(a_site)
        parsed = urlparse(asite)
        base_parsed = str(parsed.netloc)
        base_parsed_www = 'www.' + base_parsed
        self.MAIN_DICT.update({ self.BASENAME: base_parsed })
        self.MAIN_DICT.update({ self.BASENAMEwww: base_parsed_www })


        self.myprint("Starting main with: " + a_site)
        base_only_plain_repeat = []
        new_base_links_one = []
        full_addy = self.ckaddymore(a_site)
        new_sorted, repeats, the_len = [], 0, 0
        tstart_main = perf_counter()
        self.myprint('In main() STARTING OVER Getting first address: ' + full_addy)
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(full_addy, full_addy)  #first set of MAIN_DICT
            self.myprint("Step One Done with base_only_plain_repeat")   ##first time:  HOME PAGE ONLY  ##first time

            base_first_len = len(base_only_plain_repeat)
            print("length base_only_plain_repeat: " + str(base_first_len))
            if base_first_len:
                the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 6:
                repeats += 1
                self.myprint("\n\n-----repeats: " + str(repeats) + "-------------------!!In main loop ")
                for baselink in new_base_links_one:
                    new_base_links_tmp = self.get_links( baselink, full_addy)  # first set of MAIN_DICT
                    new_base_links_two = self.rem_errs(new_base_links_tmp)

                the_len = len(new_base_links_two)
                if the_len > 0:
                    new_base_links_one = new_base_links_two

        except Exception as e:
            self.myprint("Exception inside main_run: " + str(e))

        try:
            base_glob_now = base_lnks_g
            new_base_links_here, the_len_b = [], len(base_glob_now)
            while the_len_b and repeats < 6:

                repeats += 1
                self.myprint(" \n repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    base_lin, BASE_URL = baselink[0], baselink[1]
                    new_base_links_here = self.get_links(base_lin, BASE_URL)  # first set of MAIN_DICT
                the_len_b, base_glob_now = len(new_base_links_here), new_base_links_here

        except Exception as e:
            self.myprint("Exception after baselink in base_glob_now: " + str(e))

        tup = ()
        try:
            self.myprint("Step Two Done")
            any_link_to_check = []
            any_link_to_check = list(any_link_glob)

            any_link_to_check = list(set(any_link_to_check))
            for tup in any_link_to_check:    #check non-MAIN_DICT links
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
        print("totalTime: " + str(perf_counter() - tstart))
        return finlist





