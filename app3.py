from linkcheck import linkcheck
from flask import (Flask, request, render_template)
import os


import gevent
import threading
# import subprocess
#
# def foo2():
#     print('Running in foo')
#     #gevent.sleep(0)
#     print('Explicit context switch to foo again')
#
# #subprocess.call(['ls','-l'])
# sb = subprocess()
#
# sb
import time
#
#


class acsync(object):

    def longtask(self):
        print(str(time.time()))
        while self.lc != "done":
            #print("longtask val of lc: ", self.lc)

            while self.lc != "done":
                time.sleep(9)
                print("!!!! PAST SLEEP 7")
                self.lc = "done"
        print("all done!")

    def task2(self):
        while self.lc != "done":
            print("still waiting")
            time.sleep(2)
        print("done waiting")


    def __init__(self):
        lc = 0
        self.lc = lc

    def run(self):
        t1 = threading.Thread(target=self.longtask)
        t1.start()
        t2 = threading.Thread(target=self.task2)
        t2.start()

        print("threadname1: ", t1.name)
        print("threadname2: ", t2.name)




aa = acsync()
aa.run()


















#
# def foo():
#     while True:
#         print('Running in foo')
#         gevent.sleep(0)
#         print('Explicit context switch to foo again')
# def bar():
#     #while True:
#     print('Explicit context to bar')
#     print('Spawning threads now')
#     thread1 = gevent.spawn(task)
#     thread2 = gevent.spawn(task2)
#     print('Done Spawning threads now')
#     print('Explicit context to bar')
#     gevent.sleep(0)
#     time.sleep(1)
#     print('Implicit context switch back to bar')

# gevent.joinall([
#     gevent.spawn(foo),
#     gevent.spawn(bar),
# ])












# PORT = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))
# GUNICORN_CMD_ARGS="--bind=0.0.0.0"
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def get_addy():
#     print("-------------------here inside app")
#     return render_template('getaddy.html')
#
#
# @app.route('/resultpage',methods = ['POST', 'GET'])
# def result():
#     print("------------------here inside result")
#     answers = []
#     if request.method == 'POST':
#         form_resp = request.form['siteaddy']
#         print("---------------here inside app result2")
#         linkcheck_obj = linkcheck()
#         answers = linkcheck_obj.main(form_resp)
#         #answers2 = [("no broken links", "1", "2")]  # for testing
#         print("-------------------------here inside app result3")
#         print("answers: " )
#         for i in answers:
#             print(i)
#         return render_template("resultpage.html", answers = answers)
#
# HOST='0.0.0.0'
# #HOST='127.0.0.1'
# app.run(host=HOST, port=8080)
#



#Flask.debug = 1

