# python 3
# Nancy Schorr, 2018
# this file is in active development

from requests_html import HTMLSession
from requests.exceptions import ConnectionError
from src.linkcheck_utils import lc_utils
from time import perf_counter

class linkcheck(object):
    def __init__(self):
        print('In linkcheck: __init__')
        self.any_link_glob, self.base_links_glob = [],[]
        self.done_links_glob_singles, self.err_links = [],[]
        self.PRT = True
        self.link_count = 0
        self.full_addy = None
        lc = lc_utils()
        logger = lc.setup_logger()
        self.logger = logger

    def ck_status_code(self, response, parent_local):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        temp_url = response.url
        self.logger.debug("testing this now: " + temp_url)

        if response.status_code in err_codes:
            self.err_links.append((response.url, response.status_code, parent_local))
            return 1
        else:
            return 0  # ok

    def check_for_bad_data(self, this_link, parent_local, any_link_local):
        has_bad_data = lc_utils().ck_bad_data(this_link)  #check for bad data
        link_eq_parent = bool(this_link == parent_local)
        good_suffix = lc_utils().has_correct_suffix(this_link)  #check suffix
        in_any_local = bool(this_link in [i[0] for i in any_link_local])
        self.done_links_glob_singles.append(this_link)  ## add to main done list
        return has_bad_data, link_eq_parent, good_suffix, in_any_local

    def get_simple_response(self, tup):
        parent = tup[1]
        link_we_are_chkg = tup[0]
        response = None
        self.link_count += 1
        self.logger.debug("Checking this link: " + link_we_are_chkg)

        try:
            session = HTMLSession()
            response = session.get(link_we_are_chkg)
            self.ck_status_code(response, parent)

        except ConnectionError as e:
            self.logger.debug('!!!!!!!! found error------------------\n' + str(e))
            self.err_links.append((link_we_are_chkg, str(e)[:57], parent))
            pass

        except Exception as e:
            self.logger.debug('!!!!!!!! found error------------------\n' + str(e))
            self.err_links.append((link_we_are_chkg, str(e)[:57], parent))
            pass

    def add_to_any(self, this_link, parent_local): #Adding this base link to any glob
        in_any_glob = bool(this_link in [i[0] for i in self.any_link_glob])
        if not in_any_glob:
            self.any_link_glob.append((this_link, parent_local))

    def add_to_any_base(self, this_link, parent_local): #Adding this base link to base glob
        _IN_BASE_GLOB = bool(this_link in [i[0] for i in self.base_links_glob])
        if not _IN_BASE_GLOB:  # if not already in this
            self.base_links_glob.append((this_link, parent_local))
            self.logger.debug("Adding this base link to base glob: " + this_link)


    #############---------------------------------------- def
    def get_links(self, parent_local):
        any_link_local, base_links_local, response = [], [], []
        self.logger.debug("-starting-get_home_links - just got this link: " + str(parent_local))

        session = HTMLSession()
        response = session.get(parent_local)
        self.done_links_glob_singles.append(parent_local)  ## add to main done list

        try:
            if not self.ck_status_code(response, parent_local):  ## if there's an error
                try:
                    ab_links = response.html.absolute_links
                except Exception:
                    print('not a link with links: ', parent_local)
                else:
                    new_links_local = [ab_lin for ab_lin in ab_links]

                    for this_link in new_links_local:
                        _IN_DONE_GLOB = bool(this_link in self.done_links_glob_singles)
                        if not _IN_DONE_GLOB:    #NOT done yet
                            has_bad_data, link_eq_parent, good_suffix, in_any_local = \
                                self.check_for_bad_data(this_link, parent_local, any_link_local)

                            if link_eq_parent or has_bad_data:
                                pass

                            elif not good_suffix:
                                if not in_any_local:
                                    any_link_local.append((this_link, parent_local))
                                self.add_to_any(this_link, parent_local)

                            else:
                                base_pt = lc_utils().divide_url(parent_local)
                                _IS_BASE, in_base_local = lc_utils().ck_base(this_link, base_pt, base_links_local)

                                if _IS_BASE:  # IS base type
                                    if not in_base_local:  # if not already in this
                                        base_links_local.append(this_link)
                                    self.add_to_any_base(this_link, parent_local)

                                else:                   #if not a home based link
                                    if not in_any_local:
                                        any_link_local.append((this_link, parent_local))
                                    self.add_to_any(this_link, parent_local)

        except Exception as e:
            print(e)
            pass

        self.logger.debug('----end get_home_links:---returning base_links_local: ' + str(base_links_local))
        return list(set(base_links_local))

       #############---------------------------------------

    def main_run(self, a_site):
        self.full_addy = 'http://' + a_site
        self.logger.debug('\n\n------------------- STARTING OVER -----------------------')
        tstart_main = perf_counter()
        print('In main() Getting first address: {}'.format(self.full_addy))
        new_sorted, base_only_plain_repeat_grand, repeats = [], [], 0
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(self.full_addy)  #first set of base
            self.logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
            the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 10:
                repeats += 1
                if self.PRT:
                    print("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in new_base_links_one:
                    new_base_links_two = self.get_links(baselink)  # first set of base

                the_len = len(new_base_links_two)
                new_base_links_one = new_base_links_two if the_len > 0 else None

            base_glob_now = self.base_links_glob
            new_base_links_here, the_len_b = [], len(base_glob_now)

            while the_len_b and repeats < 7:
                repeats += 1
                if self.PRT: print("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    new_base_links_here = self.get_links(baselink[0])  # first set of base
                the_len_b, base_glob_now = len(new_base_links_here), new_base_links_here

            self.logger.info("Step Two Done")
            any_link_to_check = list(set(self.any_link_glob))

            for tup in any_link_to_check:    #check non-base links
                self.get_simple_response(tup)
            for tup in self.base_links_glob:
                self.get_simple_response(tup)

        except Exception as e:
            print(str(e), exc_info=True)

        finlist = lc_utils().print_errs(self.err_links)
        self.logger.debug("totalTime: " + str(perf_counter() - tstart_main))
        self.logger.debug("Links checked: " + str(self.link_count))
        return finlist

