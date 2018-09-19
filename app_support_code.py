from os import path
from datetime import datetime
import app_support_conf

thishost=app_support_conf.thishost
fullpar = '<p></p>'
linebreaks3 = fullpar + fullpar
mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"
endbod = "</body></html>"

class hcode_cls(object):

    def fin_msg(self, asite):
        global endbod,linebreaks3, thishost
        print("inside hc. ")
        outst1 = "<!DOCTYPE html><html><head><title>No Broken Links</title></head><body>"
        answer2 =  "No broken links found for " + asite +". Thanks for using LinkCheck."
        homeURL4 = "<a href=" + thishost + ">Start Over</a>"
        newstt = outst1 + answer2 + linebreaks3 + homeURL4 + endbod
        return newstt

    def datalines(self, f,data):
        global thishost, fullpar, linebreaks3, mtab, endbod
        home_url = mtab + mtab + "<h2><a href=" + thishost + ">Start Over</a></h2><p></p>"

        sm = "http://schorrmedia.com"
        smedia_url = "<h3><a href=" + sm + ">Visit SchorrMedia.com</a>"

        git_url = "<a href=https://github.com/nmschorr/linkcheck>See the code for this on Github</a></h3>"
        spaces = "&ensp;"  #two spaces
        f.write("<!doctype html><html><head></head><body><div style=margin-left:5em;>")

        f.write("<p></p><h3>Here are your broken links:</h3><p></p>")
        for line in data:
            f.write("BAD LINK-->  ")
            f.write("<a href='")
            f.write(str(line[0]))
            f.write("'>")
            f.write(str(line[0]))
            f.write("</a>")
            f.write(spaces)
            f.write("**ERROR-->  ")
            f.write(str(line[1]))  ## the error
            f.write(spaces)
            f.write("<br>" + mtab + "  ***FOUND ON: ")
            f.write("<a href='")
            f.write(str(line[2]))
            f.write("'>")
            f.write(str(line[2]))
            f.write("</a>")
            f.write(fullpar)

        f.write(linebreaks3)
        f.write(home_url)
        f.write(mtab)
        f.write(smedia_url)
        f.write(mtab)
        f.write(git_url)
        f.write("</div>" + endbod )


    def not_ready_msg(self, gsite):
        global endbod, fullpar
        usr_msg3 = "Results not ready yet."+ fullpar +"You entered: " + gsite + fullpar + \
                 "Page will automatically reload until results appear." + fullpar

        arf1 = "<a href="
        jst2 = "javascript:location.reload(true)"
        refresh4 = arf1 + jst2 + ">Refresh this page</a>"

        startdoc1 = "<!DOCTYPE html><html><head>"
        scr_st = "<script>function pageloadEvery(w_thread)"
        scr2 = scr_st + "{setTimeout('location.reload(true)', w_thread);}</script>"
        atitle3 = "<title>Not Ready</title>"

        headr0 = startdoc1 + scr2 + atitle3
        stylee1 = "<style>body {padding-left:10em;}</style></head>"
        bodreload2 = "<body onload=javascript:pageloadEvery(10000);>"
        newst = headr0 + stylee1 + bodreload2 + usr_msg3 + refresh4  + endbod
        return newst

    def getfns(self, apart):

        stat = "static"
        timestp = format(datetime.now(), '%Y%m%d%H%M%S')
        just_name = "res" + timestp + ".html"
        justandstatic = path.join(stat, just_name)
        gfulldir = path.join(apart, stat)
        fnfull = path.join(gfulldir, just_name)
        return just_name, justandstatic, fnfull

    def writeres(self, data, fnfull):
        global fullpar
        f = open(fnfull, "w")
        f.write(fullpar)
        self.datalines(f,data)
        f.close() # file is not immediately deleted because we
        print("fnfull named: ", fnfull , "f.name: ", f.name)

