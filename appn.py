
from flask import Flask, request, render_template
    ###redirect, url_for, send_from_directory, render_template
#from concurrent.futures import ThreadPoolExecutor
import time
#from flask import views
import http
import werkzeug.wsgi
from concurrent.futures import ThreadPoolExecutor
from linkcheck import linkcheck

app = Flask(__name__)
executor = ThreadPoolExecutor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods = ['POST','GET'])
def hello():
    name = request.form['name']
    #z = executor.submit(testone())
    #name='name'
    return render_template('hello.html', name=name)

@app.route('/results')
def results():
    time.sleep(5)
    #lc = linkcheck()
    #answers = lc.main('schorrmedia.com/m.html')
    return app.send_static_file('results.html')


if __name__ == '__main__':    #don't delete!
  app.run(debug=True)  #, use_reloader=False



