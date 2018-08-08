# python 3
#from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException

from src import home1, lnfeed, ercodes, badlist, full_addy, any_link_glob, base_links_glob, done_links_glob
from src import full_addy
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
        #if t in err_codes:
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
        #print("--------------------------------------------")
       # print("just got this link: ", tup[0])

        session = HTMLSession()
        response = session.get(tup[0])

        try:
            if self.ck_status_code(response.status_code) > 0:
                self.err_links.append((response.url, response.status_code, tup[1]))
                #print("\n----!! found error in link: ", response.url, response.status_code, tup[1])
        except Exception:
            pass


    def splitty(self, parent_local):
        thebase_part_local = None
        #print("\ninside splitty-----------------")
        #print("-------------------passed in: ", parent_local)
        try:
            thebase_part_local = (urlsplit(parent_local))[1]
        except Exception as e:
            print(e)
            pass
        return thebase_part_local

    #############---------------------------------------- def
    def get_home_links(self, parent_local):
        print("-starting-get_home_links - just got this link: ", parent_local)
        any_link_local, base_links_local = [], []

        thebase_part = self.splitty(parent_local)


        session = HTMLSession()
        response = session.get(parent_local)

        try:
            if self.ck_status_code(response.status_code) > 0:  ## if there's an error
                self.err_links((response.url, response.status_code))

            else:   #  not an err
                for abs_link in response.html.absolute_links:
                    if abs_link == parent_local:
                        pass
                    elif self.ck_bad_data(abs_link):
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
                            cond2 = bool(theurl in [i for i in base_links_local])
                            cond3 = bool(theurl in [i[0] for i in self.base_links_glob])

                            if cond1:
                                if not cond2:
                                    base_links_local.append(theurl)
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

        b = []
        print("\n-----end of cycle in get_home_links: ---------")
       # print("found these links any_link_local: ", any_link_local)
        #print("\n---------- found these links base_links_local: ", base_links_local)
        bb = sorted(base_links_local)
        cc = sorted(list(set(bb)))
        return cc



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        tstart = perf_counter()
        print("started timer: ", tstart)
        logger.debug('In main() Getting first address: {}'.format(full_addy))
        try:
            #############---------step ONE:
            base_only_plain_repeat = self.get_home_links(full_addy)  #first set of base
            zzzz = []
            zzzz = [(r,n) for r,n in enumerate(base_only_plain_repeat)]



            cond9 = 0
            cond9 =  filter(lambda x: x[1]==full_addy, zzzz)
            boo = bool(cond9)
            for i in zzzz:
                if i[1] == full_addy:
                    del base_only_plain_repeat[i]
            b = []
            new_large = []
            new_base_urls = []
            base_only_plain_repeat_grand = []
            for i in range(1):
                print("\n--------------------\n!!In main loop\n")
                for baselink in base_only_plain_repeat:
                    new_base_urls = self.get_home_links(baselink)
                    new_large.extend(new_base_urls)
                    base_len = len(new_base_urls)
                    new_base_urls = []
                b = sorted(new_large)
                new_large = []
                if len(b):
                    base_only_plain_repeat_grand = list(set(b))




            print("\n-------------")
            print("\n-----------\n   base_only_plain_repeat_grand: \n", base_only_plain_repeat_grand)

            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time



            logger.info("Step TwoDone")


            fp2 = list(set(sorted(self.any_link_glob)))
            fp3 = sorted(fp2)

            for i in fp3:
                #print('checking this link: ', i)
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
        self.done_links_glob = done_links_glob
        self.base_links_glob = base_links_glob
        self.any_link_glob = any_link_glob
        self.err_links = []
        self.main()

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
