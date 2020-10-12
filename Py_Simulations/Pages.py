"""
    This document contains all under the name "IMAGES" and it
    contains 2 classes. The first class, `Page`, contains the
    initialization of a page on a renderer(assumed as root).

    Furthermore it has code that builds the physical structure
    of the first page, which contains buttons that will lead
    to the simulations.
    """
import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib as mpl


#The next two imports are from self-made files.
from images import IMAGES
from messages import m1#Message for tk.messagebox about creation
                       #of duplicate first page


IMAGES = IMAGES #This contains all images needed in the GUI.
#{'planet_icon': , 'question_icon': , 'box_icon': , 'time_icon':,
#'arrow_right':, 'arrow_left':, ...}

class Page(tk.Frame):
    """
        This class contains the general layout for
        a page.
        Parameters
        --------------
        name: str -> Name of the page. This allows
        for identification of pages.

        """
    instances = {} #Will contain ALL the pages of the GUI

    conversions = {
            "nm":1e-9, "μm":1e-6, "mm":1e-3, "cm":1e-2,
            "dm":0.1, "m":1, "km":1e3, "Mm":1e6, "Gm":1e9,
            "μm":1e-6, "ms":1e-3, "s":1, "min":60, "hour":3600,
            "day":3600*24, "month":3600*24*30, "year":3600*24*30*12,
            "km/s":1e3, "kg/m3":1, "g/m3":1e-3, "C/kg":1, "C/g":1e3,
            "C/mg":1e6, "m/s":1, "kg":1}

    def __init__(self, master=False, name = "start", *args, **kwargs):
        #First we make sure the parent can resize
        master.geometry("510x400")
        master.update()
        master.columnconfigure([0], weight=1)
        master.rowconfigure([0], weight=1)

        #There is a bug that causes tkinter to not close sometimes
        #It is solved using the following code line
        master.protocol("WM_DELETE_WINDOW", lambda: [master.quit(),
                                                     master.destroy(),
                                                     plt.close("all")])

        #Then we create the frame object and place it in the parent
        tk.Frame.__init__(self, master,
                          *args, **kwargs)

        self.grid(column = 0, row = 0, sticky = "NSEW")

        #This part ensures that there is only one starting page
        #It also works as reminder in case I forget to pass an id
        #to a page.
        if name == "start" and "start" in self.__class__.instances:
            tk.messagebox.showwarning("GIVE NAME", m1)
        elif "start" not in self.__class__.instances:
            img = ImageTk.PhotoImage(IMAGES["time_icon"].resize((30, 30)))
            master.iconphoto(False, img)
            master.title("Predru's simulator")


        self.__class__.instances[name] = self
        #Now you can access the newly created instance
        #by calling Page.pages[f"{pagename}"]
        # Current pages
        # -------------
        # "main_page": Entrance of the app
        # "page1" : Solar system page
        # "page1_1": Settings for planet simualtion.
        # "page1_2": Simulation planets
        # "page4":Clock

        #This is just a list of colors for whenever colors are needed

        TABLEAU_COLORS2 = [c.strip("tab:") for c in list(mpl._color_data.TABLEAU_COLORS)]
        TABLEAU_COLORS2[0] = "blue"
        self.colors = TABLEAU_COLORS2
        self.all_colors = list(mpl._color_data.CSS4_COLORS)
        self.markers = list(mpl.markers.MarkerStyle.markers)
        self.colors+=["yellow", "white"]

    def make_navigation_buttons(self, forward = False, backward = False):
        """
            This creates the buttons that allow to go to other pages
            self.change_page() takes in the page you want to go to
            and return a function that raises that page.
            It just makes the buttons! It does not place them.
            """
        if forward:
            self.r = ImageTk.PhotoImage(IMAGES['arrow_right'].resize((20,20)))
            self.forward_button = ttk.Button(self,
                                     image = self.r,
                                     takefocus = 0,
                                     command = self.change_page(forward))
        if backward:
            self.l = ImageTk.PhotoImage(IMAGES['arrow_left'].resize((20,20)))
            self.backward_button = ttk.Button(self,
                                     image = self.l,
                                     takefocus = 0,
                                     command = self.change_page(backward))



    def change_page(self, where):
        """
            Changes current page that is being displayed
            Parameters
            ----------
            where: str -> page name
            """
        def switch():
            try:
                self.__class__.instances[where].grid(
                    row = 0, column = 0,
                    sticky = "NSEW") #Makes it easier to handle resize
                self.__class__.instances[where].tkraise()
                self.grid_forget()
            except : print("NOT IMPLEMENTED")
        return switch

    def delete_canvas(self):
        if hasattr(self, "running"):
            self.running = False
        if hasattr(self, "universe"):
            self.universe.running = False
        if hasattr(self, "canvas"):
            setattr(self, "running", False)
            for x in range(20):#Makes nice fading pattern.
                for a in self.ax.get_children():
                    a.set_alpha((20-x)/20)
                self.canvas.draw()
            self.ax.figure.clear()
            plt.close('all')
            self.canvas.get_tk_widget().delete("all")
            self.canvas.get_tk_widget().grid_forget()
            self.canvas.get_tk_widget().destroy()
            self.main_frame.update()
            delattr(self, "canvas")


