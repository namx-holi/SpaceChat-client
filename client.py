import json
import requests
import tkinter as tk
import tkinter.messagebox as tm

# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter


HOST = "0.0.0.0"
PORT = 7777
BASE_API_URL = f"http://{HOST}:{PORT}/api"

# TODO: Centre window
# TODO: Start message handler
# TODO: Etc


# TODO: Move to helpers
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



class ClientApp(tk.Tk):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		self.token = None

		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		self.container = container

		self.frame_classes = {}
		for F in (LoginPage, ClientPage):
			page_name = F.__name__
			self.frame_classes[page_name] = F

		self._frame = None
		self.switch_frame(LoginPage)


	def switch_frame(self, frame_class):
		# Show a frame for the given page name
		# NOTE: Creates an instance for the frame.

		# Create new frame
		frame = frame_class(parent=self.container, controller=self)

		# Clear bindings and delete old frame
		if self._frame is not None:
			self._frame.clear_bindings()
			self._frame.destroy()

		# Set new current frame
		self._frame = frame

		# Put all of the pages in the same location;
		# the one on the top of the stacking order
		# will be the one that is visible.
		frame.grid(row=0, column=0, sticky="nsew")
		frame.tkraise()


	# TODO: Method to show a new window



class LoginPage(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)
		controller.title("Login")
		self.controller = controller

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
		self.set_bindings()


	def set_bindings(self):
		self.bindings = []

		# Make it so you can press enter to log in
		self.controller.bind("<Return>", self._login_btn_clicked)
		self.bindings.append("<Return>")


	def clear_bindings(self):
		for binding in self.bindings:
			self.controller.unbind(binding)


	def _login_btn_clicked(self, event=None):
		username = self.entry_username.get()
		password = self.entry_password.get()

		# Clear error message before sending response
		self.label_error.configure(text="")
		data = dict(username=username, password=password)
		resp = make_request("login", data)

		if "error" in resp:
			self.label_error.configure(text=resp["error"])
			return

		token = resp.get("token", None)
		# tm.showinfo("Logged in", f"Your token is {token}")

		# Set the parent's token to received token
		self.controller.token = token
		self.controller.switch_frame(ClientPage)



class ClientPage(tk.Frame):

	def __init__(self, parent, controller):
		if not controller.token:
			controller.switch_frame(LoginPage)

		super().__init__(parent)
		controller.title("SpaceChat client")
		self.controller = controller

		self.token_label = tk.Label(self, text=self.controller.token)
		self.token_label.grid(columnspan=2, sticky=tk.E)

		self.logout_btn = tk.Button(self, text="Logout",
			command=self._logout_btn_clicked)
		self.logout_btn.grid(columnspan=2)

		self.pack()
		self.set_bindings()


	def set_bindings(self):
		self.bindings = []

		# Make it so you can press enter to log in
		self.controller.bind("<l>", self._logout_btn_clicked)
		self.bindings.append("<l>")


	def clear_bindings(self):
		for binding in self.bindings:
			self.controller.unbind(binding)


	def _logout_btn_clicked(self, event=None):
		self.controller.token = None
		self.controller.switch_frame(LoginPage)



if __name__ == "__main__":
	app = ClientApp()
	app.mainloop()
