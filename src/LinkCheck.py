# python 3

from datetime import datetime
from requests import *
from selenium import webdriver
from src.config import *
from src import LinkCheckUtil


class LinkCheck(object):

    def makeerrorlist(self, locnewlist, u):
        logger = u._ulogger
        print('newisides: ', locnewlist)
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
    def getthelinks(self, locElements, parent=firstparent, u = 0):
        logger = u._ulogger
        remcruft = u.remcruft
        emlink = ''
        baselinks = []
        nonbaselinks = []
        keepgoing = True

        try:
            for webelem in locElements:
                keepgoing = True
                if webelem.tag_name == 'a':
                    if type(webelem) == 'NoneType' or webelem is None:
                        print('Found none type')
                        keepgoing = False

                    else:
                        emlink = webelem.get_attribute('href')
                        emlen = len(emlink)
                        bd=[emlink[0:6] == 'javasc', emlink[0:1] == '/', emlink[0:7] == 'mailto:', emlen < 7]
                        keepgoing = False

                if keepgoing == True:

                    if remcruft(emlink, badlist) == 'bad': 0

                    elif any(bd):
                        print('found bad attr: ', emlink)

                    else:
                        ans1 = emlink.find(base1)  ## is the base in there?
                        ans2 = emlink.find(base2)  ## is the base in there?

                        if (ans1 + ans2) > 0:  # if either are there
                            baselinks.append((emlink, parent))
                        else:
                            nonbaselinks.append((emlink, parent))

        except BaseException as e:
            print('Exception trying: ', emlink, str(e))
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    # begin:
    def main(self, u):
        logger = u._logger
        print_er = u.print_er
        writebig = u.writebig
        writefirstset_tofile = u.writefirstset_tofile
        makeerrorlist = self.makeerrorlist
        linky = u.linky
        driver = webdriver.Firefox()
        self.driver = driver
        driver.implicitly_wait(10)

         
        print("in main section now")
        logger.debug("In run")
        first_base_links = []
        first_nonbase_links = []
        first_nonbase_errs = []
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            first_base_links, first_nonbase_links = self.getthelinks(elements, firstparent, u)

            writefirstset_tofile(first_base_links)  # first simple file

            base_erlist = makeerrorlist(first_base_links, u)  ## on first simple file only
            print_er(base_erlist)

            print("trying 2nd set")

        except BaseException as e:
            print('Exception trying main outside loop in run pt1: ', str(e))
            logger.debug(str(e), exc_info=True)
        pass

        try:
            first_nonbase_errs = self.makeerrorlist(first_nonbase_links, u)  ## check for errors
            print_er(first_nonbase_errs)

            biglist_of_links = linky(driver, first_base_links, first_nonbase_links)
            lmsg = 'Just did biglist sort ----------------------------------'
            print(lnfeed + lmsg + lnfeed)

            biglist_of_errs = self.makeerrorlist(biglist_of_links, u)  #---makeerrorlist
            big_err_list_final = list(
                set(first_nonbase_errs + biglist_of_errs))  ####-----------------makeerrorlist---------makeerrorlist--
            writebig(big_err_list_final)

        except BaseException as e:
            print('Exception trying main outside loop in run pt2: ', str(e))
            logger.debug(str(e),exc_info=True)
            pass

        print(fblack + 'Done')

        driver.close()

    def __init__(self):
        print(__name__)
        u = LinkCheckUtil()  # instantiate class which sets up logger
        self.u = u
        self.main(u)

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    print(__name__)


LinkCheck()   ## run this file
