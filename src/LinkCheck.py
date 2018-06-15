# python 3

from datetime import datetime
from requests import *
from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil
from selenium.common.exceptions import UnexpectedAlertPresentException

class LinkCheck(object):

    def makeerrorlist(self, locnewlist):
        print('new locnewlist: ', locnewlist)
        elink = ''
        errorlist = []

        ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
        tlogname = 'E:\\pylogs\\linkcheckresults' + ts + '.log'
        tlognameHndl = open(tlogname, 'w')  #
        tlognameHndl.write('Error File:' + lnfeed)

        try:  # check head
            for elinktup in locnewlist:
                
                elink = elinktup[0]
                theparent = elinktup[1]
                tlognameHndl.write('Inside Loop:' + lnfeed)

                resp = str(head(elink, data=None, timeout=30))
                print(fblack + 'resp: ', resp)
                err_resp = resp[11:14]

                responstr = 'checked: ' + elink + ' -resp: ' + err_resp + lnfeed
                tlognameHndl.write(responstr)

                if int(err_resp) in ercodes:
                    errorString = gerrstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)
                    print(fred + errorString + fblack)
                    errorlist.append(errorString)
                    tlognameHndl.write(errorString + lnfeed)
                else:
                    print(fblack + 'status code: ' + err_resp)

        except BaseException as e:
            print('Exception trying: ', elink, str(e))
            logger.debug(str(e), exc_info=True)
            pass

        tlognameHndl.close()
        return errorlist


