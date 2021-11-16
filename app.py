import requests
import json
from urllib.parse import urljoin
import time
import local_settings

SECRET = local_settings.SECRET


class Diffy(object):
	def __init__(self):
		self.secret = SECRET
		self.base_url = "https://app.diffy.website"
		self.token = None
		self.project_id = None

	def post(self, url, payload):
		print("POST URL: {}".format(url))
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
			}
		if self.token:
			headers["Authorization"] = "Bearer {}".format(self.token)
		return requests.post(url, data=json.dumps(payload), headers=headers)
	
	def get(self, url):
		print("GET URL: {}".format(url))
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
			}
		if self.token:
			headers["Authorization"] = "Bearer {}".format(self.token)
		return requests.get(url, headers=headers)

	def delete(self, url):
		print("DELETE URL: {}".format(url))
		headers = {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
			}
		if self.token:
			headers["Authorization"] = "Bearer {}".format(self.token)
		return requests.delete(url, headers=headers)

	def get_token(self):
		url = urljoin(self.base_url, "/api/auth/key")
		payload = {"key": self.secret}
		response = self.post(url, payload)
		self.token = json.loads(response.text).get('token')

	def create_project(self):
		url = urljoin(self.base_url, "/api/projects")
		project_name = '{}-{}'.format('Ayaz', int(time.time()))
		base_url = "https://blog.ayaz.pk"
		payload = {
			"name": base_url, 
			"baseUrl": base_url,
			"urls": [base_url],
			"staging": base_url,
			"scanUrl": '',
			"advanced": {
				"psScreenshotDelay": True,
				"psScreenshotDelaySec": 20,
				"psScreenshotLimitWorkersProdNumber": 30,
				"psScreenshotLimitWorkersNonProdNumber": 10,
				"psScreenshotScroll": False,
				"psScreenshotHeaders": False,
				"psScreenshotHeadersList": {}
			}
		}
		response = self.post(url, payload)
		if response.status_code == 200:
			self.project_id = int(response.text)

	def get_project(self):
		url = urljoin(self.base_url, '/api/projects/{}'.format(self.project_id))
		return self.get(url)

	def remove_project(self):
		url = urljoin(self.base_url, '/api/projects/{}'.format(self.project_id))
		return self.delete(url)

	def take_screenshot(self):
		url = urljoin(self.base_url,
					'/api/projects/{}/screenshots'.format(self.project_id)
				)
		base_url = "https://blog.ayaz.pk"		
		payload = {
			'environment': 'production',
			'baseUrl': 'base_url'
		}
		return self.post(url, payload)
		

if __name__ == '__main__':
	d = Diffy()
	r = d.get_token()
	r = d.create_project()

	r = d.take_screenshot()
	print(r.status_code)
	print(r.text)

	r = d.get_project()
	print(r.status_code)
	print(r.text)

	r = d.remove_project()
