from main import app, render_template

@app.route('/admin/<string:name>')
def admin(name):
    return render_template('admin/upload.html', title='Admin - {}'.format(name))