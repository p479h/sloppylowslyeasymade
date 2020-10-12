import numpy as np
import matplotlib as mpl
import tkinter as tk
from PIL import Image, ImageTk
from os import getcwd, path
import tkinter.ttk as ttk
from Frontpage import Controls_container
from matplotlib.pyplot import show

if __name__ == "__main__":
    from Frontpage import Window
    from Universe_page import Universe_page
    from Objects_page import Objects_page


class Last_page(tk.Frame):
    def __init__(self, window, label="Last", *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)
        self.config(height=window.winfo_height(),
                    width=window.winfo_width())
        self.name = label
        self.parent = window
        self.name_label = tk.Label(self, text=label, font="sans-serif")
        self.name_label.grid(padx=4, pady=4, row=0, sticky="W")
        self.control_pannel = Controls_container(self)
        self.control_pannel.grid(row=1, column=0, padx=10, sticky='NSEW')
        self.control_pannel.grid_propagate(False)

        def backward(): return window.show_frame("Objects")
        self.back_button = tk.Button(self, text="<-", command=backward)
        self.back_button.grid(row=2, column=0, sticky="E", pady=4)

        def play():
            if self.parent.universe:
                self.parent.universe.fig.canvas.draw()
                self.parent.universe.fig.canvas.flush_events()
                try:
                    oo = self.parent.frames['Objects page']
                    oo.delete_object.place_forget()
                    oo.delete_object_info.place_forget()
                    delattr(oo, "delete_object")
                except:
                    None
            try:
                show()
            except:
                None
            try:
                plt.close("all")
            except:
                None
        self.play_button = tk.Button(self.control_pannel, text="Play!", command=play, bg="green")
        self.play_button.grid(column=0, row=0, padx=10, pady=1)
        self.play_button.config(height=10, width=10)
