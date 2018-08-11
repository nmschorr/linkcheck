# python 3
# Nancy Schorr, 2018
# this file is in active development


from time import perf_counter
from urllib.parse import urlsplit

from lxml import etree
from requests_html import HTMLSession

from src import full_addy, any_link_glob, base_links_glob, done_links_glob
from src import the_logger as logger


class linkcheck(object):

    def ck_bad_data(self, link):
        end_val = 0
        mylist = ['#', 'tel:+']
        for i in mylist:
            if i in link:
                end_val += 1
        return end_val


    def my_print(self, the_line):
        print(the_line)

    def ck_status_code(self, response, parent_local):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        goodcodes = [200]

        if response.status_code in err_codes:
            self.err_links.append((response.url, response.status_code, parent_local))
            return 1
        else:
            return 0    #ok

    def split_url(self, url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url

    def get_simple_response(self, tup):
        self.my_print("Checking this link: " + tup[0])

        try:
            session = HTMLSession()
            response = session.get(tup[0])

            self.ck_status_code(response, tup[1])

        except Exception:
            pass

    def has_correct_suffix(self, link):
        a, b, c = 'html',  'htm',  '/'
        c1, c2, c3 = link.endswith(a), link.endswith(b), link.endswith(c)
        if (c1 or c2 or c3):
            return True
        else: return False

    def splitty(self, parent_local):
        thebase_part_local = None
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local.startswith('www'):
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            print(e)
        return thebase_part_local

    def any_glob(self, this_link, parent_local):
        in_any_glob = bool(this_link in [i[0] for i in self.any_link_glob])
        if not in_any_glob:
            self.any_link_glob.append((this_link, parent_local))

    def any_base_glob(self, this_link, parent_local):
        mp = self._MY_PRT
        _IN_BASE_GLOB = bool(this_link in [i[0] for i in self.base_links_glob])
        if not _IN_BASE_GLOB:  # if not already in this
            if mp: self.base_links_glob.append((this_link, parent_local))
            if mp: self.my_print("Adding this base link to base glob: "  + this_link)

    def check_data(self, this_link, parent_local, any_link_local):
        has_bad_data = self.ck_bad_data(this_link)
        link_eq_parent = bool(this_link == parent_local)
        good_suffix = self.has_correct_suffix(this_link)
        in_any_local = bool(this_link in [i[0] for i in any_link_local])
        self.done_links_glob_singles.append(this_link)  ## add to main done list
        return has_bad_data, link_eq_parent, good_suffix, in_any_local

    def ck_base(self, this_link, thebase_part, base_links_local):
        _IS_BASE = bool(thebase_part in this_link)
        in_base_local = bool(this_link in [i for i in base_links_local])
        return _IS_BASE, in_base_local

    def print_errs(self):
        if self.err_links:
            print("here are the errors:-------------")
            errs = list(set(self.err_links))
            errs2 = sorted(errs, key=lambda x: x[0])
            for e in errs2:
                print(e)

    def reset_timer(self, name, tstart):
        print(name, perf_counter() - tstart)
        tstart = perf_counter()

    #############---------------------------------------- def
    def get_links(self, parent_local):
        any_link_local, base_links_local, mp= [], [], self._MY_PRT
        if mp: self.my_print("-starting-get_home_links - just got this link: " + str(parent_local))

        session = HTMLSession()
        response = session.get(parent_local)

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
                                self.check_data(this_link, parent_local, any_link_local)

                            if link_eq_parent or has_bad_data:
                                pass

                            elif not good_suffix:
                                if not in_any_local:
                                    any_link_local.append((this_link, parent_local))
                                self.any_glob(this_link, parent_local)

                            else:
                                base_pt = self.splitty(parent_local)
                                _IS_BASE, in_base_local = self.ck_base(this_link, base_pt, base_links_local)

                                if _IS_BASE:  # IS base type
                                    if not in_base_local:  # if not already in this
                                        base_links_local.append(this_link)
                                    self.any_base_glob(this_link, parent_local)

                                else:                   #if not a home based link
                                    if not in_any_local:
                                        any_link_local.append((this_link, parent_local))
                                    self.any_glob(this_link, parent_local)

        except Exception as e:
            print(e)
            pass

        if mp: self.my_print('----end get_home_links:---returning base_links_local: ' + str(base_links_local))
        return list(set(base_links_local))

       #############---------------------------------------

    def main(self):
        mp = self._MY_PRT
        tstart = perf_counter()
        self.my_print("started timer: " + str(tstart))
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
                if mp: self.my_print("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in new_base_links_one:
                    new_base_links_two = self.get_links(baselink)  # first set of base

                the_len = len(new_base_links_two)
                new_base_links_one = new_base_links_two if the_len > 0 else None

            self.reset_timer("Time1", tstart) #1

            base_glob_now = self.base_links_glob
            new_base_links_here, the_len_b = [], len(base_glob_now)

            while the_len_b and repeats < 7:
                repeats += 1
                if mp: self.my_print("repeats: " + str(repeats) + "-------------------!!In main loop")
                for baselink in base_glob_now:
                    new_base_links_here = self.get_links(baselink[0])  # first set of base
                the_len_b = len(new_base_links_here)
                base_glob_now = new_base_links_here

            logger.info("Step Two Done")
            self.reset_timer("Time2", tstart)
            any_link_to_check = list(set(self.any_link_glob))

            for tup in any_link_to_check:
                self.get_simple_response(tup)

            self.reset_timer("Time3", tstart) #1

            for tup in self.base_links_glob:
                self.get_simple_response(tup)

        except Exception as e:
            logger.debug(str(e), exc_info=True)

        self.print_errs()
        print("totalTime4: ", perf_counter() - tstart)

    def __init__(self):
        print('In linkcheck: __init__')
        self.done_links_glob_singles = done_links_glob
        self.base_links_glob = base_links_glob
        self.any_link_glob = any_link_glob
        self.err_links = []
        self.full_addy = full_addy
        self._MY_PRT = True
        self.main()

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
