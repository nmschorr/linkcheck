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
    site = pcf.get_rsite()
    ac.myprint("running main_work")
    just_name = pcf.get_rjustname()
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
    import random
    rand = random.random()
    rnm = str(rand)[2:0]
    rjustname = "rjustname" + rnm
    rtimestp = "rtimestp" + rnm
    rsite = "rsite" + rnm

    pcf.prod_dict.update({rjustname: "empty"})
    pcf.prod_dict.update({rtimestp: "empty"})
    pcf.prod_dict.update({rsite: "empty"})

    site = request.form['tsite']  # from index.html
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    just_name = "res" + timestp1 + ".html"

    pcf.set_rtimestp(timestp1)
    pcf.set_rsite(site)
    pcf.set_rjustname(just_name)
    print("----------------------------------------------------")
    print("Starting over. Is it True that setting filename is done? ", just_name)
    sleep(3)
    return render_template('indexn.html', name = site)  ## has a form

@nocache             # very important so client server doesn'w_thread cache results
@app.route('/indexnn', methods = ['POST', 'GET', 'HEAD'])
def indexnn():  # git name of ur
    fname='none'
    # e_unused = request.form['name']  # from indexn.html
    print("in indexnn getting fname from pcf: ")
    just_name = pcf.get_rjustname()
    just_name_st = "./static/" + just_name
    print("just got just_name_st: ", just_name_st)
    main_work()
    sleep(3)
    return render_template('indexnn.html', filename=just_name_st)  ## has a form

if __name__ == '__main__':
    serve(app)
    #app.run('127.0.0.1', 5000, debug=True)

#    response.setHeader("Access-Control-Allow-Origin", request.getHeader("Origin"));
