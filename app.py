from waitress import serve

from flask import Flask, request, render_template
#import flask
from jinja2 import Environment, PackageLoader, select_autoescape
from datetime import datetime
import prodconf as pcf
from app_support_code import AppSupport as ac
from linkcheck import LinkCheck
#sys.stderr = sys.stdout
#rootloglev = 40
from config import conf_debug

app = Flask(__name__)

env = Environment(    # jinja2
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def make_notreadyyet_page(r, jname):
    ste = r
    newst= ac.not_ready_msg(ste)
    jstatn = './static/' + jname
    pcf.set_just_stat(jstatn)
    with open(jstatn, "w") as fhandle:
        fhandle.write(newst)

def write_no_err_pg(asited):
    just_stat = pcf.get_just_stat()
    newst2 = ac.fin_msg(asited)
    with open(just_stat, "w") as fjj:
        fjj.write(newst2)

#-----------------------------------------------------------------------------
def main_work(site):   # run LinkCheck and ac.myprint to console
    print("Just started. You entered: " + str(site))
    ac.myprint("running main_work")

    donefile_path = pcf.get_donefile_path()
    ac.myprint("donefile: " + donefile_path)
    lc = LinkCheck()
    answers = lc.main(site)

    ac.myprint("donefile in worker1: " + donefile_path + \
         "!!!!!!!!!!==---- len of answers: " + str(len(answers)))
    file_path = pcf.get_file_path()
    if len(answers) > -1:
        ac.datalines(file_path,answers)
        with open(donefile_path, 'w') as fd:
            fd.write("done")
    else:
        write_no_err_pg(site)

    dt = str(datetime.now())
    print( dt + "  main_work done")


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





@app.route('/results', methods = ['POST', 'GET'])
def results():
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    rfname = "res" + timestp1 + ".html"
    site = request.form['name']

    #flask.after_this_request(print("yes"))

    set_names(site, timestp1, rfname)
    make_notreadyyet_page(site, rfname)  # write the temp file
    main_work(site)

    return render_template('results.html', name = rfname)  ## has a form


if __name__ == '__main__':
    #serve(app)
    app.run(host='127.0.0.1', port=5000, debug=True)

    #
    # def after_this_request(f):
    #     if not hasattr(g, 'after_request_callbacks'):
    #         g.after_request_callbacks = []
    #     g.after_request_callbacks.append(f)
    #     return f
    #
    # @app.after_request
    # def call_after_request_callbacks(response):
    #     for callback in getattr(g, 'after_request_callbacks', ()):
    #         callback(response)
    #     return response

# @nocache             # very important so client server doesn'w_thread cache results

# def multi2(df):
#     from pathlib import Path
#     #sleep(1)
#     dfp = pcf.get_donefile_path()
#     doneyet = False
#     while not doneyet:
#         doneyet= Path(dfp).exists()
#         ac.myprint("Checking from worker1 for done file: " + dfp)
#         sleep(1)
#     ac.myprint("worker1 done")
#
#     #
#     donefile_path = pcf.get_donefile_path()
#     ac.myprint("donefile: " + donefile_path)
