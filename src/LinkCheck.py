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

    @staticmethod
    def alert_exception_handler(ee, child=''):
        global logger
        global driver

        logger.info("Starting alert_exception_handler.")
        mmsg = 'ALERT! -- on:' + child
        logger.debug(mmsg)
        logger.debug(str(ee), exc_info=True)
        try:
            alert = driver.switch_to.alert
            sleep(1)
            txt = alert.text
            print("alert text: " + txt)
            driver.switch_to.alert.dismiss()
            sleep(1)
            driver.switch_to.alert.accept()
            sleep(1)

        except Exception as e:
            logger.debug("dismissing alert didn\'t work")
            logger.debug(str(e), exc_info=True)
            #self.restartdrvr(driver, logger)
            pass

        logger.info("Done with alert_exception_handler.")

    #############---------------------------------------- def

    # noinspection PyStatementEffect
    def GET_HOME_LINKS(self, locElements, parent):
        home_links = []
        global driver
        global logger
        logger.info("Starting GET_HOME_LINKS.")

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a' and type(webelem) is not 'NoneType' and webelem is not None:
                    hrefw = webelem.get_attribute('href')

                    if type(hrefw) is str:
                        emlen = len(hrefw)
                        badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:', emlen < 7]
                        if self.remcruft(hrefw, badlist) == 'bad':   0
                        elif any(badchecks):  0
                        else:
                            if self.check_file_extension(hrefw):  # chk for appropriate exts for homelinks only
                                if (hrefw.find(home1) + hrefw.find(home1)) > 0:  # if either are there
                                    home_links.append((hrefw, parent))  # add to main home list\

        except StaleElementReferenceException as s:
            logger.debug(str(s), exc_info=True)
            pass

        except:
            print("Unexpected error:", exc_info()[0])
            raise
        logger.info("Done with GET_HOME_LINKS.")
        return sorted(list(set(home_links)))

    #############---------------------------------------- def
    #@staticmethod
    def GET_ALIEN_LINKS(self, locElements, parent):
        alien_links = []
        global driver
        global logger
        hrefw = ''
        logger.info("Starting GET_ALIEN_LINKS.")

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a' and type(webelem) is not 'NoneType' and webelem is not None:
                    hrefw = webelem.get_attribute('href')

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

        except StaleElementReferenceException as s:
            logger.debug(str(s), exc_info=True)
            pass

        except UnexpectedAlertPresentException as e:
            self.alert_exception_handler(e, hrefw)
            pass

        except:
            print("Unexpected error:", exc_info()[0])
            pass
            # raise

        logger.info("Done with GET_ALIEN_LINKS.")
        return sorted(list(set(alien_links)))

    #############---------------------------------------- end of def

    def GET_MORE_LINKS_home(self, loc_elems):
        global driver
        global logger
        homelinks = []
        homelinksSetList = []
        homelinks_all = []
        logger.info("Starting GET_MORE_LINKS_home.")

        if loc_elems:
            for each_tuple in loc_elems:
                tchild, tparent = each_tuple  # get a page from a link on the home page
                                                        #  tparent = each_tuple[1]
                print("child: " +  tchild)
                logger.info(str(tchild))
                driver.get(tchild)
                child_elements = driver.find_elements_by_xpath('.//a')

                try:                              ### get only alien links here
                    homelinks = self.GET_HOME_LINKS(child_elements, tparent)
                    homelinksSetList = list(set(homelinks))

                except TimeoutException as e:
                    logger.debug('ALERT! Timeout: {}'.format(tchild))
                    logger.debug(str(e), exc_info=True)
                    driver.quit()
                    logger.debug('ALERT! quit driver')
                    driver = webdriver.Firefox()
                    logger.debug('Restarted driver')
                    pass

                except UnexpectedAlertPresentException as e:
                    self.alert_exception_handler(e, tchild)
                    pass

                except:
                    print("Unexpected error:", exc_info()[0])
                    pass

                homelinks_all = list(set(homelinks_all + homelinksSetList))
        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("Done with GET_MORE_LINKS_home.")
        return sorted(list(set(homelinks_all)))

    #############---------------------------------------- end of def

    def GET_MORE_LINKS_alien(self, loc_elems):
        global driver
        global logger
        alienlinks = []
        alienlinksSetList = []
        alienlinks_all = []
        tchild =''

        logger.info("Starting GET_MORE_LINKS_alien.")

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
                    logger.debug('ALERT! Timeout in GET_MORE_LINKS_alien for: {}'.format(tchild))
                    logger.debug(str(e), exc_info=True)
                    driver = self.restartdrvr(driver, logger)
                    pass

                except UnexpectedAlertPresentException as e:
                    self.alert_exception_handler(e, tchild)
                    pass

                except Exception as e:
                    logger.debug(str(e), exc_info=True)
                    pass

                except: pass

                alienlinks_a = alienlinks_all + alienlinksSetList
                alienlinks_all = sorted(list(set(alienlinks_a)))

        else:
            logger.info("loc elems empty in GET_MORE_LINKS_alien")

        logger.info("Done with GET_MORE_LINKS_alien.")
        return alienlinks_all

    # ------------------------------------------------------------------------------------
    def scoop_new_links(self, myhome, home_all_0):
        home_more = None
        home_all_new = None
        logger.info("Starting scoop_new_links.")

        home_more = self.GET_MORE_LINKS_home(myhome)
        newlinks_home = [i for i in home_more if i not in home_all_0]

        home_all_1 = home_all_0 + newlinks_home
        alien_more = list(set(self.GET_MORE_LINKS_alien(myhome)))

        home_all_2 = list(set(home_all_1))
        logger.info("Done with scoop_new_links.")
        return newlinks_home, alien_more, home_all_2

    # ------------------------------------------------------------------------------------
    def homeset(self, home_0, alien_0):
        global driver
        global logger
        alien_all = [i for i in alien_0]
        home_all = [i for i in home_0]

        try:
            logger.info("in homeset. doing new set1 now")
            home_1, alien_1, home_all = self.scoop_new_links(home_0, home_all)
            logger.info("in homeset. doing new set2 now")
            home_2, alien_2, home_all = self.scoop_new_links(home_1, home_all)
            logger.info("in homeset. doing new set3 now")
            home_3, alien_3, home_all = self.scoop_new_links(home_2, home_all)
            logger.info("in homeset. doing new set4 now")
            home_4, alien_4, home_all = self.scoop_new_links(home_3, home_all)
            #home_5, alien_5, home_all = self.scoop_new_links(home_4, home_all)
            #home_6, alien_6, home_all = self.scoop_new_links(home_5, home_all)
            logger.info("done with new set")

            alien_all = sorted(list(set(alien_1 + alien_2 + alien_3 + alien_4  )))
            #alien_all = sorted(list(set(alien_0 + alien_1 + alien_2 + alien_3 + alien_4 + alien_5 + alien_6)))
            self.write_home_set_to_file(sorted(home_all), logger, 'home')
            self.write_home_set_to_file(alien_all, logger, 'alien')
            logger.info("just did write_home_set_to_file")

        except UnexpectedAlertPresentException as e:
            self.alert_exception_handler(e, 'unknown')
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            #driver = self.restartdrvr(driver, logger)
            pass

        return home_all, alien_all


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
            home_0 = self.GET_HOME_LINKS(home_elements, parent) #false: get all # list, str
            alien_0 = self.GET_ALIEN_LINKS(home_elements, parent) #false: get all # list, str

            logger.info("Step Two")
            home_all_final, alien_all_final = self.homeset(home_0, alien_0)

            self.geterrs(home_all_final, alien_all_final, logger)
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






