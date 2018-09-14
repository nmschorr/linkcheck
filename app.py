from flask import Flask, request, render_template, Response, flash
from linkcheck import linkcheck
import threading, time, tempfile
from datetime import datetime
from os import path

app = Flask(__name__)
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
staticdir = "static"
gfulldir = path.join(app.root_path, staticdir)
print("gfulldir: " + gfulldir)
gsite = None
t = None
done = None
justfilename = None


def writeres(data=[]):
    global justfilename
    bothp =  '<p></p>'
    spaces = "&ensp;"  #two spaces
    mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"
    print("inside writeres "  )
    timestp = format(datetime.now(), '%Y%m%d%H%M%S')
    justfilename = "res" + timestp + ".html"
    global gfulldir
    fnfull = path.join(gfulldir, justfilename)
    f = open(fnfull, "w+t")
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
    return render_template('resultsn.html', name=gsite)  ## has a form


@app.route('/notready')
def notready():
    return render_template('notready.html')

@app.route('/resultsn', methods = ['GET'])
def resultsn():   # run linkcheck and print to console
    global justfilename
    global gsite
    global done
    global t
    context = {'name': gsite}
    #threading.currentThread().is_alive()
    print ("reloaded")
    while t.is_alive():
        return render_template('notready.html')
        time.sleep(10)
    with app.app_context():
        return render_template('resultsn.html', **context)  ## has a form


# @app.route('/resultsn', methods = ['GET'])

def worker1():   # run linkcheck and print to console
        global gsite
        answers = None
        lc = linkcheck()
        print("inside worker1 thread. you entered: ", gsite)
        answers = lc.main(gsite)
        for i in answers:
            print(i)
            justfilename = writeres(answers)
        print("passing in to resultn justfilename: ", justfilename)
        print("worker1 done")




@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
def results():
    v = app.root_path
    print("root path: ", v)
    global gsite
    global t
    gsite = request.form['name']
    print ("you entered: ", gsite)
    threads = []
    t = threading.Thread(target=worker1)
    print("just started thread")
    threads.append(t)
    t.start()

    return render_template('results.html', name = gsite)  ## has a form




print("working")

app.run(host='127.0.0.1', debug=True)