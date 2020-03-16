import json
import requests
import tkinter as tk
import tkinter.messagebox as tm


HOST = "0.0.0.0"
PORT = 7777
BASE_API_URL = f"http://{HOST}:{PORT}/api"


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



class LoginFrame(tk.Frame):

	def __init__(self, master):
		super().__init__(master)

		self.label_username = tk.Label(self, text="Username")
		self.label_password = tk.Label(self, text="Password")

		self.entry_username = tk.Entry(self)
		self.entry_password = tk.Entry(self, show="*")

		self.label_username.grid(row=0, sticky=tk.E)
		self.label_password.grid(row=1, sticky=tk.E)
		self.entry_username.grid(row=0, column=1)
		self.entry_password.grid(row=1, column=1)

		self.login_btn = tk.Button(self, text="Login",
			command=self._login_btn_clicked)
		self.login_btn.grid(columnspan=2)

		# Make it so you can press enter to log in
		master.bind("<Return>", self._login_btn_clicked)

		# Focus the username entry!
		self.entry_username.focus()

		self.pack()


	def _login_btn_clicked(self, event=None):
		username = self.entry_username.get()
		password = self.entry_password.get()

		data = dict(username=username, password=password)
		resp = make_request("login", data)

		if "error" in resp:
			tm.showerror("Login error", resp["error"])
			return

		token = resp.get("token", None)
		tm.showinfo("Logged in", f"Your token is {token}")

		# TODO: Turn this frame into main app frame


root = tk.Tk()
root.focus_force() # Doesn't work on mac
lf = LoginFrame(root)
root.mainloop()
