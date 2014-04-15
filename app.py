import os, re
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
# import pymongo
#from pymongo import ModelClient
from werkzeug import secure_filename
import boto
import models

# import all of mongoengine
from flask.ext.mongoengine import mongoengine

#allowed extensions
ALLOWED_EXTENSIONS = set(['mov', 'MOV'])

#initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') # put SECRET_KEY variable inside .env file with a random string of alphanumeric characters
app.config['CSRF_ENABLED'] = True

mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

# names = []

@app.route('/', methods=['GET', 'POST'])
def index():

	video_upload_form = models.video_upload_form(request.form)

	if request.method == 'POST' and video_upload_form.validate():

		#create filename
		uploaded_file = request.files['fileupload']
		if uploaded_file and allowed_file(uploaded_file.filename):
			filename = secure_filename(uploaded_file.filename)

			#connecting to s3
			s3 = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
			b = s3.get_bucket(os.environ.get('AWS_BUCKET'))

			k = b.new_key(b)
			k.key = filename #set filename
			k.set_metadata("Content Type", uploaded_file.mimetype) #identify MIME type
			k.set_contents_from_string(uploaded_file.stream.read()) # file contents to be added
			k.set_acl('public-read') # make publicly readable


			#if the file was actually uploaded:
			if k and k.size > 0:

				submission = models.Video()
				submission.title = request.form.get('title')
				submission.filename = filename
				submission.save()

			return "File uploaded!"

		else:

			return "Uh-oh, there was an error" + uploaded_file.filename
	else:

		templateData = {
				'form' : video_upload_form
		}

		return render_template('main.html', **templateData)

@app.errorhandler(404)
def page_not_found(error):
	return "404 error", 404

@app.errorhandler(500)
def internalError(error):

	return "500 error"

#return whether it's allowed or not
def allowed_file(filename):
	return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/data')
def video_data():

	videos = models.Video.objects.order_by('-timestamp')

	if videos:

		public_data = []

		for v in videos:

			tmpVid = {
				'filename' : v.filename,
				'title' : v.title,
				'timestamp' : str(v.timestamp),
				'link' : 'https://s3.amazonaws.com/innovid_multiscreen/' + v.filename
			}

			public_data.append( tmpVid )

		data = {
			'status' : 'OK',
			'videos' : public_data
		}

		return jsonify(data)

	else:

		error = {
			'status' : 'error',
			'message' : 'unable to retrieve video links'
		}


if __name__ == '__main__':
	app.debug = os.environ.get('DEBUG', True)

	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
