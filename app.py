
from flask import Flask, request, render_template
from linkcheck import linkcheck

#PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
GUNICORN_CMD_ARGS="--bind=0.0.0.0"

app = Flask(__name__)
# to do:  spinner

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST','GET'])
def results():
    name = request.form['name']
    lc = linkcheck()

    render_template('waiting.html', name=name)
    answers = lc.main(name)
    return render_template('results.html', answers = answers)

HOST='0.0.0.0'
#HOST='127.0.0.1'
app.run(host=HOST, port=8080)


