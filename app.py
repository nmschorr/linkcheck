from linkcheck import linkcheck
from flask import (Flask, request, render_template)
#from flask_socketio import SocketIO
import sys, os


app = Flask(__name__)
#HOST_NAME = os.environ.get('OPENSHIFT_APP_DNS', 'localhost')
#APP_NAME = os.environ.get('OPENSHIFT_APP_NAME', 'flask')
#IP = os.environ.get('OPENSHIFT_PYTHON_IP', '127.0.0.1')
PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
#HOME_DIR = os.environ.get('OPENSHIFT_HOMEDIR', os.getcwd())


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




#Flask.debug = 1
# app.config.from_object(__name__) # load config from this file , flaskr.py
#app.debug = True
#path1 = '/home/jetgal/linkcheck'   #for pythonanywhere
#sys.path.append(path1)   #for pythonanywhere
#sys.path.append(path2)
#sys.path.append(path3)
# app.config['SECRET_KEY'] = 'secret!'
# socketio = SocketIO(app)