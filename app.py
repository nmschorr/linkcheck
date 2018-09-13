from flask import Flask, request, render_template, Response
from linkcheck import linkcheck
import threading, time

import tempfile
import os

commandname = "cat"

def writeres(data=[]):
    f = tempfile.NamedTemporaryFile(delete=False,mode='a+t')
    #for i in data:
    tname = f.name
    for line in data:
        nline = str(line)
        print(type(nline))
        print("this is the line: ", nline)
        f.write(nline)
        f.write('\n')

    print("tempfile named: ", f.name )
    ###tempfile.NamedTemporaryFile(buffering=True,newline=True,)
    f.close() # file is not immediately deleted because we
              # used delete=False

app = Flask(__name__)





@app.route('/resultsn')
def worker1(site='schorrmedia.com/m.html'):   # run linkcheck and print to console
    lc = linkcheck()
    print("you again entered: ", site)
    answers = lc.main()
    writeres(answers)
    for i in answers:
        print(i)


    return render_template('resultsn.html', name=answers)  ## has a form




@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
def results():
    name = request.form['name']
    print ("you entered: ", name)
    threads = []
    t = threading.Thread(target=worker1)
    threads.append(t)
    t.start()
    return render_template('results.html', name=name)  ## has a form


#
# @app.route( '/stream' )
# def stream():
#     g = proc.Group()
#     p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )
#
#     def read_process():
#         while g.is_pending():
#             lines = g.readlines()
#             for proc, line in lines:
#                 yield line
#
#     return Response( read_process(), mimetype= 'text/plain' )
#
# if __name__ == "__main__":
#     HOST = '127.0.0.1'
# #   app.run(host='127.0.0.1', port=5000)
#     app.run(host='127.0.0.1', port=8080)

print("working")

app.run(host='127.0.0.1', debug=True)