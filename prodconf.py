
import random

site = "empty"
just_name = "empty"
just_stat = "empty"
donefile_path = "empty"
donefile = "empty"
file_path = "empty"
timestp = "empty"

prod = dict()
rand = random.random()

rst = "rst" + str(rand)
rjn =  "rjn" + str(rand)
rjs =  "rjs" + str(rand)
rdp =  "rdp" + str(rand)
rfp =  "rfp" + str(rand)
rdf =  "rdf" + str(rand)
rts =  "rts" + str(rand)


prod.update({rst:site})
prod.update({rjn:just_name})
prod.update({rjs:just_stat})
prod.update({rdp:donefile_path})
prod.update({rdf:donefile})
prod.update({rfp:file_path})
prod.update({rts:timestp})


def set_site(site_a):
    prod.update({rst: site_a})
def get_site():
    return prod.get(rst)

def set_just_name(just_name_a):
    prod.update({rjn: just_name_a})
def get_just_name():
    return prod.get(rjn)

def set_just_stat(just_stat_a):
    prod.update({rjs: just_stat_a})
def get_just_stat():
    return prod.get(rjs)

def set_donefile(done_file):
    prod.update({rdf: done_file})
def get_donefile():
    return prod.get(rdf)

def set_file_path(fpath):
    prod.update({rfp: fpath})
def get_file_path():
    return prod.get(rfp)

def set_donefile_path(dfpath):
    prod.update({rdp: dfpath})
def get_donefile_path():
    return prod.get(rdp)

def set_timestp(time_st):
    prod.update({rts: time_st})
def get_timestp():
    return prod.get(rts)
