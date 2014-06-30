import json
import requests
import settings
import unittest

class TestEmailService(unittest.TestCase):

	def setUp(self):
		self.data={"to":"darshanpandhi87@gmail.com","to_name":"Darshan Pandhi","from":"darshan@mail.com","from_name":"DarshanP","subject":"A message from Mailgun test","body":"<h1>Your bill</h1><p>$10</p>"}
		self.header = {'Content-Type': 'application/json'}		
	
	def test_data_validations(self):
		data = self.data
		data["to"]=None
		response = requests.post('http://localhost:' + str(settings.SERVER_PORT) + '/email',data=json.dumps(data),headers=self.header)
		self.assertEqual(400, response.status_code)
		self.assertTrue(('blank value cannot be provided for - to' in response.text))
		
	def test_missing_values_in_request(self):
		data = self.data
		data.pop('to', None)
		response = requests.post('http://localhost:' + str(settings.SERVER_PORT) + '/email',data=json.dumps(data),headers=self.header)
		self.assertEqual(400, response.status_code)
		self.assertTrue(('missing value for - to' in response.text))

	def test_sending_emails(self):
		response = requests.post('http://localhost:' + str(settings.SERVER_PORT) + '/email',data=json.dumps(self.data),headers=self.header)
		self.assertEqual(200, response.status_code)
		self.assertTrue('success' in response.text)	

	
def main():
	unittest.main()
	
	
if __name__ == '__main__':
	main()