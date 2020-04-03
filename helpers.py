
import json
import requests

from config import Config
BASE_API_URL = f"http://{Config.HOST}:{Config.PORT}/api"


def make_request(endpoint, data):
	url = f"{BASE_API_URL}/{endpoint}"

	# Try make request
	try:
		r = requests.post(url=url, json=data)
	except requests.exceptions.ConnectionError as e:
		tm.showerror("Server Error", "Server is down")
		raise e

	# Try read response
	try:
		resp = r.json()
	except Exception as e:
		print(r.text)
		raise e

	print(resp)
	return resp
