
import select
import socket
import threading

from config import Config
from helpers import make_request, read_broadcast_packet


class MessageManager:

	def __init__(self, parent):
		self.parent = parent

		# Default handler when none is set
		self.msg_handler = lambda resp: print(resp)

		self.connect_to_message_server()


	def bind_message_handler(self, func):
		self.msg_handler = func


	def send_message(self, msg):
		...


	def connect_to_message_server(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((Config.BROADCAST_HOST, Config.BROADCAST_PORT))
		self.broadcast_conn = s

		broadcast_handle_thread = threading.Thread(
			target=self.broadcast_handle_loop)
		broadcast_handle_thread.start()


	def broadcast_handle_loop(self):
		# Send our token
		self.broadcast_conn.send(self.parent.controller.token.encode())
		resp = read_broadcast_packet(self.broadcast_conn)
		print(f" [*] {resp['msg']}")

		if "error" in resp:
			print("ERROR: ", resp)
			return

		while self.parent.controller.token is not None:
			ready = select.select(
				[self.broadcast_conn], [], [],
				Config.BROADCAST_POLL_DELAY)

			if ready[0]:
				resp = read_broadcast_packet(self.broadcast_conn)
				
				# Handle the message!
				self.msg_handler(resp)

		self.broadcast_conn.send("EXIT".encode())
		self.broadcast_conn.close()
		self.broadcast_conn = None
