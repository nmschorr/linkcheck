from os import path
from datetime import datetime
import app_support_conf

thishost=app_support_conf.thishost
print("host: ", thishost)
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

        sc1 = "<!DOCTYPE html><html><head>"
        sc2 = '<script src=./jscript.js></script>'
        sc3 = '<script>   '
        sc4 = ' function checkDoneFile(){ '
        sc5 = ' var dname=window.location.href + "done";  '
        sc6 = ' var rel=doesFileExist(dname); '
        sc7 = " if (rel==true) { location.reload(true); }}</script>"
        sc7b = "<title>Not Ready</title>"
        headr0 = sc1 + sc2 + sc3 + sc4 + sc5 + sc6 + sc7 + sc7b

        st1 = "<style>body {padding-left:10em;}</style></head>"
        st2 = "<body>   "
        st2b = "<script>setInterval(checkDoneFile, 2000);</script>"


        newst = headr0 + st1 + st2 + st2b + usr_msg3 + refresh4  + endbod
        return newst

    def make_filenames(self, ospath):
        stat = "static"
        timestp = format(datetime.now(), '%Y%m%d%H%M%S')
        nme_only = "res" + timestp + ".html"
        nme_plus_static = path.join(stat, nme_only)
        fname_only = "res" + timestp + ".html"
        os_donefile =  "res" + timestp + ".htmldone"

        os_path_plus_stat = path.join(ospath, stat)
        ospath_full =      path.join(os_path_plus_stat, fname_only)
        os_donefile_path = path.join(os_path_plus_stat, os_donefile)
        print("make_filenames os_donefile_path: ", os_donefile_path)

        return ospath_full, os_donefile_path, nme_only, nme_plus_static

        #  reg_os_file_path, osdonefile, just_name, just_stat

    def writeres(self, data, fnfull, osdonefile_loc):
        global fullpar
        f = open(fnfull, "w")
        f.write(fullpar)
        self.datalines(f,data)
        f.close() # file is not immediately deleted because we
        print("reg_os_file_path named: ", fnfull , "f.name: ", f.name)
        print("osdonef in writeres: ", osdonefile_loc)
        fd = open(osdonefile_loc,"w")
        fd.write("done")
        fd.close() # file is not immediately deleted because we

