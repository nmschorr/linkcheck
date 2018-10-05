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
from werkzeug.wrappers import Response


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
#def main_work(re):  # run LinkCheck and ac.myprint to console

    #siteb = re.response
    #site = siteb[0].decode("utf-8")

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

#
# def get_msg(site):  # the callback
#     print("calling main_work now")
#     main_work(site)
#
# def after_this_request(func, site):
#     return func(site)
#--------------------------------------------------------------
from flask import g
from flask import after_this_request


# def after_this_request(f):
#     if not hasattr(g, 'after_request_callbacks'):
#         g.after_request_callbacks = []
#     g.after_request_callbacks.append(f)
#     return f
#
#
#
# @app.after_request
# def call_after_request_callbacks(response):
#     for callback in getattr(g, 'after_request_callbacks', ()):
#         response = callback(response)
#     return response


@app.route('/results', methods = ['POST', 'GET'])
def results():
    timestp1 = format(datetime.now(), '%Y%m%d%H%M%S')
    rfname = "res" + timestp1 + ".html"
    site = request.form['name']
    set_names(site, timestp1, rfname)
    make_notreadyyet_page(site, rfname)  # write the temp file

    # def __init__(self, response=None, status=None, headers=None,
    #              mimetype=None, content_type=None, direct_passthrough=False):

    # fheaders = {
    #         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0',
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #         'Accept-Language': 'en-US,en;q=0.5',
    #         'Accept-Encoding': 'gzip, deflate',
    # }


    # @after_this_request
    # def mainw(resp):
    #     resp = Response(site, status=200, headers=fheaders)
    #     main_work(resp)

    main_work(site)

    return render_template('results.html', name = rfname)  ## has a form


if __name__ == '__main__':
    #serve(app)
    app.run(host='127.0.0.1', port=5000, debug=True)


















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
