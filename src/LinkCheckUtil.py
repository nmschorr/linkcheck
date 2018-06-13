# python 3

import sys
from requests import *
from selenium import webdriver
from datetime import datetime
from src.config import *


#############---------------------------------------- end of def

def remcruft(this, localink, mlist):
    res = 'good'
    for i in mlist:
        if i in localink:
            res = 'bad'
    #res = list(filter(lambda x: x in locallink, mlist))
    return res   # good or bad for now


def print_er(e):
    for er2 in e:
        print('error: ', er2)


#
#     #############---------------------------------------- end of def
#
#
#     #############---------------------------------------- end of def
#     def makeerrorlist(this,locnewlist):
#         print(this.makeerrorlist.__name__ + "here is locnewlist: ", locnewlist)
#         errorlist = []
#         ercodes = [400, 404, 408, 409, 501, 502, 503]
#         ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
#         tlogname = 'E:\\pylogs\\linkcheckresults' + ts + '.log'
#         tlognameHndl = open(tlogname, 'w')  #
#         tlognameHndl.write('Error File:' + lnfeed)
#
#         try:  # check head
#             for elinktup in locnewlist:
#                 elink = elinktup[0]
#                 theparent = elinktup[1]
#                 tlognameHndl.write('Inside Loop:' + lnfeed)
#
#                 resp = str(head(elink, data=None, timeout=4))
#                 print(Fore.BLACK + 'resp: ', resp)
#                 err_resp = resp[11:14]
#
#                 responstr = 'checked: '+ elink + ' -resp: ' + err_resp + lnfeed
#                 tlognameHndl.write(responstr)
#
#                 if int(err_resp) in ercodes:
#                     errstr = 'ERROR ---- ! ---Result code: '
#                     errorString = errstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)
#                     print(Fore.RED + errorString)
#                     errorlist.append(errorString)
#                     tlognameHndl.write(errorString +lnfeed )
#                 else:
#                     print(Fore.BLACK + 'status code: ' + err_resp)
#
#         except BaseException as e:
#             print('Exception trying: ', stringi, str(e))
#             pass
#
#         tlognameHndl.close()
#         return errorlist
#
#
#     #############---------------------------------------- end of def
#
#     def getthelinks(this, webElementsLoc, parent = None):
#         print(this.getthelinks().__name__)
#         emLINK = None
#         baselinks = []
#         nonbaselinks = []
#         badlist = ['#','com/#', '?', 'blogger.com', '/search', 'javascript:void(0)', 'widgetType','mailto:']
#
#         if parent == None:
#             parent = base1
#
#         try:
#             for webElems in webElementsLoc:
#                 emLINK = None
#                 if webElems.tag_name == 'a':
#                     emLINK = webElems.get_attribute('href')
#
#                     if any([type(emLINK) == 'NoneType' or emLINK == None]):
#                         print('Found none type')
#
#                     elif this.remcruft(emLINK, badlist) == 'bad': 0
#
#                     elif any([emLINK[0:6] == 'javasc', emLINK[0:1] == '/', emLINK[0:7] == 'mailto:', len(emLINK)< 7]):
#                         print('found bad attr: ', emLINK)
#
#                     else:
#                         answer1 = emLINK.find(base1)  ## is the base in there?
#                         answer2 = emLINK.find(base2) ## is the base in there?
#
#                         if answer1 > 0 or answer2 > 0:  # if either are there
#                             baselinks.append((emLINK,parent))
#                         else:
#                             nonbaselinks.append((emLINK,parent))
#
#         except BaseException as e:
#             print('Exception trying: ', emLINK, str(e))
#             pass
#
#         nonbaselinksSorted = list(set(nonbaselinks))  ## sort and delete dupes
#
#         baselinksSort= list(set(baselinks))
#         baselinksSorted= sorted(baselinksSort)
#
#         return baselinksSorted, nonbaselinksSorted
#
#     #############---------------------------------------- end of def
#     def linky(this, firstSetLinks, biglistnew):
#         nnbseLinks = []
#         for first_links in firstSetLinks:
#             nnbseLinks = []
#             placeholder = []
#             this.driver.get(first_links[0])  # get a page from a link on the home page
#             placeholder, nnbseLinks = this.getthelinks(this.driver.find_elements_by_xpath('.//a'), parent=first_links)  ## for each link on homepage
#             biglistloc = list(set(biglistnew + nnbseLinks))
#         return sorted(biglistloc)
#
#     #############---------------------------------------- end of def
#     def writefe(this, big_ERR_listFinal):
#         timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
#         bigerr_file = 'E:\\pylogs\\BigErrs' + timenow + '.txt'
#         bigerr_h = open(bigerr_file, 'w')  #
#         for b in big_ERR_listFinal:
#             bigerr_h.write(b + lnfeed)
#         bigerr_h.close()
#     #############---------------------------------------- end of def
#
#     def print_er(this,e):
#         for er2 in e: print('error: ', er2)
#
#     #############---------------------------------------- end of def
#
#     def writefirstset(this, firstSetLinks):
#         timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
#         basefile = 'E:\\pylogs\\BaseLinks' + timestp + '.txt'
#         if firstSetLinks:     ## if the list isn't empty
#             filen1_h = open(basefile, 'w')  #
#             for b in firstSetLinks:
#                 filen1_h.write(b[0] + lnfeed)
#             filen1_h.close()
#
#     #############---------------------------------------- end of def
#     # begin:
#
#     def rungets(self):
#         driver = webdriver.Firefox()
#         driver.implicitly_wait(10)
#         base_erlist =[]
#         firstSetOfLinks = None
#         print("in main section now")
#         biglistOne = []
#         try:
#             driver.get(address)
#             elements = driver.find_elements_by_xpath('.//a')  # elements = driver.find_elements_by_tag_name('a')
#             firstSetOfLinks, firstnonbaseLinks = getthelinks(elements, parent = None )
#
#             writefirstset(firstSetOfLinks)
#
#             base_erlist = this.makeerrorlist(firstSetOfLinks)  ## check for errors
#             firstnonbase_erlist = this.makeerrorlist(firstnonbaseLinks)  ## check for errors
#             this.print_er(base_erlist)
#             this.print_er(firstnonbase_erlist)
#
#             biglist = this.linky(firstSetOfLinks, biglistOne)
#             print(lnfeed + 'Just did biglist sort ----------------------------------' + lnfeed)
#             big_ERR_list = this.makeerrorlist(biglist)  ####-----------------makeerrorlist---------makeerrorlist--
#             big_erlistFinal = list(set(base_erlist + big_ERR_list))  ####-----------------makeerrorlist---------makeerrorlist--
#             this.writefe(big_erlistFinal)
#
#         except BaseException as e:
#             print('Exception trying outside loop: ', str(e))
#             pass
#
#         print(Fore.BLACK + 'Done')
#
#         driver.close()
#
#     def main(self):
#         self.rungets()
#
#     if __name__ == '__main__':
#         print()
#
#
# g = LinkCheck().rungets()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
