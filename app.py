from flask import Flask, render_template, request
from src.linkcheck import linkcheck

#app.secret_key = "super secret key"
#app.config['SESSION_TYPE'] = 'memcached'
#app.config['SECRET_KEY'] = 'super secret key'
app = Flask(__name__)

@app.route('/')
def get_addy():
   return render_template('getaddy.html')

@app.route('/resultpage',methods = ['POST', 'GET'])
def result():
    lc = linkcheck()
    if request.method == 'POST':
      form_resp = request.form['siteaddy']
      answers = lc.main_run(form_resp)
      return render_template("resultpage.html",answers = answers)

if __name__ == '__main__':
   app.run(debug = True, port=8080 )


###app.run(debug = True, host='0.0.0.0', port=8080 )



# def run():
#     lc = linkcheck()
#     site = 'schorrmedia.com/mytest.html'
#     lines = lc.main_run(site)
#     return render_template('index.html', title='Home', lines=lines, parent=site)
# def handle_data():
#     projectpath = request.form['projectFilepath']

