from Pages import Page, IMAGES, Main_page, np, ImageTk, ttk, tk
from Page1 import Page1
import matplotlib.pyplot as plt
import matplotlib as mpl
from DirPage4 import time_ as t
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
mpl.use("TkAgg")
mpl.style.use("fast")

class Page4(Page):
    """
    This is the page that has support for planetary motion
    """
    def __init__(self, *args, **kwargs):
        Page.__init__(self, name = "page4", *args, **kwargs)
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
                             columnspan=22, rowspan = 28,
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

        self.make_navigation_buttons(forward = "page2",backward = "main_page")
        self.backward_button.config(command = lambda: [self.delete_canvas(),
                                                       self.change_page("main_page")()])
        self.forward_button.grid(row = 27, column = 28,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )

        self.backward_button.grid(row = 27, column = 26,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                  )


        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################

        self.make_clock_b = ttk.Button(self,
                                       text = "Make clock",
                                       command = self.make_clock,
                                       takefocus = 0
                                        )
        self.clock_but = ttk.Button(self,
                                    text = "Play",
                                    takefocus = 0,
                                    command = lambda: t.show_time(self))

        self.clock_stop = ttk.Button(self,
                                    text = "Stop",
                                    takefocus = 0,
                                    command = lambda: setattr(self,
                                    "running", False))

        self.clock_rem_b = ttk.Button(self,
                                    text = "Remove",
                                    takefocus = 0,
                                    command = self.delete_canvas,
                                    )

        self.clock_but.grid(row=4, column=24, rowspan = 2,
                            columnspan = 5)
        self.clock_stop.grid(row=6, column=24, rowspan = 2,
                             columnspan = 5)
        self.make_clock_b.grid(row=2, column=24, rowspan = 2,
                               columnspan = 5)
        self.clock_rem_b.grid(row=8, column=24, rowspan = 2,
                              columnspan = 5)

        self.grid_forget()

    def make_clock(self):
        if not hasattr(self, "canvas"):
            t.make_clock(self)


if __name__ == "__main__":
    """This part is just for testing"""
    window = tk.Tk()
    main_page = Main_page(window)
    #page1 = Page1(window)
    page4 = Page4(window)
    main_page.tkraise()
    window.mainloop()
