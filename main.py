from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from operation import backend
from adminPanel import admin
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['FILES_UPLOAD'] = 'upload'

@app.context_processor
def example():
    return dict(enumerate=enumerate, list=list)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        reg_no = request.form['regiInput']
        semester = request.form.get('select')
        try:
            json = backend().generate_API(reg_no, semester)
            return render_template("result.html", title='Result', info=json)
        except Exception as e:
            return str(e)
    return render_template('home.html', title="CSE")

@app.route('/result/api/<string:semester>/<string:reg_no>', methods=['POST', 'GET'])
def api(reg_no, semester):
    if request.method=='GET':
        return jsonify(backend().generate_API(reg_no, semester))


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user', None)
    if request.method == 'POST':
        res = admin().login(request.form['email'], request.form['passwd'])
        # res = True
        if res==True:
            session['user'] = request.form['email'].strip('@')[0]
            return redirect(url_for('admin_panel', name=session['user']))
        else:
            return jsonify(res)
    return render_template('admin/login.html', title='Admin-login')


@app.route('/admin-panel')
def admin_panel():
    if 'user' in session: 
        return render_template('admin/adminHome.html', title='Admin')
    else: 
        return redirect('login')  


@app.route('/admin/upload', methods=['GET', 'POST'])
def uploadTXT():
    if 'user' in session:
        if request.method == "POST":
            semester = request.form.get('select')
            year = request.form['year']
            txt = request.files['inputFile']
            txt.save(os.path.join(app.config['FILES_UPLOAD'], txt.filename))          
            backend().upload_results(txt.filename, semester, year)
        return render_template('admin/upload.html', title='Admin')
    else:
        return redirect('login')


@app.route('/admin/create-tables', methods=['POST', 'GET'])
def create_tables():
    if 'user' in session:
        if request.method == "POST":
            return backend().create_tables_in_database()
        return render_template('admin/create_table.html', title='Admin- Create-tables')
    return redirect('login')



if __name__=="__main__":
    app.run(host='localhost', port=8080, debug=True)



# 4321 4900 1235 6512