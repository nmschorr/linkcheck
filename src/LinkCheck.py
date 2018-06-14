# python 3

import src.LinkCheckUtil as u
# from src.LinkCheckUtil import print_er, logr
# from src.LinkCheckUtil import remcruft
#####from src.LinkCheck import *
from datetime import datetime
#import urllib.request
#from urllib.parse import urlparse
from requests import *
from selenium import webdriver
from src.config import *

class LinkCheck(object):

    def makeerrorlist(self, locnewlist=[()]):
        print('newisides: ', locnewlist)
        elink = ''
        errorlist = []

        ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
        tlogname = 'E:\\pylogs\\linkcheckresults' + ts + '.log'
        tlognameHndl = open(tlogname, 'w')  #
        tlognameHndl.write('Error File:' + lnfeed)
        logr = lc.logr

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
            logr.debug(str(e), exc_info=True)
            pass

        tlognameHndl.close()
        return errorlist

    #############---------------------------------------- end of def
    @classmethod
    def getthelinks(self, locElements, parent=''):
        emLINK = None
        baselinks = []
        nonbaselinks = []
        logr = u.logr
        # print(self.getthelinks().__name__)
        if parent == '':
            parent = base1

        try:
            for webElems in locElements:
                emLINK = None
                if webElems.tag_name == 'a':
                    emLINK = webElems.get_attribute('href')
                    lenem = len(emLINK)
                    if not lenem > 0:
                        print("problem with len of link")

                    if any([type(emLINK) == 'NoneType' or emLINK is None]):
                        print('Found none type')

                    elif u.remcruft(emLINK, badlist) == 'bad':
                        0

                    elif any([emLINK[0:6] == 'javasc', emLINK[0:1] == '/', emLINK[0:7] == 'mailto:', lenem < 7]):
                        print('found bad attr: ', emLINK)

                    else:
                        answer1 = emLINK.find(base1)  ## is the base in there?
                        answer2 = emLINK.find(base2)  ## is the base in there?

                        if answer1 > 0 or answer2 > 0:  # if either are there
                            baselinks.append((emLINK, parent))
                        else:
                            nonbaselinks.append((emLINK, parent))

        except BaseException as e:
            print('Exception trying: ', emLINK, str(e))
            logr.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    def linky(self, driver2, firstSetLinks, biglistnew):
        for first_links in firstSetLinks:
            driver2.get(first_links[0])  # get a page from a link on the home page
            placeholder, nnbseLinks = self.getthelinks(self.driver.find_elements_by_xpath('.//a'),
                                                       parent=first_links)  ## for each link on homepage
            biglistloc = list(set(biglistnew + nnbseLinks))
        return sorted(biglistloc)

    #############---------------------------------------- end of def
    def writebig(self, big_ERR_listFinal):
        print("inside writebig")
        timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
        bigerr_file = 'E:\\pylogs\\BIGerrs' + timenow + '.txt'
        bigerr_h = open(bigerr_file, 'w')  #
        for b in big_ERR_listFinal:
            bigerr_h.write(b + lnfeed)
        bigerr_h.close()

    #############---------------------------------------- end of def

    def writefirstset_tofile(self, firstSetLinks=[]):
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
        if firstSetLinks:  ## if the list isn't empty
            filen1_h = open(basefile, 'w')  #
            for b in firstSetLinks:
                filen1_h.write(b[0] + lnfeed)
            filen1_h.close()

    #############---------------------------------------- end of def
    # begin:
    def run(self):
        logr = u.logr()
        driver = webdriver.Firefox()
        self.driver = driver
        driver.implicitly_wait(10)
        biglist_of_links = []
        biglist_of_errs = []
        print("in main section now")
        logr.debug("In run")
        first_base_links = []
        first_nonbase_links = [()]
        first_nonbase_errs = []
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            first_base_links, first_nonbase_links = self.getthelinks(elements)

            self.writefirstset_tofile(first_base_links)
            print("this is firstsetoflinks: ", first_base_links)

            base_erlist = self.makeerrorlist(self.first_base_links)  ## check for errors
            self.print_er(base_erlist)

            print("trying 2nd set")

            first_nonbase_errs = self.makeerrorlist(first_nonbase_links)  ## check for errors
            self.print_er(first_nonbase_errs)

            biglist_of_links = self.linky(driver, first_base_links, first_nonbase_links)

            print(lnfeed + 'Just did biglist sort ----------------------------------' + lnfeed)

            biglist_of_errs = self.makeerrorlist(biglist_of_links)  ####-----------------makeerrorlist---------makeerrorlist--
            big_erlistFinal = list(
                set(first_nonbase_errs + biglist_of_errs))  ####-----------------makeerrorlist---------makeerrorlist--
            self.writebig(big_erlistFinal)

        except BaseException as e:
            print('Exception trying main outside loop: ', str(e))
            logr.debug(str(e),exc_info=True)
            pass

        print(fblack + 'Done')

        driver.close()

    def main(self):
        # LinkCheck().run()
        self.run()

    #if __name__ == "__main__":
    #    main()

LinkCheck().run()
# LinkCheck().run()
