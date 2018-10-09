import app_support_conf
from config import conf_debug
#from time import sleep

class AppSupport:
    _DEBUG = conf_debug

    def __init__(self):
        self.conf_debug = conf_debug

    @staticmethod
    def myprint(print_str,_DEBUG=0 ):
        _DEBUG = conf_debug
        if _DEBUG:
            print(print_str)

    @classmethod
    def datalines(cls, filey, data, special=0):
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
            f.write('<meta http-equiv="Cache-Control" content="no-cache" />')
            f.write('<meta http-equiv="Pragma" content="no-cache"  />')
            f.write('<meta http-equiv="Expires" content="0"  />')

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


