# python 3
#from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException

from src import home1, lnfeed, ercodes, badlist, full_addy, any_link_glob, base_links_glob, done_links_glob
from src import the_logger as logger
from time import perf_counter
from urllib.parse import urlsplit
from requests_html import HTMLSession
from lxml import etree

#class linkcheck(linkckutil):
class linkcheck(object):

    def ck_bad_data(self, link):
        x = 0
        mylist = ['#', 'tel:+']
        for i in mylist:
            if i in link:
                x += 1
        return x

    def ck_status_code(self,t):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        goodcodes = [200]

        if t not in goodcodes:
            return 1
        else:
            return 0    #ok

    def split_url(self, url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url
    #############---------------------------------------- def
    def get_simple_response(self, tup):
        print("Checking this link: ", tup[0])

        try:
            session = HTMLSession()
            response = session.get(tup[0])

            if self.ck_status_code(response.status_code) > 0:
                self.err_links.append((response.url, response.status_code, tup[1]))
                #print("\n----!! found error in link: ", response.url, response.status_code, tup[1])
        except Exception:
            pass


    def splitty(self, parent_local):
        thebase_part_local = None
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
            if thebase_part_local[0:3]=='www':
                thebase_part_local = thebase_part_local[4:]
        except Exception as e:
            print(e)
            pass
        return thebase_part_local

    #############---------------------------------------- def
    def get_links(self, parent_local):
        print("-starting-get_home_links - just got this link: ", parent_local)
        any_link_local, base_links_local = [], []

        thebase_part = self.splitty(parent_local)

        session = HTMLSession()
        response = session.get(parent_local)

        try:
            if self.ck_status_code(response.status_code) > 0:  ## if there's an error
                self.err_links((response.url, response.status_code))

            else:   #  not an err
                new_links_local = [lin for lin in response.html.absolute_links]

                for this_link in new_links_local:
                    _IS_BASE = bool(thebase_part in this_link)
                    _IN_DONE_GLOB = bool(this_link in self.done_links_glob_singles)
                    link_eq_parent = bool(this_link == parent_local)
                    in_base_local = bool(this_link in [i for i in base_links_local])
                    _IN_BASE_GLOB = bool(this_link in [i[0] for i in self.base_links_glob])
                    in_any_local = bool(this_link in [i[0] for i in any_link_local])
                    in_any_glob = bool(this_link in [i[0] for i in self.any_link_glob])
                    has_bad_data = self.ck_bad_data(this_link)

                    if link_eq_parent or has_bad_data:
                        pass

                    elif not _IN_DONE_GLOB:    #NOT done yet
                        self.done_links_glob_singles.append(this_link)  ## add to main done list

                        if _IS_BASE:                               # IS base type
                            if not in_base_local:                       #if not already in this
                                base_links_local.append(this_link)
                            if not _IN_BASE_GLOB:                     #if not already in this
                                self.base_links_glob.append((this_link, parent_local))

                                print("Adding this base link to base glob: ", this_link)

                        else:                   #if not a home based link
                            if not in_any_local:
                                any_link_local.append((this_link, parent_local))
                            if not in_any_glob:
                                self.any_link_glob.append((this_link, parent_local))




        except etree.XMLSyntaxError:
            pass
        except BaseException:
            pass

        print("----end of cycle in get_home_links: ---------")
        print("\n------------base_links_local: ", base_links_local)


        sorted_base = sorted(list(set(base_links_local)))
        print("\n------------returning base links local: ", base_links_local)
        return sorted_base



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        tstart = perf_counter()
        print("started timer: ", tstart)
        logger.debug('In main() Getting first address: {}'.format(self.full_addy))
        b, new_sorted, base_only_plain_repeat_grand, agroup = [], [], [], []
        repeats = 0
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_links(self.full_addy)  #first set of base
            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time

            the_len = len(base_only_plain_repeat)
            v, new_base_links_two, new_sorted = [], [], []
            new_base_links_one = base_only_plain_repeat

            while the_len and repeats < 4:
                repeats += 1
                print("repeats: ", repeats, "-------------------!!In main loop")
                for baselink in new_base_links_one:
                    new_base_links_two = self.get_links(self.full_addy)  # first set of base
                    the_len = len(new_base_links_two)

                if the_len > 0:
                    new_base_links_one = new_base_links_two

            base_glob_now = self.base_links_glob
            the_len_b = len(base_glob_now)
            while the_len_b and repeats < 4:
                repeats += 1
                print("repeats: ", repeats, "-------------------!!In main loop")
                for baselink in base_glob_now:
                    base2 =  baselink[0]
                    new_base_links_here = self.get_links(base2)  # first set of base
                    the_len_b = len(new_base_links_here)

                if the_len_b > 0:
                    base_glob_now = new_base_links_here

            logger.info("Step TwoDone")
            any_link_glob2 = list(set(self.any_link_glob))
            any_link_to_check = sorted(any_link_glob2, key=lambda x:x[0])

            for i in any_link_to_check:
                print('checking this link: ', i)
                self.get_simple_response(i)

            for i in self.base_links_glob:
                print('checking this link: ', i)
                self.get_simple_response(i)

            print('check for errors--------------')
            if (self.err_links):
                print("here are the errors:-------------")
                for i in self.err_links:
                    print(i)



            print("totalTime: ", perf_counter() - tstart)

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            pass

    def __init__(self):
        #super().__init__()
        print('In linkcheck: __init__')
        self.done_links_glob_singles = done_links_glob
        self.base_links_glob = base_links_glob
        self.any_link_glob = any_link_glob
        self.err_links = []
        self.full_addy = full_addy
        self.main()

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
