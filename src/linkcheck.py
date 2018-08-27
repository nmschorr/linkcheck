# python 3
# Nancy Schorr, 2018
# this file is in active development

from urllib.parse import urlsplit
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
        self.lc = lc_utils()

    def get_simple_response(self, tup):
        parent = tup[1]
        link_we_are_chkg = tup[0]
        response = None
        self.link_count += 1
        print("Checking this link: " + link_we_are_chkg)

        try:
            session = HTMLSession()
            response = session.get(link_we_are_chkg)

            self.lc.ck_status_code(response, parent)

        except ConnectionError as e:
            print('!!!!!!!! found bad error-------------------------')
            print(e)
            short_e = str(e)[:57]
            self.err_links.append((link_we_are_chkg, short_e, parent))
            pass

        except Exception as e:
            print('!!!!!!!! found error-------------------------')
            print(e)
            short_e = str(e)[:57]
            self.err_links.append((link_we_are_chkg, short_e, parent))
            pass

    def divide_url(self, parent_local):
        thebase_part_local = None
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            print(e)
        return thebase_part_local

    def add_to_any(self, this_link, parent_local): #Adding this base link to any glob
        in_any_glob = bool(this_link in [i[0] for i in self.any_link_glob])
        if not in_any_glob:
            self.any_link_glob.append((this_link, parent_local))

    def add_to_any_base(self, this_link, parent_local): #Adding this base link to base glob
        _IN_BASE_GLOB = bool(this_link in [i[0] for i in self.base_links_glob])
        if not _IN_BASE_GLOB:  # if not already in this
            if self.PRT: self.base_links_glob.append((this_link, parent_local))
            if self.PRT: print("Adding this base link to base glob: " + this_link)

    def check_for_bad_data(self, this_link, parent_local, any_link_local):
        has_bad_data = self.lc.ck_bad_data(this_link)  #check for bad data
        link_eq_parent = bool(this_link == parent_local)
        good_suffix = self.lc.has_correct_suffix(this_link)  #check suffix
        in_any_local = bool(this_link in [i[0] for i in any_link_local])
        self.done_links_glob_singles.append(this_link)  ## add to main done list
        return has_bad_data, link_eq_parent, good_suffix, in_any_local

    def ck_base(self, this_link, thebase_part, base_links_local):
        _IS_BASE = bool(thebase_part in this_link)
        in_base_local = bool(this_link in [i for i in base_links_local])
        return _IS_BASE, in_base_local

    def print_errs(self):
        fin_list = []
        answer_string, e = '', ''
        if self.err_links:
            errs = list(set(self.err_links))
            er_len = len(errs)
            print("\nTotal errors: ", er_len)
            print("-------------- Here are the errors ------------- :")
            errs2 = sorted(errs, key=lambda x: x[0])  # sort on first
            for e in errs2:
                p0 = "BAD LINK: "
                p1 = " REASON: "
                p2 = " REFERRING PAGE: "
                st0 = str(e[0])
                st1 = str(e[1])
                st2 = str(e[2])
                answer_string = p0 + st0 + p1 + st1 + p2 + st2 + '\n'
                fin_list.append(answer_string)
        return fin_list

    #############---------------------------------------- def
    def get_links(self, parent_local):
        any_link_local, base_links_local = [], []
        if self.PRT: print("-starting-get_home_links - just got this link: " + str(parent_local))
        response = []

        session = HTMLSession()
        response = session.get(parent_local)
        self.done_links_glob_singles.append(parent_local)  ## add to main done list

        try:
            if not self.lc.ck_status_code(response, parent_local):  ## if there's an error
                try:
                    # noinspection PyUnresolvedReferences
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
                                base_pt = self.divide_url(parent_local)
                                _IS_BASE, in_base_local = self.ck_base(this_link, base_pt, base_links_local)

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

        if self.PRT: print('----end get_home_links:---returning base_links_local: ' + str(base_links_local))
        return list(set(base_links_local))

       #############---------------------------------------

    def main_run(self, a_site):
        logger = self.lc.setup_logger()

        self.full_addy = 'http://' + a_site
        print('\n\n------------------- STARTING OVER -----------------------')
        tstart_main = perf_counter()
        logger.debug('In main() Getting first address: {}'.format(self.full_addy))
        new_sorted, base_only_plain_repeat_grand, repeats = [], [], 0
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(self.full_addy)  #first set of base
            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
            the_len = len(base_only_plain_repeat)
            new_base_links_two, new_sorted, new_base_links_one= [], [], base_only_plain_repeat

            while the_len and repeats < 10:
                repeats += 1
                if self.PRT: print("repeats: " + str(repeats) + "-------------------!!In main loop")
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

            logger.info("Step Two Done")
            any_link_to_check = list(set(self.any_link_glob))

            for tup in any_link_to_check:    #check non-base links
                self.get_simple_response(tup)
                                                ##map(lambda x: self.get_simple_response(x), any_link_to_check)

            for tup in self.base_links_glob:
                self.get_simple_response(tup)

        except Exception as e:
            logger.debug(str(e), exc_info=True)

        finlist = self.print_errs()
        print("totalTime: ", perf_counter() - tstart_main)
        print("Links checked: ", self.link_count)
        return finlist

