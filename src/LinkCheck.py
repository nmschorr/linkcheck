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
        keepgoing=True
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
            print('Exception trying: '+ str(hrefw) + str(e))
            logger.debug(str(e), exc_info=True)
            pass

        nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes

        baselinksSort = list(set(baselinks))
        baselinksSorted = sorted(baselinksSort)

        return baselinksSorted, nonbaselinksSorted

    #############---------------------------------------- end of def

    def GET_MORE_LINKS(self, loc_elems=[]):
        #third = []
        first = []
        sec = []
        first2 = []
        sec2 = []

        for each_tuple in loc_elems:
            child = each_tuple[0]  # get a page from a link on the home page
            parent = each_tuple[1]
            driver.get(child)
            child_elements = driver.find_elements_by_xpath('.//a')

            try:
            #selenium.common.exceptions.UnexpectedAlertPresentException:
                first, sec =  self.GET_MANY_LINKS_LARGE(child_elements, parent)

                first2 = list(set(first))
                sec2 = list(set(sec))
            except UnexpectedAlertPresentException:
                print('alert')
                pass

        return first2, sec2

    #############---------------------------------------- end of def
    # begin:
    def main(self):
        global logger
        logger = mu.setuplogger()
        print_er = mu.print_er
        writebig = mu.writebig
        write_home_set_to_file = mu.write_home_set_to_file
        makeerrorlist = self.makeerrorlist

        global driver
        driver = webdriver.Firefox()
        driver.implicitly_wait(10)

         
        print("In main() now")
        logger.debug("In main()")
        home_sum_total = []
        first_nonbase_links = []
        #first_nonbase_errs = []
        try:
            driver.get(address)
            parent = address
            homepage_elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')

   ##first time:  HOME PAGE ONLY  ##first time:

            home_sum_total, homepg_foreign_links \
            = self.GET_MANY_LINKS_LARGE(homepage_elements, parent) #list, 1 str

            write_home_set_to_file(home_sum_total)  # first simple file

            base_erlist = makeerrorlist(home_sum_total)  ## on first simple file only
            print_er(base_erlist)

            print("trying 2nd set")

        except BaseException as e:
            print('Exception trying main outside loop in run pt1: ', str(e))
            logger.debug(str(e), exc_info=True)
        pass

        try:
            first_nonbase_errs = self.makeerrorlist(first_nonbase_links)  ## check for errors
            print_er(first_nonbase_errs)

            print('doing GET_MORE_LINKS next')


#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time#2nd time

            home_1, alien_1 = self.GET_MORE_LINKS(home_sum_total)

    # ------------------------------------------------------------------------------------
            home_2, alien_2 = self.GET_MORE_LINKS(home_1)

            home_xtras_3 = [item for item in home_2 if item not in home_1]

            home_sum_total = list(set(home_sum_total + home_xtras_3))

    #------------------------------------------------------------------------------------
            home_4, alien_4 = self.GET_MORE_LINKS(home_xtras_3)

            home_xtras_4 = [item for item in home_4 if item not in home_sum_total]

            home_sum_total = list(set(home_sum_total + home_xtras_4))

    #------------------------------------------------------------------------------------
            home_5, alien_5 = self.GET_MORE_LINKS(home_xtras_4)

            home_xtras_5 = [item for item in home_5 if item not in home_sum_total]

            home_sum_total = list(set(home_sum_total + home_xtras_5))

    # ------------------------------------------------------------------------------------
            home_6, alien_6 = self.GET_MORE_LINKS(home_xtras_5)

            home_xtras_6 = [item for item in home_6 if item not in home_sum_total]

            home_sum_total = list(set(home_sum_total + home_xtras_6))

            # ------------------------------------------------------------------------------------
            write_home_set_to_file(home_sum_total)


            thi, alien_7 = self.GET_MORE_LINKS(homepg_foreign_links)   ## throw out thi


            lmsg = 'Just did biglist sort ----------------------------------'
            print(lnfeed + lmsg + lnfeed)

            biglist_link_new = home_sum_total + alien_1 + alien_2 + alien_4 + alien_5 + alien_6 + alien_7
            biglist_links = list(set(biglist_link_new))
            biglist_of_errs = self.makeerrorlist(biglist_links)  #---makeerrorlist
            big_err_list_final = list(
                set(first_nonbase_errs + biglist_of_errs))  ####-----------------makeerrorlist---------makeerrorlist--
            writebig(big_err_list_final)

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
