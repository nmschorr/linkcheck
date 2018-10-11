
import random

class ProfConf(object):
    def __init__(self):
        self.prod_dict = dict()
        rand = random.random()
        rnm = str(rand)[2:0]
        self.rst = "rst" + rnm
        self.rjn =  "rjn" + rnm
        self.rfp =  "rfp" + rnm
        self.rts =  "rts" + rnm

        self.prod_dict.update({self.rst:"empty"})
        self.prod_dict.update({self.rjn:"empty"})
        self.prod_dict.update({self.rts:"empty"})
        self.prod_dict.update({self.rfp:"empty"})

    def set_site(self, site_a):
        self.prod_dict.update({self.rst: site_a})
        
    def get_site(self,):
        return self.prod_dict.get(self.rst)
    
    def set_just_name(self,just_name_a):
        self.prod_dict.update({self.rjn: just_name_a})

    def get_just_name(self):
        return self.prod_dict.get(self.rjn)

    def set_file_path(self,fpath):
        self.prod_dict.update({self.rfp: fpath})
    def get_file_path(self):
        return self.prod_dict.get(self.rfp)
    
    def set_timestp(self,time_st):
        self.prod_dict.update({self.rts: time_st})
    def get_timestp(self):
        return self.prod_dict.get(self.rts)
    
    def prod_reset(self):
        self.prod_dict.update({self.rfp: 'reset'})
        self.prod_dict.update({self.rts: 'reset'})
        self.prod_dict.update({self.rst: 'reset'})
        self.prod_dict.update({self.rjn: 'reset'})
