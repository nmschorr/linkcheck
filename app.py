from flask import Flask,  session, request, render_template, redirect
from flask_restful import Resource, Api
from src.linkcheck import linkcheck

#app.secret_key = "super secret key"
#app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = 'super secret key'
app = Flask(__name__)


@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    print("The email address is '" + email + "'")
    return redirect('/')

#@app.route('/')
# def run():
#     lc = linkcheck()
#     site = 'schorrmedia.com/mytest.html'
#     lines = lc.main_run(site)
#     return render_template('index.html', title='Home', lines=lines, parent=site)
#
# def handle_data():
#     projectpath = request.form['projectFilepath']


if __name__ == '__main__':
    app.run(debug=True)



