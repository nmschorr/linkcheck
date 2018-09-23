from flask import Flask, request, render_template, g
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
import datetime
from app_support_code import AppSupport


class ProdConfig(object):
    site = "empty"
    just_name = "empty"
    just_stat = "empty"
    os_donefile = "empty"
    os_donefile = "empty"
    reg_os_file_path = "empty"

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

    def set_os_donefile(self, os_donefile):
        self.os_donefile = os_donefile
    def get_os_donefile(self):
        return self.os_donefile

    def set_reg_os_file_path(self, reg_os_file_path):
        self.reg_os_file_path = reg_os_file_path
    def get_reg_os_file_path(self):
        return self.reg_os_file_path

    def set_osdonefile(self, osdonefile):
        self.osdonefile = osdonefile
    def get_osdonefile(self):
        return self.osdonefile

pc = ProdConfig()

def create_app():
    app = Flask(__name__)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    osroot = app.root_path  # os path

    just_name, just_stat, donef_name, file_os_path_all, os_donefile_path = AppSupport.make_filenames(app, osroot )

    pc.set_just_name(just_name)
    pc.set_just_name(just_stat)
    pc.set_just_name(donef_name)
    pc.set_just_name(file_os_path_all)
    pc.set_just_name(os_donefile_path)
    return app

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
    reg_os_file_path = pc.get_reg_os_file_path()
    osdonefile = pc.get_os_donefile()
    print("osdonefile in worker1: ", osdonefile)
    site = pc.get_site()
    print("inside worker1 thread. you entered: ", site)
    answers = lc.main(site)
    time.sleep(2)
    if len(answers) > 0:
        AppSupport.writeres(answers, reg_os_file_path, osdonefile)
    else:
        print("no errors found")
        write_no_err_pg()
    dt = datetime.datetime.now()
    print(dt + "  worker1 done")

    #-----------------------------------------------------------------------------


# def add_header(response):
#     return response
    #-----------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
@nocache             # very important so client server doesn'w_thread cache results
def results():
    with app.app_context():
        site = request.form['name']
        pc.set_site(site)
        notreadyyet(site)

        threads = []
        w_thread = threading.Thread(target=worker1)
        threads.append(w_thread)
        w_thread.start()
        print("just started thread. root path: " + app.root_path + " you entered: ", site)

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

