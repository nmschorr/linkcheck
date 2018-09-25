
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


def set_site(site):
    prod.update({rst: site})
def get_site():
    return prod.get(rst)

def set_just_name(just_name):
    prod.update({rjn: just_name})
def get_just_name():
    return prod.get(rjn)

def set_just_stat(just_stat):
    prod.update({rjs: just_stat})
def get_just_stat():
    return prod.get(rjs)

def set_donefile(donefile):
    prod.update({rdf: donefile})
def get_donefile():
    return prod.get(rdf)

def set_file_path(file_path):
    prod.update({rfp: file_path})
def get_file_path():
    return prod.get(rfp)

def set_donefile_path(donefile_path):
    prod.update({rdp: donefile_path})
def get_donefile_path():
    return prod.get(rdp)

def set_timestp(timestp):
    prod.update({rts: timestp})
def get_timestp():
    return prod.get(rts)
