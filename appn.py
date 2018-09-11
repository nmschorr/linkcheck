
from flask import Flask, request, render_template
from linkcheck import linkcheck
import time
from concurrent.futures import ThreadPoolExecutor
from flask import copy_current_request_context
import gevent.monkey


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')  ## has a form



@app.route('/waiting', methods = ['POST','GET'])
def waiting():
    name = request.form['name']

    def w(name='schorrmedia.com/m.html'):
        print("waiting")
        lc = linkcheck()
        namee = 'schorrmedia.com/m.html'
        answers = lc.main(namee)
        print (answers)

    def p():
        print("hello")

    gevent.joinall([
        gevent.spawn(w),
        gevent.spawn(p),
    ])
    return render_template('waiting.html')  ## has a form


@app.route('/waiting')
def printwait():
    answers = 'waiting'
    return answers





#GUNICORN_CMD_ARGS="--bind=0.0.0.0"
#PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
HOST='0.0.0.0'
HOST='127.0.0.1'
app.run(host=HOST, port=8080)


