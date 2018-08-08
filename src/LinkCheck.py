# python 3
#from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException

from src.LinkCheckUtil import linkckutil
from src import home1, lnfeed, ercodes, badlist, full_addy, any_link_glob, base_links_glob, done_links_glob
from src import full_addy, err_links
from src import the_logger as logger
from time import perf_counter
from urllib.parse import urlsplit
from requests_html import HTMLSession
from lxml import etree

class linkcheck(linkckutil):


    def ck_bad_data(self, link):
        x = 0
        mylist = ['#', 'tel:+']
        for i in mylist:
            if i in link:
                x += 1
        return x

    def ck_status_code(self,t):
        err_codes = [400, 404, 408, 409, 501, 502, 503]
        if t in err_codes:
            return 1
        else:
            return 0    #ok

    def split_url(self, url):
        if '?' in url:
            url = (url.split('?'))[0]
        return url
    #############---------------------------------------- def
    def get_simple_response(self, local_url):
        print("--------------------------------------------")
        print("just got this link: ", local_url)

        session = HTMLSession()
        response = session.get(local_url)

        try:
            if self.ck_status_code(response.status_code) > 0:
                self.err_links.append((response.url, response.status_code))
                print("found error in link: ", local_url)
        except Exception:
            pass

    #############---------------------------------------- def
    def get_home_links(self, parent_local):
        print("--------------------------------------------")
        print("just got this link: ", parent_local)
        any_link_local, base_links_local = [], []
        thebase_part = (urlsplit(parent_local))[1]
        session = HTMLSession()
        response = session.get(parent_local)

        try:
            if self.ck_status_code(response.status_code) > 0:
                self.err_links((response.url, response.status_code))

            else:   #  not an err
                for abs_link in response.html.absolute_links:
                    if self.ck_bad_data(abs_link):
                        pass
                    else:
                        cond0 = bool(abs_link in [i[0] for i in self.done_links_glob ])

                        if not cond0:   #if not already done
                            html_resp_local = session.get(abs_link)
                            turl = html_resp_local.url
                            theurl = self.split_url(turl)

                            if self.ck_bad_data(abs_link):
                                pass
                            else:
                                self.done_links_glob.append(theurl)   ## add to main done list
                        #############----------------------------------------

                            cond1 = bool(thebase_part in theurl)
                            cond2 = bool(theurl in [i[0] for i in base_links_local])
                            cond3 = bool(theurl in [i[0] for i in self.base_links_glob])

                            if cond1:
                                if not cond2:
                                    base_links_local.append((theurl, parent_local))
                                if not cond3:
                                    self.base_links_glob.append((theurl, parent_local))

                            else:
                                #if not a home based link
                                cond4 = bool(theurl in [i[0] for i in any_link_local])
                                cond5 = bool(theurl in [i[0] for i in self.any_link_glob])

                                if not cond4:
                                    any_link_local.append((theurl, parent_local))
                                if not cond5:
                                    self.any_link_glob.append((theurl, parent_local))




        except etree.XMLSyntaxError:
            pass
        except BaseException:
            pass


        print("found these links any_link_local: ", any_link_local)
        return any_link_local, base_links_local



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        driver = 0
        tstart = perf_counter()
        print("started timer: ", tstart)
        logger.debug('In main() Getting first address: {}'.format(full_addy))
        try:
            #############---------step ONE:

            any_link_main_one, base_only_one_t = self.get_home_links(full_addy)

            base_only_one_t.sort(key=lambda tup: tup[0])
            base_only_one = list(set(base_only_one_t))
            print("\n-------------")
            print("base_only_one: ", base_only_one)

            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time

            #############---------step TWO:
            base_only_two, base_only_3 = [], []
            for base_one in base_only_one:
                any_links2, base_only_two = self.get_home_links(base_one[0])

            for base_two in base_only_two:
                any_links3, base_only_3 = self.get_home_links(base_two[0])


            base_links_glob_final = sorted(list(set(self.base_links_glob)))

            print("base final list: ----------------")
            for i in base_links_glob_final:
                print(i)


            logger.info("Step TwoDone")

            print('--------------big pile:')

            fp2 = list(set(sorted(self.any_link_glob)))
            fp3 = sorted(fp2)

            for i in fp3:
                self.get_simple_response(i)


            print()
            print("here are the errors:-------------")
            for i in self.err_links:
                print(i)



            print("totalTime: ", perf_counter() - tstart)

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            pass

    def __init__(self):
        print('In linkcheck: __init__')
        #super().__init__()
        #self.any_link_glob = []
        #self.err_links = []
        #self.base_links_glob, self.done_links_glob = [], []
        self.main()

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
