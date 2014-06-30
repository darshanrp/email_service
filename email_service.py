from array import array
from datetime import datetime
from database import db_session, init_db
from models import Email
from exceptions import Exception
from flask import Flask, request, make_response, abort, g
from flask.ext.sqlalchemy import SQLAlchemy
import html2text
import json
import logging
from pytz import timezone
import re
import requests
import settings
import sqlite3

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object('settings')


@app.route("/email", methods=['POST'])
def email():
	"""
	This function listens to the '/email' endpoint and accepts HTTP 'POST' 
	requests only.	On receiving a HTTP 'POST' request it performs necessary 
	validations for all the fields.	If validation is successful, it sends the
	email by reading the settings from the settings.py file.
	"""
	if request.method == 'POST':
		data = request.get_json(force=True)
		data = validations(data)
		response = send_email(data)
		if  response == 'success':
			return make_response("Email sent successfully!")
		else:
			abort(500, response)
	emails = Email.query.all()	


def send_email(data):
	"""
	This is a helper function for sending emails based on the settings 
	provided in the settings.py file.
	"""
	if not settings.URL:
		abort(500,'Email provider URL is not set')
	if not settings.API_KEY:
		abort(500,'Email provider API_KEY is not set')

	status = False
	if settings.EMAIL_PROVIDER == 'MAILGUN':
		status = send_email_using_mailgun(data, settings.URL, settings.API_KEY)
		if status != 'success' and settings.AUTO_SWITCH_EMAIL_PROVIDER:		#check to auto switch email provider
			return send_email_using_mandrill(data, settings.ALT_URL, settings.ALT_API_KEY)

	elif settings.EMAIL_PROVIDER == 'MANDRILL':
		status = send_email_using_mandrill(data, settings.URL, settings.API_KEY)
		if status != 'success' and settings.AUTO_SWITCH_EMAIL_PROVIDER:		#check to auto switch email provider
			return send_email_using_mailgun(data, settings.ALT_URL, settings.ALT_API_KEY)

	if status == 'success':		#Storing emails sent in the database
		email = Email(to_name=data['to_name'], to_email=data['to'],
					  from_email=data['from'], from_name=data['from_name'],
					  subject=data['subject'], body=data['body'])
		if 'send_at' in data and data['send_at']:
			email.send_at = data['send_at']
		
		db_session.add(email)
		db_session.commit()
	
	return status


def send_email_using_mailgun(data, url, api_key):

	try:
		params = {}
		params['from'] = data['from_name'] + ' <' + data['from'] + '>'
		params['to'] = data['to_name'] + ' <' + data['to'] + '>'
		params['text'] = data['body']
		params['subject'] = data['subject']
		if 'send_at' in data and data['send_at']:
			try:
				local_timezone = timezone(settings.TIMEZONE)
				date = local_timezone.localize(datetime.strptime(data['send_at'], '%Y-%m-%d %H:%M:%S'))
				params['o:deliverytime'] = date.strftime('%a, %d %b %Y %H:%M:%S %Z')
			except ValueError, e:
				log.exception(e.message)
				abort(400, 'Invalid delivery date/time provided. Please provide date/time in the format Y-m-d H:M:S')

		response = requests.post(
			url, auth=('api', api_key),
			data=params)
		log.debug('response from server: ' + response.text)
		
		if response.status_code != 200:
			return response.text
	except Exception,e:
		log.exception(e.message)
		return e.message
	return 'success'
	
	
def send_email_using_mandrill(data, url, api_key):

	try:
		message = {}
		message['text'] = data['body']
		message['subject'] = data['subject']
		message['from_email'] = data['from']
		message['from_name'] = data['from_name']
		message['to'] = [{'email': data['to'],'name': data['to_name'], 'type': 'to'}]
		
		params = {}
		params['message'] = message
		params['key'] = api_key
		
		if 'send_at' in data and data['send_at']:
			try:
				local_timezone = timezone(settings.TIMEZONE)
				date = local_timezone.localize(datetime.strptime(data['send_at'], '%Y-%m-%d %H:%M:%S'))
				params['sent_at'] = date.strftime('%Y-%m-%d %H:%M:%S')
			except ValueError, e:
				log.exception(e.message)
				abort(400, 'Invalid delivery date/time provided. Please provide date/time in the format Y-m-d H:M:S')

		response = requests.post(
			url,
			data=json.dumps(params))
		log.debug('response from server: ' + response.text)
		if response.status_code != 200:
			return response.text
		if response and json.loads(response.text)[0]['status'] == 'error':
			return response.text
	except Exception,e:
		log.exception(e.message)
		return e.message
	return 'success'
	

def validations(data):
	"""
	This function performs all the necessary validations on all the fields 
	before sending an email.
	"""
	required_fields = ('to', 'to_name', 'from', 'from_name', 'subject', 'body')
	for field in required_fields:
		if field not in data:
			log.exception('missing value for - %s' % field)
			abort(400, 'missing value for - %s' % field)
		if not data[field]:
			log.exception('blank value cannot be provided for - %s' % field)
			abort(400, 'blank value cannot be provided for - %s' % field)
	
	if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['to']):
		log.exception('Invalid receiver email address')
		abort(400, 'Invalid receiver email address')
	if not re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['from']):
		log.exception('Invalid sender email address')
		abort(400, 'Invalid sender email address')

	data['body'] = html2text.html2text(data['body'])
	return data

@app.route("/")
def home():
	return make_response('Only the "/email" endpoint is supported by this webservice.')
	
	
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

	
if __name__ == "__main__":
	init_db()
	app.run(host='0.0.0.0',port=settings.SERVER_PORT)