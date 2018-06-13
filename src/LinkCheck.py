# python 3

import sys
from requests import *
from selenium import webdriver
from datetime import datetime
from src.config import *
from src.LinkCheckUtil import remcruft, print_er
from src.LinkCheck import *
import logging
import logging.handlers

class LinkCheck(object):
    def logr(self):
        logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logr = logging.getLogger('logr')
        formatter = logging.Formatter(
            '%(asctime)s-%(name)s-%(levelname)s: Message: %(message)s: Function: %(funcName)s',
            datefmt='%m%d%y-%H.%M%S')
        filehandle = logging.FileHandler(finame)
        filehandle.setFormatter(formatter)
        filehandle.setLevel(level=logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level=logging.DEBUG)

        logr.setLevel(level=logging.DEBUG)
        logr.addHandler(filehandle)
        logr.addHandler(console)
        logging.getLogger('').addHandler(console)  # add to root
        logr.info('Completed configuring logger ')
        lev = logging.getLogger().getEffectiveLevel()
        print("\nLogging level is: ", lev)
        return logr

    def makeerrorlist(this,locnewlist):
        print(this.makeerrorlist.__name__ + "here is locnewlist: ", locnewlist)
        #ercodes = [400, 404, 408, 409, 501, 502, 503]
        ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
        tlogname = 'E:\\pylogs\\linkcheckresults' + ts + '.log'
        tlognameHndl = open(tlogname, 'w')  #
        tlognameHndl.write('Error File:' + lnfeed)

        try:  # check head
            for elinktup in locnewlist:
                elink = elinktup[0]
                theparent = elinktup[1]
                tlognameHndl.write('Inside Loop:' + lnfeed)

                resp = str(head(elink, data=None, timeout=4))
                print(Fore.BLACK + 'resp: ', resp)
                err_resp = resp[11:14]

                responstr = 'checked: '+ elink + ' -resp: ' + err_resp + lnfeed
                tlognameHndl.write(responstr)

                if int(err_resp) in ercodes:
                    errstr = 'ERROR ---- ! ---Result code: '
                    errorString = errstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)
                    print(fred + errorString + fblack)
                    errorlist.append(errorString)
                    tlognameHndl.write(errorString +lnfeed )
                else:
                    print(fblack + 'status code: ' + err_resp)

        except BaseException as e:
            print('Exception trying: ', stringi, str(e))
            this.logr.fatal(str(e),exc_info=True)

            pass

        tlognameHndl.close()
        return errorlist


    #############---------------------------------------- end of def
    @classmethod
    def getthelinks(this, locElements, parent=''):
        #print(this.getthelinks().__name__)
        if parent == '':
            parent = base1

        try:
            for webElems in locElements:
                emLINK = None
                if webElems.tag_name == 'a':
                    emLINK = webElems.get_attribute('href')

                    if any([type(emLINK) == 'NoneType' or emLINK == None]):
                        print('Found none type')

                    elif remcruft(this, emLINK, badlist) == 'bad': 0

                    elif any([emLINK[0:6] == 'javasc', emLINK[0:1] == '/', emLINK[0:7] == 'mailto:', len(emLINK)< 7]):
                        print('found bad attr: ', emLINK)

                    else:
                        answer1 = emLINK.find(base1)  ## is the base in there?
                        answer2 = emLINK.find(base2) ## is the base in there?

                        if answer1 > 0 or answer2 > 0:  # if either are there
                            baselinks.append((emLINK,parent))
                        else:
                            nonbaselinks.append((emLINK,parent))

        except BaseException as e:
            print('Exception trying: ', emLINK, str(e))
            this.logr.fatal(str(e),exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort= list(set(baselinks))
        baselinksSorted= sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def
    def linky(this, firstSetLinks, biglistnew):
        for first_links in firstSetLinks:
            nnbseLinks = []
            placeholder = []
            this.driver.get(first_links[0])  # get a page from a link on the home page
            placeholder, nnbseLinks = this.getthelinks(this.driver.find_elements_by_xpath('.//a'), parent=first_links)  ## for each link on homepage
            biglistloc = list(set(biglistnew + nnbseLinks))
        return sorted(biglistloc)

    #############---------------------------------------- end of def
    def writefe(this, big_ERR_listFinal):
        timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
        bigerr_file = 'E:\\pylogs\\BigErrs' + timenow + '.txt'
        bigerr_h = open(bigerr_file, 'w')  #
        for b in big_ERR_listFinal:
            bigerr_h.write(b + lnfeed)
        bigerr_h.close()


    #############---------------------------------------- end of def

    def writefirstset(this, firstSetLinks):
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
        if firstSetLinks:     ## if the list isn't empty
            filen1_h = open(basefile, 'w')  #
            for b in firstSetLinks:
                filen1_h.write(b[0] + lnfeed)
            filen1_h.close()

    #############---------------------------------------- end of def
    # begin:
    @classmethod
    def mainset(self, v):
        mylog = LinkCheck.logr(self)
        driver = webdriver.Firefox()
        v.driver = driver
        driver.implicitly_wait(10)
        elements = []
        print("in main section now")
        #gg = LinkCheck()
        try:
            driver.get(address)
            elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

            firstSetOfLinks, firstnonbaseLinks =  v.getthelinks(elements)

            v.writefirstset(firstSetOfLinks)

            base_erlist = v.makeerrorlist(firstSetOfLinks)  ## check for errors
            firstnonbase_erlist = v.makeerrorlist(firstnonbaseLinks)  ## check for errors
            print_er(base_erlist)
            print_er(firstnonbase_erlist)

            biglist = v.linky(firstSetOfLinks, biglistOne)
            print(lnfeed + 'Just did biglist sort ----------------------------------' + lnfeed)
            big_ERR_list = v.makeerrorlist(biglist)  ####-----------------makeerrorlist---------makeerrorlist--
            big_erlistFinal = list(set(base_erlist + big_ERR_list))  ####-----------------makeerrorlist---------makeerrorlist--
            v.writefe(big_erlistFinal)

        except BaseException as e:
            print('Exception trying main outside loop: ', str(e))
            #logr.fatal(str(e),exc_info=True)

            pass

        print(fblack + 'Done')

        driver.close()

    def main(self):
        print("in main")
        v = LinkCheck()
        v.mainset(v)

    if __name__ == '__main__':
        g = main(g)


g = LinkCheck()
g.main()















