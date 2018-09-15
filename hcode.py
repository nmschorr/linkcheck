from os import path
from datetime import datetime
from socket import gethostname, gethostbyaddr

bothp = '<p></p>'
mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"

def hc(gsite, hostnamenow):
    print("inside hc. ")
    outst1 = "<!DOCTYPE html><html><head><title>No Broken Links</title></head><body>"
    answer2 =  "No broken links found for " + gsite +". Thanks for using LinkCheck."
    linebreaks3 = "<p></p><p></p>"
    homeURL4 = "<a href=http://" + hostnamenow + ">Start Over</a>"
    endb5 = "</body></html>"

    newstt = outst1 + answer2 + linebreaks3 + homeURL4 + endb5
    return newstt

def datalines(f,data, bothp):
    spaces = "&ensp;"  #two spaces
    mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"
    for line in data:
        f.write(str(line[0]))
        f.write(spaces)
        f.write(str(line[1]))
        f.write("<br>" + mtab + "  FOUND ON: ")

        f.write("<a href='")
        f.write(str(line[2]))
        f.write("'>")
        f.write(str(line[2]))
        f.write("</a>")
        f.write(bothp)

def not_redy_msg(site):
    notred = "Results not ready yet. You entered: " + site + \
             " Page will automatically reload until they appear. &nbsp;&nbsp;"
    reload = "<a href=" + "javascript:location.reload(true)" + ">Refresh this page</a>"
    scr = "<script>function pageloadEvery(w_thread) {setTimeout('location.reload(true)', w_thread);}</script>"
    headr = "<!DOCTYPE html><html><head>" + scr + "<title>Not Ready</title></head>"
    bodreload = "<body onload=javascript:pageloadEvery(10000);>"
    newst = headr + bodreload + notred + reload  + "</body></html>"
    return newst

def getfns(p):
    timestp = format(datetime.now(), '%Y%m%d%H%M%S')
    just_name = "res" + timestp + ".html"
    justandstatic = path.join("static", just_name)
    gfulldir = path.join(p, "static")
    fnfull = path.join(gfulldir, just_name)
    return just_name, justandstatic, fnfull

def gethostinfo():
    if gethostname().find('.') >= 0:
        namesock = gethostname()
    else:
        namesock = gethostbyaddr(gethostname())[0]
    return namesock


def writeres(data=[]):
    global fnfull,  bothp
    f = open(fnfull, "w")
    f.write(bothp)
    datalines(f,data,bothp)
    f.close() # file is not immediately deleted because we
    print("fnfull named: ", fnfull , "f.name: ", f.name)
    return