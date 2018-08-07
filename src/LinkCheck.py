# python 3

from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException
from src import home1, home2, lnfeed, ercodes, badlist, start_driver, full_addy, driver
from src import the_logger as logger

class linkcheck(linkckutil):

    #############---------------------------------------- def
    def get_home_links(self, parent):
        from urllib.parse import urlsplit
        from requests_html import HTMLSession
        any_link, home_links = [], []

        thebase_part = (urlsplit(parent))[1]
        session = HTMLSession()
        response = session.get(parent)

        for page in response.html.absolute_links:
            each_ses = session.get(page)
            theurl = each_ses.url
            if '?' in theurl:
                theurl = (theurl.split('?'))[0]

            cond1 = theurl not in any_link
            cond2 = theurl not in self.main_list_links
            if cond1 and cond2:
                any_link.append((theurl, parent))
                self.main_list_links.append((theurl, parent))

            cond3 = thebase_part in theurl
            cond4 = theurl not in home_links
            if cond3 and cond4:
                home_links.append((theurl, parent))
                self.base_list_links.append((theurl, parent))

        print("found these links: ", home_links)
        return any_link, home_links



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        driver = 0
        self.main_list_links, self.base_list_links = [], []

        logger.debug('In main() Getting first address: {}'.format(full_addy))
        try:
            new_links_main, parent_links_main = self.get_home_links(full_addy)
            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time

            logger.info("Step Two")

            for alink in parent_links_main:
                new_links2, parent_links2 = self.get_home_links(alink[0])

            print('--------------big pile:')

            finalproduct = sorted(list(set(self.main_list_links)))
            for i in finalproduct:
                print(i)

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            pass

    def __init__(self):
        print('In linkcheck: __init__')
        super().__init__()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
