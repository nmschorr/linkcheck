from os import path, getenv
import app_support_conf

class AppSupport:
    _DEBUG = 0

    # _DEBUG = getenv('_DEBUG')

    def __init__(cls):
        cls._DEBUG = AppSupport._DEBUG


    @staticmethod
    def myprint(print_str):
        if not AppSupport._DEBUG:
            None
            #print(print_str)
            #logging.info(print_str)
        else:
            #logging.debug(print_str)
            print(print_str)
            
            
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
        home_url =  "&nbsp;&nbsp;&nbsp;&nbsp;" +  "&nbsp;&nbsp;&nbsp;&nbsp;" + \
                "<h2><a href=" + thishost + ">Start Over</a></h2><p></p>"

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
        f.write("&nbsp;&nbsp;&nbsp;&nbsp;")
        f.write(git_url)
        f.write("</div>" + "</body></html>")

    @classmethod
    def not_ready_msg(cls, gsite):

        arf1 = "<a href="
        jst2 = "javascript:location.reload(true)"

        sc1 = "<!DOCTYPE html><html><head>"
        sc2 = '<script src=./linkjscript.js></script>'
        sc3 = '<script>   '
        sc4 = ' function checkDoneFile(){ '
        sc5 = ' var dname=window.location.href + "done";  '

        # sc5 = ' var dname=' + dname
        sc6 = ' var rel=doesFileExist(dname); '
        sc7 = " if (rel==true) { location.reload(true); }}</script>"
        sc7b = "<title>Not Ready</title>"
        toppt = sc1 + sc2 + sc3 + sc4 + sc5 + sc6 + sc7 + sc7b

        st1 = "<style>body {padding-left:10em;}</style></head>"
        st2 = "<body>   "
        st3 = "<script>setInterval(checkDoneFile, 2000);</script>"
        st4 = "Results not ready yet." + '<p></p>' + "You entered: " + gsite + '<p></p>' + \
                   "Page will automatically reload until results appear." + '<p></p>'
        refrsh_pg = arf1 + jst2 + ">Refresh this page</a>"
        whole_page = toppt + st1 + st2 + st3 + st4 + refrsh_pg + "</body></html>"
        return whole_page

    @classmethod
    def make_filenames(cls, osroot, timestp, just_name2):
        stat = "static"
        just_stat = path.join(stat, just_name2)
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
        f.write('<p></p>')
        cls.datalines(f,data)

        f.close() # file is not immediately deleted because we
        AppSupport.myprint("reg_os_file_path named: " + fnfull + "f.name: " + f.name)
        AppSupport.myprint("osdonef in writeres: " + osdonefile_loc)
        fd = open(osdonefile_loc,"w")
        fd.write("done")
        fd.close() # file is not immediately deleted because we
