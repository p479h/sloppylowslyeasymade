
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from os import getcwd, path, chdir
import sys
print(sys.path)
if __name__ == "__main__":
    from Universe_page import *
    from Objects_page import *
    from Last_page import *
    sys.path.insert(1, r"C:\Users\phfer\Desktop\Python\Physics")  # To allow to use Physics
    from Physics import Physics
    from Object import Object, Large_object, Sun, Planet, Moon


try:
    if getattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
        print('running in a PyInstaller bundle')
        bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    else:
        print('running in a normal Python process')
        bundle_dir = path.join(getcwd(),"GUI", "icons")
except:
    bundle_dir = path.join(getcwd(), "GUI","icons")


class Window(tk.Tk):
    """This will be the actual frame where all other actions take place."""

    def __init__(self, geometry='500x400', title='My universe', *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry(geometry)
        self.title(title)
        self.image_path = bundle_dir
        self.icon = tk.PhotoImage(file=path.join(self.image_path, 'planet.png'))
        self.iconphoto(False, self.icon)
        self.grid_propagate(False)
        self.frames = {}
        self.universe = None  # Placeholder
        self.objects = []

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    def update_pages(self, *pages):
        for page in pages:
            self.frames[page.name] = page
            page.grid(column=0, row=0, sticky="NSEW")
        self.frames['Universe'].tkraise()


class Controls_container(tk.Frame):
    """This will be the frame sitting bellow the titleE"""

    def __init__(self, container, height=320, width=450, relief="sunken", *args, **kwargs):
        tk.Frame.__init__(self, container, *args, **kwargs)
        self.config(height=height, width=width, relief=relief, bd=1)
        self.grid_propagate(False)


if __name__ == "__main__":
    window = Window()
    page1 = Universe_page(window)
    page2 = Objects_page(window)
    page3 = Last_page(window)
    window.update_pages(page1, page2, page3)
    window.mainloop()

#
#
# window = Master(geometry='500x490', title="My universe")
# Current_page = General_page(window)
# Current_frame = Current_page.main_frame
# for x in range(10):
#     button = tk.Button(Current_frame, text=f"{x}")
#     button.grid()
# # Other_page = General_page(window, label="Other_universe")
# window.mainloop()
