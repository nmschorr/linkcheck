from flask import Flask, request, render_template, g
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
from app_support_code import AppSupport
import datetime


class ProdConfig(object):
    site = "empty"
    just_name = "empty"
    just_stat = "empty"
    donefile_path = "empty"
    donefile = "empty"
    file_path = "empty"

    def set_site(self, site):
        self.site = site
    def get_site(self):
        return self.site

    def set_just_name(self, just_name):
        self.just_name = just_name

    def get_just_name(self):
        return self.just_name

    def set_just_stat(self, just_stat):
        self.just_stat = just_stat

    def get_just_stat(self):
        return self.just_stat

    def set_donefile(self, donefile):
        self.donefile = donefile
    def get_donefile(self):
        return self.donefile

    def set_file_path(self, file_path):
        self.file_path = file_path
    def get_file_path(self):
        return self.file_path

    def set_donefile_path(self, donefile_path):
        self.donefile_path = donefile_path
    def get_donefile_path(self):
        return self.donefile_path

pc = ProdConfig()

def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    osroot = app.root_path  # os path

    # just_name, just_stat, donefile, file_path, donefile_path = AppSupport.make_filenames(app, osroot )
    #
    # pc.set_just_name(just_name)
    # pc.set_just_stat(just_stat)
    # pc.set_donefile(donefile)
    # pc.set_file_path(file_path)
    # pc.set_donefile_path(donefile_path)
    return app

def cleanup():
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
    print("donefile in worker1: ", donefile_path)
    site = pc.get_site()
    print("inside worker1 thread. you entered: ", site)
    answers = lc.main(site)
    time.sleep(4)
    if len(answers) > 0:
        AppSupport.writeres(answers, file_path, donefile_path)
    else:
        print("no errors found")
        write_no_err_pg()
    dt = str(datetime.datetime.now())
    print(dt + "  worker1 done")
    cleanup()
    file_path = pc.get_file_path()
    print("at end value of file_path: ", file_path)

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
    print("just started thread. You entered: ", site)

    just_name = pc.get_just_name()
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

