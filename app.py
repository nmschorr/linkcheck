from flask import Flask, request, render_template, Response
from linkcheck import linkcheck
import threading, time, tempfile

app = Flask(__name__)

def writeres(data=[]):
    print("inside writeres "  )
    f = open("demo.html", "w+t")
    for line in data:
        print("this is the line: ", str(line))
        f.write(str(line))
        f.write('\n')

    f.close() # file is not immediately deleted because we
    print("file named: ", f.name )
    return f.name  # used delete=False## file name so we can read it



def worker1(site='schorrmedia.com/m.html'):   # run linkcheck and print to console
    lc = linkcheck()
    print("inside thread. you again entered: ", site)
    answers = lc.main()
    for i in answers:
        print(i)
    fname = writeres(answers)
    print("filenm: ", fname)




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
    return render_template('results.html')  ## has a form




print("working")

app.run(host='127.0.0.1', debug=True)