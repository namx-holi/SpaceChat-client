from requests.exceptions import ConnectionError
import tkinter as tk
# import tkinter.messagebox as tm

from helpers import make_request
from pages.page_base import PageBase


class LoginPage(PageBase):

	def __init__(self, parent, controller):
		super().__init__(parent, controller)
		controller.title("Login")

		self.label_username = tk.Label(self, text="Username")
		self.label_password = tk.Label(self, text="Password")

		self.entry_username = tk.Entry(self)
		self.entry_password = tk.Entry(self, show="*")

		# To show errors with
		self.label_error = tk.Label(self, text="", fg="red", font=("Courier", 10))

		self.label_username.grid(row=0, sticky=tk.E)
		self.label_password.grid(row=1, sticky=tk.E)
		self.entry_username.grid(row=0, column=1)
		self.entry_password.grid(row=1, column=1)
		self.label_error.grid(columnspan=2)

		self.login_btn = tk.Button(self, text="Login",
			command=self._login_btn_clicked)
		self.login_btn.grid(columnspan=2)

		# Focus the username entry!
		self.entry_username.focus()

		self.pack()

		# Set up keyboard shortcuts
		self.add_binding("<Return>", self._login_btn_clicked)


	def _login_btn_clicked(self, event=None):
		username = self.entry_username.get()
		password = self.entry_password.get()
		# Clear the password field
		self.entry_password.delete(0, "end")

		# Clear error message before sending response
		self.label_error.configure(text="")
		data = dict(username=username, password=password)

		# Make a login attempt
		try:
			resp = make_request("login", data)
		except ConnectionError as e:
			self.label_error.configure(text="Cannot connect to server")
			return

		if "error" in resp:
			self.label_error.configure(text=resp["error"])
			return

		token = resp.get("token", None)
		# tm.showinfo("Logged in", f"Your token is {token}")

		# Set the parent's token to received token
		self.controller.token = token
		self.controller.switch_frame("MainPage")
