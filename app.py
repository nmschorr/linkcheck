from flask import Flask, request, render_template, Response
from linkcheck import linkcheck
import threading, time, tempfile
from datetime import datetime

app = Flask(__name__)
fnfull = "0"

def writeres(data=[]):
    print("inside writeres "  )
    timestp = format(datetime.now(), '%Y%m%d%H%M%S')
    dir = "resultsn/"
    justfilename = "results" + timestp + ".html"
    global fnfull
    fnfull = dir + justfilename
    f = open(fnfull, "w+t")
    for line in data:
        print("this is the line: ", str(line))
        f.write(str(line))
        f.write('\n')

    f.close() # file is not immediately deleted because we
    print("file named: ", f.name )
    return justfilename  # used delete=False## file name so we can read it


@app.route('/resultsn', methods = ['GET'])
def worker1(site='schorrmedia.com/m.html'):   # run linkcheck and print to console
    lc = linkcheck()
    print("inside thread. you again entered: ", site)
    answers = lc.main()
    for i in answers:
        print(i)
        justfilename = writeres(answers)
    print("filenm: ", justfilename)
    return render_template('resultsn.html', name = justfilename)  ## has a form

@app.route('/demotest')
def demotest():
   return app.static_url_path('demotest.html')



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