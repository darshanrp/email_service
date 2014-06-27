from array import array
from exceptions import Exception
from flask import Flask, request, render_template, make_response, abort
import html2text
import json
import logging
import re
import requests
import settings

log = logging.getLogger(__name__)

app = Flask(__name__)

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
		#response.headers['Access-Control-Allow-Origin'] = '*'

		if send_email(data):
			return make_response("Email sent successfully!")
		else:
			abort(500, "Error sending email. Check logs for error details.")


def send_email(data):
	"""
	This is a helper function for sending emails based on the settings 
	provided in the settings.py file.
	"""
	if not settings.URL:
		abort(500,'Email provider URL is not set')
	if not settings.API_KEY:
		abort(500,'Email provider API_KEY is not set')

	if settings.EMAIL_PROVIDER == 'MAILGUN':
		return send_email_using_mailgun(data, settings.URL, settings.API_KEY)
	elif settings.EMAIL_PROVIDER == 'MANDRILL':
		return send_email_using_mandrill(data, settings.URL, settings.API_KEY)


def send_email_using_mailgun(data, url, api_key):
	try:
		data['from'] = data['from_name'] + ' <' + data['from'] + '>'
		data['to'] = data['to_name'] + ' <' + data['to'] + '>'
		data['text'] = data['body']
		response = requests.post(
			url, auth=('api', api_key),
			data=data)
		response = None
		log.debug('response from server: ' + response.text)
	except Exception,e:
		log.exception(e.message)
		return False
	return True
	
	
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
		response = requests.post(
			url,
			data=json.dumps(params))
		log.debug('response from server: ' + response)
	except Exception,e:
		log.exception(e.message)
		return False
	return True
	

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
	return render_template('usage.html')


if __name__ == "__main__":
	app.debug = True
	app.run(host='0.0.0.0',port=8081)