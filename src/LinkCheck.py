# python 3

from datetime import datetime
from requests import *
from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil

class LinkCheck(object):

    def makeerrorlist(self, locnewlist, mu):
        logger = self.mlogger
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

    #############---------------------------------------- end of def
    def getthelinks(self, locElements, parent, u):
        logger = self.mlogger
        remcruft = u.remcruft

        try:
            for webelem in locElements:
                u.keepgoing = True
                if webelem.tag_name == 'a':
                    if type(webelem) == 'NoneType' or webelem is None:
                        print('Found none type')
                        u.keepgoing = False

                    else:  # setup for next section
                        u.emlink = webelem.get_attribute('href')
                        u.emlen = len(u.emlink)
                        badchecks=[u.emlink[0:6] == 'javasc', u.emlink[0:1] == '/', u.emlink[0:7] == 'mailto:', u.emlen < 7]

                if u.keepgoing == True:

                    if remcruft(u.emlink, badlist) == 'bad': None

                    elif any(badchecks):
                        print('found bad attr: ', u.emlink)

                    else:
                        ans1 = u.emlink.find(base1)  ## is the base in there?
                        ans2 = u.emlink.find(base2)  ## is the base in there?

                        if (ans1 + ans2) > 0:  # if either are there
                            u.baselinks.append(u.emlink, parent)
                        else:
                            u.nonbaselinks.append(u.emlink, parent)

        except BaseException as e:
            print('Exception trying: ', u.emlink, str(e))
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(u.nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(u.baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    # begin:
    def main(self, mutil):
        print()
        mlogger = mutil.setuplogger()
        self.mlogger = mlogger
        print_er = mutil.print_er
        writebig = mutil.writebig
        writefirstset_tofile = mutil.writefirstset_tofile
        makeerrorlist = self.makeerrorlist
        linky = mutil.linky

        driver = webdriver.Firefox()
        self.driver = driver
        driver.implicitly_wait(10)

         
        print("in main section now")
        mlogger.debug("In main()")
        first_base_links = []
        first_nonbase_links = []
        #first_nonbase_errs = []
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            first_base_links, first_nonbase_links = self.getthelinks(elements, firstparent, mutil)

            writefirstset_tofile(first_base_links)  # first simple file

            base_erlist = makeerrorlist(first_base_links, mutil)  ## on first simple file only
            print_er(base_erlist)

            print("trying 2nd set")

        except BaseException as e:
            print('Exception trying main outside loop in run pt1: ', str(e))
            mlogger.debug(str(e), exc_info=True)
        pass

        try:
            first_nonbase_errs = self.makeerrorlist(first_nonbase_links, mutil)  ## check for errors
            print_er(first_nonbase_errs)

            biglist_of_links = linky(driver, first_base_links, first_nonbase_links)
            lmsg = 'Just did biglist sort ----------------------------------'
            print(lnfeed + lmsg + lnfeed)

            biglist_of_errs = self.makeerrorlist(biglist_of_links, mutil)  #---makeerrorlist
            big_err_list_final = list(
                set(first_nonbase_errs + biglist_of_errs))  ####-----------------makeerrorlist---------makeerrorlist--
            writebig(big_err_list_final)

        except BaseException as e:
            print('Exception trying main outside loop in run pt2: ', str(e))
            mlogger.debug(str(e),exc_info=True)
            pass

        print(fblack + 'Done')
        driver.close()

    def __init__(self):
        print(__name__)
        self.utils = linkckutil(gdict)  # instantiate class which sets up logger, etc.

        self.main(self.utils)

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    print(__name__)


LinkCheck()   ## run this file
