# python 3

from colorama import Fore

# # address = 'http://astrology1234.com'
# # address = 'http://astrologistblog.blogspot.com'
# # thebase = '//astrologistblog.blogspot.com'
# # address = 'http://www.repercussions.com'
# # thebase = '//www.repercussions.com'
# # base1 = 'astrology1234.com'
# # base2 = '//astrologistblog.blogspot'
base1 = 'www.repercussions.com'
base2 = 'repercussions'
#base1 = 'www.clarinetinstitute.com'
#base2 = 'clarinetinstitute'






address ='http://' + base1
erlist = []
errorlist = []
baselinks = []
nonbaselinks = []
nnbseLinks = []
errorString = ''
stringi = ''
resp = ''
elinktup = ''
lnfeed = '\n'
emLINK = None
fred = Fore.RED
fblack = Fore.BLACK
res = 'good'
ercodes = [400, 404, 408, 409, 501, 502, 503]
badlist = ['#','com/#', '?', 'blogger.com', '/search', 'javascript:void(0)', 'widgetType','mailto:']
firstSetOfLinks = None
errstr = 'ERROR ---- ! ---Result code: '
biglistOne = []
finame = 'E:\\pylogs\\finame' + base2 + '-' + '.log'


#ts = format(datetime.now(), '%Y%m%d.%H.%M%S')
#tlogname = 'E:\\pylogs\\lnkchk_' + base2 + '-' + ts + '.log'

# elink = elinktup[0]
# theparent = elinktup[1]
# err_resp = resp[11:14]
# responstr = 'checked: '+ elink + ' -resp: ' + err_resp + lnfeed
# errorString = errstr + '{} in: {} from parent: {}'.format(err_resp, elink, theparent)















