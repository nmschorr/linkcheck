
import random

class ProfConf(object):
    def __init__(self):

        site = "empty"
        just_name = "empty"
        just_stat = "empty"
        donefile_path = "empty"
        donefile = "empty"
        file_path = "empty"
        timestp = "empty"

        prod_dict = dict()
        self.prod_dict = prod_dict
        rand = random.random()

        rst = "rst" + str(rand)
        rjn =  "rjn" + str(rand)
        rjs =  "rjs" + str(rand)
        rdp =  "rdp" + str(rand)
        rfp =  "rfp" + str(rand)
        rdf =  "rdf" + str(rand)
        rts =  "rts" + str(rand)
        self.rjn = rjn
        self.rst = rst
        self.rjs = rjs
        self.rdp = rdp
        self.rdf = rdf
        self.rts = rts
        self.rfp = rfp

        prod_dict.update({rst:site})
        prod_dict.update({rjn:just_name})
        prod_dict.update({rjs:just_stat})
        prod_dict.update({rdp:donefile_path})
        prod_dict.update({rdf:donefile})
        prod_dict.update({rfp:file_path})
        prod_dict.update({rts:timestp})
    
    
    def set_site(self, site_a):
        self.prod_dict.update({self.rst: site_a})
        
    def get_site(self,):
        return self.prod_dict.get(self.rst)
    
    def set_just_name(self,just_name_a):
        self.prod_dict.update({self.rjn: just_name_a})
    def get_just_name(self):
        return self.prod_dict.get(self.rjn)
    
    def set_just_stat(self,just_stat_a):
        self.prod_dict.update({self.rjs: just_stat_a})
    def get_just_stat(self):
        return self.prod_dict.get(self.rjs)
    
    def set_donefile(self,done_file):
        self.prod_dict.update({self.rdf: done_file})
    def get_donefile(self):
        return self.prod_dict.get(self.rdf)
    
    def set_file_path(self,fpath):
        self.prod_dict.update({self.rfp: fpath})
    def get_file_path(self):
        return self.prod_dict.get(self.rfp)
    
    def set_donefile_path(self, dfpath):
        self.prod_dict.update({self.rdp: dfpath})
    def get_donefile_path(self):
        return self.prod_dict.get(self.rdp)
    
    def set_timestp(self,time_st):
        self.prod_dict.update({self.rts: time_st})
    def get_timestp(self):
        return self.prod_dict.get(self.rts)
    
    def prod_reset(self):
        self.prod_dict.update({self.rjs: 'na'})
        self.prod_dict.update({self.rdf: 'na'})
        self.prod_dict.update({self.rfp: 'na'})
        self.prod_dict.update({self.rdp: 'na'})
        self.prod_dict.update({self.rts: 'na'})
        self.prod_dict.update({self.rst: 'na'})
        self.prod_dict.update({self.rjn: 'na'})
