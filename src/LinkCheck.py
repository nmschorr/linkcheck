# python 3

from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException
from src import home1, home2, lnfeed, ercodes, badlist, start_driver, full_addy, driver
from src import the_logger as logger

class linkcheck(linkckutil):

    #############---------------------------------------- def
    def get_home_links(self, parent_loc):
        from urllib.parse import urlsplit
        from requests_html import HTMLSession
        any_link_loc, base_links_loc = [], []

        thebase_part = (urlsplit(parent_loc))[1]
        session = HTMLSession()
        response = session.get(parent_loc)

        for abs_link in response.html.absolute_links:
            cond0 = abs_link not in self.done_links_glob
            if cond0:
                each_ses = session.get(abs_link)


                theurl = each_ses.url
                if '?' in theurl:
                    theurl = (theurl.split('?'))[0]

                self.done_links_glob.append(theurl)
            #############----------------------------------------

                cond1 = theurl not in any_link_loc
                cond2 = theurl not in self.any_link_glob
                if cond1 and cond2:
                    any_link_loc.append((theurl, parent_loc))
                    self.any_link_glob.append((theurl, parent_loc))

                cond3 = thebase_part in theurl
                cond4 = theurl not in base_links_loc
                if cond3 and cond4:
                    base_links_loc.append((theurl, parent_loc))
                    self.base_links_glob.append((theurl, parent_loc))

        print("found these links: ", any_link_loc)
        return any_link_loc, base_links_loc



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        driver = 0

        logger.debug('In main() Getting first address: {}'.format(full_addy))
        try:
            #############---------step ONE:

            any_link_main_one, base_only_one = self.get_home_links(full_addy)
            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time

            #############---------step TWO:

            for blink in base_only_one:
                new_links2, base_only_two = self.get_home_links(blink[0])

            logger.info("Step TwoDone")

            print('--------------big pile:')

            fp = sorted(self.any_link_glob)
            fp2 = list(set(fp))
            fp3 = sorted(fp2)

            for i in fp3:
                print(i)

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            pass

    def __init__(self):
        print('In linkcheck: __init__')
        super().__init__()
        self.any_link_glob = []
        self.base_links_glob, self.done_links_glob = [], []
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
