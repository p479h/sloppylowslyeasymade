"""
    This is the page you go to after you click the planet button.
    Itself along with page1_1 and page1_2 make up all necessary 
    requirements for the simulation of planetary motion.
    
    Note that this simulation can take "charge" as argument for making
    the objects in the simulation. But I have not tested that option yet.
    So if you play around with it and find any issues, please tell me. 
    I have been making this by myself in quite a hurry. So there are definitely
    mistakes somewhere.
    """
from Pages import Page, IMAGES, Main_page, ImageTk, plt
from DirPage1.box import make_box_interactive
from messages import page1messages
import tkinter as tk
from tkinter import ttk

class Page1(Page):
    """
    This is the page that has support for planetary motion
    """
    def __init__(self, *args, **kwargs):
        Page.__init__(self, name = "page1", *args, **kwargs)
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
                                   border = 1,
                                   )

        self.main_frame.grid(column=1, row=1, sticky="NSEW",
                             columnspan=28, rowspan = 28,
                             )
        self.main_frame.update()
        grid_len = [x for x in range(30)]
        minsize = (self.main_frame.winfo_width()/32,
                   self.main_frame.winfo_height()/30)
        self.main_frame.rowconfigure(grid_len,
                                     minsize = minsize[1],
                                     weight =1
                                     )
        self.label_main = tk.Label(self,
                                   text = "Universe",
                                   font = ("Consolas","13","bold"),
                                   )
        self.label_main.grid(row=0, rowspan=3,
                             column = 1, columnspan = 5,
                             sticky = "N")

        self.main_frame.columnconfigure(grid_len+[30, 31],
                                        minsize = minsize[0],
                                        weight = 1,
                                        )

        self.make_navigation_buttons(forward = "page1_1",backward = "main_page")
        self.forward_button.grid(row = 27, column = 28,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )

        self.backward_button.grid(row = 27, column = 26,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )

        #The next function ensures that plots are deleted
        #This is done for efficiency purpuses
        self.backward_button.config(
            command = lambda:[
                              self.box_interactive.set(False),
                              self.update_box(),
                              self.change_page("main_page")(),#Note the ()!!! Change page is a wraper!
                              ])

        self.forward_button.config(
            command = lambda:[
                              self.box_interactive.set(False),
                              self.update_box(),
                              self.change_page("page1_1")(),#Note the ()!!! Change page is a wraper!
                              ])


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



        #These two will just help the code stay cleaner in the
        #following lines
        self.font = ("Consolas","10","bold")
        self.gridparams = dict(column=1, columnspan=8, rowspan=2,
                               sticky = "w")


        self.time_label = tk.Label(self.main_frame,
                                   text = "Display time",
                                   font = self.font,
                                   justify = "left",
                                   )
        self.time_label.grid(row = 2, **self.gridparams)

        self.stars_label = tk.Label(self.main_frame,
                                    text = "Show stars",
                                    font = self.font,
                                    justify = "left",
                                    )
        self.stars_label.grid(row=5, **self.gridparams)

        #Follows number of dimensions label
        self.nd_label = tk.Label(self.main_frame,
                                 text = "N dimensions",
                                 font = self.font,
                                 justify = "left",
                                 )
        self.nd_label.grid(row=8, **self.gridparams)

        self.init_t_label = tk.Label(self.main_frame,
                                     text="Initial t",
                                     font = self.font,
                                     justify = "left",
                                     )

        self.init_t_label.grid(row = 11, **self.gridparams)

        self.init_dt_label = tk.Label(self.main_frame,
                                      text = "Initial dt",
                                      font = self.font,
                                      justify = "left",
                                      )
        self.init_dt_label.grid(row=14, **self.gridparams)

        #Label for the physical dimensions of the universe
        self.uni_dims_label = tk.Label(self.main_frame,
                                       text= 'Side length',
                                       font = self.font,
                                       justify = "left",
                                       )
        self.uni_dims_label.grid(row=17, **self.gridparams)


        self.title_label = tk.Label(self.main_frame,
                                    text="Universe's name",
                                    font = self.font,
                                    justify = "left",
                                    )
        self.title_label.grid(row = 20, **self.gridparams)

        self.blit_label = tk.Label(self.main_frame,
                                   text = "Blit? (3D only)",
                                   font = self.font,
                                   justify = "left",
                                   )
        self.blit_label.grid(row = 23, **self.gridparams)


        #I am now giving this variable a new value because the
        #old ones are now useless
        self.gridparams = dict(column = 8, rowspan = 2,
                               columnspan = 6,)
        self.show_time = tk.BooleanVar()
        self.show_time.set(True)
        self.time_cb = ttk.Checkbutton(self.main_frame,
                                       variable = self.show_time,
                                       text = "yes",
                                        onvalue = True,
                                        offvalue = False,
                                        takefocus = 0,
                                        )
        self.time_cb.grid(row = 2, **self.gridparams)

        self.show_stars = tk.BooleanVar()
        self.show_stars.set(True)
        self.stars_cb = ttk.Checkbutton(self.main_frame,
                                        variable = self.show_stars,
                                        text = "yes",
                                        onvalue = True,
                                        offvalue = False,
                                        takefocus = 0,
                                        )
        self.stars_cb.grid(row = 5, **self.gridparams)

        #Radiobutton for 2 dimensions
        self.num_dims = tk.IntVar()
        self.num_dims.set(3)
        self.R2 = ttk.Radiobutton(self.main_frame,
                                  variable = self.num_dims,
                                  text = "2",
                                  value = 2,
                                  takefocus = 0,
                                  command = \
                                  lambda: self.blit_cb.grid_forget()
                                  )
        self.R2.grid(row=8, column = self.gridparams["column"]+1,
                     rowspan = self.gridparams["rowspan"],
                     columnspan = 3,
                     sticky = "w",)

        self.R3 = ttk.Radiobutton(self.main_frame,
                                  variable = self.num_dims,
                                  text = "3",
                                  value = 3,
                                  takefocus = 0,
                                  command = \
                                  lambda: self.blit_cb.grid(
                                      row = 23, **self.gridparams)
                                  )

        self.R3.grid(row=8, column = self.gridparams["column"]+2,
                     rowspan = self.gridparams["rowspan"],
                     columnspan = 3,
                     sticky = "e",)


        self.init_t_entry = ttk.Entry(self.main_frame,
                                      width = 10,
                                      )
        self.init_t_entry.insert(0, "0")
        self.init_t_entry.grid(row=11, **self.gridparams)


        self.init_dt_entry = ttk.Entry(self.main_frame,
                                      width = 10,
                                      )
        self.init_dt_entry.grid(row=14, **self.gridparams)
        self.init_dt_entry.insert(0, "0.01")


        self.uni_dims_entry = ttk.Entry(self.main_frame,
                                      width = 10,
                                      )
        self.uni_dims_entry.grid(row=17, **self.gridparams)
        self.uni_dims_entry.insert(0, "2000")


        self.title_entry = ttk.Entry(self.main_frame,
                                      width = 10,
                                      )
        self.title_entry.grid(row=20, **self.gridparams)
        self.title_entry.insert(
            0, "Predru's world")

        self.blit = tk.BooleanVar()
        self.blit.set(False)
        self.blit_cb = ttk.Checkbutton(self.main_frame,
                                       variable = self.blit,
                                       text="yes",
                                       onvalue = True,
                                       offvalue = False,
                                       takefocus = 0,
                                       )

        self.blit_cb.grid(row = 23, **self.gridparams)


        self.optionmenustyle = ttk.Style()
        self.optionmenustyle.configure(
            "new_option.TMenubutton",
            background = "white",
            )

        self.units_t = tk.StringVar()
        units  = "ms, s, min, hour, day, month, year".split(", ")
        self.init_t_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_t,
                                          "s", *units,
                                          style = "new_option.TMenubutton")
        self.init_t_drop.grid(row=11,
                              column=self.gridparams["column"]+5,
                              columnspan = self.gridparams["columnspan"],
                              rowspan =2,
                              )
        self.units_dt = tk.StringVar()
        units  = "μm, ms, s, min, hour, day, month, year".split(", ")
        self.init_dt_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_dt,
                                          "s", *units,
                                          style = "new_option.TMenubutton")
        self.init_dt_drop.grid(row=14,
                              column=self.gridparams["column"]+5,
                              columnspan = self.gridparams["columnspan"],
                              rowspan = 2,
                              )

        self.units_d = tk.StringVar()
        self.units_d_ = "nm, μm, mm, cm, dm, m, km, Mm, Gm".split(", ")
        self.units_d_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_d,
                                          "m", *self.units_d_,
                                          style = "new_option.TMenubutton")
        self.units_d_drop.grid(row=17,
                              column=self.gridparams["column"]+5,
                              columnspan = self.gridparams["columnspan"],
                              rowspan =2,
                              )
        self.question_icon = ImageTk.PhotoImage(IMAGES["question_icon"].resize((24, 24)))
        row = 2; col = 18; rowspan = 2; columnspan=2
        for x in range(8):
            but = tk.Button(self.main_frame, border = 0,
                            image = self.question_icon,
                            )
            but.grid(column = col, row=row, columnspan = columnspan,
                     rowspan = rowspan)
            row+=3
            setattr(self, f"help_b{x}", but)
        self.give_function_to_help_bs()


        self.box_img = ImageTk.PhotoImage(IMAGES['box_icon'].resize((154,155)))
        self.box_lab = ttk.LabelFrame(
            self.main_frame, text = "Visuals",)
        self.box_labin = tk.Label(
            self.box_lab, image = self.box_img)
        self.box_labin.pack(side="left")
        self.box_lab.grid(row=2, column=21, rowspan = 15,
                          columnspan = 10)


        #Update button
        self.button_style = ttk.Style()
        self.button_style.configure("Mybt.TButton",
            highlightbackground = "green",
            background = self.master['background'],
            highlightcolor = "green",
            foreground = "green",
            font = ("Consolas","11","bold")
            )
        self.update_b = ttk.Button(
            self.main_frame, text = "Make universe",
            style = "Mybt.TButton",
            command = lambda:
                [setattr(self, "universe_dict", self.get_values()),
                print(self.universe_dict)],
            takefocus = False,
            )
        self.update_b.grid(row=17, column = 21, columnspan = 10,
                           rowspan = 3, sticky = "NSEW")


        self.premade_button = ttk.Button(
            master=self.main_frame, text = "Premade",
            command = lambda: print("Does not do anything yet!"),
            style = "Mybt.TButton",)
        self.premade_button.grid(row=20, column = 21, columnspan = 10,
                           rowspan = 3, sticky = "NSEW")


        self.box_interactive = tk.BooleanVar()
        self.interactive_check = ttk.Checkbutton(self.main_frame,
                                       variable = self.box_interactive,
                                       text="Interactive",
                                       onvalue = True,
                                       offvalue = False,
                                       takefocus = 0,
                                       command = self.update_box
                                       )

        self.interactive_check.grid(row=0, column=20, columnspan=7,
                                    rowspan=2, sticky="S")


        self.grid_forget()


    def get_values(self):
        """
        Converts inputs into STI units and then
        returns them as a dictionary that can be
        readily used to make the universe
        """
        conversions = self.__class__.conversions

        t_conversion = conversions[self.units_t.get()]
        dt_conversion = conversions[self.units_dt.get()]
        d_conversion = conversions[self.units_d.get()]

        try:
            dictionary = dict(
                show_time = self.show_time.get(),
                stars = self.show_stars.get(),
                num_dims = self.num_dims.get(),
                t = float(self.init_t_entry.get())*t_conversion,
                dt = float(self.init_dt_entry.get())*dt_conversion,
                u_size = float(self.uni_dims_entry.get())*d_conversion,
                title = self.title_entry.get(),
                blit = self.blit.get(),
                )
            return dictionary
        except:
            tk.messagebox.showwarning(
                "PROBLEM", "YOU HAVE MADE SENSELESS INPUTS SOMEWHERE\n"\
                "☭")


    def update_box(self):
        if self.box_interactive.get():
            self.delete_canvas()#Just a check
            make_box_interactive(self)
        else:
            plt.close("all")
            self.delete_canvas()
            self.box_labin.pack(side="left")



    def give_function_to_help_bs(self):
        """
            This function will provide the information about each
            entry in the form of tkinter messageboxes.

            Help buttons follow the following name system:
            name(x) = help_b{x}

            where x goes from 0 till n, where n is the number of
            help buttons in the page.

            0 is to top help button.

            It uses premade messages that come from
            messages.py
            """
        mess = page1messages
        command = lambda x: lambda : tk.messagebox.showinfo(
                                        "Helpful information", mess[x])
        for x in range(8):
            button = getattr(self, f"help_b{x}")
            button.config(
                command = command(x)
                )



if __name__ == "__main__":
    """This part is just for testing"""
    window = tk.Tk()
    main_page = Main_page(window)
    page1 = Page1(window)
    main_page.tkraise()
    window.mainloop()
