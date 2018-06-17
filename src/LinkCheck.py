# python 3

#from requests import *
from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


#############---------------------------------------- def

class linkcheck(linkckutil):

    def restartdrvr(self,drver):
        drver.quit()
        logger.debug('ALERT! quit driver from restartdrvr')
        drver = webdriver.Firefox()
        logger.debug('Restarted driver from restartdrvr')
        return drver

    #############---------------------------------------- def
    def check_file_extension(self,hrefw=''): # chk for appropriate exts for homelinks only
        html4 = hrefw[-4:]  # html
        htm3 = hrefw[-3:]  # htm
        php = hrefw[-3:]  # htm
        phpx = hrefw[-3:-1]  # phpx
        lastchar = hrefw[-1:]
        if any([html4 == 'html', htm3 == 'htm', lastchar == '/', php == 'php', phpx == 'php']):
            return True
        else:
            return False

    #############---------------------------------------- def
    #@staticmethod
    def GET_MANY_LINKS_LARGE(self, locElements, parent, talien=True):
        home_links = []
        alien_links = []
        remcruft = self.remcruft
        global driver

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a':
                    if type(webelem) is not 'NoneType':
                        if webelem is not None:
                            hrefw = webelem.get_attribute('href')

                            if type(hrefw) is str:
                                emlen = len(hrefw)
                                badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:',
                                             emlen < 7]
                                                            # if hrefw == 'http://www.repercussions.com/contact.htm':
                                if remcruft(hrefw, badlist) == 'bad': 0

                                elif any(badchecks): 0
                                                    #logger.info('Found bad attr: ' + hrefw)
                                else:
                                    if talien == False:  #don't get alien links
                                        ans1 = hrefw.find(home_1)  ## is the home_ in there?
                                        ans2 = hrefw.find(home_2)  ## is the home_ in there?

                                        if self.check_file_extension(hrefw): # chk for appropriate exts for homelinks only

                                            if (ans1 + ans2) > 0 :  # if either are there
                                                home_links.append((hrefw, parent))  # add to main home list
                                        else:
                                            alien_links.append((hrefw, parent))    # tuple - put pdfs here \
                                    else: #if talien == true
                                                                #  since they won't be searched for links
                                        alien_links.append((hrefw, parent))  # tuple - put pdfs, txt, mid, jpg etc here \

        except StaleElementReferenceException as s:
            logger.debug(str(s), exc_info=True)
            pass

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            driver = self.restartdrvr(driver)
            pass

        alien_linksSort = list(set(alien_links))  ## sort and delete dupes
        alien_linksSorted = sorted(alien_linksSort)  ## sort and delete dupes

        home_linksSort = list(set(home_links))
        home_linksSorted = sorted(home_linksSort)

        return home_linksSorted, alien_linksSorted

    #############---------------------------------------- end of def

    def GET_MORE_LINKS(self, loc_elems=[]):
        homelinks = []
        alienlinks = []
        homelinksSetList = []
        alienlinksSetList = []
        homelinks_all = []
        alienlinks_all = []
        global driver

        for each_tuple in loc_elems:
            tchild = each_tuple[0]  # get a page from a link on the home page
            tparent = each_tuple[1]
            print("child: " +  tchild)
            logger.info(tchild)
            driver.get(tchild)
            child_elements = driver.find_elements_by_xpath('.//a')

            try:
                homelinks, alienlinks = self.GET_MANY_LINKS_LARGE(child_elements, tparent, True)
                homelinksSetList = list(set(homelinks))
                alienlinksSetList = list(set(alienlinks))

                # selenium.common.exceptions.UnexpectedAlertPresentException:
            except (UnexpectedAlertPresentException) as e:
                logger.debug('ALERT! -- on: {}'.format(tchild))
                logger.debug(str(e), exc_info=True)

                try:
                    alert = driver.switch_to.alert
                    driver.switch_to.alert.dismiss()
                except:
                    driver.quit()
                    logger.debug('ALERT! quit driver')
                    driver = webdriver.Firefox()
                    logger.debug('Restarted driver')
                    pass

                pass

            except (TimeoutException) as e:
                logger.debug('ALERT! Timeout: {}'.format(tchild))
                logger.debug(str(e), exc_info=True)
                driver.quit()
                logger.debug('ALERT! quit driver')
                driver = webdriver.Firefox()
                logger.debug('Restarted driver')
                pass

            except BaseException as e:
                logger.debug('ALERT! --BaseException: {}'.format(tchild))
                logger.debug(str(e), exc_info=True)
                driver.quit()
                logger.debug('ALERT! quit driver')
                driver = webdriver.Firefox()
                logger.debug('Restarted driver')
                pass

            homelinks_all += homelinksSetList
            alienlinks_all += alienlinksSetList

        homelinks_all_sorted = list(set(homelinks_all))
        alienlinks_all_sorted = list(set(alienlinks_all))

        return homelinks_all_sorted, alienlinks_all_sorted

    # ------------------------------------------------------------------------------------
    def homeset(self, home_0, alien_0):
        global driver
        home_all_final = []
        alien_all_final = []

        try:
            home_1, alien_1 = self.GET_MORE_LINKS(home_0)
            home_xtras_1 = [item for item in home_1 if item not in home_0]  ## get the new diffs
            home_all_1 = list(set(home_1 + home_xtras_1))  ## add them to base set

            home_2, alien_2 = self.GET_MORE_LINKS(home_xtras_1)
            home_xtras_2 = [item for item in home_2 if item not in home_all_1]
            home_all_2 = list(set(home_all_1 + home_xtras_2))

            home_3, alien_3 = self.GET_MORE_LINKS(home_xtras_2)
            home_xtras_3 = [item for item in home_3 if item not in home_all_2]
            home_all_3 = list(set(home_all_2 + home_xtras_3))

            home_4, alien_4 = self.GET_MORE_LINKS(home_xtras_3)
            home_xtras_4 = [item for item in home_4 if item not in home_all_3]
            home_all_4 = list(set(home_all_3 + home_xtras_4))

            home_5, alien_5 = self.GET_MORE_LINKS(home_xtras_4)
            home_xtras_5 = [item for item in home_5 if item not in home_all_4]
            home_all_5 = list(set(home_all_4 + home_xtras_5))

            home_6, alien_6 = self.GET_MORE_LINKS(home_xtras_5)
            home_xtras_6 = [item for item in home_6 if item not in home_all_5]
            home_all_6 = list(set(home_all_5 + home_xtras_6))

            #  WRITE!!       # ------------------------------------------------------------------------------------
            home_all_final = sorted(home_all_6)
            self.write_home_set_to_file(home_all_final, logger, 'home')

            # ------------------------------------------------------------------------------------
            alien_00a = alien_0 + alien_1 + alien_2 + alien_3 + alien_4 + alien_5 + alien_6
            alien_00b = list(set(alien_00a))
            alien_all_final = sorted(alien_00b)
            self.write_home_set_to_file(alien_all_final, logger, 'alien')
            logger.info("just did write_home_set_to_file")

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            driver = self.restartdrvr(driver)
            pass

        return home_all_final, alien_all_final


    #############---------------------------------------- end of def
    # begin:
    def main(self):
        super
        global logger
        home_0 = []
        alien_0 = []
        parent = address
        global driver
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        driver.get(address)

        logger = self.setuplogger()
        logger.debug('In main() Getting first address: {}'.format(address))

        try:
            home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                 ##first time:  HOME PAGE ONLY  ##first time:
            home_0, alien_0 = self.GET_MANY_LINKS_LARGE(home_elements, parent, False)  # list, str

            home_all_final, alien_all_final = self.homeset(home_0, alien_0)

            self.geterrs(home_all_final, alien_all_final, logger)
            logger.info('Done with main()')
            driver.close()
            logger.info('Done close driver. Bye.')

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            driver = self.restartdrvr(driver)
            pass

    def __init__(self):
        print('Init: ' + __name__)
                    # global mu
                    # mu = linkckutil()  # instantiate class which sets up logger, etc.
        self.main()

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None

linkcheck()  ## run this file






