from flask import Flask, request, render_template
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
import app_support_code
import app_support_conf
import datetime


gsite, w_thread, fnfull, just_name, just_stat = None, None, None, None, None
lc = linkcheck.LinkCheck()
thishost=app_support_conf.thishost

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

hc_obj = app_support_code.hcode_cls()

app.config['TEMPLATES_AUTO_RELOAD'] = True
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def setupfile():
    global just_name, fnfull, just_stat
    arp = app.root_path
    just_name, just_stat, fnfull = hc_obj.getfns(arp)

def notreadyyet():
    global just_stat, gsite
    newst= hc_obj.not_ready_msg(gsite)
    fj = open(just_stat, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg():
    global just_stat, gsite
    newstt = hc_obj.fin_msg(gsite)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1():   # run LinkCheck and print to console
        global gsite, fnfull, just_name
        print("inside worker1 thread. you entered: ", gsite)
        answers = lc.main(gsite)
        time.sleep(5)
        if len(answers) > 0:
            hc_obj.writeres(answers, fnfull)
        else:
            print("no errors found")
            write_no_err_pg()
        print("passing in to resultn just_name: " + just_name + "  worker1 done")
        print(datetime.datetime.now())

    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------

@app.route('/')
def index():
    setupfile()
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
@nocache             # very important so client server doesn'w_thread cache results
def results():
    global gsite, w_thread, just_name
    threads = []
    gsite = request.form['name']
    notreadyyet()
    w_thread = threading.Thread(target=worker1)
    threads.append(w_thread)
    w_thread.start()
    print("just started thread. root path: " + app.root_path + " you entered: ", gsite)
    return render_template('results.html', name = just_name)  ## has a form



HOSTIP = os.getenv('HOSTIP', default='0.0.0.0')
HOSTPORT = os.getenv('HOSTPORT', default=8080)
#HOSTPORT = 5000
HOSTPORT = 8080
print("hostip: " + HOSTIP + "  HOSTPORT: ", HOSTPORT)
debugnow = os.getenv('debug', default=False)
app.run(host=HOSTIP, port=HOSTPORT, debug=True)

