from flask import Flask, request, render_template, Response
from linkcheck import linkcheck
import time


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  ## has a form

@app.route('/results', methods = ['POST','GET'])
def results():
    name = request.form['name']
    print ("got: ", name)

    return render_template('results.html', name=name)  ## has a form


#
# @app.route( '/stream' )
# def stream():
#     g = proc.Group()
#     p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )
#
#     def read_process():
#         while g.is_pending():
#             lines = g.readlines()
#             for proc, line in lines:
#                 yield line
#
#     return Response( read_process(), mimetype= 'text/plain' )
#
# if __name__ == "__main__":
#     HOST = '127.0.0.1'
# #   app.run(host='127.0.0.1', port=5000)
#     app.run(host='127.0.0.1', port=8080)

app.run(host='127.0.0.1', debug=True)