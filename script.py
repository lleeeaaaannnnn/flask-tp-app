from flask import Flask, redirect, url_for, request, render_template, make_response, session
import json
app = Flask(__name__)
app.secret_key = 'abc123'

def get_saved_data():
    try:
	    data = json.loads(request.cookies.get('my_cookie'))  #returns dict
    except TypeError:
	    data = {}
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student')
def student():
    return render_template('student.html', result=get_saved_data())

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        req_form_json = json.dumps(dict(request.form.items()))
        data = get_saved_data()
        request_form_dict = dict(request.form.items())
        data['Physics'] += request_form_dict['Physics']
        #ddata.update(dict(request.form.items()))
        response = make_response(render_template('result.html', result = data))
        response.set_cookie('my_cookie',req_form_json)
        return response

@app.route('/success/<nm>/<age>')
def success(nm,age):
    return render_template("success.html", name=nm,age=age,username=session['username'])
   #return 'welcome {}. {} years old. You are logged in as {}'.format(nm,age,session['username'])

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      #user = request.form['nm']
      #age = request.form['age']
      #new_dict = {'name': user, 'age':age}
      session['username'] = request.form['nm']
      session['age'] = request.form['age']
      return redirect(url_for('success',**dict(request.form.items())))
   else:
      user = request.args.get('nm')
      age = request.args.get('age')
      return redirect(url_for('success',nm = user, age = age))


@app.route('/logout')
def logout():
    session.pop('username',None)
    return "logged out!"


if __name__ == '__main__':
   app.run(debug = True, port = 5001)
