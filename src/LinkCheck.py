# python 3

#from requests import *
from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from time import sleep
from sys import exc_info
import src.setuplog as setuplog
import logging

#############---------------------------------------- def

class linkcheck(linkckutil):
   # global logger, driver
    global driver
    global logger
    logger = logging.getLogger('mainlogger')
    driver = setuplog.makelogger.rdriver()

    #@staticmethod
    def alert_exception_handler(self, ee, child):
        global driver
        logger.info("-------------------------------------->Starting alert_exception_handler.")
        mmsg = 'ALERT! -- on:' + child
        logger.debug(mmsg)
        logger.debug(str(ee), exc_info=True)
        sleep(1)

        try:
            driver.switch_to.alert.dismiss()
            sleep(1)
            driver.switch_to.alert.accept()
            sleep(1)
            driver.switch_to.alert.cancel()
            sleep(1)

        except Exception as e:
            logger.debug("Dismissing alert didn\'t work. Restarting driver/browser.")
            logger.debug(str(e), exc_info=True)
            linkckutil.restartdrvr(driver)
            pass

        logger.info("Done with alert_exception_handler.")

    #############---------------------------------------- def

    # noinspection PyStatementEffect
    def HREF_finder(self, locElements, parent):
        loc_links = []

        global driver
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
            pass

        except (UnexpectedAlertPresentException, TimeoutException, Exception) as e:
            logger.debug(str(e), exc_info=True)
            self.restartdrvr(driver)
            pass

        logger.info("Done with HREF_finder.")
        loc_links_a = list(set(loc_links))
        loc_links_b = sorted(loc_links_a)
        return loc_links_b

    #############---------------------------------------- def
    # #@staticmethod
    # def HREF_finder_alien(self, locElements, parent):
    #     alien_links = []
    #     global logger
    #     hrefw = ''
    #     logger.info("-------------------------------------->Starting HREF_finder_alien.")
    #
    #     try:
    #         counter = enumerate(range(len(locElements)))
    #         for i, y in counter:
    #                                             #for webelem in locElements:
    #             webelem = locElements[i]
    #                                         #if webelem.tag_name == 'a' and type(webelem) is not 'NoneType' and webelem is not None:
    #
    #             if webelem.tag_name == 'a' and type(webelem) is not 'NoneType' and webelem is not None:
    #                 if webelem.get_attribute('href'):  # it needs to have an href attribute to continue
    #
    #                     try:
    #                         hrefw = webelem.get_attribute('href')
    #                         print('-----------------!!!!  here is link in alien: ' + hrefw)
    #
    #                         if type(hrefw) is str:
    #                             homex = hrefw.find(home1)
    #                             homey = hrefw.find(home2)
    #                             sumit = homex + homey
    #                             emlen = len(hrefw)
    #                             badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:',emlen < 7]
    #
    #                             if self.remcruft(hrefw, badlist) == 'bad': 0
    #
    #                             elif any(badchecks): 0
    #
    #                             elif sumit <= 0:  ## no home links found
    #                                 alien_links.append((hrefw, parent))  # tuple - put pdfs, txt, mid, jpg etc here \
    #
    #                         self.wr2f(alien_links, 'GET_MORE_LINKS_home')  #write to file
    #                         next(counter)
    #
    #                     except StaleElementReferenceException as s:
    #                         logger.debug(str(s), exc_info=True)
    #                         next(counter)
    #                         pass
    #
    #                     except UnexpectedAlertPresentException as e:
    #                         logger.debug(str(e), exc_info=True)
    #                         linkckutil.restartdrvr(driver)
    #                         next(counter)
    #                         pass
    #
    #                     except BaseException as e:
    #                         logger.debug(str(e), exc_info=True)
    #                         linkckutil.restartdrvr(driver)
    #                         next(counter)
    #                         pass
    #
    #
    #     except BaseException as e:
    #         logger.debug(str(e), exc_info=True)
    #         linkckutil.restartdrvr(driver)
    #         pass
    #
    #     logger.info("Done with HREF_finder_alien.")
    #     return sorted(list(set(alien_links)))
    #
    #############---------------------------------------- end of def

    def GET_MORE_LINKS_home(self, loc_elems):
        global driver, logger
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
                    self.alert_exception_handler(e, tchild)
                    driver = self.restartdrvr(driver)
                    next(ctr, None)
                    pass

            homelinks_all = list(set(homelinks_all + homelinksSetList))
            self.wr2f(homelinks_all, 'GET_MORE_LINKS_home')

        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("\nDone with GET_MORE_LINKS_home.")
        return sorted(list(set(homelinks_all)))

    #############---------------------------------------- end of def

    # def GET_MORE_LINKS_alien(self, loc_elems):
    #     global driver, logger
    #     alienlinks = [];  alienlinksSetList = []; alienlinks_all = []; tchild =''
    #     logger.info("\n-------------------------------------->Starting GET_MORE_LINKS_alien.")
    #
    #     if loc_elems:
    #         for each_tuple in loc_elems:
    #             tchild, tparent = each_tuple    #  tparent = each_tuple[1]
    #             mmsg="In GET_MORE_LINKS_alien. child: " + tchild
    #             logger.info(mmsg)
    #             driver.get(tchild)
    #             child_elements = driver.find_elements_by_xpath('.//a')
    #
    #             try:                              ### get only alien links here
    #                 alienlinks = self.HREF_finder_alien(child_elements, tparent)
    #                 alienlinksSetList = list(set(alienlinks))
    #
    #             except TimeoutException as e:
    #                 logger.debug('\nALERT! Timeout in GET_MORE_LINKS_alien for: {}'.format(tchild))
    #                 logger.debug(str(e), exc_info=True)
    #                 driver = self.restartdrvr(driver)
    #                 pass
    #
    #             except UnexpectedAlertPresentException as e:
    #                 self.alert_exception_handler(e, tchild)
    #                 pass
    #
    #             except BaseException as e:
    #                 logger.debug(str(e), exc_info=True)
    #                 pass
    #
    #             alienlinks_a = alienlinks_all + alienlinksSetList
    #             alienlinks_all = sorted(list(set(alienlinks_a)))
    #
    #     else:
    #         logger.info("loc elems empty in GET_MORE_LINKS_alien")
    #
    #     self.wr2f(alienlinks_all, 'GET_MORE_LINKS_alien')
    #     logger.info("\nDone with GET_MORE_LINKS_alien.")
    #     return alienlinks_all
    #
    # ------------------------------------------------------------------------------------
    def scoop_new_links(self, myhome_arg, home_group_arg):
        home_more = None;  home_all_new = None
        logger.info("\n-------------------------------------->Starting scoop_new_links.")

        new_home_links = self.GET_MORE_LINKS_home(myhome_arg)

        home_grp_a = home_group_arg + new_home_links
        home_grp = list(set(home_grp_a))

        # ## now get alien link using the home links
        alien_more = self.GET_MORE_LINKS_alien(home_grp)
        #########################################

        alien_sort = list(set(alien_more))

        newly_found_links_fin = list(set(new_home_links))

        return newly_found_links_fin, alien_sort, home_grp
        ### return new, alien, all
    # ------------------------------------------------------------------------------------
       #############---------------------------------------- end of def
    # begin:
    def main(self):
        global driver, logger
        home_0 = []; alien_0 = []
        parent = address
        #driver = webdriver.Firefox()
        #driver.implicitly_wait(10)
        driver.get(address)

        logger.debug('In main() Getting first address: {}'.format(address))

        try:
            home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                 ##first time:  HOME PAGE ONLY  ##first time:

            logger.info("Step One")
            base_links = self.HREF_finder(home_elements, parent) #false: get all # list, str

            logger.info("Step Two")
            newly_found_links1, home_all_1 = self.scoop_new_links(base_links, [])

            newly_found_links2, home_all_2 = self.scoop_new_links(newly_found_links1, home_all_1)

            newly_found_links3, home_all_3 = self.scoop_new_links(newly_found_links2, home_all_2)

            newly_found_links4, home_all_4 = self.scoop_new_links(newly_found_links3, home_all_3)

            newly_found_links5, home_all_5 = self.scoop_new_links(newly_found_links4, home_all_4)

            newly_found_links6, home_all_6 = self.scoop_new_links(newly_found_links5, home_all_5)

            logger.info("!! Done with new set")

            self.write_home_set_to_file(home_all_6, ttype='all')
            logger.info("just did write_home_set_to_file")

            self.geterrs(home_all_6, logger)
            logger.info('Done with main()')
            driver.close()
            logger.info('Done close driver. Bye.')

        except UnexpectedAlertPresentException as e:
            self.alert_exception_handler(e, 'unknown')
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            #driver = self.restartdrvr(driver)


    def __init__(self):
        global logger, driver
        print('In linkcheck: __init__')
        super().__init__()
        #logger = setuplog.makelogger.setup_logger()
        #driver = setuplog.makelogger.rdriver()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file
