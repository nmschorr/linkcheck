# python 3

import requests
import logging
from src import home1, home2, lnfeed, ercodes, badlist, start_driver, address, driver
from src import the_logger as logger
from datetime import datetime

from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, RequestError, NewConnectionError
from selenium import webdriver

class linkckutil(object):


        #############---------------------------------------- end of def

    def check_file_extension(self, hrefw=''):  # chk for appropriate exts for homelinks only
        # html4 = hrefw[-4:]  # html  # htm3 = hrefw[-3:]   php = hrefw[-3:]  # htm  # phpx = hrefw[-3:-1]  # phpx
        # if any([html4 == 'html', htm3 == 'htm', lastchar == '/', php == 'php', phpx == 'php']):
        # bad exts: mid, pdf, css, xml,
        return True

        #############---------------------------------------- end of def

    def GET_ERRORS(self, home_all_final):
        #driver = self.driver

        logger.info("\n--------------------------------------> Starting GET_ERRORS.")
        try:
            home_errs = self.make_error_list(home_all_final, logger)  # ---make_error_list

            home_errs_b = list(set(home_errs))
            self.write_error_file(sorted(home_errs_b), 'all')

        except (UnexpectedAlertPresentException, TimeoutException, BaseException) as e:
            logger.debug(str(e), exc_info=True)
            driver.quit()
            self.driver = start_driver()
            pass

        logger.info("Done with GET_ERRORS.")

        #############---------------------------------------- end of def

    def make_error_list(self, locnewlist, drv):
        logger.info('\n-------------------------------------->Starting make_errorList.')
        errorlist = []
        myiter = iter(range(len(locnewlist)))
        gerrstr = 'ERROR ---- ! ---Result code: '
        driver = self.driver

        for i in myiter:
            print('iterator in loop: ' + str(i))

            try:
                for elinktup in locnewlist:
                    try:  # check head
                        logger.info('\n-------------------------------------->Restarting loop in make_error_list with: ' +str(elinktup))
                        elink = elinktup[0]
                        theparent = elinktup[1]

                        resp = str(requests.head(elink, data=None, timeout=10))
                        mmsg = 'resp: for HEAD from ' + elink + ': ' + str(resp)
                        logger.info(mmsg)
                        err_resp = str(resp[11:14])

                        responstr = 'Checked using HEAD only: ' + elink + ' -resp: ' + err_resp + lnfeed
                        logger.info(responstr)
                        err_int = int(err_resp)
                        if err_int in ercodes:
                            logger.info('------------------------------!!! > Got an error. Retrying with a GET.' + elink)
                            resp2 = str(requests.get(elink, data=None, timeout=10))

                            err_resp2 = str(resp2[11:14])
                            responstr2 = '----- Checked using Get only: ' + elink + ' -resp: ' + err_resp2 + lnfeed
                            logger.debug(responstr2)
                            err_int2 = int(err_resp2)

                            if err_int2 in ercodes:
                                errorString2 = lnfeed + '------------------------------!!! >GET response: {} in: {} from parent: {}'.format(err_resp2, elink, theparent)
                                logger.info(errorString2)

                                errorlist.append(errorString2)
                                logger.info(errorString2 + lnfeed)

                            requests.session().close()             #urllib3.connectionpool.HTTPConnectionPool.close()
                        else:
                            logger.info('status code on second get: ' + err_resp)

                    except (ConnectTimeoutError, MaxRetryError, RequestError, NewConnectionError) as e:
                        print("----------------in new except now!!!------------------------------")
                        logger.debug(str(e), exc_info=True)
                        driver.quit()
                        driver = start_driver()

                        #requests.session().close()

                    except BaseException as e:
                        print("----------------in Base except now!!!------------------------------")
                        logger.debug(str(e), exc_info=True)
                        driver.quit()
                        driver = start_driver()

                        #requests.session().close()
                        pass

                    next(myiter, None)

            except BaseException as e:
                print("----------------in OUTER Base except now!!!------------------------------")
                logger.debug(str(e), exc_info=True)
                next(myiter, None)
                requests.session().close()
                pass

        logger.info("Done with make_error_list.")
        return errorlist

    #############---------------------------------------- end of def

    def remcruft(self, localink, mlist):
        res = 'good'
        for i in mlist:
            if i in localink:
                res = 'bad'
        #res = list(filter(lambda x: x in locallink, mlist))
        return res   # good or bad for now

    #############---------------------------------------- end of def

    def wr2f(self, firstSetLinks, ttype):
        
        logger.info('In write_home_set_to_file to file.')
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\Links_'+ ttype + timestp + '.txt'
        filen1_h = open(basefile, 'w')  #
        for b in firstSetLinks:
            filen1_h.write("-> child: " + b[0] + lnfeed + " ----- parent: " + b[1] + lnfeed )
        filen1_h.close()
        logger.info('Done with write_home_set_to_file to file.')

    def write_home_set_to_file(self, firstSetLinks, ttype='none'):
        
        logger.info('In write_home_set_to_file to file.')
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\Links_'+ ttype + timestp + '.txt'
        filen1_h = open(basefile, 'w')  #
        for b in firstSetLinks:
            filen1_h.write(b[0] + lnfeed)
        filen1_h.close()
        logger.info('Done with write_home_set_to_file to file.')

        #############---------------------------------------- end of def

    def write_error_file(self, big_err_list_final, ttype):
        
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
        self.driver = start_driver()
        driver = self.driver

        print("In linkckutil (super()) __init__")
