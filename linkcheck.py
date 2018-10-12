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
    def add_any_bse_g(self, zlink, parent_local):  # Adding this MAIN_DICT link to MAIN_DICT glob
       # rb = self.rb
        base_lnks_g = self.MAIN_DICT.get(self.rb)

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
        base_lnks_g2 = list(set(base_lnks_g))
        self.MAIN_DICT.update({self.rb: base_lnks_g2})
    #---------------------------------------------------------------------------------------
    def add_any(self, tlink, parent_local, any_link_loc=None):  # Adding this MAIN_DICT link to any glob
        any_link_glob = self.MAIN_DICT.get(self.rany)
        isparent = self.isTHEparent(tlink)

        if any_link_loc is None:
            any_link_loc = []
        if isparent:
            return any_link_loc
        try:
            if any_link_glob:  # don'w_thread try without something there
                glob_bool = bool(tlink in [i[0] for i in any_link_glob])
                if not glob_bool:
                    any_link_glob.append((tlink, parent_local))  # add if not there
                    any_link_loc.append((tlink, parent_local))
            else:
                any_link_glob.append((tlink, parent_local))  # make it if starting empty
                any_link_loc.append((tlink, parent_local))
            self.MAIN_DICT.update({self.rany: any_link_glob})
        except Exception as e:
            self.myprint("exception in add_any: " + str(e))

        return any_link_loc


    # #----------------------------------------------------------------------get_links-
    def get_links(self, mainlin, par_link):
        done_ln_gl_sing = self.MAIN_DICT.get(self.rdone)
        any_link_glob= self.MAIN_DICT.get(self.rany)
        if mainlin not in done_ln_gl_sing:

            any_lnk_loc, new_lnks_loc, base_lnks_loc, response, ab_links = [], [], [], "0", []
            # #---------------  web response get here!!!!!!!!--------------------------------
            response, resp_err = self.do_response(mainlin, par_link)

            try:
                if response.status_code != "0":
                    self.myprint("Status code: " + str(response.status_code))
            except Exception as e:
                self.myprint("Exception no valid response from: " + mainlin)
                return

            if resp_err == 0:  ## if there's an error  - 0 is good to continue
                try:
                    ab_links = response.html.absolute_links
                    new_lnks_loc2 = [ab for ab in ab_links]
                    new_lnks_loc  = list(set(new_lnks_loc2))
                except Exception as e:
                    self.myprint("Exception inside get_links: " + str(e))
                    return

                self.myprint("Starting Main Check of: " + mainlin + "\n")
                for the_link in new_lnks_loc:
                    _IS_BASE2 = False
                    has_bad = False
                    issame = self.is_same_site_link(the_link)
                    if issame:
                        continue

                    elif the_link not in done_ln_gl_sing:

                        _IN_AN_LOC = self.ck_loc(the_link, any_lnk_loc)
                        if not _IN_AN_LOC and not self._DONE_YET(the_link):    #NOT done yet  cg = check glob
                            good_suffix = True

                            try:
                                #self.myprint("new_lnks_loc === going to check bad data next: " + str(THIS_LN))
                                has_bad, good_suffix = self.ck_bad_data(the_link)  # check for bad data
                                if has_bad:
                                    continue

                            except Exception as e:
                                self.handle_exc(e, the_link, par_link)
                                continue

                            try:
                                _IS_BASE2, in_base_local= self.ck_for_base(the_link, base_lnks_loc)

                                if _IS_BASE2 and good_suffix:  # IS MAIN_DICT type
                                    if not in_base_local:
                                        base_lnks_loc.append(the_link)
                                    else:
                                        self.add_any_bse_g(the_link, par_link)
                                else:                   #if not a home based link
                                    if not self.ck_g(the_link):  ## add bad suffix here too
                                        if not _IS_BASE2:
                                            any_lnk_loc = self.add_any(the_link, par_link)  #does global too

                            except Exception as e:
                                self.handle_exc(e, the_link, par_link)
                                continue

            #self.myprint('---returning base_links_local: ' + str(base_lnks_loc))
            #self.myprint('!! NEW----end get_home_links \n\n')
            self.MAIN_DICT.update({self.rdone: done_ln_gl_sing})
            self.MAIN_DICT.update({self.rany: any_link_glob})
            self.myprint("- done with getlinks-----------\n")

            return list(set(base_lnks_loc))
        else:
            return []



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

        except Exception as e:
            self.myprint("Exception inside main_run: " + str(e))

        self.get_more_baselinks()
        self.any_link_ck()

        finlist = self.return_errors()
        for i in finlist:
               print("err: " + i[0])
        print("totalTime: " + str(perf_counter() - tstart))
        return finlist

    #-------------------------------------------------------------------

    def step_one(self, base_only_plain_repeat_here, link_w_scheme_here):
        try:
            new_base_links_two, new_base_links_one = [], base_only_plain_repeat_here
            repeats = 0
            base_len = len(base_only_plain_repeat_here)
            while base_len and repeats < 6:
                repeats +=1
                self.myprint('\n' + " -----repeats: " + str(repeats) + "--------- In set_one loop ")
                for baselink in new_base_links_one:
                    isparent= self.isTHEparent(baselink)
                    if not isparent:
                        new_base_links_tmp = self.get_links(baselink, link_w_scheme_here)  # first set of MAIN_DICT
                        new_base_links_two = self.rem_errs(new_base_links_tmp)

                base_len = len(new_base_links_two)
                if base_len > 0:
                    new_base_links_one = new_base_links_two
                else:
                    continue

        except Exception as e:
            self.myprint("Exception inside main_run: " + str(e))

    #-------------------------------------------------------------------

    def get_more_baselinks(self):
        base_glob_now = self.MAIN_DICT.get(self.rb)
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

            self.MAIN_DICT.update({self.rb: base_glob_now})

        except Exception as e:
            self.myprint("Exception after baselink in base_glob_now: " + str(e))

    #-------------------------------------------------------------------

    def any_link_ck(self):
        self.myprint("Step Two Done")
        ag= self.MAIN_DICT.get(self.rany)
        rde= self.MAIN_DICT.get(self.rdone)
        any_link_to_check  =  list(set(ag))

        try:
            if any_link_to_check:
                for tupy in any_link_to_check:  # check non-MAIN_DICT links
                    rde.append(tupy[0])
                    self.get_simple_response(tupy)
                # for tup in base_lnks_g:
                #     self.get_simple_response(tup)
                self.MAIN_DICT.update({self.rdone: rde})

        except Exception as e:
            if tupy:
                a, b = self.handle_exc(e, tupy[0], tupy[1])
                return a, b
            else:
                self.myprint((str(e)))
                return 0, 0

        # rederdatf = self.MAIN_DICT.get(self.redirs)
        # print()
        # print('Here are the redirect errors - they should be fixed too:')
        # for i in rederdatf:
        #     print(i)

# k = "kaldu.com"
# s = 'schorrmedia.com/m.html'
# if __name__ == "__main__":
#     lc = LinkCheck()
#     lc.main(k)