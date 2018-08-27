from src.linkcheck import linkcheck
from flask import Flask, flash, session, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
                    # api = Api(app)
app.secret_key = "super secret key"
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
#sess = session()
#sess.init_app(app)
from src.linkcheck import linkcheck

@app.route('/')
def app():
    lc = linkcheck()
    site = 'schorrmedia.com/mytest.html'
    answer = lc.main_run(site)

    #flash(message)
    #for a in answer:
    #    print(a)
    a = str(answer[0])
    print(a)

    '''
    <html>
        <head>
            <title>LinkCheck Results</title>
        </head>
        <body>
            <h1>''' +  a + '''</h1>
        </body>
    </html>
    '''


app()

# @app.route('/<string:page_name>/')
# def hello():
#     answer = linkcheck('schorrmedia.com')
# #     return str(answer)
#
# @app.route('/<string:page_name>/')
# def static_page(page_name):
#     return render_template('%s.html' % page_name)

#
# @app.route("/")
# def hello():
#     return '<form action="/echo" method="POST"><input name="text"><input type="submit" value="Test Links"></form>'
#
# @app.route("/echo", methods=['GET', 'POST'])
# def echo():
#     ret = linkcheck(<'text'>)
#     return "Testing this site: " + request.form['text']
#
# def login():
#     if request.method == 'POST':
#         do_the_login()
#     else:
#         show_the_login_form()



# @app.route('/')
# @app.route('/index')
# def index():
#     answer = linkcheck('schorrmedia.com')
#     user = {'username': 'Miguel'}
#     return '''
# <html>
#     <head>
#         <title>Home Page - Microblog</title>
#     </head>
#     <body>
#         <h1>Hello, ''' + user['username'] + '''!</h1>
#     </body>
# </html>'''
#
#



