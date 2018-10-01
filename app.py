from waitress import serve
from threading import Thread
from socket import gethostbyaddr, gethostname
from flask import Flask, request, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import prodconf as pcf
from app_support_code import AppSupport as ac
from time import sleep
from linkcheck import LinkCheck
#import requests
# from nocache import nocache

#sys.stderr = sys.stdout
#rootloglev = 40
from config import conf_debug

app = Flask(__name__)

env = Environment(    # jinja2
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def notreadyyet(ste, jname):
    newst= ac.not_ready_msg(ste)
    js = './static/' + jname
    pcf.set_just_stat(js)
    fj = open(js, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg(asited):
    just_stat = pcf.get_just_stat()
    newstt = ac.fin_msg(asited)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1(df):
    from pathlib import Path
    sleep(1)
    dfp = pcf.get_donefile_path()
    doneyet = False
    while not doneyet:
        doneyet= Path(dfp).exists()
        ac.myprint("Checking from worker1 for done file: " + dfp)
        sleep(1)
    ac.myprint("worker1 done")

    #-----------------------------------------------------------------------------

def worker2(site, timestmp, jname):   # run LinkCheck and ac.myprint to console
    print("Just started thread. You entered: " + site)
    ac.myprint("running worker2 thread")
    set_names(site, timestmp, jname)
    notreadyyet(site, jname)
    donefile_path = pcf.get_donefile_path()
    ac.myprint("donefile:" + donefile_path)
    lc = LinkCheck()
    answers = lc.main(site)

    ac.myprint("donefile in worker1: " + donefile_path)
    ac.myprint("!!!!!!!!!!==---- len of answers: " + str(len(answers)))
    file_path = pcf.get_file_path()
    if len(answers) > -1:
        ac.writeres(answers, file_path, donefile_path)
    else:
        #logging.debug("no errors found")
        write_no_err_pg(site)

    sleep(1)
    dt = str(datetime.now())
    print( dt + "  worker2 done")


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
    site = request.form['name']
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    rfname = "res" + timestp1 + ".html"
    threads = []
    w1_thread = Thread(target=worker1, args=(rfname,)) #provide args a tuple!!!
    w1_thread.setDaemon(True)
    ac.myprint('rfname: ' + rfname)

    w2_thread = Thread(target=worker2, args=(site,timestp1, rfname))
    threads.append(w1_thread)
    threads.append(w2_thread)
    w2_thread.start()
    w1_thread.start()

    sleep(4)  ## openshift is slow!
    return render_template('results.html', name = rfname)  ## has a form


#serve(app, listen="127.0.0.1:8080")

if __name__ == '__main__':
    serve(app, channel_timeout=9960)
    #app.run(host='127.0.0.1', port=5000, debug=True)






    # stat = 404
    # thost = gethostbyaddr(gethostname())[0]
    # doneurl = "http://" + thost + "/static/" + df + "done"
    # #df = "http://Delia:8080/static/" + df + "done"
    # ac.myprint("checking: " + df)
    # while stat == 404:
    #     stat = requests.head(doneurl).status_code
    #     ac.myprint("file not done yet " + str(stat))
    #     sleep(1)