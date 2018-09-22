from os import path
from datetime import datetime
import app_support_conf



class hcode_cls(object):
    one_para_returns = '<p></p>'
    two_para_returns = one_para_returns + one_para_returns
    blank4spaces = "&nbsp;&nbsp;&nbsp;&nbsp;"
    end_body_html_tags = "</body></html>"
    ospath_full = 'notset'
    os_donefile_path = 'notset'
    just_name_cls = "notset"
    just_stat_cls = "notset"
    gsite_cls = "notset"

    def __init__(self):
        self.os_donefile = "empty"
        self.ospath_full = 'notset'
        self.os_donefile_path = 'notset'
        self.just_name_cls = "notset"
        self.just_stat_cls = "notset"
        self.gsite_cls = "notset"

    def fin_msg(self, asite):
        thishost = app_support_conf.thishost
        print("inside hc. ")
        outst1 = "<!DOCTYPE html><html><head><title>No Broken Links</title></head><body>"
        answer2 =  "No broken links found for " + asite +". Thanks for using LinkCheck."
        homeURL4 = "<a href=" + thishost + ">Start Over</a>"
        newstt = outst1 + answer2 + self.two_para_returns + homeURL4 + self.end_body_html_tags
        return newstt

    def datalines(self, f,data):
        thishost = app_support_conf.thishost
        home_url = self.blank4spaces + self.blank4spaces + "<h2><a href=" + thishost + ">Start Over</a></h2><p></p>"

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
            f.write("<br>" + self.blank4spaces + "  ***FOUND ON: ")
            f.write("<a href='")
            f.write(str(line[2]))
            f.write("'>")
            f.write(str(line[2]))
            f.write("</a>")
            f.write(self.one_para_returns)

        f.write(self.two_para_returns)
        f.write(home_url)
        f.write(self.blank4spaces)
        f.write(smedia_url)
        f.write(self.blank4spaces)
        f.write(git_url)
        f.write("</div>" + self.end_body_html_tags)


    def not_ready_msg(self, gsite):
        usr_msg3 = "Results not ready yet." + self.one_para_returns + "You entered: " + gsite + self.one_para_returns + \
                 "Page will automatically reload until results appear." + self.one_para_returns

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


        newst = headr0 + st1 + st2 + st2b + usr_msg3 + refresh4 + self.end_body_html_tags
        return newst

    def make_filenames(self, ospath):
        stat = "static"
        timestp = format(datetime.now(), '%Y%m%d%H%M%S')
        nme_only = "res" + timestp + ".html"
        nme_plus_static = path.join(stat, nme_only)
        fname_only = "res" + timestp + ".html"
        self.os_donefile =  "res" + timestp + ".htmldone"

        os_path_plus_stat = path.join(ospath, stat)
        self.ospath_full = path.join(os_path_plus_stat, fname_only)
        self.os_donefile_path = path.join(os_path_plus_stat, self.os_donefile)
        print("make_filenames os_donefile_path: ", self.os_donefile_path)

        return nme_only, nme_plus_static

        #  reg_os_file_path, osdonefile, just_name, just_stat

    def ret_ospaths(self):
        return self.ospath_full, self.os_donefile_path



    def writeres(self, data, fnfull, osdonefile_loc):
        f = open(fnfull, "w")
        f.write(self.one_para_returns)
        self.datalines(f,data)
        f.close() # file is not immediately deleted because we
        print("reg_os_file_path named: ", fnfull , "f.name: ", f.name)
        print("osdonef in writeres: ", osdonefile_loc)
        fd = open(osdonefile_loc,"w")
        fd.write("done")
        fd.close() # file is not immediately deleted because we


    def setname(self, jnme):
        self.just_name_cls = jnme

    def getname(self):
        return self.just_name_cls

    def setstat(self, nme):
        self.just_stat_cls = nme

    def getstat(self):
        return self.just_stat_cls

    def setgsite(self, gse):
        self.gsite_cls = gse

    def getgsite(self):
        return self.gsite_cls
