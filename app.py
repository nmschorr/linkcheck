from linkcheck import linkcheck
from flask import (Flask, request, render_template)
import os

PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
GUNICORN_CMD_ARGS="--bind=0.0.0.0"

app = Flask(__name__)


@app.route('/')
def get_addy():
    print("-------------------here inside app")
    return render_template('getaddy.html')


@app.route('/resultpage',methods = ['POST', 'GET'])
def result():
    print("------------------here inside result")
    answers = []
    if request.method == 'POST':
        form_resp = request.form['siteaddy']
        print("---------------here inside app result2")
        answers = linkcheck().main(form_resp)
        #answers2 = [("no broken links", "1", "2")]  # for testing
        print("-------------------------here inside app result3")
        print("answers: " )
        for i in answers:
            print(i)
        return render_template("resultpage.html", answers = answers)

HOST='0.0.0.0'
#HOST='127.0.0.1'
app.run(host=HOST, port=8080)




#Flask.debug = 1

