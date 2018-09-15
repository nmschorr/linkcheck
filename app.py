from flask import Flask, request, render_template
from linkcheck import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
from hcode import datalines, hc, getfns, not_redy_msg, gethostinfo, writeres

gsite, w_thread, fnfull, just_name, just_stat = None, None, None, None, None

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def setupfile():
    global just_name, fnfull, just_stat, gsite
    just_name, just_stat, fnfull = getfns(app.root_path)

def notreadyyet(site):
    global just_stat
    newst= not_redy_msg(site)
    fj = open(just_stat, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg():
    global just_stat, gsite
    hostnamenow = gethostinfo()
    newstt = hc(gsite,hostnamenow)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1():   # run linkcheck and print to console
        global gsite
        lc = linkcheck()
        print("inside worker1 thread. you entered: ", gsite)
        answers = lc.main(gsite)
        if len(answers) > 0:
            writeres(answers)
        else:
            print("no errors found")
            write_no_err_pg()
        print("passing in to resultn just_name: " + just_name + "  worker1 done")


@app.route('/')
def index():
    setupfile()
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
@nocache             # very important so client server doesn'w_thread cache results
def results():
    global gsite, w_thread
    threads = []
    gsite = request.form['name']
    notreadyyet(gsite)
    w_thread = threading.Thread(target=worker1)
    threads.append(w_thread)
    w_thread.start()
    print("just started thread. root path: " + app.root_path + " you entered: ", gsite)
    time.sleep(1)
    return render_template('results.html', name = just_name)  ## has a form

ns = gethostinfo()
print("LinkCheck started.   " + ns)

HOSTIP = os.getenv('HOSTIP', default='0.0.0.0')
HOSTPORT = os.getenv('HOSTPORT', default=8080)
print("hostip: " + HOSTIP + "  HOSTPORT: ", HOSTPORT)
debugnow = os.getenv('debug', default=False)

app.run(host=HOSTIP, port=HOSTPORT, debug=debugnow)