from Pages import Page, IMAGES, Main_page, ImageTk, plt, mpl
from Page1 import Page1
from Page1_1 import Page1_1
from Page3 import Page3
from Page4 import Page4
from DirPage1.Physics import Physics
from DirPage1.Object import Large_object
from messages import mdt, m_cycles
import numpy as np
import tkinter as tk
from tkinter import ttk

class Page1_2(Page):
    """
    THis is the page where the actual simulation
    will take place.
    """
    def __init__(self, master, name = "page1_2",*args, **kwargs):
        Page.__init__(self, name=name, master = master, *args, **kwargs)

        #Setting up the grid
        self.columnconfigure([x for x in range(30)],
                             minsize = self.master.winfo_width()/30,
                             weight = 1)

        self.rowconfigure([x for x in range(30)],
                          minsize = self.master.winfo_height()/30,
                          weight = 1)


        #Making the forward and backward buttons
        #We both know that forward wont do nothing. But it looks cool.
        self.make_navigation_buttons(forward = "page1_1", backward = "page1_1")
##        self.forward_button.grid(row = 27, column = 28,
##                                 rowspan = 2, columnspan = 2,
##                                 sticky = "NSEW",
##                                 )

        self.backward_button.grid(row = 27, column = 27,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                  )
        self.backward_button.config(
            command = lambda: [
                self.delete_canvas(),
                self.del_colorbar(),
                self.master.geometry("510x400"),
                self.change_page("page1_1")(),])

        #Now we add the heading
        self.label_main = tk.Label(self,
                                   text = "Simulation",
                                   font = ("Consolas","16","bold"),
                                   )
        self.label_main.grid(row=0, rowspan=2,
                             column = 13, columnspan = 6,
                             sticky = "N")


        #Time to add the main frame. But first a nptebook
        self.notebook = ttk.Notebook(self,)

        #Now we place the notebook
        self.notebook.grid(column=1, row=1, sticky="NSEW",
                            columnspan=28, rowspan = 28,
                             )
        self.notebook.lower()


        self.main_frame = ttk.Frame(self.notebook, border = 1) #Where the simulation will play out.
        self.params_frame = ttk.Frame(self.notebook, border= 1) #Deeper chaing and adding things to animation
        self.animation_frame = ttk.Frame(self.notebook, border=1) #Using funcanimation to save video or GIF

        #Now we add the pages to the notebooks.
        self.notebook.add(self.main_frame, text= "Animation")
        self.notebook.add(self.params_frame, text = "Parameters")
        self.notebook.add(self.animation_frame, text = "Animation")



        #Now we move on to working on the main frame
        self.main_frame.columnconfigure([x for x in range(30)],
                                        minsize = self.master.winfo_width()/30,
                                        weight =1,)
        self.main_frame.rowconfigure([x for x in range(30)],
                                     minsize = self.master.winfo_height()/30,
                                     weight =1,)

        #Now we make the drawing area
        self.canvas_area = tk.Frame(self.main_frame, relief = "sunken", border=1)
        self.canvas_area.grid(row =0, column = 0, rowspan = 27, columnspan = 24,
                              sticky = "NSEW")


        #Now we work on the buttons in the bottom of the page.
        self.lower_frame = tk.Frame(self.main_frame)
        self.lower_frame.grid(row = 27, rowspan = 3, column = 0, columnspan =30,
                              sticky = "NSEW")
        self.lower_frame.update()

        self.lower_frame.rowconfigure([x for x in range(6)],
                                      minsize = self.lower_frame.winfo_height()/6,
                                      weight = 0)
        self.lower_frame.columnconfigure([x for x in range(19)],
                                         minsize = self.lower_frame.winfo_width()/19,
                                         weight =0)
        self.lower_frame.columnconfigure([0],
                                         minsize = self.lower_frame.winfo_width()/80,
                                         weight =0)


        self.play_icon = ImageTk.PhotoImage(IMAGES['play_icon'].resize((17,17)))
        self.replay_icon = ImageTk.PhotoImage(IMAGES['replay_icon'].resize((17,17)))
        self.pause_icon = ImageTk.PhotoImage(IMAGES['pause_icon'].resize((17,17)))
        self.magnifying_icon = ImageTk.PhotoImage(IMAGES['magnifying_icon'].resize((17,17)))
        self.star_icon = ImageTk.PhotoImage(IMAGES['star_icon'].resize((17, 17)))
        self.play_button = ttk.Button(self.lower_frame,
                                      command = self.play,
                                      takefocus = 0,
                                      image = self.play_icon
                                      )
        self.play_button.grid(row = 1, column=1, rowspan = 2, sticky = "NSEW")


        self.stop_button = ttk.Button(self.lower_frame,
                                      image = self.pause_icon,
                                      command = self.stop,
                                      takefocus = 0,
                                      )
        self.stop_button.grid(row =1, rowspan =2, column = 2, sticky = "NSEW")

        self.replay_button = ttk.Button(self.lower_frame,
                                        command = self.replay,
                                        takefocus = 0,
                                        image = self.replay_icon,
                                        )
        self.replay_button.grid(row =1, rowspan=2, column=3, sticky = "NSEW")


        self.time_icon = ImageTk.PhotoImage(IMAGES['time_icon'].resize((17,17)))
        self.path_button = ttk.Button(self.lower_frame, image = self.time_icon,
                                      command = self.show_path,
                                      takefocus = 0,
                                      )
        self.path_button.grid(row=1, rowspan =2, column = 4, sticky = "NSEW")

        self.stars_button = ttk.Button(self.lower_frame,
                                       command =self.turn_stars_on_off,
                                       takefocus = 0, image = self.star_icon,
                                       )
        self.stars_button.grid(row =1, rowspan =2, column=5, sticky = "NSEW")

        self.zoom_button = ttk.Button(self.lower_frame,
                                       command = self.play_button["command"],
                                      takefocus = 0, image = self.magnifying_icon)
        self.zoom_button.grid(row=1, rowspan =2, column=6, stick = "NSEW")


        self.cmap_left_button = ttk.Button(
            self.lower_frame, text="-",
            takefocus = 0, width =1,
            command = lambda: self.update_colorbar("-"),
            )
        self.cmap_left_button.grid(row =3, rowspan = 2, column = 1, sticky = "NSEW")



        self.cmap_icon = ImageTk.PhotoImage(
            IMAGES['cmap_icon'].resize((110, 23)))
        self.cmap_label = tk.Label(self.lower_frame,
                                   image = self.cmap_icon)
        self.cmap_label.grid(row =3, column=2, columnspan=4, rowspan=2, sticky ="NSEW",
                             )

        self.cmap_right_button = ttk.Button(
            self.lower_frame, text = "+",
            takefocus = 0, width =1,
            command = lambda: self.update_colorbar("+"))
        self.cmap_right_button.grid(
            row = 3, rowspan=2, column=6, sticky = "NSEW")

        # Making the slider pack for dt
        self.dt_label = tk.Label(self.lower_frame, text = "dt",
                                 font = ("Consolas","8","bold"))
        self.dt_label.grid(row=1, rowspan=2, column = 7, sticky = "NSEW",)


        self.dt_text = tk.DoubleVar()
        self.dt_slider = ttk.Scale(self.lower_frame, from_=0., to=1,
                                   orient = "horizontal",
                                   variable = self.dt_text,
                                   command = lambda s: \
                                   self.update_dt(s)
                                   )
        self.dt_slider.set(0.5)
        self.dt_slider.grid(row=1, rowspan=2, column = 8, columnspan=2,
                            sticky = "NSEW")

        self.dt_display = ttk.Label(self.lower_frame,
                                    textvar = self.dt_text,
                                    )
        self.dt_display.grid(row=1, column = 10, columnspan=1,
                             rowspan = 2,
                             sticky = "NSEW")


        self.scales = [f"* 1e{x} s" for x in range(-5, 5)]

        s = ttk.Style()
        s.configure("white2.TMenubutton",
                    highlightbackground = "white",
                    background = self.master['background'],
                    highlightcolor = "white",
                    bg = "white",
                    font = ("Consolas","5","bold"))


        self.dt_drop = ttk.Combobox(
            self.lower_frame,
            values = self.scales,
            style = "white2.TMenubutton",
            width=5, justify = tk.LEFT,
            takefocus = 0, state = 'readonly'
            )

        self.dt_drop.set("* 1e0 s")
        self.dt_drop.grid(row=1, rowspan=2, column = 11,
                          columnspan = 2, sticky ="NSEW")



        # Making the slider pack for number of cycles
        self.nc_label = tk.Label(self.lower_frame, text = "n",
                                 font = ("Consolas","8","bold"))
        self.nc_label.grid(row=3, rowspan=2, column = 7, sticky = "NSEW",)


        self.nc_text = tk.DoubleVar()
        self.nc_slider = ttk.Scale(self.lower_frame, from_=0, to=10,
                                   orient = "horizontal",
                                   variable = self.nc_text,
                                   command = lambda s: \
                                   self.update_cycles(s))

        self.nc_slider.set(5)
        self.nc_slider.grid(row=3, rowspan=2, column = 8, columnspan=2,
                            sticky = "NSEW")

        self.nc_display = ttk.Label(self.lower_frame,
                                    textvar = self.nc_text,
                                    )
        self.nc_display.grid(row=3, column = 10, columnspan=1,
                             rowspan = 2,
                             sticky = "NSEW",)


        self.nc_scales = [f"* 1e{x} cycles" for x in range(0, 5)]

        s = ttk.Style()
        s.configure("white2.TMenubutton",
                    highlightbackground = "white",
                    background = self.master['background'],
                    highlightcolor = "white",
                    bg = "white",
                    font = ("Consolas","5","bold"))


        self.nc_drop = ttk.Combobox(
            self.lower_frame,
            values = self.nc_scales,
            style = "white2.TMenubutton",
            width=5, justify = tk.LEFT,
            takefocus = False,
            state = "readonly"
            )

        self.nc_drop.set("* 1e0 cycle")
        self.nc_drop.grid(row=3, rowspan=2, column = 11,
                          columnspan = 2, sticky ="NSEW")



        #Making the buttons that explain how dt and ncycles work
        question_icon = IMAGES['question_icon'].resize((15, 15))
        self.question_icon = ImageTk.PhotoImage(question_icon)
        self.help_dt = tk.Button(
                            self.lower_frame,
                            image = self.question_icon,
                            command = lambda: \
                            tk.messagebox.showinfo(
                            "dt info", mdt),
                            border = 0,
                            )
        self.help_dt.grid(row=1, rowspan=2, column=13, columnspan=1)


        self.help_nc = tk.Button(
                            self.lower_frame,
                            image = self.question_icon,
                            command = lambda: \
                            tk.messagebox.showinfo(
                            "dt info", m_cycles),
                            border = 0,
                            )
        self.help_nc.grid(row=3, rowspan=2, column=13, columnspan=1)


        #Make a button to draw all the necessary canvas
        s = ttk.Style()
        self.font = ("Consolas","10","bold")
        s.configure(
            "red.TButton",
            font = self.font,
            foreground = "orangered"
            )
        s.configure(
            "green.TButton",
            font = self.font,
            foreground = "green"
            )

        self.make_canvas_but = ttk.Button(
            self.lower_frame, text = "DRAW!",
            command = self.draw_simulation,
            takefocus = 0,
            style = "green.TButton")
        self.make_canvas_but.grid(
            row =1, rowspan =2, column = 14,columnspan =2
            )


        self.erase_canvas_but = ttk.Button(
            self.lower_frame, text = "ERASE!",
            takefocus = 0,
            command = lambda:
                [
                self.delete_canvas(),
                self.del_colorbar(),
                ],
            style = "red.TButton")
        self.erase_canvas_but.grid(
            row =3, rowspan =2, column = 14,columnspan =2
            )


        #This is a frame that holds the widgets on the right side of thepage.
        self.right_frame = tk.Frame(self.main_frame, bg = "orange",
                                    )
        self.right_frame.grid(row = 0, column=24, rowspan=27, columnspan=6,
                              sticky = "NSEW")
        self.right_frame.update()
        self.right_frame.rowconfigure([0, 1], minsize = \
                                      self.right_frame.winfo_height()/2,
                                      weight =1)
        self.right_frame.columnconfigure([0], minsize = \
                                        self.right_frame.winfo_width(),
                                        weight =1)

        self.top_framelabel = ttk.LabelFrame(
            self.right_frame, text = "Show", )
        self.top_framelabel.grid(row=0, column=0, sticky = "NSEW",
                                 )
        self.top_framelabel.update()
        self.top_framelabel.rowconfigure(
            [x for x in range(8)],
            minsize = self.top_framelabel.winfo_height()/9,
            weight =1)


        self.bottom_framelabel = ttk.LabelFrame(
            self.right_frame, text = "Color by",border=1)
        self.bottom_framelabel.grid(row=1, column=0, sticky = "NSEW",
                                    )

        self.bottom_framelabel.rowconfigure(
            [x for x in range(8)],
            minsize = self.top_framelabel.winfo_height()/9,
            weight =1)

        #Now we make a style for the checkbuttons below
        s = ttk.Style()
        s.configure("newCbt.TCheckbutton",
                    font = ("Consolas", "10"))

        self.p_var = tk.IntVar()
        self.planet_box = ttk.Checkbutton(
            self.top_framelabel, text = "Planets",
            takefocus = False,style = "newCbt.TCheckbutton",
            variable = self.p_var,command  = self.update_displayed)
        self.planet_box.grid(row =0, column=0, sticky = "NSEW",)

        self.s_var = tk.IntVar()
        self.sun_box = ttk.Checkbutton(
            self.top_framelabel, text = "Suns",
            takefocus = False,style = "newCbt.TCheckbutton",
            variable = self.s_var, command  = self.update_displayed)
        self.sun_box.grid(row =1, column=0, sticky = "NSEW")

        self.m_var = tk.IntVar()
        self.moon_box = ttk.Checkbutton(
            self.top_framelabel, text = "Moons",
            takefocus = False,style = "newCbt.TCheckbutton",
            variable = self.m_var, command  = self.update_displayed)
        self.moon_box.grid(row =2, column=0, sticky = "NSEW")

        self.a_var = tk.IntVar()
        self.a_var.set(1)
        self.all_box = ttk.Checkbutton(
            self.top_framelabel, text = "All",
            takefocus = False,style = "newCbt.TCheckbutton",
            variable = self.a_var, command  = self.update_displayed)
        self.all_box.grid(row =3, column=0, sticky = "NSEW")

        self.o_var = tk.IntVar()
        self.other_box = ttk.Checkbutton(
            self.top_framelabel, text = "Others",
            takefocus = False,style = "newCbt.TCheckbutton",
            variable = self.o_var, command  = self.update_displayed)
        self.other_box.grid(row =4, column=0, sticky = "NSEW")

        # self.energies_box = ttk.Checkbutton(
        #     self.top_framelabel, text = "Energies",
        #     takefocus = False,style = "newCbt.TCheckbutton")
        # self.energies_box.grid(row =5, column=0, sticky = "NSEW")



        self.show_comp = tk.StringVar()
        self.show_comp.set("None")
        self.v_box = ttk.Radiobutton(
            self.bottom_framelabel, text = "Speed",
            variable = self.show_comp,
            value = "speed",
            takefocus = False, command = self.show_path)
        self.v_box.grid(row =0, column=0, sticky = "NSEW")

        self.vx_box = ttk.Radiobutton(
            self.bottom_framelabel, text = "Vx",
            takefocus = False,
            value = "vx", variable = self.show_comp,
            command = self.show_path)
        self.vx_box.grid(row =1, column=0, sticky = "NSEW")

        self.vy_box = ttk.Radiobutton(
            self.bottom_framelabel, text = "Vy",
            takefocus = False,
            variable = self.show_comp,
            value = "vy",command = self.show_path)
        self.vy_box.grid(row =2, column=0, sticky = "NSEW")

        self.vz_box = ttk.Radiobutton(
            self.bottom_framelabel, text = "Vz",
            takefocus = False,
            value = "vz", variable = self.show_comp,
            command = self.show_path)
        self.vz_box.grid(row =3, column=0, sticky = "NSEW")

        self.vnone_box = ttk.Radiobutton(
            self.bottom_framelabel, text = "None",
            takefocus = False,
            value = "None", variable = self.show_comp,
            command = self.show_path)
        self.vnone_box.grid(row =4, column=0, sticky = "NSEW")


        #Now we make it possible to make a premade simulation from an
        #earlier page. THis was not done in the page to prevent dependency
        b = self.__class__.instances["page1"].premade_button
        b.config(command = lambda: Physics.threed(self))

        self.grid_forget()

    def update_displayed(self):
        """
        Hides the objects that are not meant to be displayed.
        """
        if not hasattr(self, "universe"): return
        tags = []
        for attr in "p_var, m_var, a_var, o_var, s_var".split(", "):
            if getattr(self, attr).get()==1:
                tags.append(attr[0]) #First letter is enough
        print(tags, "are the tags")
        if "a" in tags:
            for object in self.universe.objects:
                if self.universe.running:
                    object.plot.set_visible(True)
                    if object.ring:
                        object.ring.set_visible(True)
                else:
                    object.scatt.set_visible(True)
                    if object.ring:
                        object.ring.set_visible(False)
            if hasattr(self, "canvas"):
                self.canvas.draw()
                self.canvas.flush_events()
            return

        for object in self.universe.objects:
            if object.name[0].lower() in tags:
                if self.universe.running:
                    object.plot.set_visible(True)
                    if object.ring:
                        object.ring.set_visible(True)
                else:
                    object.scatt.set_visible(True)
                    if object.ring:
                        object.ring.set_visible(False)
            else:
                object.plot.set_visible(False)
                object.scatt.set_visible(False)
                if object.ring:
                    object.ring.set_visible(False)
        if hasattr(self, "canvas"):
            self.canvas.draw()
            self.canvas.flush_events()



    def show_path(self):
        if hasattr(self, "universe"):
            self.universe.new_collect_data()
            self.universe.show_comp()
            self.canvas.draw()
            self.canvas.flush_events()


    def update_cycles(self, s):
        if hasattr(self, "nc_drop"):
            self.nc_text.set(f"{round(float(s), 2)}")
            self.cycles = int(float(s)*eval(self.nc_drop.get()[2:6].strip()))
        if hasattr(self, "universe"):
            self.universe.data_collected = False

    def update_dt(self, s):
        self.dt_text.set(f"{round(float(s),2)}")
        if hasattr(self, "universe"):
            dt = float(s)*eval(self.dt_drop.get()[2:6].strip())
            self.universe.dt = dt
        if hasattr(self, "universe"):
            self.universe.data_collected = False

    def play(self):
        if hasattr(self, "universe"):
            self.universe.play()

    def stop(self):
        if hasattr(self, "universe"):
            self.universe.running = False

    def replay(self):
        if hasattr(self, "universe"):
            self.universe.replay()

    def turn_stars_on_off(self):
        if hasattr(self, "universe"):
            if self.universe.stars1._visible:
                self.universe.stars1._visible = False
                self.universe.stars2._visible = False
                self.universe.stars3._visible = False
            else:
                self.universe.stars1._visible = True
                self.universe.stars2._visible = True
                self.universe.stars3._visible = True
            self.canvas.draw()
            self.canvas.flush_events()

    def draw_simulation(self):
        if not hasattr(self, "canvas"):
            # try:
            instances = self.__class__.instances
            self.make_colorbar()

            universe = instances["page1"].universe_dict \
            if hasattr(instances["page1"], "universe_dict") \
            else instances["page1"].get_values()

            self.universe = Physics(**universe, page = self)

            objects = instances["page1_1"].get_final_object_dictionary()
            if objects:
                for object in objects:
                    o = Large_object(**objects[object], universe = self.universe,
                                )

                #The following ensures more precise orbit setting.
                planets = []
                suns = []
                moons = []
                others = []
                for object in self.universe.objects:
                    if object.name[0].lower() == "p":
                        planets.append(object)
                    elif object.name[0].lower() == "m":
                        moons.append(object)
                    elif object.name[0].lower() == "s":
                        suns.append(object)
                    else:
                        others.append(object)
                for typ in (others, suns, planets, moons):
                    for object in typ:
                        object.find_orbit()
                        object.check_orbit(True) #Makes the orbits random looking

            self.canvas = self.universe.canvas
            self.ax = self.universe.ax
            self.canvas.draw()
            self.canvas.flush_events()

            # except:
            #     tk.messagebox.showwarning("PROBLEM",
            #                   "You have not created the objects and or universe")
            #     return
        else:
            self.canvas.draw()
            self.canvas.flush_events()

    def del_colorbar(self):
        """
        Placement of the colorbar in the cmap label.
        OR it's deletion if it get's called twice."""
        if hasattr(self, "colorbar"):
            grid_info = self.canvascb.get_tk_widget().grid_info()
            self.cmap_label.grid(**grid_info)
            self.canvascb.get_tk_widget().grid_forget()
            plt.close(self.figcb)
            del self.figcb
            del self.axcb
            del self.colorbar
            del self.cmap_grid

    def make_colorbar(self):
        if not hasattr(self, "colorbar"):
            #cb stands for colorbar
            self.figcb = plt.figure(figsize = (0.005, 0.005))
            self.canvascb = mpl.backends.backend_tkagg.FigureCanvasTkAgg(
                self.figcb,
                self.lower_frame,
                )

            grid_info = self.cmap_label.grid_info()
            self.canvascb.get_tk_widget().grid(**grid_info)
            self.cmap_label.grid_forget()
            self.axcb = self.figcb.add_axes([0,0.05,1,0.9])
            self.axcb.axis("off")

            #Cmap grid stands for np grid that will be used in imshow.
            gradient = np.linspace(0,1,40)
            self.cmap_grid = np.vstack((gradient, gradient))

            self.colorbar = self.axcb.imshow(
                self.cmap_grid, aspect = "auto", cmap = "viridis")

            if not hasattr(self, "cmaps"):
                self.cmaps = plt.colormaps()
                self.cmap_index = self.cmaps.index("viridis")

            self.canvascb.draw()
            self.canvascb.flush_events()

    def update_colorbar(self, symbol):
        """
        Updates the color of the colorbar assuming that
        the name of the colorbar is colorbar."""
        if hasattr(self, "colorbar"):
            if symbol == "+" and self.cmap_index<len(self.cmaps)-1:
                self.cmap_index+=1
            elif symbol == "-" and self.cmap_index>=0:
                self.cmap_index-=1
            self.colorbar.set_cmap(self.cmaps[self.cmap_index])
            self.show_path()
            self.colorbar.axes.figure.canvas.draw()
            self.colorbar.axes.figure.canvas.flush_events()



if __name__ == "__main__":
    from Page4 import Page4
    window = tk.Tk()
    main_page = Main_page(window)
    page1 = Page1(window)
    page1_1 = Page1_1(window)
    page4 = Page4(window)
    page1_2 = Page1_2(window)
    page3 = Page3(window)
    window.mainloop()
