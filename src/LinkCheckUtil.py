# python 3

from datetime import datetime
#import sys
#from requests import get, head,
import requests
from src.config import *
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, RequestError, NewConnectionError
#import urllib3


class linkckutil(object):

        #############---------------------------------------- end of def
    def restartdrvr(self, drver, logr):
        drver.quit()
        logr.debug('\n-------------->ALERT! quit driver from restartdrvr')
        drver = webdriver.Firefox()
        logr.debug('\n-----------------> Restarted driver from restartdrvr')
        return drver

        #############---------------------------------------- end of def

    @staticmethod
    def check_file_extension(hrefw=''):  # chk for appropriate exts for homelinks only
        html4 = hrefw[-4:]  # html
        htm3 = hrefw[-3:]  # htm
        php = hrefw[-3:]  # htm
        phpx = hrefw[-3:-1]  # phpx
        lastchar = hrefw[-1:]
        if any([html4 == 'html', htm3 == 'htm', lastchar == '/', php == 'php', phpx == 'php']):
            return True
        else:
            return False

        #############---------------------------------------- end of def

    def geterrs(self, home_all_final, alien_all_final, logr, driver):

        logr.info("\n--------------------------------------> Starting geterrs.")
        try:
            logr.info("\n-------------------------------------->Starting geterrs for home_all_final.")
            home_errs = self.make_error_list(home_all_final, logr, driver )  # ---make_error_list
            logr.info("\n-------------------------------------->Starting geterrs for alien_all_final.")
            alien_errs = self.make_error_list(alien_all_final, logr, driver)  # ---make_error_list

            home_errs_b = list(set(home_errs))
            alien_errs_b = list(set(alien_errs))

            self.write_error_file(sorted(home_errs_b), logr, 'home')
            self.write_error_file(sorted(alien_errs_b), logr, 'alien')

        except (UnexpectedAlertPresentException, TimeoutException, BaseException) as e:
            logr.debug(str(e), exc_info=True)
            self.restartdrvr(driver, logr)
            pass
        logr.info("Done with geterrs.")

        #############---------------------------------------- end of def

    @staticmethod
    def make_error_list(locnewlist, loggr, drv):
                                            #http_pm = urllib3.PoolManager()
        loggr.info('\n-------------------------------------->Starting make_errorList.')
        errorlist = []
        myiter = iter(range(len(locnewlist)))
        gerrstr = 'ERROR ---- ! ---Result code: '

        for i in myiter:
            print('iterator in loop: ' + str(i))

            try:
                for elinktup in locnewlist:
                    try:  # check head
                        loggr.info('\n-------------------------------------->Restarting loop in make_error_list with: ' +str(elinktup))
                        elink = elinktup[0]
                        theparent = elinktup[1]
                                                #resp = http_pm.request('HEAD', elink)

                                                # loggr.info('Inside Loop:' + lnfeed)
                        resp = str(requests.head(elink, data=None, timeout=10))
                        mmsg = 'resp: for HEAD from ' + elink + ': ' + str(resp)
                        loggr.info(mmsg)
                        err_resp = str(resp[11:14])
                                                                        #err_resp = str(resp.status)
                        responstr = 'Checked using HEAD only: ' + elink + ' -resp: ' + err_resp + lnfeed
                        loggr.info(responstr)
                        err_int = int(err_resp)
                        if err_int in ercodes:
                            loggr.info('------------------------------!!! > Got an error. Retrying with a GET.' + elink)
                            resp2 = str(requests.get(elink, data=None, timeout=10))

                            #resp2 = http.request('GET', elink)
                            err_resp2 = str(resp2[11:14])
                            responstr2 = '----- Checked using Get only: ' + elink + ' -resp: ' + err_resp2 + lnfeed
                            loggr.debug(responstr2)
                            err_int2 = int(err_resp2)

                            if err_int2 in ercodes:
                                errorString2 = lnfeed + '------------------------------!!! >GET response: {} in: {} from parent: {}'.format(err_resp2, elink, theparent)
                                loggr.info(errorString2)

                                errorlist.append(errorString2)
                                loggr.info(errorString2 + lnfeed)

                            requests.session().close()             #urllib3.connectionpool.HTTPConnectionPool.close()
                        else:
                            loggr.info('status code on second get: ' + err_resp)

                    except (ConnectTimeoutError, MaxRetryError, RequestError, NewConnectionError) as e:
                        print("----------------in new except now!!!------------------------------")
                        loggr.debug(str(e), exc_info=True)
                        requests.session().close()

                    except BaseException as e:
                        print("----------------in Base except now!!!------------------------------")
                        loggr.debug(str(e), exc_info=True)
                        requests.session().close()
                        pass

                    next(myiter, None)

            except BaseException as e:
                print("----------------in OUTER Base except now!!!------------------------------")
                loggr.debug(str(e), exc_info=True)
                next(myiter, None)
                requests.session().close()
                pass

        loggr.info("Done with make_error_list.")
        return errorlist

    #############---------------------------------------- end of def

    @staticmethod
    def remcruft(localink, mlist):
        res = 'good'
        for i in mlist:
            if i in localink:
                res = 'bad'
        #res = list(filter(lambda x: x in locallink, mlist))
        return res   # good or bad for now

    #############---------------------------------------- end of def

    @staticmethod
    def write_home_set_to_file(firstSetLinks, logger, ttype):
        logger.info('In write_home_set_to_file to file.')
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\Links_'+ ttype + timestp + '.txt'
        filen1_h = open(basefile, 'w')  #
        for b in firstSetLinks:
            filen1_h.write(b[0] + lnfeed)
        filen1_h.close()
        logger.info('Done with write_home_set_to_file to file.')

        #############---------------------------------------- end of def

    @staticmethod
    def write_error_file(big_err_list_final, logger, ttype):
        timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
        logger.info('In write_error_file - timenow')
        bigerr_file = 'E:\\pylogs\\ERRORS.' + ttype + timenow + '.log'
        bigerr_h = open(bigerr_file, 'w')  #
        for b in big_err_list_final:
            bigerr_h.write(b + lnfeed)
        bigerr_h.close()
        logger.info('Done with write_error_file - timenow')

    #############---------------------------------------- end of def

    def __init__(self):
        print("In linkckutil super() __init__")
