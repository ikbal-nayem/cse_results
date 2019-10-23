from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from operation import backend, admin, database
from calculator import cgpa
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['FILES_UPLOAD'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
SEMESTER, YEAR = admin().get_last_result()

@app.context_processor
def example():
    return dict(enumerate=enumerate, list=list, len=len, int=int)

#                                       HOME

@app.route('/', methods=['GET', 'POST'])
@app.route('/result', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        try:
            js = backend().generate_API(request.form['regiInput'], request.form['select'])
            return render_template("result.html", title='Result', info=js)
        except Exception as e:
            return render_template('includes/error.html', err=str(e))
    return render_template('home.html', semester=SEMESTER, year=YEAR)

@app.route('/result/find', methods=['GET', 'POST'])
def find():
    if request.method == 'POST':
        try:
            return jsonify({'reg_no': database().find_regi(request.form['batch'], request.form['name'])})
        except:
            return jsonify(database().find_name(request.form['batch']))
    return render_template('find_student.html', title='Find yourself')

@app.route('/subscribe', methods=['POST'])
def email():
    if database().add_email(request.form['reg_no'], request.form['email']):
        return jsonify({'submitted':True, 'htmlValue': render_template('get_email.html')})
    else:
        return jsonify({'submitted': False})

#                                       API

@app.route('/result/api/<string:semester>/<string:reg_no>', methods=['POST', 'GET'])
def api(reg_no, semester):
    if request.method=='GET':
        return jsonify(backend().generate_API(reg_no, semester))


#                                      CALCULATOR

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        gArr = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        gr, cr= [], []
        for i in range(int(request.form.get('select'))):
            gr.append(request.form[gArr[i]].upper())
            cr.append(float(request.form[gArr[i]+'-c']))
        json = {'result': cgpa(gr, cr), 'array': gArr, 'grades': gr, 'cradits': cr}
        return render_template('calculator.html', title='Calculator', data=json)
    return render_template('calculator.html', title='Calculator')

#                                       LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('user', None)
    if request.method == 'POST':
        res = admin().login(request.form['email'], request.form['passwd'])
        if res==True:
            session['user'] = request.form['email'].split('@')[0]
            return redirect(url_for('admin_panel'))
        else:
            return res
    return render_template('admin/login.html', title='Admin-login')

#                                   ADMIN PANEL

@app.route('/admin-panel')
def admin_panel():
    if 'user' in session: 
        return render_template('admin/adminHome.html', title='Admin', user=session['user'])
    else: 
        return redirect('login')  

@app.route('/new-admin/', methods=['POST', 'GET'])
def new_admin():
    if 'user' in session:
        if request.method == 'POST':
            v = admin().add_new(request.form['email'], request.form['password'])
            return jsonify({'success': True}) if v else jsonify({'success': False})
        else:
            return render_template('admin/new_admin.html', title='New admin', user=session['user'])
    else:
        return redirect(url_for('login'))

#                                              upload file


@app.route('/admin/upload', methods=['GET', 'POST'])
def uploadTXT():
    if 'user' in session:
        if request.method == "POST":
            semester = request.form.get('select')
            year = request.form['year']
            txt = request.files['inputFile']
            txt.save(os.path.join(app.config['FILES_UPLOAD'], txt.filename))     
            backend().upload_results(txt.filename, semester, year, session['user'])
            return jsonify({"success":True})
        return render_template('admin/upload.html', title='Admin-Upload', user=session['user'])
    else:
        return redirect('login')


@app.route('/admin/create-tables', methods=['POST', 'GET'])
def create_tables():
    if 'user' in session:
        if request.method == "POST":
            backend().create_tables_in_database()
        return render_template('admin/create_table.html', title='Admin- Create-tables', user=session['user'])
    return redirect('login')

@app.route('/admin/log')
def log():
    if 'user' in session:
        log = admin().get_log()
        return render_template('admin/log.html', title='Log', data=log, user=session['user'])
    else:
        return redirect(url_for('login'))




if __name__=="__main__":
    app.run(host='localhost', port=8080, debug=True)



