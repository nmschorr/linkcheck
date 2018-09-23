from flask import Flask, request, render_template, views
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
from app_support_code import AppSupport
import datetime
from prodconf import ProdConfig
import logging


def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    roote = logging.getLogger()
    roote.setLevel(50)
    #app.jinja_env.cache = {}
    global pc
    pc = ProdConfig()
    return app

def cleanup():
    app.template_global(pc)
    pc.set_just_name("empty")
    pc.set_just_stat("empty")
    pc.set_donefile("empty")
    pc.set_file_path("empty")
    pc.set_donefile_path("empty")
    pc.set_site("empty")


app = create_app()



env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def notreadyyet(ste):
    from app_support_code import AppSupport
    newst= AppSupport.not_ready_msg(ste)
    just_stat = pc.get_just_stat()

    fj = open(just_stat, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg(ste):
    from app_support_code import AppSupport
    just_stat = pc.get_just_stat()
    newstt = AppSupport.fin_msg(ste)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1():   # run LinkCheck and print to console
    from app_support_code import AppSupport
    lc = linkcheck.LinkCheck()
    lc.__init__()
    file_path = pc.get_file_path()
    donefile_path = pc.get_donefile_path()
    logging.debug("donefile in worker1: " + donefile_path)
    site = pc.get_site()
    logging.debug("inside worker1 thread. you entered: " + site)
    answers = lc.main(site)
    time.sleep(2)
    if len(answers) > 0:
        AppSupport.writeres(answers, file_path, donefile_path)
    else:
        logging.debug("no errors found")
        write_no_err_pg("no errors found")
    dt = str(datetime.datetime.now())
    logging.debug( dt + "  worker1 done")
    cleanup()
    file_path = pc.get_file_path()
    logging.debug("at end value of file_path: " + file_path)

    #-----------------------------------------------------------------------------


# def add_header(response):
#     return response
    #-----------------------------------------------------------------------------
def set_names(site):
    pc.set_site(site)
    osroot = app.root_path  # os path

    just_name, just_stat, donefile, file_path, donefile_path = AppSupport.make_filenames(app, osroot)
    pc.set_just_name(just_name)
    pc.set_just_stat(just_stat)
    pc.set_donefile(donefile)
    pc.set_file_path(file_path)
    pc.set_donefile_path(donefile_path)


@app.route('/')
def index():
    return render_template('index.html')  ## has a form

# class MyRequest(views):
#     def dispatch_request(self):
#         name = request.args.get('name')
#         return 'Hello, %s!' % name
#
# app.add_url_rule(
#     '/results', view_func=MyRequest.as_view('my_request')
# )

@app.route('/results', methods = ['POST','GET'])
@nocache             # very important so client server doesn'w_thread cache results
def results():
    site = request.form['name']
    set_names(site)
    notreadyyet(site)
    threads = []
    w_thread = threading.Thread(target=worker1)
    threads.append(w_thread)
    w_thread.start()
    logging.debug("just started thread. You entered: ", site)

    just_name = pc.get_just_name()
    return render_template('results.html', name = just_name)  ## has a form

# @app.after_request
# def apply_caching(response):
#     response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
#     return response


import socket
print(socket.gethostbyaddr(socket.gethostname())[0])

HOSTIP = os.getenv('HOSTIP', default='0.0.0.0')
#HOSTPORT = os.getenv('HOSTPORT', default=8080)
HOSTPORT = 8080
print("hostip: " + HOSTIP + "  HOSTPORT: ", HOSTPORT)
app.run(host=HOSTIP, port=HOSTPORT, debug=False)


