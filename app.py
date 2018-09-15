from flask import Flask, request, render_template
from linkcheck import linkcheck
import threading, time
from datetime import datetime
from os import path
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

gsite, t, fnfull, justfilename, justandstatic = None, None, None, None, None
gfulldir, fnfull, mtab, bothp, timestp = None, None, None, None, None


def setupfile():
    global justfilename, gfulldir, fnfull, mtab, bothp, justandstatic, fnfull, timestp
    bothp =  '<p></p>'
    mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"
    gfulldir = path.join(app.root_path, "static")
    print("gfulldir: " + gfulldir)
    timestp = format(datetime.now(), '%Y%m%d%H%M%S')
    justfilename = "res" + timestp + ".html"
    justandstatic = path.join("static",justfilename)
    notred = "Results not ready yet. Keep reloading page until they appear." + mtab
    reload = "<a href=" + "javascript:location.reload(true)" + ">Refresh this page</a>"
    scr = "<script>function pageloadEvery(t) {setTimeout('location.reload(true)', t);}</script>"
    headr = "<!DOCTYPE html><html><head>" + scr + "<title>Not Ready</title></head>"
    bodreload = "<body onload=javascript:pageloadEvery(10000);>"
    newst = headr + bodreload + notred + reload  + "</body></html>"
    fnfull = path.join(gfulldir, justfilename)
    fj = open(justandstatic, "w")
    fj.write(newst)
    fj.close()


def writeres(data=[]):
    global justfilename, gfulldir, fnfull, mtab, bothp
    spaces = "&ensp;"  #two spaces
    print("inside writeres "  )
    print("justfilename: ", justfilename)

    f = open(fnfull, "w")
    f.write(bothp)
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

    f.close() # file is not immediately deleted because we
    print("fnfull named: ", fnfull )
    print("f.name: ", f.name)
    return


def writenote():
    global justandstatic
    print("inside writenote. ")
    answer =  "No broken links found. Thanks for using LinkCheck."
    outstt = "<!DOCTYPE html><html><head><title>No Broken Links</title></head><body>"
    newstt = outstt + answer + "</body></html>"
    fjj = open(justandstatic, "w")
    fjj.write(newstt)
    fjj.close()

def worker1():   # run linkcheck and print to console
        global gsite
        answers = None
        lc = linkcheck()
        print("inside worker1 thread. you entered: ", gsite)
        answers = lc.main(gsite)
        if len(answers) > 0:
            writeres(answers)
        else:
            print("no errors found")
            writenote()

        print("passing in to resultn justfilename: ", justfilename)
        print("worker1 done")


@app.route('/')
def index():
    setupfile()
    return render_template('index.html')  ## has a form


@app.route('/results', methods = ['POST','GET'])
@nocache
def results():
    global gsite, t
    threads = []
    rootpath = app.root_path
    print("root path: ", rootpath)
    gsite = request.form['name']
    print ("you entered: ", gsite)
    t = threading.Thread(target=worker1)
    print("just started thread")
    threads.append(t)
    t.start()
    time.sleep(1)
    return render_template('results.html', name = justandstatic)  ## has a form



print("LinkCheck started.")
HOST='127.0.0.1'
#HOST='0.0.0.0'
debug = False
debug = True
app.run(host=HOST, port=8080, debug=debug)