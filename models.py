from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime

class Video(mongoengine.Document):

	#title of Video
	title = mongoengine.StringField(max_length=120, required=True)
	filename = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())

video_form = model_form(Video)

class video_upload_form(video_form):
	fileupload = FileField('Upload a video', validators=[])
