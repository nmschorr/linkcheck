# python 3

import src.LinkCheckUtil as lc
# from src.LinkCheckUtil import print_er, logr
# from src.LinkCheckUtil import remcruft
from src.LinkCheck import *
from datetime import datetime
import src.LinkCheckUtil as ut
#import urllib.request
#from urllib.parse import urlparse
from requests import *
from selenium import webdriver

class LinkCheck(object):

    def makeerrorlist(self, locnewlist):
        elink = ''
        errorlist = []
        print(self.makeerrorlist.__name__ + "here is locnewlist: ", locnewlist)
        ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
        tlogname = 'E:\\pylogs\\linkcheckresults' + ts + '.log'
        tlognameHndl = open(tlogname, 'w')  #
        tlognameHndl.write('Error File:' + ut.lnfeed)
        logr = lc.logr

        try:  # check head
            for elinktup in locnewlist:
                
                elink = elinktup[0]
                theparent = elinktup[1]
                tlognameHndl.write('Inside Loop:' + ut.lnfeed)

                resp = str(head(elink, data=None, timeout=30))
                print(ut.black + 'resp: ', resp)
                err_resp = resp[11:14]

                responstr = 'checked: ' + elink + ' -resp: ' + err_resp + ut.lnfeed
                tlognameHndl.write(responstr)

                if int(err_resp) in ut.ercodes:
                    errorString = ut.gerrstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)
                    print(ut.fred + errorString + ut.black)
                    errorlist.append(errorString)
                    tlognameHndl.write(errorString + ut.lnfeed)
                else:
                    print(ut.black + 'status code: ' + err_resp)

        except BaseException as e:
            print('Exception trying: ', elink, str(e))
            logr.debug(str(e), exc_info=True)

            pass

        tlognameHndl.close()
        return errorlist

    #############---------------------------------------- end of def
    @classmethod
    def getthelinks(cls, locElements, parent=''):
        emLINK = None
        baselinks = []
        nonbaselinks = []
        logr = lc.logr
        # print(self.getthelinks().__name__)
        if parent == '':
            parent = ut.base1

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

                    elif lc.remcruft(emLINK, ut.badlist) == 'bad':
                        0

                    elif any([emLINK[0:6] == 'javasc', emLINK[0:1] == '/', emLINK[0:7] == 'mailto:', lenem < 7]):
                        print('found bad attr: ', emLINK)

                    else:
                        answer1 = emLINK.find(ut.base1)  ## is the base in there?
                        answer2 = emLINK.find(ut.base2)  ## is the base in there?

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
            bigerr_h.write(b + ut.lnfeed)
        bigerr_h.close()

    #############---------------------------------------- end of def

    def writefirstset(self, firstSetLinks=None):
        if firstSetLinks is None:
            firstSetLinks = []
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
        if firstSetLinks:  ## if the list isn't empty
            filen1_h = open(basefile, 'w')  #
            for b in firstSetLinks:
                filen1_h.write(b[0] + ut.lnfeed)
            filen1_h.close()

    #############---------------------------------------- end of def
    # begin:
    @classmethod
    def run(cls):
        logr = lc.logr()
        driver = webdriver.Firefox()
        cls.driver = driver
        driver.implicitly_wait(10)
        biglistOne = []
        print("in main section now")
        # gg = LinkCheck()
        logr.debug("yes")
        firstSetLinks = []
        try:
            driver.get(ut.address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            firstSetOfLinks, firstnonbaseLinks = cls.getthelinks(elements)

            cls.writefirstset(firstSetOfLinks)

            base_erlist = cls.makeerrorlist(firstSetOfLinks)  ## check for errors
            print("trying 2nd set")
            firstnonbase_erlist = cls.makeerrorlist(firstnonbaseLinks)  ## check for errors
            cls.print_er(base_erlist)
            cls.print_er(firstnonbase_erlist)

            biglist = cls.linky(driver, firstSetOfLinks, biglistOne)
            print(ut.lnfeed + 'Just did biglist sort ----------------------------------' + ut.lnfeed)
            big_ERR_list = cls.makeerrorlist(biglist)  ####-----------------makeerrorlist---------makeerrorlist--
            big_erlistFinal = list(
                set(base_erlist + big_ERR_list))  ####-----------------makeerrorlist---------makeerrorlist--
            cls.writebig(big_erlistFinal)

        except BaseException as e:
            print('Exception trying main outside loop: ', str(e))
            # logr.fatal(str(e),exc_info=True)

            pass

        print(ut.black + 'Done')

        driver.close()

    def main(self):
        # LinkCheck().run()
        self.run()

    if __name__ == '__main__':
        LinkCheck().run()

# g = LinkCheck()
# LinkCheck().run()
