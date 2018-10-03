from os import path
import app_support_conf
from config import conf_debug
from time import sleep

class AppSupport:
    _DEBUG = conf_debug

    def __init__(self):
        self.conf_debug = conf_debug

    @staticmethod
    def myprint(print_str,_DEBUG=0 ):

        _DEBUG = conf_debug

        if _DEBUG:
            print(print_str)
            #logging.info(print_str)
        else:
            #logging.debug(print_str)
            None

    @staticmethod
    def fin_msg(asite):
        thishost = app_support_conf.thishost
        AppSupport.myprint("inside hc. ")
        outst1 = "<!DOCTYPE html><html><head><title>No Broken Links</title></head><body>"
        answer2 =  "No broken links found for " + asite +". Thanks for using LinkCheck."
        home_url = "<a href=" + thishost + ">Start Over</a>"
        newstt = outst1 + answer2 + '<p></p>' + home_url + "</body></html>"
        return newstt

    @classmethod
    def datalines(cls, f, data):
        thishost = app_support_conf.thishost
        home_url = "&nbsp;&nbsp;&nbsp;&nbsp;" +  "&nbsp;&nbsp;&nbsp;&nbsp;" + \
                "<h2><a href=" + thishost + ">Start Over</a></h2><p></p>"

        sm = "http://schorrmedia.com"
        smedia_url = "<h3><a href=" + sm + ">Visit SchorrMedia.com</a>"

        git_url = "<a href=https://github.com/nmschorr/linkcheck>See the code for this on Github</a></h3>"
        spaces = "&ensp;"  #two spaces
        f.write("<!DOCTYPE html><html><head>")
        f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
        f.write("</head><body><div style=margin-left:5em;>")

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
            f.write("<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + "  ***FOUND ON: ")
            f.write("<a href='")
            f.write(str(line[2]))
            f.write("'>")
            f.write(str(line[2]))
            f.write("</a>")
            f.write('<p></p>')

        f.write('<p></p>')
        f.write(home_url)
        f.write("&nbsp;&nbsp;&nbsp;&nbsp;")
        f.write(smedia_url)
        f.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        f.write(git_url)
        f.write("</div>" + "</body></html>")

    @classmethod
    def not_ready_msg(cls, gsite):

        arf1 = "<a href="
        jst2 = "javascript:location.reload(true)"

        sc1 = "<!DOCTYPE html><html><head> "
        sc1b='<meta charset=utf-8> <style> p { padding-left:10em;} </style>'
        sc2 = '<script> function finddone(ur) { var xhr = new XMLHttpRequest() ;'
        sc3 = '  xhr.open("HEAD", ur, false); xhr.send(); '
        sc3b = ' if (xhr.status == "404") { return false; } else {'
        sc3c = 'return true; location.reload(true);}}'
        sc4 = ' function cdf(){ '
        sc5 = ' var df=window.location.href + "done";  '

        sc6 = ' var rel=finddone(df); '
        sc7 = " if (rel==true) { location.reload(true); }}</script>"
        sta = "<script>function doit() { setInterval(cdf, 2000);} </script>"
        sc7b = "<title>Not Ready</title> </head>"
        toppt = sc1 + sc1b + sc2 + sc3 + sc3b + sc3c + sc4 + sc5 + sc6 + sc7 + sta + sc7b


        st2 = "<body onload=doit()> <div padding-left:10em;>"
        st4 = "<p>Results not ready yet." + '</p><p> </p><p>' + "You entered: " + gsite + '</p><p></p>' + \
            "<p>If server times out or gives an error, reload the page with the shift key down." + '</p><p></p>'
        refrsh_pg = "<p><a href=" + jst2 + ">Refresh this page</a></p>"
        whole_page = toppt + st2 + st4 + refrsh_pg + "</div></body></html>"
        return whole_page

    @classmethod
    def make_filenames(cls, osroot, timestp, just_name2):
        stat = "static"
        just_stat = "./static/" + just_name2
        donef_name =  "res" + timestp + ".htmldone"

        os_path_plus_stat = path.join(osroot, stat)
        file_os_path_all = path.join(os_path_plus_stat, just_name2)
        os_donefile_path = path.join(os_path_plus_stat, donef_name)
        AppSupport.myprint("make_filenames os_donefile_path: " + os_donefile_path)
        return just_stat, donef_name, file_os_path_all, os_donefile_path


    @classmethod
    def writeres(cls, data, fnfull, osdonefile_loc):
        AppSupport.myprint("INSIDE WRITERES!!!!!-----------------------")
        AppSupport.myprint("osdonefile_loc WRITERES!!!!!-----------------------" + osdonefile_loc)
        f = open(fnfull, "w")
        sleep(.4)
        f.write('<p></p>')
        cls.datalines(f,data)

        f.close() # file is not immediately deleted because we
        AppSupport.myprint("reg_os_file_path named: " + fnfull + "  f.name: " + f.name)
        AppSupport.myprint("osdonef in writeres: " + osdonefile_loc)
        fd = open(osdonefile_loc,"w")
        fd.write("done")
        fd.close() # file is not immediately deleted because we
