
import tkinter as tk
# import tkinter.messagebox as tm

from pages.page_base import PageBase
from message_manager import MessageManager


class MainPage(PageBase):

	def __init__(self, parent, controller):
		if not controller.token:
			controller.switch_frame("LoginPage")

		super().__init__(parent, controller)
		controller.title("SpaceChat client")

		self.token_label = tk.Label(self, text=self.controller.token)
		self.token_label.grid(row=1, columnspan=1, sticky=tk.E)

		self.logout_btn = tk.Button(self, text="Logout",
			command=self._logout_btn_clicked)
		self.logout_btn.grid(row=2, columnspan=1)

		self.incoming_message_box_scrollbar = tk.Scrollbar(self)
		self.incoming_message_box = tk.Text(self, height=4, width=50)
		self.incoming_message_box_scrollbar.grid(row=1, column=3, rowspan=2)
		self.incoming_message_box.grid(row=1, column=2, rowspan=2)
		self.incoming_message_box_scrollbar.config(
			command=self.incoming_message_box.yview)
		self.incoming_message_box.config(
			yscrollcommand=self.incoming_message_box_scrollbar.set)

		self.pack()

		# Set up keyboard shortcuts
		self.add_binding("<l>", self._logout_btn_clicked)

		# Connect to the message server!
		self.msg_manager = MessageManager(self)
		self.msg_manager.bind_message_handler(
			lambda resp: self.incoming_message_box.insert(tk.END, repr(resp)))


	def _logout_btn_clicked(self, event=None):
		self.controller.token = None
		self.controller.switch_frame("LoginPage")


	def close(self):
		self.clear_bindings()

		# Close broadcast server connection
		# Done by the token being set to None