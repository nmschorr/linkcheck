# python 3

from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException
from src import home1, home2, lnfeed, ercodes, badlist, start_driver, address, driver
from src import the_logger as logger

#############---------------------------------------- def
# noinspection PyRedeclaration
class linkcheck(linkckutil):

    #############---------------------------------------- def

    # noinspection PyStatementEffect
    def HREF_finder(self, locElements, parent):
        driver = self.driver
        loc_links = []
        logger.info("-------------------------------------->Starting HREF_finder.")
        try:
            for webelem in locElements:
                if webelem.tag_name == 'a':
                    if type(webelem) is not 'NoneType' and webelem is not None:
                        if webelem.get_attribute('href'):  # it needs to have an href attribute to continue
                            hrefw = webelem.get_attribute('href')

                            if type(hrefw) is str:
                                print('-----------------!!!!  here is link in home: ' + hrefw)
                                badchecks = \
                                    [hrefw[0:6]=='javasc', hrefw[0:1] == '/',hrefw[0:7]=='mailto:',len(hrefw)<7]
                                if 'oz' in hrefw:
                                    print('\n\n----------------------------------- current hrefw:' + hrefw)
                                    logger.debug('found oz in ...HREF_finder ')
                                    logger.debug(hrefw)

                                if self.remcruft(hrefw, badlist) == 'bad' or any(badchecks):
                                    msg2 = "discarded HOME link: {}".format(hrefw)
                                    logger.info(msg2)
                                else:
                                    loc_links.append((hrefw, parent))  # add to main home list\

        except StaleElementReferenceException as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            driver = start_driver()
            pass

        except (UnexpectedAlertPresentException, TimeoutException, Exception) as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            driver = start_driver()
            pass

        loc_links_a = list(set(loc_links))
        loc_links_b = sorted(loc_links_a)
        logger.debug('Leaving ' + classmethod.__name__ )
        return loc_links_b

    #############---------------------------------------- def

    def GET_MORE_LINKS(self, loc_elems):
        driver = self.driver
        homelinks, homelinksSetList, homelinks_all = [],[],[]

        logger.info("\n-------------------------------------->Starting GET_MORE_LINKS.")
        if loc_elems:
            ctr = enumerate(range(len(loc_elems)))
            for i,y in ctr:
                tchild, tparent = loc_elems[i]
                logger.info(str(tchild))

                try:
                    driver.get(tchild)
                    child_elements = driver.find_elements_by_xpath('.//a')
                    homelinks = self.HREF_finder(child_elements, tparent)
                    homelinksSetList = list(set(homelinks))

                except (TimeoutException, UnexpectedAlertPresentException, Exception) as e:
                    logger.debug(str(e), exc_info=True)
                    driver.quit()
                    driver = start_driver()
                    next(ctr, None)
                    pass

            homelinks_all = list(set(homelinks_all + homelinksSetList))
            self.wr2f(homelinks_all, 'GET_MORE_LINKS')

        else:
            logger.info("loc elems empty in " + classmethod.__name__)

        logger.debug('Leaving ' + classmethod.__name__ )
        return sorted(list(set(homelinks_all)))

    #############---------------------------------------- def

    def scoop_new_links(self, myhome_arg):
        home_more = None;  home_all_new = None
        logger.info("\n-------------------------------------->Starting: "  + classmethod.__name__)
        home_grp_a = self.GET_MORE_LINKS(myhome_arg)
        home_grp = list(set(home_grp_a))
        newly_found_links_fin = list(set(home_grp))
        logger.debug('Leaving ' + classmethod.__name__ )
        return newly_found_links_fin
    # ------------------------------------------------------------------------------------
    def get_home_links(self, home1):
        from urllib.parse import urlsplit
        from requests_html import HTMLSession

        parent = 'http://schorrmedia.com/'
        thebase_part = (urlsplit(parent))[1]

        links = []
        homelinks = []
        session = HTMLSession()
        response = session.get(parent)

        for page in response.html.absolute_links:
            each_ses = session.get(page)
            theurl = each_ses.url
            if '?' in theurl:
                theurl = (theurl.split('?'))[0]

            links.append((theurl, parent))
            if thebase_part in theurl:
                homelinks.append((theurl, parent))

        return links, homelinks



       #############---------------------------------------- end of def
    # begin:
    def main(self):
        home_0 = []; homelist=[]; homelist2 = []; homelist3 = []; homelist4= [];
        parent = address
        #driver = self.driver
        #driver.get(address)
        #driver.set_window_size(200,200)

        logger.debug('In main() Getting first address: {}'.format(address))
        big_pile = []
        try:
            new_links_main, parent_links_main = self.get_home_links(home1)
            big_pile.append(new_links_main)

            logger.info("Step One Done")   ##first time:  HOME PAGE ONLY  ##first time
                        #home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                        #base_links = self.HREF_finder(home_elements, parent) #false: get all # list, str

            logger.info("Step Two")

            for alink in parent_links_main:
                new_links2, parent_links2 = self.get_home_links(alink)
                big_pile.append(new_links2)
                parent_links_main.append(parent_links2)

           # base_links2= self.scoop_new_links(base_links)

            for x in base_links2:
                if home2 in x[0]:
                    homelist2.append(x)

            base_links3= self.scoop_new_links(homelist2)

            for x in base_links3:
                if home2 in x[0]:
                    homelist3.append(x)

            # base_links4 = self.scoop_new_links(homelist3)
            # for x in base_links4:
            #     if home2 in x[0]:
            #         homelist4.append(x)
            #
            # base_links5 = self.scoop_new_links(homelist4)

           # biglist = [base_links2, base_links3, base_links4, base_links5]
            big_pile_of_list_tups=[]

            big_list_of_tups = [base_links2, base_links3 ]

            for bt in big_list_of_tups:
                big_pile_of_list_tups.append(bt)

            bigpile_onelist = sum(big_pile, [])
            bt2 = list(set(bigpile_onelist))

            self.GET_ERRORS(bt2)

            logger.info("!! Done with new set")

            #self.write_home_set_to_file(big_pile_sort, ttype='all')
            logger.info("just did write_home_set_to_file")

            driver.quit()
            logger.info('Done with main(). Done closing driver. Bye.')

        except UnexpectedAlertPresentException as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            driver = start_driver()
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            driver = start_driver()
            pass

    def __init__(self):
        print('In linkcheck: __init__')
        super().__init__()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file/class
