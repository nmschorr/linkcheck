# python 3

from datetime import datetime
from requests import *
from selenium import webdriver
from src.config import *
from src.LinkCheckUtil import linkckutil

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

    #############---------------------------------------- end of def
    def getthelinks(self, locElements, parent):
        remcruft = mu.remcruft
        emlink= [] 
        baselinks=[]
        nonbaselinks=[]
        keepgoing=True
        
        try:
            for webelem in locElements:
                keepgoing = True
                if webelem.tag_name == 'a':
                    if type(webelem) == 'NoneType' or webelem is None:
                        print('Found none type')
                        keepgoing = False

                    else:  # setup for next section
                        emlink = webelem.get_attribute('href')
                        mu.emlen = len(emlink)
                        badchecks=[emlink[0:6] == 'javasc', emlink[0:1] == '/', emlink[0:7] == 'mailto:', mu.emlen < 7]

                if keepgoing == True:

                    if remcruft(emlink, badlist) == 'bad': None

                    elif any(badchecks):
                        print('found bad attr: ', emlink)

                    else:
                        ans1 = emlink.find(base1)  ## is the base in there?
                        ans2 = emlink.find(base2)  ## is the base in there?

                        if (ans1 + ans2) > 0:  # if either are there
                            baselinks.append((emlink, parent)) # tuple
                        else:
                            nonbaselinks.append((emlink, parent))  # tuple

        except BaseException as e:
            print('Exception trying: ', emlink, str(e))
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def

    def linky(self, driver2, firstSetLinks, biglistnew):
        biglistloc = []
        for first_link in firstSetLinks:
            parent = first_link[1]
            driver2.get(first_link[0])  # get a page from a link on the home page
            placeholder, nnbseLinks = \
                self.getthelinks(driver.find_elements_by_xpath('.//a'), parent)  # for each link on homepage
            biglistloc = list(set(biglistnew + nnbseLinks))
        return sorted(biglistloc)

    #############---------------------------------------- end of def
    # begin:
    def main(self):
        global logger
        logger = mu.setuplogger()
        print_er = mu.print_er
        writebig = mu.writebig
        writefirstset_tofile = mu.writefirstset_tofile
        makeerrorlist = self.makeerrorlist

        global driver
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)

         
        print("In main() now")
        logger.debug("In main()")
        first_base_links = []
        first_nonbase_links = []
        #first_nonbase_errs = []
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            first_base_links, first_nonbase_links = self.getthelinks(elements, firstparent)

            writefirstset_tofile(first_base_links)  # first simple file

            base_erlist = makeerrorlist(first_base_links)  ## on first simple file only
            print_er(base_erlist)

            print("trying 2nd set")

        except BaseException as e:
            print('Exception trying main outside loop in run pt1: ', str(e))
            logger.debug(str(e), exc_info=True)
        pass

        try:
            first_nonbase_errs = self.makeerrorlist(first_nonbase_links)  ## check for errors
            print_er(first_nonbase_errs)

            biglist_of_links = self.linky(driver, first_base_links, first_nonbase_links)
            lmsg = 'Just did biglist sort ----------------------------------'
            print(lnfeed + lmsg + lnfeed)

            biglist_of_errs = self.makeerrorlist(biglist_of_links)  #---makeerrorlist
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
        print('Init: ' + __name__)
        global mu
        mu = linkckutil()  # instantiate class which sets up logger, etc.
        self.main()
                                # mu = linkckutil(gdict)  # instantiate class which sets up logger, etc.

if __name__ == "__main__":  ## if loaded and called by something else, go fish
    None


LinkCheck()   ## run this file
