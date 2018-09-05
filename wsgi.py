
from linkcheck import linkcheck

from flask import (Flask, request, render_template)
import sys, os
import gunicorn

app = Flask(__name__)
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
GUNICORN_CMD_ARGS="--bind=0.0.0.0"


@app.route('/')
def get_addy():
    print("-------------------here inside app")
    return render_template('getaddy.html')

@app.route('/resultpage',methods = ['POST', 'GET'])
def result():
    print("------------------here inside result")
    answers = []
    #lc = linkcheck()
    if request.method == 'POST':
        form_resp = request.form['siteaddy']
        print("---------------here inside app result2")
        answers = linkcheck().main(form_resp)
        answers2 = [("no broken links", "1", "2")]
        print("-------------------------here inside app result3")
        print("answers: " )
        #for i in answers2:
        #    print(i)
        return render_template("resultpage.html", answers = answers2)


app.run(host='0.0.0.0', port=8080)




GUNICORN_CMD_ARGS="--bind=0.0.0.0"
app.run(host='0.0.0.0', port=8080)
