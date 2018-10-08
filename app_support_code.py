from os import path, unlink
import app_support_conf
from config import conf_debug
#from time import sleep

class AppSupport:
    _DEBUG = conf_debug
    #_DEBUG = 0

    def __init__(self):
        self.conf_debug = conf_debug

    @staticmethod
    def myprint(print_str,_DEBUG=0 ):

        _DEBUG = conf_debug
        #_DEBUG = 0

        if _DEBUG:
            print(print_str)

    @staticmethod
    def fin_msg(asite):
        thishost = app_support_conf.thishost
        AppSupport.myprint("inside hc. ")
        outst1 = '<!DOCTYPE html><html><head><title>No Broken Links</title>'
        ob ='<link rel=stylesheet href="../static/style.css"></head><body>'

        answer2 =  "No broken links found for " + asite +". Thanks for using LinkCheck."
        home_url = "<a href=" + thishost + ">Start Over</a>"
        newstt = outst1 + ob + answer2 + '<p></p>' + home_url + "</body></html>"
        return newstt

    @classmethod
    def datalines(cls, filey, data, special=0):
        unlink(filey)
        thishost = app_support_conf.thishost
        home_url = "&nbsp;&nbsp;&nbsp;&nbsp;" +  "&nbsp;&nbsp;&nbsp;&nbsp;" + \
                "<h2><a href=" + thishost + ">Start Over</a></h2><p></p>"

        sm = "http://schorrmedia.com"
        smedia_url = "<h3><a href=" + sm + ">Visit SchorrMedia.com</a>"

        git_url = "<a href=https://github.com/nmschorr/linkcheck>See the code for this on Github</a></h3>"
        spaces = "&ensp;"  #two spaces
        first = "BAD LINK-->  "
        sec = "**ERROR-->  "
        third = "  ***FOUND ON: "
        fourth = "Here are your broken links:"
        if special == 1:
            first = "No broken links."
            sec = "No errors found."
            third = ""
            fourth = "Thanks for using LinkCheck."
        with open(filey, 'w') as f:

            f.write("<!DOCTYPE html><html><head><style> h3 { color:#36d1af;}</style>")
            f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            f.write('<link rel=stylesheet href="./static/style.css"></head><body><div style=margin-left:5em;>')
            f.write("<p></p><h3>" + fourth + "</h3><p></p>")

            for line in data:
                #f.write("<p>&nbsp;</p>")
                f.write(first)
                f.write("<a href='")
                f.write(str(line[0]))
                f.write("'>")
                f.write(str(line[0]))
                f.write("</a>")
                f.write(spaces)
                f.write(sec)
                f.write(str(line[1]))  ## the error
                f.write(spaces)
                f.write("<br>" + "&nbsp;&nbsp;&nbsp;&nbsp;" + third)
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

