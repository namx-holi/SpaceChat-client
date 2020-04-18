
import tkinter as tk

from helpers import make_request


class PageBase(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		# Used for keyboard shortcuts
		self.bindings = []

		# Makes sure users are logged out on quit
		self.controller.protocol("WM_DELETE_WINDOW", self.on_quit)


	def on_quit(self):
		print(" [*] Exiting.")
		if self.controller.token is not None:
			make_request("logout", dict(token=self.controller.token))
		self.controller.destroy()


	def add_binding(self, key, func):
		# Adds a global keyboard shortcut function binding
		self.controller.bind(key, func)
		self.bindings.append(key)


	def clear_bindings(self):
		print(" [*] Clearing bindings called from {}!".format(type(self)))
		# Removes all global keyboard shortcut function bindings
		for binding in self.bindings:
			self.controller.unbind(binding)


	def close(self):
		self.clear_bindings()
