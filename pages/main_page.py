
import tkinter as tk
# import tkinter.messagebox as tm

from pages.page_base import PageBase


class MainPage(PageBase):

	def __init__(self, parent, controller):
		if not controller.token:
			controller.switch_frame("LoginPage")

		super().__init__(parent, controller)
		controller.title("SpaceChat client")

		self.token_label = tk.Label(self, text=self.controller.token)
		self.token_label.grid(columnspan=2, sticky=tk.E)

		self.logout_btn = tk.Button(self, text="Logout",
			command=self._logout_btn_clicked)
		self.logout_btn.grid(columnspan=2)

		self.pack()

		# Set up keyboard shortcuts
		self.add_binding("<l>", self._logout_btn_clicked)


	def _logout_btn_clicked(self, event=None):
		self.controller.token = None
		self.controller.switch_frame("LoginPage")
