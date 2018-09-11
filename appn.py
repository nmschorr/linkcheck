
from flask import Flask, request, render_template
from linkcheck import linkcheck
import time
from concurrent.futures import ThreadPoolExecutor
#PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
#GUNICORN_CMD_ARGS="--bind=0.0.0.0"

app = Flask(__name__)
# to do:  spinner
exec = ThreadPoolExecutor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST','GET'])
def results():
    time.sleep(1)
    name = request.form['name']
    exec.submit(runme('schorrmedia.com/m.html'))

    return render_template('waiting.html', name=name)


def runme(name='schorrmedia.com/m.html'):
    lc = linkcheck()
    answers = lc.main(name)   # later name from form
    render_template('results.html', answers = answers)


HOST='0.0.0.0'
HOST='127.0.0.1'
app.run(host=HOST, port=8080)


