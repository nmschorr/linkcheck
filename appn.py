
from flask import Flask, request, render_template
from linkcheck import linkcheck

app = Flask(__name__)
# to do:  spinner

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods = ['POST','GET'])
def results():
    name = request.form['name']
    lc = linkcheck()

    render_template('waiting.html', name=name)
    answers = lc.main(name)
    return render_template('results.html', answers = answers)


if __name__ == '__main__':    #don't delete!
  app.run(debug=True)



