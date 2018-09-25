from flask import Flask, request, render_template, views
import linkcheck
import threading, time, os
from jinja2 import Environment, PackageLoader, select_autoescape
from nocache import nocache
from app_support_code import AppSupport
import datetime
from prodconf import ProdConfig
import logging
from app_support_code import AppSupport
from  werkzeug.debug import get_current_traceback

rootloglev = 30


def cleanup(pc):
    with app.app_context():
        #app.template_global(pc)
        pc.set_just_name("empty")
        pc.set_just_stat("empty")
        pc.set_donefile("empty")
        pc.set_file_path("empty")
        pc.set_donefile_path("empty")
        pc.set_site("empty")


def createpc():
    with app.app_context():
        pc = ProdConfig()
        return pc

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config.FLASK_ENV='development'
app.config['FLASK_ENV'] ='development'
#roote = logging.getLogger()
#roote.setLevel(rootloglev)



env = Environment(
    loader=PackageLoader('linkcheck', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
)

def notreadyyet(ste, just_stat):
    ### start here
    newst= AppSupport.not_ready_msg(ste)
    fj = open(just_stat, "w")
    fj.write(newst)
    fj.close()

def write_no_err_pg(ste, pc):
    just_stat = pc.get_just_stat()
    newstt = AppSupport.fin_msg(ste)
    fjj = open(just_stat, "w")
    fjj.write(newstt)
    fjj.close()

def worker1(site, timestmp, jname):   # run LinkCheck and print to console
    with app.app_context():
        print("running worker1 thread")
        pc = createpc()
        answers = []
        set_names(pc, site, timestmp, jname)
        just_stat = pc.just_stat
        notreadyyet(site, just_stat)
        lc = linkcheck.LinkCheck()
        lc.__init__()
        file_path = pc.get_file_path()
        answers = lc.main(site)
        donefile_path = pc.get_donefile_path()
        print("donefile:", donefile_path)
        time.sleep(1)

        # logging.debug("donefile in worker1: " + donefile_path)
        # logging.debug("inside worker1 thread. you entered: " + site)
        print("!!!!!!!!!!==---- len of answers: " + str(len(answers)))
        if len(answers) > 0:
            AppSupport.writeres(answers, file_path, donefile_path)
        else:
            #logging.debug("no errors found")
            write_no_err_pg("no errors found", pc)

        dt = str(datetime.datetime.now())
        print( dt + "  worker1 done")
        #cleanup(pc)
    #time.sleep(5)
    #lc.__init__()

    #file_path = pc.get_file_path()
    #print("at end value of file_path: " + file_path)


    #-----------------------------------------------------------------------------


# def add_header(response):
#     return response
    #-----------------------------------------------------------------------------
def set_names(pc, site, timestp4, justn):
    just_name = justn
    pc.set_timestp(timestp4)
    pc.set_site(site)
    pc.set_just_name(just_name)
    osroot = app.root_path  # os path
    just_stat, donefile, file_path, donefile_path = AppSupport.make_filenames(osroot, timestp4, just_name)
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
    with app.app_context():
        try:
            site = request.form['name']
            threads = []
            timestp1 = format(datetime.datetime.now(), '%Y%m%d%H%M%S')
            just_name = "res" + timestp1 + ".html"
            w_thread = threading.Thread(target=worker1, args=(site,timestp1, just_name))
            threads.append(w_thread)
            w_thread.start()
            print("just started thread. You entered: " + site)
        except Exception as e:
            track = get_current_traceback(skip=1, show_hidden_frames=True,
                                          ignore_system_exceptions=False)
            t = str(track)
            print(t)
        return render_template('results.html', name = just_name)  ## has a form

@app.teardown_appcontext
def teardown(exception):
    None
    #db = getattr(g, '_database', None)
    #if db is not None:
        #db.close()
#from socket import gethostbyaddr, gethostname
#print(gethostbyaddr(gethostname())[0])
#HOSTIP = os.getenv('HOSTIP')
#HOSTIP='127.0.0.1'
#HOSTPORT = 8080
#print("hostip: " + HOSTIP + "  HOSTPORT: ", HOSTPORT)
#use_debugger = True
#app.run(host='127.0.0.1', port=8080,use_debugger=use_debugger, debug=app.debug,use_reloader=False )
try:

    app.run(host='127.0.0.1', port=8099, use_reloader=False )

except Exception as e:
    track = get_current_traceback(skip=1, show_hidden_frames=True, ignore_system_exceptions=False)
    # track.log()
    t = str(track)
    print(t)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, use_reloader=False)




# class MyRequest(views):
#     def dispatch_request(self):
#         name = request.args.get('name')
#         return 'Hello, %s!' % name
#
# app.add_url_rule(
#     '/results', view_func=MyRequest.as_view('my_request')
# )