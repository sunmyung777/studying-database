# -- coding: utf-8 --
import os
from flask import Flask,url_for,render_template,request,redirect
import sqlite3 as lite
from werkzeug import secure_filename
app=Flask(__name__)

UPP_FOLDER='static/img'
ALLOW=set(['png','jpg','jpeg','gif','PNG'])

app.config['UPP_FOLDER']=UPP_FOLDER

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.',1)[1] in ALLOW


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index',methods=['POST'])
def index():
	file=request.files['file']
	if file and allowed_file(file.filename):
		filename=secure_filename(file.filename)
		file.save(os.path.join(app.config['UPP_FOLDER'],filename))

		database_filename='db/hello.db'
		conn = lite.connect(database_filename)
		cs = conn.cursor()
		url='../static/img/'+str(filename)
		cs.execute('INSERT INTO img VALUES (?,?);',(filename,url))
		conn.commit()
		order='SELECT img FROM img WHERE name=="'+filename+'";'
		log_name=cs.execute(order).fetchall()
		a=log_name[0][0]
		log_name=0
		cs.close()
		conn.close()
		return render_template('hello.html',img=a)
	else:
		return redirect(url_for('main'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html',e=e), 404

@app.errorhandler(500)
def page_not_found(e):
	return render_template('error.html',e=e), 500
	
if __name__ == '__main__':
    app.run(debug=True)
