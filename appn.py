
from flask import Flask, request, render_template
    ###redirect, url_for, send_from_directory, render_template
#from concurrent.futures import ThreadPoolExecutor
#import time, cgi
#from flask import views
import http
import werkzeug.wsgi


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello', methods = ['POST','GET'])
def hello():
    name = request.form['name']
    namen='name'
    return render_template('hello.html', name=name)

if __name__ == '__main__':    #don't delete!
  app.run(debug=True)  #, use_reloader=False



