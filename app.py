from waitress import serve
from time import sleep
from os import path
from flask import Flask, request, render_template
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime

from linkcheck import LinkCheck
from app_support_code import nocache
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
    ac.myprint("running main_work")
    just_name = pcf.get_just_name()
    os_path_plus_stat = path.join(app.root_path, "static")
    file_path = path.join(os_path_plus_stat, just_name)

    lc = LinkCheck()
    answers = lc.main(site)
    len_ans = len(answers)
    if len_ans == 0:
        ac.datalines(file_path, [('','','')], special=1)  #special=1 is a page with no broken links
    else:
        ac.datalines(file_path,answers)
    dt = str(datetime.now())
    print( dt + "  main_work done")

    #-----------------------------------------------------------------------------
# def set_names(site):
#     just_name = "res" + timestp1 + ".html"
#     pcf.set_site(site)
#     return True

@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@nocache             # very important so client server doesn'w_thread cache results
@app.route('/indexn', methods = ['POST', 'GET', 'HEAD'])
def indexn():  # git name of url, construct names and pages, present page with button to next step
    site = request.form['tsite']  # from index.html
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    just_name = "res" + timestp1 + ".html"
    pcf.set_site(site)
    pcf.set_just_name(just_name)
    print("----------------------------------------------------")
    print("Starting over. Is it True that setting filename is done? ", just_name)
    sleep(2)
    return render_template('indexn.html', name = site)  ## has a form

@nocache             # very important so client server doesn'w_thread cache results
@app.route('/indexnn', methods = ['POST', 'GET', 'HEAD'])
def indexnn():  # git name of ur
    fname='none'
    # e_unused = request.form['name']  # from indexn.html
    just_name = pcf.get_just_name()
    fname = "./static/" + just_name
    print("fname: ", fname)
    main_work()
    sleep(3)
    return render_template('indexnn.html', filename=fname)  ## has a form

if __name__ == '__main__':
    #serve(app)
    app.run('127.0.0.1', 5000, debug=True)

#    response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
