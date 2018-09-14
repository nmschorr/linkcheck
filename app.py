from flask import Flask, request, render_template, Response
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


def writeres(data=[]):
    beginp = '<p>'
    endp = '</p>'
    bothp =  '<p></p>'
    spaces = "&ensp;"  #two spaces
    mtab = "&nbsp;&nbsp;&nbsp;&nbsp;"
    print("inside writeres "  )
    timestp = format(datetime.now(), '%Y%m%d%H%M%S')
    dir = "static/"
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
    return justfilename  # used delete=False## file name so we can read it


@app.route('/resultsn', methods = ['GET'])
def worker1(site='schorrmedia.com/m.html'):   # run linkcheck and print to console
    lc = linkcheck()
    print("inside thread. you again entered: ", site)
    answers = lc.main()
    for i in answers:
        print(i)
        justfilename = writeres(answers)
    print("passing in to resultn justfilename: ", justfilename)
    return render_template('resultsn.html', name = justfilename)  ## has a form

# @app.route('/demotest')
# def demotest():
#    return app.static_url_path('demotest.html')



@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
def results():
    v = app.root_path
    print("root path: ", v)
    name = request.form['name']
    print ("you entered: ", name)
    threads = []
    t = threading.Thread(target=worker1)
    print("just started thread")
    threads.append(t)
    t.start()
    return render_template('results.html', name = name)  ## has a form




print("working")

app.run(host='127.0.0.1', debug=True)