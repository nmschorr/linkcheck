from flask import Flask, request, render_template
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
import app_support_code
import app_support_conf
import datetime




app = Flask(__name__)
##app.config['SECRET_KEY'] = 'secret!'

app.config['TEMPLATES_AUTO_RELOAD'] = True
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)
gc = app_support_code.hcode_cls()


def setup():
    reg_os_file_path, osdonefile = gc.ret_ospaths()
    os_root_path = app.root_path        #os path
    just_name, just_stat= gc.make_filenames(os_root_path)
    gc.setname(just_name)
    gc.setstat(just_stat)
    print("in init - osdonefile: ", osdonefile)

def notreadyyet():
    gsite = gc.getgsite()
    just_stat = gc.getstat()
    newst= gc.not_ready_msg(gsite)
    fj = open(just_stat, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg():
    gsite = gc.getgsite()
    just_stat = gc.getstat()
    newstt = gc.fin_msg(gsite)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1():   # run LinkCheck and print to console
    lc = linkcheck.LinkCheck()
    reg_os_file_path, osdonefile = gc.ret_ospaths()
    print("osdonefile in worker1: ", osdonefile)
    gsite = gc.getgsite()

    print("inside worker1 thread. you entered: ", gsite)
    answers = lc.main(gsite)
    time.sleep(2)
    if len(answers) > 0:
        gc.writeres(answers, reg_os_file_path, osdonefile)
    else:
        print("no errors found")
        write_no_err_pg()
    dt = datetime.datetime.now()
    print(dt + "  worker1 done")

    #-----------------------------------------------------------------------------

    #-----------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
@nocache             # very important so client server doesn'w_thread cache results
def results():
    setup()

    threads = []
    gsite = request.form['name']
    gc.setgsite(gsite)
    just_name = gc.getname()
    notreadyyet()
    w_thread = threading.Thread(target=worker1)
    threads.append(w_thread)
    w_thread.start()
    print("just started thread. root path: " + app.root_path + " you entered: ", gsite)
    return render_template('results.html', name = just_name)  ## has a form

import socket
print(socket.gethostbyaddr(socket.gethostname())[0])

HOSTIP = os.getenv('HOSTIP', default='0.0.0.0')
HOSTPORT = os.getenv('HOSTPORT', default=8080)
#HOSTPORT = 5000
HOSTPORT = 8080
print("hostip: " + HOSTIP + "  HOSTPORT: ", HOSTPORT)
debugnow = os.getenv('debug', default=False)
app.run(host=HOSTIP, port=HOSTPORT, debug=True)

