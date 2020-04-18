
import tkinter as tk
import tkinter.messagebox as tm

from helpers import make_request
from message_manager import MessageManager
from pages.page_base import PageBase


class MainPage(PageBase):

	def __init__(self, parent, controller):
		if not controller.token:
			controller.switch_frame("LoginPage")

		super().__init__(parent, controller)
		controller.title("SpaceChat client")

		# Token shower
		self.token_label = tk.Label(self, text=self.controller.token)
		self.token_label.grid(row=1, columnspan=1, sticky=tk.E)

		# Logout Button
		self.logout_btn = tk.Button(self, text="Logout",
			command=self._logout_btn_clicked)
		self.logout_btn.grid(row=2, columnspan=1)

		# Incoming message box
		self.incoming_message_box = tk.Text(self, height=4, width=50)
		self.incoming_message_box_scrollbar = tk.Scrollbar(self)
		self.incoming_message_box.grid(row=1, column=2, rowspan=2)
		self.incoming_message_box_scrollbar.grid(row=1, column=3, rowspan=2, sticky="NSW")
		self.incoming_message_box_scrollbar.config(
			command=self.incoming_message_box.yview)
		self.incoming_message_box.config(
			yscrollcommand=self.incoming_message_box_scrollbar.set,
			state="disabled") # prevents user from typing in it

		# Outgoing message box
		self.outgoing_message_box = tk.Entry(self, width=50)
		self.outgoing_message_box.grid(row=3, column=2, rowspan=1)
		# We want to add a binding just to the message sending box
		self.outgoing_message_box.bind("<Return>", self._send_message)

		self.pack()

		# Set up global keyboard shortcuts
		# TODO: Test on windows
		self.add_binding("<Alt-l>", self._logout_btn_clicked)
		self.add_binding("<Command-l>", self._logout_btn_clicked) # Mac

		# Connect to the message server!
		self.msg_manager = MessageManager(self)
		self.msg_manager.bind_message_handler(self.message_handler)
		self.add_text_to_incoming("Logged into server!")


	def add_text_to_incoming(self, text):
		# Used to add text to the incoming box
		self.incoming_message_box.configure(state="normal")
		self.incoming_message_box.insert("end", text)
		self.incoming_message_box.see("end") # Scrolls to bottom
		self.incoming_message_box.configure(state="disabled")


	def message_handler(self, resp):
		msg_type = resp.get("type", None)
		if msg_type is None:
			# TODO: Error?
			print(resp)

		elif msg_type == "generic":
			# TODO
			print(resp)

		elif msg_type == "user":
			username = resp["username"]
			msg = resp["msg"]

			msg_format = f"\n{username}: {msg}"
			self.add_text_to_incoming(msg_format)

		elif msg_type == "whisper":
			from_user = resp["username"]
			to_user = resp["recipient"]
			msg = resp["msg"]

			msg_format = f"\nwhisper from {from_user} to {to_user}: {msg}"
			self.add_text_to_incoming(msg_format)

		elif msg_type == "server":
			msg = resp["msg"]
			tm.showinfo("Server Message", msg)

		elif msg_type == "alert":
			msg = resp["msg"]

			msg_format = f"\nALERT! {msg}"
			self.add_text_to_incoming(msg_format)

		else:
			# TODO: Error? Unsupported format
			print(resp)


	def _logout_btn_clicked(self, event=None):
		self.controller.token = None

		# TODO: Move this to some request handler
		make_request("logout", dict(token=self.controller.token))

		self.controller.switch_frame("LoginPage")


	def _send_message(self, event=None):
		msg = self.outgoing_message_box.get()
		# Clear message box
		self.outgoing_message_box.delete(0,"end")

		if msg == "":
			return

		self.msg_manager.send_message(msg)
