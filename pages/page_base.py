
import tkinter as tk


class PageBase(tk.Frame):

	def __init__(self, parent, controller):
		super().__init__(parent)
		self.controller = controller

		# Used for keyboard shortcuts
		self.bindings = []


	def add_binding(self, key, func):
		# Adds a keyboard shortcut function binding
		self.controller.bind(key, func)
		self.bindings.append(key)


	def clear_bindings(self):
		print(" [*] Clearing bindings called from {}!".format(type(self)))
		# Removes all keyboard shortcut function bindings
		for binding in self.bindings:
			self.controller.unbind(binding)


	def close(self):
		self.clear_bindings()
