from waitress import serve
from time import sleep
from os import path
from flask import Flask, request, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime

from linkcheck import LinkCheck
from nocache import nocache
from app_support_code import AppSupport as ac
from prodconf import ProfConf
#sys.stderr = sys.stdout   rootloglev = 40


pcf = ProfConf()

app = Flask(__name__)

env = Environment(    # jinja2
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

#-----------------------------------------------------------------------------
def main_work():   # run LinkCheck and ac.myprint to console
    site = pcf.get_site()
    #print("Just started. You entered: " + site)
    ac.myprint("running main_work")

    donefile_path = pcf.get_donefile_path()
    ac.myprint("donefile: " + donefile_path)
    lc = LinkCheck()
    answers = lc.main(site)
    len_ans = len(answers)
    ac.myprint("donefile in worker1: " + donefile_path + \
         "!!!!!!!!!!==---- len of answers: " + str(len_ans))
    file_path = pcf.get_file_path()
    if len_ans > -1:
        if len_ans == 0:
            ac.datalines(file_path, [('','','')], special=1)  #special=1 is a page with no broken links
        else:
            ac.datalines(file_path,answers)
        with open(donefile_path, 'w') as fd:
            fd.write("done")
    else:
        None

    dt = str(datetime.now())
    print( dt + "  main_work done")

    #-----------------------------------------------------------------------------
def set_names(site):
    osroot = app.root_path  # os path
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    just_name = "res" + timestp1 + ".html"
    just_stat = "./static/" + just_name
    donefile = just_name + "done"
    os_path_plus_stat = path.join(osroot, "static")
    file_path = path.join(os_path_plus_stat, just_name)
    donefile_path = path.join(os_path_plus_stat, donefile)
    #AppSupport.myprint("make_filenames os_donefile_path: " + os_donefile_path)
    pcf.set_timestp(timestp1)
    pcf.set_site(site)
    pcf.set_just_name(just_name)
    pcf.set_just_stat(just_stat)
    pcf.set_file_path(file_path)
    pcf.set_donefile(donefile)
    pcf.set_donefile_path(donefile_path)

@app.route('/')
def index():
    pcf.prod_reset()
    return render_template('index.html')  ## has a form

@nocache             # very important so client server doesn'w_thread cache results
@app.route('/indexn', methods = ['POST', 'GET', 'HEAD'])
def indexn():  # git name of url, construct names and pages, present page with button to next step
    site = request.form['name']  # from index.html
    set_names(site)
    sleep(2)
    return render_template('indexn.html', name = site)  ## has a form

@app.route('/indexnn', methods = ['POST', 'GET', 'HEAD'])
def indexnn():  # git name of ur
    theinput = request.form['name']  # from indexn.html
    #jsn = pcf.get_just_name()
    fname = pcf.get_just_stat()
    #fname = "./static/" + jsn
    main_work()
    sleep(1)
    return render_template('indexnn.html', name = fname)  ## has a form

if __name__ == '__main__':
    #serve(app)
    app.run('127.0.0.1', 5000, debug=True)

#    response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
