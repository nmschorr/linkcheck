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

@app.route('/')
def index():
    message = linkcheck('cosmictoys.blogspot.com')
    flash(message)
    for i in message.err_links:
        print(i)

    return render_template('home.html')




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
if __name__ == '__main__':
     app.debug = True
     app.run(port=5000)


