from flask import Flask, request, render_template
#import logging

from linkcheck import LinkCheck
from time import sleep
from threading import Thread
from jinja2 import Environment, PackageLoader, select_autoescape
# from nocache import nocache
from datetime import datetime
import prodconf as pcf
from app_support_code import AppSupport as ac
#from werkzeug.debug import get_current_traceback
# this comment is new

#logr = logging.getLogger('werkzeug').setLevel(logging.DEBUG)
#import sys

#fsock = open('error.log', 'w')               1
#sys.stderr = sys.stdout

#rootloglev = 40

#app = Flask(__name__, instance_relative_config=True)
app = Flask(__name__)

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def notreadyyet(ste, jname):
    newst= ac.not_ready_msg(ste)
    js = './static/' + jname
    print("just_stat: ", js)
    fj = open(js, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg(asited):
    just_stat = pcf.get_just_stat()
    print("just_stat: ", just_stat)
    newstt = ac.fin_msg(asited)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1(site, timestmp, jname):   # run LinkCheck and print to console
    ac.myprint("running worker1 thread")
    set_names(site, timestmp, jname)
    just_stat = pcf.get_just_stat()
    notreadyyet(site, jname)
    lc = LinkCheck()
    lc.__init__()
    answers = lc.main(site)
    donefile_path = pcf.get_donefile_path()
    ac.myprint("donefile:" + donefile_path)
    sleep(1)

    ac.myprint("donefile in worker1: " + donefile_path)
    ac.myprint("!!!!!!!!!!==---- len of answers: " + str(len(answers)))
    file_path = pcf.get_file_path()
    if len(answers) > -1:
        ac.writeres(answers, file_path, donefile_path)
    else:
        #logging.debug("no errors found")
        write_no_err_pg(site)

    dt = str(datetime.now())
    ac.myprint( dt + "  worker1 done")


    #-----------------------------------------------------------------------------
    #-----------------------------------------------------------------------------
def set_names(site, timestp4, justn):
    just_name = justn
    pcf.set_timestp(timestp4)
    pcf.set_site(site)
    pcf.set_just_name(just_name)
    osroot = app.root_path  # os path
    just_stat, donefile, file_path, donefile_path = ac.make_filenames(osroot, timestp4, just_name)
    pcf.set_just_stat(just_stat)
    pcf.set_donefile(donefile)
    pcf.set_file_path(file_path)
    pcf.set_donefile_path(donefile_path)



@app.route('/')
def index():
    return render_template('index.html')  ## has a form

# @nocache             # very important so client server doesn'w_thread cache results

@app.route('/results', methods = ['POST', 'GET'])
def results():
    #try:
    site = request.form['name']
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    name = "res" + timestp1 + ".html"
    threads = []
    w_thread = Thread(target=worker1, args=(site,timestp1, name))
    threads.append(w_thread)
    w_thread.start()
    #sleep(3)
    #ac.myprint("just started thread. You entered: " + site)
    #except Exception as e:
        #ac.myprint(str(e))
    return render_template('results.html', name = name)  ## has a form

# from socket import gethostname
# thehost = gethostname()
#_DEBUG = getenv('_DEBUG')
#_DEBUG = 0
#HOSTIP = getenv('HOSTIP')
#'127.0.0.1'
#HOSTIP = '0.0.0.0'
#app.run(host=HOSTIP, port=8080)
#app.run('0.0.0.0', 8080, debug=True)

#app.run('127.0.0.1', 8080, debug=True)

# app.config['PROPAGATE_EXCEPTIONS'] = True
#
# try: {
#     #app.run('127.0.0.1', 8080, debug=True)
#
# }
# except Exception as e:
#     track = get_current_traceback(skip=1, show_hidden_frames=True, ignore_system_exceptions=False)
#     # track.log()
#     t = str(track)
#     print(t)

app.run('0.0.0.0', 8080)

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)
