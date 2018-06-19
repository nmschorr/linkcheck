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

#############---------------------------------------- def

class linkcheck(linkckutil):
    global driver, logger

    #@staticmethod
    def alert_exception_handler(self, ee, child=''):
        global driver, logger

        logger.info("-------------------------------------->Starting alert_exception_handler.")
        mmsg = 'ALERT! -- on:' + child
        logger.debug(mmsg)
        logger.debug(str(ee), exc_info=True)
        sleep(1)

        try:
            driver.switch_to.alert.dismiss()
        except BaseException as e:
            pass

        try:
            driver.switch_to.alert.accept()

        except BaseException as e:
            logger.debug("Dismissing alert.")
            pass

        try:
            driver.switch_to.alert.cancel()

        except BaseException as e:
            logger.debug("Dismissing alert.")
            pass

        except Exception as e:
            logger.debug("Dismissing alert didn\'t work")
            logger.debug(str(e), exc_info=True)
            linkckutil.restartdrvr(driver, logger)
            pass

        logger.info("Done with alert_exception_handler.")

    #############---------------------------------------- def

    # noinspection PyStatementEffect
    def href_finder_hm(self, locElements, parent):
        home_links = []
        global driver, logger
        logger.info("-------------------------------------->Starting href_finder_hm.")

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a':
                    if  type(webelem) is not 'NoneType' and webelem is not None:
                        hrefw = webelem.get_attribute('href')

                        if type(hrefw) is str:
                            print('-----------------!!!!  here is link in home: ' + hrefw)
                            emlen = len(hrefw)

                            badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:', emlen < 7]

                            if 'oz' in hrefw:
                                print('\n\n----------------------------------- current hrefw:' + hrefw)
                                logger.debug('found oz in ...href_finder_hm ')
                                logger.debug(hrefw)

                            if self.remcruft(hrefw, badlist) == 'bad':
                                msg2 = "discarded HOME link remcruft: {}".format(hrefw)
                                logger.info(msg2)

                            elif any(badchecks):
                                msg3 = "discarded HOME link badchecks: {}".format(hrefw)
                                logger.info(msg3)

                            elif self.check_file_extension(hrefw):  # chk for appropriate exts for homelinks only
                                if (hrefw.find(home1) + hrefw.find(home1)) > 0:  # if either are there
                                    msg4 = "adding HOME link: {}".format(hrefw)
                                    logger.info(msg4)
                                    home_links.append((hrefw, parent))  # add to main home list\
                            else:
                                msg5 = "discarded HOME link for check_file_extension or home-link-within : {}".format(hrefw)
                                logger.info(msg5)

        except StaleElementReferenceException as s:
            logger.debug(str(s), exc_info=True)
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            raise
        logger.info("Done with href_finder_hm.")
        newset = list(set(home_links))
        newset2 = sorted(newset)
        return newset2

    #############---------------------------------------- def
    #@staticmethod
    def GET_ALIEN_LINKS(self, locElements, parent):
        alien_links = []
        global driver, logger
        hrefw = ''
        logger.info("-------------------------------------->Starting GET_ALIEN_LINKS.")

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a' and type(webelem) is not 'NoneType' and webelem is not None:
                    hrefw = webelem.get_attribute('href')
                    print('-----------------!!!!  here is link in alien: ' + hrefw)

                    if type(hrefw) is str:
                        homx = hrefw.find(home1)
                        homy = hrefw.find(home2)
                        sumit = homx + homy
                        emlen = len(hrefw)
                        badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:',emlen < 7]

                        if self.remcruft(hrefw, badlist) == 'bad': 0

                        elif any(badchecks): 0

                        elif sumit <= 0:  ## no home links found
                            alien_links.append((hrefw, parent))  # tuple - put pdfs, txt, mid, jpg etc here \

                self.write_list_to_file(alien_links, 'GET_MORE_LINKS_home')

        except StaleElementReferenceException as s:
            logger.debug(str(s), exc_info=True)
            pass

        except UnexpectedAlertPresentException as e:
            self.alert_exception_handler(e, hrefw)
            pass

        except BaseException as e:
            self.alert_exception_handler(e, hrefw)
            pass
            # raise

        logger.info("Done with GET_ALIEN_LINKS.")
        return sorted(list(set(alien_links)))

    #############---------------------------------------- end of def

    def GET_MORE_LINKS_home(self, loc_elems):
        global driver, logger
        homelinks = [] ; homelinksSetList = [] ; homelinks_all = []

        logger.info("\n-------------------------------------->Starting GET_MORE_LINKS_home.")
        if loc_elems:
            ctr = enumerate(range(len(loc_elems)))
            for i,y in ctr:
                            #for each_tuple in loc_elems:
                each_tuple = loc_elems[i]
                tchild, tparent = each_tuple  # get a page from a link on the home page
                                                        #  tparent = each_tuple[1]
                print("child: " +  tchild)
                logger.info(str(tchild))
                                    ## put new code here : put an iter like the other loop

                try:                              ### get only alien links here
                    driver.get(tchild)
                    child_elements = driver.find_elements_by_xpath('.//a')
                    homelinks = self.href_finder_hm(child_elements, tparent)
                    homelinksSetList = list(set(homelinks))

                except TimeoutException as e:
                    logger.debug('ALERT! Timeout: {}'.format(tchild))
                    logger.debug(str(e), exc_info=True)
                    driver = self.restartdrvr(driver, logger)
                    next(ctr, None)   ## get on to next item
                    pass

                except UnexpectedAlertPresentException as e:
                    self.alert_exception_handler(e, tchild)
                    driver = self.restartdrvr(driver, logger)
                    next(ctr, None)
                    pass

                except BaseException as e:
                    self.alert_exception_handler(e, ' ')
                    next(ctr, None)
                    pass

            homelinks_all = list(set(homelinks_all + homelinksSetList))
            self.write_list_to_file(homelinks_all, 'GET_MORE_LINKS_home')

        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("\nDone with GET_MORE_LINKS_home.")
        return sorted(list(set(homelinks_all)))

    #############---------------------------------------- end of def

    def GET_MORE_LINKS_alien(self, loc_elems):
        global driver, logger
        alienlinks = [];  alienlinksSetList = []; alienlinks_all = []; tchild =''
        logger.info("\n-------------------------------------->Starting GET_MORE_LINKS_alien.")

        if loc_elems:
            for each_tuple in loc_elems:
                tchild, tparent = each_tuple    #  tparent = each_tuple[1]
                mmsg="In GET_MORE_LINKS_alien. child: " + tchild
                logger.info(mmsg)
                driver.get(tchild)
                child_elements = driver.find_elements_by_xpath('.//a')

                try:                              ### get only alien links here
                    alienlinks = self.GET_ALIEN_LINKS(child_elements, tparent)
                    alienlinksSetList = list(set(alienlinks))

                except TimeoutException as e:
                    logger.debug('\nALERT! Timeout in GET_MORE_LINKS_alien for: {}'.format(tchild))
                    logger.debug(str(e), exc_info=True)
                    driver = self.restartdrvr(driver, logger)
                    pass

                except UnexpectedAlertPresentException as e:
                    self.alert_exception_handler(e, tchild)
                    pass

                except BaseException as e:
                    logger.debug(str(e), exc_info=True)
                    pass

                alienlinks_a = alienlinks_all + alienlinksSetList
                alienlinks_all = sorted(list(set(alienlinks_a)))

        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        self.write_list_to_file(alienlinks_all, 'GET_MORE_LINKS_alien')
        logger.info("\nDone with GET_MORE_LINKS_alien.")
        return alienlinks_all

    # ------------------------------------------------------------------------------------
    def scoop_new_links(self, myhome, home_all_passed_in):
        home_more = None
        home_all_new = None
        logger.info("\n-------------------------------------->Starting scoop_new_links.")

        home_more = self.GET_MORE_LINKS_home(myhome)
        #newly_found_links = [i for i in home_more if i not in home_all_passed_in]
        newly_found_links = [i for i in home_more]

        home_glued_together = home_all_passed_in + newly_found_links
        alien_more = list(set(self.GET_MORE_LINKS_alien(newly_found_links)))

        home_glued_together_setlist = list(set(home_glued_together))
        logger.info("\nDone with scoop_new_links.")

        newly_found_links_fin = list(set(newly_found_links))
        return newly_found_links_fin, alien_more, home_glued_together_setlist

    # ------------------------------------------------------------------------------------
    def homeset(self, home_0, alien_0):
        global driver
        global logger
        self.write_list_to_file(home_0, 'homeset0_home_0')
        self.write_list_to_file(alien_0, 'homeset0_alien_0')


        alien_all = [i for i in alien_0]
        home_all_0 = [i for i in home_0]
        self.write_list_to_file(alien_0, 'homeset0_home_all_0')

        try:
            logger.info("\n-------------------------in homeset. doing new set1 now")
            self.write_list_to_file(home_0, 'homeset0-hm')
            self.write_list_to_file(alien_0, 'homeset0-aln')

            newly_found_links1, alien_1, home_all_1 = self.scoop_new_links(home_0, home_all_0)
            self.write_list_to_file(newly_found_links1, 'homeset1_newly_found_links1')
            self.write_list_to_file(alien_1,            'homeset1_aln_alien_1')
            self.write_list_to_file(home_all_1,            'homeset1_home_all_1')


            logger.info("\n-------------------------in homeset. doing new set2 now")

            newly_found_links2, alien_2, home_all_2 = self.scoop_new_links(newly_found_links1, home_all_1)
            self.write_list_to_file(newly_found_links2, 'homeset2_newly_found_links2')
            self.write_list_to_file(alien_2, 'homeset2_aln_alien_2')
            self.write_list_to_file(home_all_2, 'homeset1_home_all_2')

            logger.info("\n-------------------------in homeset. doing new set3 now")
            newly_found_links3, alien_3, home_all_3 = self.scoop_new_links(newly_found_links2, home_all_2)
            self.write_list_to_file(newly_found_links3, 'homeset3_newly_found_links3')
            self.write_list_to_file(alien_3, 'homeset3_aln_alien_3')
            self.write_list_to_file(home_all_3, 'homeset1_home_all_3')


            logger.info("\n-------------------------in homeset. doing new set4 now")
            newly_found_links4, alien_4, home_all_4 = self.scoop_new_links(newly_found_links3, home_all_3)
            self.write_list_to_file(newly_found_links4, 'homeset4_newly_found_links4')
            self.write_list_to_file(alien_4, 'homeset4_aln_alien_4')
            self.write_list_to_file(home_all_4, 'homeset1_home_all_4')

            newly_found_links5, alien_5, home_all_5 = self.scoop_new_links(newly_found_links4, home_all_4)
            newly_found_links6, alien_6, home_all_6 = self.scoop_new_links(newly_found_links5, home_all_5)
            logger.info("done with new set")

            alien_all2 = sorted(list(set(alien_all + alien_1 + alien_2 + alien_3 + alien_4 + alien_5 + alien_6 )))
            #alien_all = sorted(list(set(alien_0 + alien_1 + alien_2 + alien_3 + alien_4 + alien_5 + alien_6)))
            self.write_home_set_to_file(sorted(home_all_6), logger, 'home')
            self.write_home_set_to_file(alien_all2, logger, 'alien')
            logger.info("just did write_home_set_to_file")

        except UnexpectedAlertPresentException as e:
            self.alert_exception_handler(e, 'unknown')
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            #driver = self.restartdrvr(driver, logger)
            pass
        for i in home_all_6:
            print(i)
        return home_all_6, alien_all


    #############---------------------------------------- end of def
    # begin:
    def main(self):
        global driver
        global logger
        home_0 = []
        alien_0 = []
        parent = address
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.get(address)

        logger.debug('In main() Getting first address: {}'.format(address))

        try:
            home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                 ##first time:  HOME PAGE ONLY  ##first time:

            logger.info("Step One")
            home_0 = self.href_finder_hm(home_elements, parent) #false: get all # list, str
            alien_0 = self.GET_ALIEN_LINKS(home_elements, parent) #false: get all # list, str

            logger.info("Step Two")
            home_all_final, alien_all_final = self.homeset(home_0, alien_0)

            self.geterrs(home_all_final, alien_all_final, logger, driver)
            logger.info('Done with main()')
            driver.close()
            logger.info('Done close driver. Bye.')

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            #driver = self.restartdrvr(driver, logger)
            pass

    def __init__(self):
        global logger
        global driver
        print('In linkcheck: __init__')
        super().__init__()
        logger = setuplog.makelogger.setup_logger()
        self.main()


if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file






