from src.linkcheck import linkcheck
from flask import Flask, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


#@app.route("/")
# @app.route('/<string:page_name>/')
# def hello():
#     answer = linkcheck('schorrmedia.com')
# #     return str(answer)
#
# @app.route('/<string:page_name>/')
# def static_page(page_name):
#     return render_template('%s.html' % page_name)
#
#
# if __name__ == '__main__':
#     app.debug = True
#     app.run(port=5000)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return '''
<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''


if __name__ == '__main__':
     app.debug = True
     app.run(port=5000)




#class app(object):
    # from pathlib import Path
    # filenme = Path("./src/runargs.txt")
    # res, res_list = 1, []
    # with open(filenme, 'r+') as file:
    #     while res:
    #         res = file.readline()
    #         if not res.startswith('#'):
    #             res_list.append(res.rstrip())
    # if res_list:
    #     res_list.pop(-1)  # last one comes in empty

    # " for site in res_list:
    #linkcheck(site)

#app()