#====================================================
    def getthelinks_two(self, hrefz, parent):
        remcruft = mu.remcruft
        hrefw = []
        baselinks = []
        nonbaselinks = []
        keepgoing = True
        emlen = 1

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a':
                    print('TYPE OF OBJECT: -----' + str(type(webelem)))

                    if type(webelem) is not 'NoneType':
                        if webelem is not None:
                            hrefw = webelem.get_attribute('href')
                            print('JUST GOT hrefw: -----' + str(hrefw))
                            print('TYPE OF hrefw: -----' + str(type(hrefw)))

                            if type(hrefw) is str:
                                emlen = len(hrefw)
                                badchecks = [hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:',
                                             emlen < 7]

                                if remcruft(hrefw, badlist) == 'bad':
                                    0

                                elif any(badchecks):
                                    print('found bad attr: ' + str(hrefw))

                                else:
                                    ans1 = hrefw.find(base1)  ## is the base in there?
                                    ans2 = hrefw.find(base2)  ## is the base in there?

                                    if (ans1 + ans2) > 0:  # if either are there
                                        baselinks.append((hrefw, parent))  # tuple
                                    else:
                                        nonbaselinks.append((hrefw, parent))  # tuple

        except BaseException as e:
            print('Exception trying: ' + hrefw + str(e))
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    def GET_MANY_LINKS_LARGE(self, locElements, parent):
        remcruft = mu.remcruft
        hrefw= []
        baselinks=[]
        nonbaselinks=[]

        try:
            for webelem in locElements:
                if webelem.tag_name == 'a':
                    print('TYPE OF OBJECT: -----' + str(type(webelem)))

                    if type(webelem) is not 'NoneType':
                        if webelem is not None:
                            hrefw = webelem.get_attribute('href')
                            print('JUST GOT hrefw: -----' + str(hrefw))
                            print('TYPE OF hrefw: -----' + str(type(hrefw)))

                            if type(hrefw) is str:
                                emlen = len(hrefw)
                                badchecks=[hrefw[0:6] == 'javasc', hrefw[0:1] == '/', hrefw[0:7] == 'mailto:', emlen < 7]

                                if remcruft(hrefw, badlist) == 'bad':
                                    0

                                elif any(badchecks):
                                    print('found bad attr: ' + str(hrefw))

                                else:
                                    ans1 = hrefw.find(base1)  ## is the base in there?
                                    ans2 = hrefw.find(base2)  ## is the base in there?

                                    if (ans1 + ans2) > 0:  # if either are there
                                        baselinks.append((hrefw, parent)) # tuple
                                    else:
                                        nonbaselinks.append((hrefw, parent))  # tuple

        except BaseException as e:
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def

    def GET_MORE_LINKS(self, loc_elems=[]):
        homelinks = []
        alienlinks = []
        homelinks2 = []
        alienlinks2 = []

        for each_tuple in loc_elems:
            tchild = each_tuple[0]  # get a page from a link on the home page
            tparent = each_tuple[1]
            driver.get(tchild)
            child_elements = driver.find_elements_by_xpath('.//a')

            try:
                homelinks, alienlinks =  self.GET_MANY_LINKS_LARGE(child_elements, tparent)
                homelinks2 = list(set(homelinks))
                alienlinks2 = list(set(alienlinks))
                                                    # selenium.common.exceptions.UnexpectedAlertPresentException:
            except UnexpectedAlertPresentException:
                logger.debug('ALERT! -- UnexpectedAlertPresentException on: {}'.format(tchild))
                logger('ALERT! -- UnexpectedAlertPresentException on: {}'.format(tchild))
                pass

        return homelinks2, alienlinks2

    #############---------------------------------------- end of def
    # begin:
    def main(self):
        global logger
        logger = mu.setuplogger()
        print_er = mu.print_er
        write_error_file = mu.write_error_file
        write_home_set_to_file = mu.write_home_set_to_file
        makeerrorlist = self.makeerrorlist
        home_00 = []
        alien_00 = []
        parent = address

        global driver
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)
        logger.debug("In main()")

        try:
            logger.info('Getting first address: {}'.format(address))
            driver.get(address)
            home_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
                     ##first time:  HOME PAGE ONLY  ##first time:
            home_00, alien_0  = self.GET_MANY_LINKS_LARGE(home_elements, parent)     # list, str

        except BaseException as e:
            logger.debug('Exception trying main outside loop in run pt1: {}'.format(e.msg))
            logger.debug(str(e), exc_info=True)
            pass

        try:
            logger.info('doing GET_MORE_LINKS next')
                        #2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time

            home_1, alien_1 = self.GET_MORE_LINKS(home_00)
            home_xtras_1 = [item for item in home_1 if item not in home_00]
            home_00 = list(set(home_00 + home_xtras_1))

    # ------------------------------------------------------------------------------------
            home_2, alien_2 = self.GET_MORE_LINKS(home_xtras_1)

            home_xtras_2 = [item for item in home_2 if item not in home_1]

            home_00 = list(set(home_00 + home_xtras_2))

            # ------------------------------------------------------------------------------------

            home_3, alien_3 = self.GET_MORE_LINKS(home_xtras_2)

            home_xtras_3 = [item for item in home_3 if item not in home_00]

            home_00 = list(set(home_00 + home_xtras_3))

        #------------------------------------------------------------------------------------
            home_4, alien_4 = self.GET_MORE_LINKS(home_xtras_3)

            home_xtras_4 = [item for item in home_4 if item not in home_00]

            home_00 = list(set(home_00 + home_xtras_4))

    #------------------------------------------------------------------------------------
            home_5, alien_5 = self.GET_MORE_LINKS(home_xtras_4)

            home_xtras_5 = [item for item in home_5 if item not in home_00]

            home_00 = list(set(home_00 + home_xtras_5))

    # ------------------------------------------------------------------------------------
            home_6, alien_6 = self.GET_MORE_LINKS(home_xtras_5)

            home_xtras_6 = [item for item in home_6 if item not in home_00]

            home_00 = list(set(home_00 + home_xtras_6))

            # ------------------------------------------------------------------------------------
            write_home_set_to_file(home_00, logger)
            home_00_a = list(set(home_00))
            home_00_b = sorted(home_00_a)

            # ------------------------------------------------------------------------------------
            alien_00 = home_00 + alien_1 + alien_2 + alien_3 + alien_4 + alien_5 + alien_6
            alien_00_a = list(set(alien_00))
            alien_00_b = sorted(alien_00_a)
            write_home_set_to_file(alien_00_b, logger)

            logger.info("here")


            home_errs = self.makeerrorlist(home_00_b)  #---makeerrorlist
            alien_errs = self.makeerrorlist(alien_00_b)  #---makeerrorlist

            write_error_file(home_errs, logger)
            write_error_file(alien_errs, logger)

        except BaseException as e:
            print('Exception trying main outside loop in run pt2: ' + str(e))
            logger.debug(str(e),exc_info=True)
            pass

        print(fblack + 'Done')
        driver.close()

    def __init__(self):
        print('Init: ' + __name__)
        global mu
        mu = linkckutil()  # instantiate class which sets up logger, etc.
        self.main()
                                # mu = linkckutil(gdict)  # instantiate class which sets up logger, etc.

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None


LinkCheck()   ## run this file
