# python 3

#from requests import *
#from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from time import sleep
#from sys import exc_info
import src.setuplog as setuplog
import logging

#############---------------------------------------- def

# noinspection PyRedeclaration
class linkcheck(linkckutil):
    global logger
    logger = logging.getLogger('mainlogger')



    #############---------------------------------------- def

    # noinspection PyStatementEffect
    def HREF_finder(self, locElements, parent):
        driver = setuplog.makelogger.start_driver()
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
            driver = setuplog.makelogger.start_driver()
            pass

        except (UnexpectedAlertPresentException, TimeoutException, Exception) as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            driver = setuplog.makelogger.start_driver()
            pass

        logger.info("Done with HREF_finder.")
        loc_links_a = list(set(loc_links))
        loc_links_b = sorted(loc_links_a)
        driver.quit()
        return loc_links_b

    #############---------------------------------------- def


    def GET_MORE_LINKS_home(self, loc_elems):
        driver = setuplog.makelogger.start_driver()
        global logger
        homelinks = [] ; homelinksSetList = [] ; homelinks_all = []

        logger.info("\n-------------------------------------->Starting GET_MORE_LINKS_home.")
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
                    driver = setuplog.makelogger.start_driver()
                    next(ctr, None)
                    pass

            homelinks_all = list(set(homelinks_all + homelinksSetList))
            self.wr2f(homelinks_all, 'GET_MORE_LINKS_home')

        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("\nDone with GET_MORE_LINKS_home.")
        driver.quit()
        return sorted(list(set(homelinks_all)))

    def scoop_new_links(self, myhome_arg, home_group_arg):
        driver = setuplog.makelogger.start_driver()
        home_more = None;  home_all_new = None
        logger.info("\n-------------------------------------->Starting scoop_new_links.")

        new_home_links = self.GET_MORE_LINKS_home(myhome_arg)

        home_grp_a = home_group_arg + new_home_links
        home_grp = list(set(home_grp_a))
        newly_found_links_fin = list(set(new_home_links))
        driver.quit()

        return newly_found_links_fin, home_grp
        ### return new, alien, all
    # ------------------------------------------------------------------------------------
       #############---------------------------------------- end of def
    # begin:
    def main(self):
        global logger
        home_0 = []; alien_0 = []; homelist=[]
        parent = address
        main_driver = setuplog.makelogger.start_driver()
        main_driver.get(address)
        main_driver.minimize_window()

        logger.debug('In main() Getting first address: {}'.format(address))

        try:
            home_elements = main_driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                 ##first time:  HOME PAGE ONLY  ##first time:

            logger.info("Step One")
            base_links = self.HREF_finder(home_elements, parent) #false: get all # list, str

            logger.info("Step Two")
            main_driver.quit()
            newly_found_links1, home_all_1 = self.scoop_new_links(base_links, [])
            for x in newly_found_links1:
                if home2 in x[0]:
                    homelist.append(x)

            newly_found_links2, home_all_2 = self.scoop_new_links(newly_found_links1, homelist)

            newly_found_links3, home_all_3 = self.scoop_new_links(newly_found_links2, home_all_2)

            newly_found_links4, home_all_4 = self.scoop_new_links(newly_found_links3, home_all_3)

            #newly_found_links5, home_all_5 = self.scoop_new_links(newly_found_links4, home_all_4)

            #newly_found_links6, home_all_6 = self.scoop_new_links(newly_found_links5, home_all_5)

            logger.info("!! Done with new set")

            self.write_home_set_to_file(home_all_4, ttype='all')
            logger.info("just did write_home_set_to_file")

            self.geterrs(home_all_4, logger)
            logger.info('Done with main()')
            logger.info('Done close driver. Bye.')

        except UnexpectedAlertPresentException as e:
            logger.debug(str(e), exc_info=True)
            main_driver.quit()
            main_driver = setuplog.makelogger.start_driver()
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            main_driver.quit()
            main_driver = setuplog.makelogger.start_driver()
            pass

    def __init__(self):
        global logger
        print('In linkcheck: __init__')
        super().__init__()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file
