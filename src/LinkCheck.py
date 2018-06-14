# python 3

import src.LinkCheckUtil as u
import sys
# from src.LinkCheckUtil import print_er, logger
# from src.LinkCheckUtil import remcruft
#####from src.LinkCheck import *
from datetime import datetime
#import urllib.request
#from urllib.parse import urlparse
from requests import *
from selenium import webdriver
from src.config import *
import logging




class LinkCheck(object):
    def makeerrorlist(self, locnewlist=0):
        print('newisides: ', locnewlist)
        elink = ''
        errorlist = []
        logger = logging.getLogger('__main__')

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

    #############---------------------------------------- end of def
    def getthelinks(self, locElements, parent=''):
        emLINK = None
        baselinks = []
        nonbaselinks = []
        if parent == '':
            parent = base1
        logger = logging.getLogger('__main__')

        try:
            for webElems in locElements:
                emLINK = ''
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
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    def linky(self, driver2, firstSetLinks, biglistnew):
        biglistloc = []
        for first_links in firstSetLinks:
            driver2.get(first_links[0])  # get a page from a link on the home page
            placeholder, nnbseLinks = self.getthelinks(self.driver.find_elements_by_xpath('.//a'),
                                                       parent=first_links)  ## for each link on homepage
            biglistloc = list(set(biglistnew + nnbseLinks))
        return sorted(biglistloc)


    #############---------------------------------------- end of def
    # begin:
    def run(self):
        logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        print(__name__)
        logger = logging.getLogger(__name__)
        formatter = logging.Formatter(
            '%(asctime)s-%(name)s-%(levelname)s: Message: %(message)s: Function: %(funcName)s',
            datefmt='%m%d%y-%H.%M%S')
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        fname = 'E:\\pylogs\\Logger-' + timestp + '.log'
        filehandle = logging.FileHandler(fname)
        filehandle.setFormatter(formatter)
        filehandle.setLevel(level=logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        #console.setFormatter(formatter)
        #console.setLevel(level=logging.DEBUG)

        logger.setLevel(level=logging.DEBUG)
        logger.addHandler(filehandle)
        #logger.addHandler(console)
        logging.getLogger('').addHandler(console)  # add to root
        logger.info('Completed configuring logger')
        lev = logging.getLogger().getEffectiveLevel()
        print("\nLogging level is: ", lev)


        driver = webdriver.Firefox()
        self.driver = driver
        driver.implicitly_wait(10)
        biglist_of_links = []
        biglist_of_errs = []
        print("in main section now")
        logger.debug("In run")
        self.first_base_links = []
        first_nonbase_links = []
        self.first_nonbase_errs = []
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            first_base_links, first_nonbase_links = self.getthelinks(elements)

            u.writefirstset_tofile(first_base_links)

            base_erlist = self.makeerrorlist(self.first_base_links)  ## check for errors
            u.print_er(base_erlist)

            print("trying 2nd set")

            first_nonbase_errs = self.makeerrorlist(first_nonbase_links)  ## check for errors
            u.print_er(first_nonbase_errs)

            biglist_of_links = self.linky(driver, first_base_links, first_nonbase_links)
            lmsg = 'Just did biglist sort ----------------------------------'
            print(lnfeed + lmsg + lnfeed)

            biglist_of_errs = self.makeerrorlist(biglist_of_links)  #---makeerrorlist
            big_err_list_final = list(
                set(first_nonbase_errs + biglist_of_errs))  ####-----------------makeerrorlist---------makeerrorlist--
            u.writebig(big_err_list_final)

        except BaseException as e:
            print('Exception trying main outside loop: ', str(e))
            logger.debug(str(e),exc_info=True)
            pass

        print(fblack + 'Done')

        driver.close()

    def __init__(self):
        None
        #logger = u.logger
        #self.logger = logger

    def main(self):
        # LinkCheck().run()
        self.run()

    #if __name__ == "__main__":
    #    main()

LinkCheck().run()
# LinkCheck().run()
