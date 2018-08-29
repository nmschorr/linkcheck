from flask import Flask, flash, session, request, render_template
from flask_restful import Resource, Api
from src.linkcheck import linkcheck

app = Flask(__name__)
#app.secret_key = "super secret key"
#app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = 'super secret key'


@app.route('/')
def run():
    lc = linkcheck()
    site = 'schorrmedia.com/mytest.html'
    answer = lc.main_run(site)
    thelines = str(answer[0])
    return render_template('index.html', title='Home', thelines=thelines, parent=site)

if __name__ == '__main__':
    app.run(debug=True)



