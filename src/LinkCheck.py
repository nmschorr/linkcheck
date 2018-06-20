# python 3

from selenium import webdriver
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
        #driver = webdriver.Firefox()
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

        logger.info("Done with HREF_finder.")
        loc_links_a = list(set(loc_links))
        loc_links_b = sorted(loc_links_a)
        #driver.quit()
        return loc_links_b

    #############---------------------------------------- def

    def GET_MORE_LINKS(self, loc_elems):
        driver = self.driver
        homelinks = [] ; homelinksSetList = [] ; homelinks_all = []

        logger.info("\n-------------------------------------->Starting GET_MORE_LINKS.")
        if loc_elems:
            ctr = enumerate(range(len(loc_elems)))
            for i,y in ctr:
                tchild, tparent = loc_elems[i]
                logger.info(str(tchild))

                try:                              ### get only alien links here
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
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("\nDone with GET_MORE_LINKS.")
        #driver.quit()
        return sorted(list(set(homelinks_all)))

    def scoop_new_links(self, myhome_arg):
        #driver = webdriver.Firefox()
        home_more = None;  home_all_new = None
        logger.info("\n-------------------------------------->Starting scoop_new_links.")

        home_grp_a = self.GET_MORE_LINKS(myhome_arg)

        home_grp = list(set(home_grp_a))
        newly_found_links_fin = list(set(home_grp))
        #driver.quit()

        return newly_found_links_fin
        ### return new, alien, all
    # ------------------------------------------------------------------------------------
       #############---------------------------------------- end of def
    # begin:
    def main(self):
        home_0 = []; alien_0 = []; homelist=[]; homelist2 = []; homelist3 = []; homelist4= [];
        parent = address
        #'driver = webdriver.Firefox()
        driver = self.driver

        driver.get(address)
        driver.minimize_window()

        logger.debug('In main() Getting first address: {}'.format(address))
        big_pile = []
        try:
            home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                 ##first time:  HOME PAGE ONLY  ##first time:

            logger.info("Step One")
            base_links = self.HREF_finder(home_elements, parent) #false: get all # list, str
            big_pile.append(base_links)

            logger.info("Step Two")

            #driver.quit()

            base_links2= self.scoop_new_links(base_links)

            for x in base_links2:
                if home2 in x[0]:
                    homelist2.append(x)

            base_links3= self.scoop_new_links(homelist2)

            for x in base_links3:
                if home2 in x[0]:
                    homelist3.append(x)

            base_links4 = self.scoop_new_links(homelist3)
            for x in base_links4:
                if home2 in x[0]:
                    homelist4.append(x)

            base_links5 = self.scoop_new_links(homelist4)
            big_pile.append(base_links2,base_links3,base_links4,base_links5 )
            big_pile_set = list(set(big_pile))
            big_pile_sort = sorted(big_pile_set)

            logger.info("!! Done with new set")

            self.write_home_set_to_file(big_pile_sort, ttype='all')
            logger.info("just did write_home_set_to_file")

            self.GET_ERRORS(big_pile_sort, logger)
            logger.info('Done with main(). Done close driver. Bye.')

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
        driver = self.driver
        print('In linkcheck: __init__')
        super().__init__()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file
