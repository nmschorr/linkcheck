# python 3
# Nancy Schorr, 2018
# this file is in active development

from requests_html import HTMLSession
from src.linkcheck_utils import lc_utils as lc
from time import perf_counter

class linkcheck(object):
    def __init__(self):
        self.any_link_glob, self.base_links_glob = [],[]
        self.done_ln_gl_sing, self.err_links, self.link_count = [], [], 0
        self.logger = lc().setup_logger()
        self.logger.debug('In linkcheck: __init__')

    def handle_exc(self, e, link, plink):
        print(str(e))
        self.logger.debug('!!!!!!!! found error------------------\n' + str(e))
        self.err_links.append((link, str(e)[:57], plink))
        pass

    def get_simple_response(self, tup):
        er = None
        link_we_are_chkg, parent, response = tup[0], tup[1], None
        self.link_count += 1
        self.logger.debug("Checking this link: " + link_we_are_chkg)
        try:
            session = HTMLSession()
            response = session.get(link_we_are_chkg)
            er, self.err_links = lc.ck_status_code(response, parent, self.err_links )
        except Exception as e:
            self.handle_exc(e, link_we_are_chkg, parent)

    #-----------------------------------------------------------------------
    def do_response(self, tpar):
        er2 = 0
        try:
            self.logger.debug("-starting-get_home_links - just got this link: " + str(tpar))
            session = HTMLSession()
            resp = session.get(tpar)
            self.done_ln_gl_sing.append(tpar)  ## add to main done list
            er2 = self.ck_status_code(resp, tpar)  ## if there's    an error

        except Exception as e:
            print(str(e))
        return resp, er2

    #-----------------------------------------------------------------------
    def get_links(self, parent_local):
        this_link, any_link_local,new_links_local, base_links_local, response, ab_links = None, [], [], [], None, []
        response, resp_err = self.do_response(parent_local)
        _IS_PARNT = bool(this_link == parent_local)  # is it the parent?

        if resp_err == 0:  ## if there's an error  - 0 is good to continue
            try:
                ab_links = response.html.absolute_links
                new_links_local = [ab_lin for ab_lin in ab_links]
            except Exception as e:   print(str(e))

            for this_link in new_links_local:
                in_any_local = self.tn(this_link, any_link_local)
                if in_any_local and not self.cg(this_link):    #NOT done yet  cg = check glob

                    try:
                        has_bad_data, good_suffix = lc.ck_bad_data(this_link)  # check for bad data
                        self.done_ln_gl_sing = lc.check_for_bad_data(this_link, self.done_ln_gl_sing)

                    except Exception as e:  self.handle_exc(e, this_link, parent_local)

                    try:
                        if _IS_PARNT or has_bad_data:   pass

                        elif good_suffix:
                            if not in_any_local:
                                self.any_link_glob, any_link_local = \
                                    lc.add_to_any(this_link, parent_local, self.any_link_glob, any_link_local)

                            else:
                                base_pt = lc.divide_url(parent_local)
                                _IS_BASE, in_base_local = lc.ck_base(this_link, base_pt, base_links_local)

                                if _IS_BASE:  # IS base type
                                    if not in_base_local:  # if not already in this
                                        base_links_local.append(this_link)
                                    self.base_links_glob = lc.add_to_any_basegl(this_link, parent_local, self.base_links_glob)

                                else:                   #if not a home based link
                                    if not in_any_local:
                                        any_link_local.append((this_link, parent_local))
                                    if not self.ck_g(this_link):
                                        self.any_link_glob = lc.add_to_any(this_link, parent_local, self.any_link_glob)

                    except Exception as e:
                        self.handle_exc(e, this_link, parent_local)


        self.logger.debug('----end get_home_links:---returning base_links_local: ' + str(base_links_local))
        return list(set(base_links_local))

       #############---------------------------------------
    def ck_g(self, this_link):
        tru_fal = bool(this_link in [i[0] for i in self.any_link_glob])
        return tru_fal
        
    def cg(self, this_link):
        return bool(this_link in self.done_ln_gl_sing)

    def tn(self, this_lin, any_link_loc):
        return bool(this_lin in [i[0] for i in any_link_loc])  # is it local?

    def ck_status_code(self, response, parent_local):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        if response.status_code in err_codes:
            self.err_links.append((response.url, response.status_code, parent_local))
            return 1
        else: return 0  # ok


    def main_run(self, a_site):
        full_addy = 'http://' + a_site
        new_sorted, base_only_plain_repeat_grand, repeats = [], [], 0
        self.logger.debug('\n\n------------------- STARTING OVER -----------------------')
        tstart_main = perf_counter()
        print('In main() Getting first address: {}'.format(full_addy))
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(full_addy)  #first set of base
            self.logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
            the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 10:
                repeats += 1
                self.logger.debug("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in new_base_links_one:
                    new_base_links_two = self.get_links(baselink)  # first set of base
                the_len = len(new_base_links_two)
                new_base_links_one = new_base_links_two if the_len > 0 else None

        except Exception as e:
            print(str(e))

        try:
            base_glob_now = self.base_links_glob
            new_base_links_here, the_len_b = [], len(base_glob_now)
            while the_len_b and repeats < 7:

                repeats += 1
                self.logger.debug("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    base_lin = baselink[0]
                    parent_lin = baselink[1]
                    new_base_links_here = self.get_links(base_lin)  # first set of base
                the_len_b, base_glob_now = len(new_base_links_here), new_base_links_here

        except Exception as e:
            self.handle_exc(e, base_lin, parent_lin)

        try:
            self.logger.info("Step Two Done")
            any_link_to_check = list(set(self.any_link_glob))
            for tup in any_link_to_check:    #check non-base links
                self.get_simple_response(tup)
            for tup in self.base_links_glob:
                self.get_simple_response(tup)

        except Exception as e:
            self.handle_exc(e, tup[0] ,tup[1])

        finlist = lc.print_errs(self.err_links)
        self.logger.debug("totalTime: " + str(perf_counter() - tstart_main))
        self.logger.debug("Links checked: " + str(self.link_count))
        x = len(self.done_ln_gl_sing)
        print("done_links_glob_singles: ", x)
        return finlist

