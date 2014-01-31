import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename


#path to upload directory
UPLOAD_FOLDER = 'uploads'

#allowed extensions
ALLOWED_EXTENSIONS = set(['pdf', 'jpg', 'jpeg', 'png', 'mov'])

#initialize Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

names = []

#return whether it's allowed or not
def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			names.append(str(filename))
			return redirect(url_for('uploaded_file', filename=filename))

	return render_template('index.html')


#expecting the name of a file -- will locate file on the upload directory and show in the browser
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
	app.run()
