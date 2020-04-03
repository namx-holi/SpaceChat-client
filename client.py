import tkinter as tk
import tkinter.messagebox as tm

from pages.login_page import LoginPage
from pages.main_page import MainPage

# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter


# TODO: Centre window
# TODO: Start message handler
# TODO: Etc



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
		for F in (LoginPage, MainPage):
			page_name = F.__name__
			self.frame_classes[page_name] = F

		self._frame = None
		self.switch_frame("LoginPage")


	def switch_frame(self, page_name):
		# Show a frame for the given page name
		# NOTE: Creates an instance for the frame.

		# Create new frame
		frame_class = self.frame_classes[page_name]
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



if __name__ == "__main__":
	app = ClientApp()
	app.mainloop()
