from linkcheck import linkcheck
from flask import (Flask, request, render_template)
#import sys

#path1 = '/home/jetgal/linkcheck'   #for pythonanywhere


#sys.path.append(path1)   #for pythonanywhere
#sys.path.append(path2)
#sys.path.append(path3)

app = Flask(__name__)
app.config.from_object(__name__) # load config from this file , flaskr.py
#app.debug = True

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