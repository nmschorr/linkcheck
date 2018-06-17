# python 3

from datetime import datetime
import sys
from requests import *
from src.config import *
from selenium.common.exceptions import UnexpectedAlertPresentException
#from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

    #############---------------------------------------- end of def

class linkckutil(object):

        #############---------------------------------------- end of def

    def geterrs(self, home_all_final, alien_all_final, logr):
        try:
            home_errs = self.make_error_list(home_all_final, logr)  # ---make_error_list
            alien_errs = self.make_error_list(alien_all_final, logr)  # ---make_error_list

            home_errs_b = list(set(home_errs))
            alien_errs_b = list(set(alien_errs))

            self.write_error_file(home_errs_b, logr, 'home')
            self.write_error_file(alien_errs_b, logr, 'alien')

        except (UnexpectedAlertPresentException, TimeoutException, BaseException) as e:
            logr.debug(str(e), exc_info=True)
            pass


        #############---------------------------------------- end of def

    def make_error_list(self, locnewlist, loggr):
        loggr.info('Starting make_errorList ')
        errorlist = []

        try:  # check head
            for elinktup in locnewlist:
                elink = elinktup[0]
                theparent = elinktup[1]
                # loggr.info('Inside Loop:' + lnfeed)
                resp = str(head(elink, data=None, timeout=30))
                # loggr.info('resp: ' + resp)
                err_resp = resp[11:14]
                responstr = 'checked: ' + elink + ' -resp: ' + err_resp + lnfeed
                loggr.info(responstr)

                if int(err_resp) in ercodes:
                    errorString = gerrstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)
                    loggr.info(errorString)
                    errorlist.append(errorString)
                    loggr.info(errorString + lnfeed)
                else:
                    loggr.info('status code: ' + err_resp)

        except BaseException as e:
            loggr.debug('Exception in: ')
            loggr.debug(str(e), exc_info=True)
            pass

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


    def write_home_set_to_file(self, firstSetLinks, logger, ttype):
        logger.info('In write_home_set_to_file to file.')
        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
        basefile = 'E:\\pylogs\\Links_'+ ttype + timestp + '.txt'
        filen1_h = open(basefile, 'w')  #
        for b in firstSetLinks:
            filen1_h.write(b[0] + lnfeed)
        filen1_h.close()
        logger.info('Done with write_home_set_to_file to file.')

        #############---------------------------------------- end of def

    def write_error_file(self, big_err_list_final, logger, ttype):
        timenow = format(datetime.now(), '%Y%m%d.%H.%M%S')
        logger.info('In write_error_file - timenow')
        bigerr_file = 'E:\\pylogs\\ERRORS.' + ttype + timenow + '.log'
        bigerr_h = open(bigerr_file, 'w')  #
        for b in big_err_list_final:
            bigerr_h.write(b + lnfeed)
        bigerr_h.close()
        logger.info('Done with write_error_file - timenow')


    #############---------------------------------------- end of def
    def setuplogger(self):

        timestp = format(datetime.now(), '%Y%m%d.%H.%M%S')
            #logging.basicConfig(format='\n%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logger1 = logging.getLogger('mainlogger')

        formatter = logging.Formatter('%(asctime)s-%(levelname)s: Msg: %(message)s: Function: %(funcName)s',
                                      datefmt='%m%d%y-%H.%M%S')
        fname = 'E:\\pylogs\\Logger-' + timestp + '.log'
        filehandle = logging.FileHandler(fname)
        filehandle.setFormatter(formatter)
        filehandle.setLevel(level=logging.DEBUG)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level=logging.DEBUG)

        logger1.setLevel(level=logging.DEBUG)
        logger1.addHandler(filehandle)
        logger1.addHandler(console)
                                                ##logging.getLogger('').addHandler(console)  # add to root

        lev = logging.getLogger().getEffectiveLevel()
        logger1.info('Completed configuring logger. Logging level is: '+ str(lev))
        return logger1

    def __init__(self):
        None
        #self.__dict__.update(adict)   #globals