class Main_page(Page):
    """
        This is the first page of the application.
        It makes use of the class defined above to
        configure the widgets and other parameters
        """
    def __init__(self, *args, **kwargs):
        Page.__init__(self, name = "main_page", *args, **kwargs)
        self.master.geometry("510x400")
        self.master.update()

        #The next part makes the use of grid easier
        #The idea is to use many squares like large pixels
        grid_len = [x for x in range(30)]
        minsize = (self.master.winfo_width()/30,
                   self.master.winfo_height()/30)

        self.columnconfigure(grid_len,
                             minsize = minsize[0],
                             weight = 1,
                             )

        self.rowconfigure(grid_len,
                          minsize = minsize[1],
                          weight=1,
                          )

        self.main_frame = tk.Frame(self,
                                   relief = "sunken",
                                   border = 1
                                   )

        self.main_frame.grid(column=1, row=1, sticky="NSEW",
                             columnspan=28, rowspan = 28,
                             )
        self.main_frame.update()
        grid_len = [x for x in range(30)]
        minsize = (self.main_frame.winfo_width()/30,
                   self.main_frame.winfo_height()/30)
        self.main_frame.rowconfigure(grid_len,
                                     minsize = minsize[1],
                                     weight =1
                                     )

        self.main_frame.columnconfigure(grid_len,
                                        minsize = minsize[0],
                                        weight = 1,
                                        )

        self.make_navigation_buttons(forward = "page2",backward = "None")
        self.forward_button.grid(row = 27, column = 28,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )
        self.forward_button.config(cursor ="pirate")

        self.backward_button.grid(row = 27, column = 26,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                  )
        self.backward_button.config(cursor = "pirate")

        #Since we can't edit the font, a dummy variable with a style will be made
        s = ttk.Style()
        s.configure("new.TButton", font = ("Consolas","15","bold"))
        self.planet_icon = ImageTk.PhotoImage(IMAGES["planet_icon"].resize((80,80)))
        self.large_sim_button = ttk.Button(self.main_frame,
                                           text="Large scale",
                                           image = self.planet_icon,
                                           takefocus = 0,
                                           compound = tk.BOTTOM,
                                           style = "new.TButton",
                                           command = self.change_page("page1"),
                                           )

        self.large_sim_button.grid(row=2, column=3,
                                   rowspan=13, columnspan = 11,
                                   sticky="NSEW",
                                   )

        self.question_icon = ImageTk.PhotoImage(IMAGES["question_icon"].resize((80,80)))
        self.help_button = ttk.Button(self.main_frame,
                                      text = "Help",
                                      image = self.question_icon,
                                      takefocus = 0,
                                      compound =tk.BOTTOM,
                                      style = "new.TButton",
                                      command = self.change_page("helppage"),
                                      cursor = "pirate"
                                      )

        self.help_button.grid(row=2, column=14, rowspan=13,
                              columnspan = 11, sticky = "NSEW",
                              )

        self.time_icon = ImageTk.PhotoImage(IMAGES["time_icon"].resize((80, 80)))
        self.spring_icon = ImageTk.PhotoImage(IMAGES["spring_icon"].resize((80,80)))
        self.coils_button = ttk.Button(self.main_frame,
                                      text = "Hook's law",
                                      image = self.spring_icon,
                                      takefocus = 0,
                                      compound =tk.BOTTOM,
                                      style = "new.TButton",
                                      command = lambda: [
                                          self.change_page("page3")(),
                                          self.master.geometry("550x500"),
                                          ],
                                      cursor = "pirate",
                                      )
        self.coils_button.grid(row=15, column=3,
                              rowspan=13, columnspan = 11,
                              sticky="NSEW",
                              )

        self.sub_icon = ImageTk.PhotoImage(IMAGES["time_icon"].resize((80, 80)))
        self.subatomic_b = ttk.Button(self.main_frame,
                                      text = "Subatomic",
                                      image = self.time_icon,
                                      takefocus = 0,
                                      compound =tk.BOTTOM,
                                      style = "new.TButton",
                                      command = self.change_page("page4"),
                                      )

        self.subatomic_b.grid(row=15, column=14,
                              rowspan=13, columnspan = 11,
                              sticky="NSEW",
                              )



if __name__ == "__main__":
    """This part is just for testing"""
    window = tk.Tk()
    main_page = Main_page(window)
    window.mainloop()
