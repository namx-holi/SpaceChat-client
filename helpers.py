
import json
import requests
import struct
import traceback

from config import Config
BASE_API_URL = f"http://{Config.HOST}:{Config.PORT}/api"


def make_request(endpoint, data):
	url = f"{BASE_API_URL}/{endpoint}"

	# Try make request
	try:
		r = requests.post(url=url, json=data)
	except requests.exceptions.ConnectionError as e:
		print(" [!] Error in making request")
		traceback.print_exc()
		raise e

	# Try read response
	try:
		resp = r.json()
	except Exception as e:
		print(r.text)
		raise e

	print(f"RESP: {resp}")
	return resp


def read_broadcast_packet(conn):
	len_bytes = conn.recv(4)
	content_len = struct.unpack("I", len_bytes)[0]

	content_bytes = conn.recv(content_len)
	content = content_bytes.decode()
	return json.loads(content)
