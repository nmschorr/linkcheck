
import random

class ProfConf(object):
    def __init__(self):
        self.prod_dict = dict()
        rand = random.random()
        rnm = str(rand)[2:0]
        self.rjustname =  "rjustname" + rnm
        self.rtimestp =  "rtimestp" + rnm
        self.rsite =  "rsite" + rnm

        self.prod_dict.update({self.rjustname:"empty"})
        self.prod_dict.update({self.rtimestp:"empty"})
        self.prod_dict.update({self.rsite:"empty"})

    def set_rsite(self, sita):
        self.prod_dict.update({self.rsite: sita})
    def get_rsite(self):
        return self.prod_dict.get(self.rsite)
    
    def set_rjustname(self, jname):
        self.prod_dict.update({self.rjustname: jname})
    def get_rjustname(self):
        return self.prod_dict.get(self.rjustname)

    def set_rtimestp(self,time_st):
        self.prod_dict.update({self.rtimestp: time_st})
    def get_rtimestp(self):
        return self.prod_dict.get(self.rtimestp)
    
    def prod_reset(self):
        self.prod_dict.update({self.rtimestp: 'reset'})
        self.prod_dict.update({self.rjustname: 'reset'})
        self.prod_dict.update({self.rsite: 'reset'})
