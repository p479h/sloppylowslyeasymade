import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from os import getcwd, path
from Frontpage import Controls_container
import sys
from matplotlib.pyplot import show
sys.path.insert(1, r"C:\Users\phfer\Desktop\Python\Physics")  # To allow to use Physics
if __name__ == "__main__":
    from Frontpage import Window
    from Universe_page import Universe_page
    from Last_page import Last_page
if True:
    from Physics import Physics
    from Object import Moon, Planet, Sun, Object, Large_object


class Objects_page(tk.Frame):
    """The actual page that will contain the universe setters"""
    instances = []

    def __init__(self, window, label="Objects", *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)
        self.config(height=window.winfo_height(),
                    width=window.winfo_width())
        self.name = label
        self.name_label = tk.Label(self, text=label, font="sans-serif")
        self.name_label.grid(padx=4, pady=4, row=0, sticky="W")
        self.parent = window
        window.frames["Objects page"] = self

        # Creating Notebook
        self.Notebook = ttk.Notebook(self)
        self.control_pannel1 = Controls_container(self.Notebook)
        self.control_pannel2 = Controls_container(self.Notebook)
        height, width = 290, 440
        self.control_pannel1.config(height=height, width=width)
        self.control_pannel2.config(height=height, width=width)
        self.Notebook.add(self.control_pannel1, text="Custom")
        self.Notebook.add(self.control_pannel2, text="Lazy")
        self.Notebook.grid(row=1, column=0, padx=10, sticky='NSEW')
        self.control_pannel1.rowconfigure([5, 6, 7, 8], minsize=10)

        # Making the most important labels
        self.labels_ = "Color, Marker, Ring, Charge, Charge density, Initialv, Initialp, Radius".split(", ")
        for index, label in enumerate(self.labels_):
            label = tk.Label(self.control_pannel1, text=label)
            label.grid(column=0, row=index+1, padx=10, pady=2, sticky="W")
            setattr(self, f"label{index+1}", label)

        # Making the actual buttons
        self.category = tk.StringVar()
        self.category.set("Planet")
        self._menu_names = {"Sun", "Planet", "Moon", "Other"}
        s = ttk.Style()
        s.configure('Kim.TMenubutton', background = "lightgray")
        self.menu = ttk.OptionMenu(self.control_pannel1, self.category,
                                  style = 'Kim.TMenubutton', *self._menu_names)
        self.menu.grid(column=1, row=0, pady=0, padx=10)
        self.label0 = tk.Label(self.control_pannel1, text='Type of object')
        self.label0.grid(column=0, row=0, pady=2, padx=10)

        self.color = tk.StringVar()
        self.color.set("random")
        self.color_names = "blue, red, pink, purple, black, white, gray, orange, yellow, random".split(", ")
        self.color_menu = ttk.OptionMenu(self.control_pannel1, self.color,
                                        style = 'Kim.TMenubutton', *self.color_names)
        self.color_menu.grid(column=1, row=1, padx=10, pady=0)

        self.markers = "o h 8 . * > < ^".split()
        self.marker = tk.StringVar()
        self.marker.set("o")
        self.marker_menu = ttk.OptionMenu(self.control_pannel1, self.marker,
                                          style = 'Kim.TMenubutton', *self.markers)
        self.marker_menu.grid(column=1, row=2, padx=10, pady=0)

        self.ring = tk.BooleanVar()
        self.ring.set(False)
        self.ring_check = ttk.Checkbutton(self.control_pannel1, variable=self.ring,
                                         onvalue=True, offvalue=False,
                                         takefocus = 0)
        self.ring_check.grid(column=1, row=3, padx=10, pady=1)

        self.charge = tk.IntVar()
        self.charge.set(0)
        self.charge_negative = ttk.Radiobutton(self.control_pannel1, variable=self.charge,
                                              value=-1, text="-1", takefocus = 0)
        self.charge_negative.grid(column=1, row=4, padx=1, pady=1, sticky="W")

        self.charge_0 = ttk.Radiobutton(self.control_pannel1, variable=self.charge,
                                       value=0, text="0", takefocus = 0)
        self.charge_0.grid(column=1, row=4, padx=1, pady=1)

        self.charge_positive = ttk.Radiobutton(self.control_pannel1, variable=self.charge,
                                              value=1, text="1", takefocus = 0)
        self.charge_positive.grid(column=1, row=4, padx=1, pady=1, sticky="E")

        self.charge_density_entry = tk.Entry(self.control_pannel1, width=13, relief = "flat")
        self.charge_density_entry.grid(column=1, row=5, padx=10, pady=0)
        self.charge_density_entry.insert(0, 1)

        #self.parent.rowconfigure([5, 6, 7, 8], minsize=10)

        self.parentesis = dict()
        self.commas = dict()
        for x in range(4):
            if x % 2 == 0:
                self.parentesis[x] = tk.Label(self.control_pannel1, text="(")
                self.parentesis[x].grid(column=1, row=6+int(x/2), sticky="W")
            else:
                self.parentesis[x] = tk.Label(self.control_pannel1, text=")")
                self.parentesis[x].grid(column=1, row=6+int(x/2), sticky="E")
        for x in range(2):
            self.commas[x] = tk.Label(self.control_pannel1, text=",", width=1)
            self.commas[x].place(x=x*34+130, y=183)

            self.commas[x+2] = tk.Label(self.control_pannel1, text=",", width=1)
            self.commas[x+2].place(x=x*34+130, y=158)

        self.vector_v = dict()
        self.vector_p = dict()
        self.vector_v["x"], self.vector_v["y"], self.vector_v["z"] =\
            [tk.Entry(self.control_pannel1, width=2, relief = "flat") for x in range(3)]
        self.vector_p["x"], self.vector_p["y"], self.vector_p["z"] =\
            [tk.Entry(self.control_pannel1, width=2, relief = "flat") for x in range(3)]

        directions = 'x y z'.split()
        for x in range(3):
            self.vector_v[directions[x]].place(x=x*32+116, y=154)
            self.vector_p[directions[x]].place(x=x*32+116, y=180)

        self.radius_entry = tk.Entry(self.control_pannel1, width=13, relief = "flat")
        self.radius_entry.grid(column=1, row=8, padx=10, pady=0)
        self.update_r_entry()

        img = Image.open(path.join(window.image_path, "question.png")).resize((20, 20))
        self.question_mark = ImageTk.PhotoImage(img)
        for x in range(10):
            help = tk.Button(self.control_pannel1, compound="left", relief = "flat")#, bg='blue')
            help["border"] = "0"
            help.config(image=self.question_mark)
            help.grid(column=2, row=x, padx=20)
            setattr(self, f"help{x}", help)

        img = Image.open(path.join(window.image_path, "question.png")).resize((90, 90))
        self.question_mark2 = ImageTk.PhotoImage(img)
        self.help11 = tk.Button(self.control_pannel2, image=self.question_mark2,
                                relief = "flat", border = 0)
        self.help11.config(height=100, width=100)
        self.help11.place(x=300, y=10)
        window.update_pages(self)

        self.density_label = tk.Label(self.control_pannel1, text="Density")
        self.density_label.grid(row=9, column=0, sticky="W", padx=10)

        self.density = tk.Entry(self.control_pannel1, width=13, relief = "flat")
        self.density.grid(row=9, column=1)
        self.density.insert(0, 100000000000)

        self.add_object_button = tk.Button(self.control_pannel1, text="Add object")
        self.add_object_button.config(command=self.make_object)
        self.add_object_button.config(height=3, width=10, bg="green")
        self.add_object_button.grid(row=0, column=3, pady=10, padx=5, columnspan=2, rowspan=3)

        # Creating the buttons to change page
        def forward(): return window.show_frame("Last")
        self.forward_button = tk.Button(self, text="->", command=forward)
        self.forward_button.grid(row=2, column=1, sticky="E")

        def backward(): return window.show_frame("Universe")
        self.back_button = tk.Button(self, text="<-", command=backward)
        self.back_button.grid(row=2, column=0, sticky="E", pady=4)

        def make_planets_orbit():
            try:
                sun = None
                for thing in self.parent.universe.objects:
                    if thing.category == "sun":
                        sun = thing
                        break
                for other in self.parent.universe.objects:
                    if other.category != "sun":
                        other.orbit = sun
                        other.check_orbit("yes")
                        print("ORBIT CHECKED AND GUD TU GO!")
                try:
                    sun.scatt.ax.figure.canvas.draw()
                    None
                except:
                    None
            except:
                meddge = """To use this you need at least one sun and one planet"""
                tk.messagebox.showerror("Not enough objects", meddge)
        self._orbit = tk.Button(self.control_pannel1, text="Set all planets in orbit")
        self._orbit.grid(row=4, column=4, pady=10, padx=1, columnspan=1, rowspan=2)
        self._orbit.config(command=make_planets_orbit)
        help = tk.Button(self.control_pannel1, compound="left", relief = "flat",
                        border = 0)#, bg='blue')
        help.config(image=self.question_mark)
        help.grid(row=4, column=5, pady=10, padx=5, columnspan=1, rowspan=2)
        setattr(self, f"help{10}", help)

        window.update_pages(self)

        # Now everything concerns the second page Lazy
        self.premade1_b = tk.Button(self.control_pannel2, text="Solar system 2d",
                                    command=lambda: Physics.twod())
        self.premade2_b = tk.Button(self.control_pannel2, text="Solar system 3d",
                                    command=lambda: Physics.threed())
        self.premade1_b.grid(column=0, row=0)
        self.premade2_b.grid(column=1, row=0)
        self.assign_functions_to_questions()

    def make_object(self):
        if not self.parent.universe:
            tk.messagebox.showwarning("CREATE UNIVERSE FIRST!!!", "CREATE UNIVERSE FIRST!!!  "*10)
        else:
            window = self.parent
            universe_page = window.frames["Universe"]
            num_dims = window.universe.num_dims
            category = self.category.get()
            color = self.color.get() if self.color.get() != "random" else None
            ring = self.ring.get()
            charge = self.charge.get()
            marker = self.marker.get()
            try:
                charge_density = float(self.charge_density_entry.get()) if\
                    eval(self.charge_density_entry.get()) else 1
            except:
                charge_density = 1
                tk.messagebox.showwarning("Weird charge density input", "We have set it to one")
            init_v = []
            init_p = []
            try:
                if num_dims == 2:
                    init_v.append(float(self.vector_v['x'].get()))
                    init_v.append(float(self.vector_v['y'].get()))
                else:
                    init_v.append(float(self.vector_v['x'].get()))
                    init_v.append(float(self.vector_v['y'].get()))
                    init_v.append(float(self.vector_v['z'].get()))
            except:
                message = "If you are working in two dimensions,\nleave the z component empty"
                message = message+"\nThe inputs are in the form(x, y, z) if working in 3 dimensions"
                message = message+"\nElse, (x, y)\n The velocity was set to 0, so don't worry."
                tk.messagebox.showwarning("Weird velocity input!", message)
                init_v = [0 for x in range(num_dims)]

            try:
                if num_dims == 2:
                    init_p.append(float(self.vector_p['x'].get()))
                    init_p.append(float(self.vector_p['y'].get()))
                else:
                    init_p.append(float(self.vector_p['x'].get()))
                    init_p.append(float(self.vector_p['y'].get()))
                    init_p.append(float(self.vector_p['z'].get()))
            except:
                message = "If you are working in two dimensions,\nleave the z component empty"
                message = message+"\nThe inputs are in the form(x, y, z) if working in 3 dimensions"
                message = message+"\nElse, (x, y)\nThe position was set to 0. So you might have to worry."
                tk.messagebox.showwarning("Weird position input!", message)
                init_p = [0 for x in range(num_dims)]
            try:
                radius = float(self.radius_entry.get()) if eval(self.radius_entry.get()) \
                    else 10
            except:
                radius = 10
            try:
                density = float(self.density.get()) if eval(self.density.get()) else 1e10
            except:
                density = 1e12

            if category == "Sun":
                object = Sun(color=color, marker=marker, ring=ring,
                             charge=charge, radius=radius, charge_density=charge_density,
                             init_p=init_p, init_v=init_v, density=density, universe=window.universe)
            elif category == "Planet":
                object = Planet(color=color, marker=marker, ring=ring,
                                charge=charge, radius=radius, charge_density=charge_density,
                                init_p=init_p, init_v=init_v, density=density,
                                universe=window.universe)
            elif category == "Moon":
                try:
                    orbit = window.universe.objects[-1]
                    object = Moon(color=color, marker=marker, ring=ring,
                                  charge=charge, radius=radius, charge_density=charge_density,
                                  init_p=init_p, init_v=init_v, density=density, universe=window.universe,
                                  orbit=orbit)
                except:
                    message = """To add a moon it is necessary to have just created
                    the planet it will orbit. There appears to be no planet or sun
                    in the current universe. Create them first. Then the moon.
                    The moon will automatically orbit the last created object."""
                    tk.messagebox.showwarning("Missing planet", message)
            else:
                object = Large_object(color=color, marker=marker, ring=ring,
                                      charge=charge, radius=radius, charge_density=charge_density,
                                      init_p=init_p, init_v=init_v, density=density,
                                      universe=window.universe, rel_size=0.1)
                object.category = "all"
            if not hasattr(self, 'objects'):
                self.objects = []
            self.objects.append(object)
            tk.messagebox.showinfo("Success", "Your object was created succesfuly!")

            if not hasattr(self, "delete_object"):
                self.delete_object = tk.Button(self.control_pannel1, text="Delete last object")
                self.delete_object_info = tk.Button(self.control_pannel1, text="?")
                print("message1")

                def object_deleter():
                    try:
                        self.objects[-1].scatt.remove()
                    except:
                        self.delete_object.place_forget()
                        self.delete_object_info.place_forget()
                        delattr(self, "delete_object")
                        return
                    self.objects.pop()
                    self.parent.universe.objects.pop()
                    tk.messagebox.showinfo("Success", "The last created object was deleted")
                    if len(self.objects) == 0:
                        self.delete_object.place_forget()
                        self.delete_object_info.place_forget()
                        delattr(self, "delete_object")

                def object_delter_info():
                    tk.messagebox.showinfo("Deleter", "This function deletes the object that was last created.")
                self.delete_object.config(command=object_deleter)
                self.delete_object_info.config(command=object_delter_info)
                self.delete_object.place(x=290, y=90)
                self.delete_object_info.place(x=400, y=90)

    def assign_functions_to_questions(self):
        message0 = """
        The object type will not do much just yet.
        But let's say you don't want to calculate
        the specific velocity an object needs to orbit
        another. Then you can create 1 Sun. As many planets
        as you like. Then click the button to set all orbits.
        Creating a moon will lead to an orbit around the last
        planet created automatically."""
        message1 = """
        Color that the object will have
        in the animation."""
        message2 = """
        Shape of object in animation."""
        message3 = """
        Creates a ring around the object.
        Causes the animation to become really
        slow and can have weird proportions on
        different scales. Leave it out if possible."""
        message4 = """
        If the object has a charge.
        Like charges repel.
        0 Charge does nothing.
        Different charges attract.
        The strength of interaction follows coulumbs law."""
        message5 = """
        Charge density in C kg-1."""
        message6 = """
        Initial velocity and position are both
        vecors. Make sure the input matches the universe
        number of dimensions. If you have 2d, write on the
        first 2 boxes, else, write on all boxes. Do so even if
        your vector has a component of 0 magnetude."""
        message7 = message6
        message8 = """
        The radius will be used with the density
        to calculate the mass of the object assuming
        spherical symetry. This is used to calculate
        net acceleration caused by gravity and or charge."""
        message9 = """
        Density is the actual density of the object.
        It has units kg m-3."""
        message10 = """
        If you create a Sun and a few planets,
        this button will make those planets orbit
        that Sun. I have not programed this
        very carefully so make sure you only have
        one Sun... Or don't. It is your simulation."""
        message11 = """
        These two buttons contain pre-made
        simulations of miniature solar systems.
        Clicking either one will start the simulation."""

        def func(title, message):
            return tk.messagebox.showinfo(title, message)
        messages = [message0, message1, message2, message3,
                    message4, message5, message6, message7, message8, message9, message10, message11]
        titles = "Type of object, Color, Marker, Ring, Charge, Charge density, Initial velocity".split(", ") +\
            "Initial position, Radius, Density, Make all planets orbit sun, Pre-made simulation".split(", ")
        buttons = [self.help0, self.help1, self.help2, self.help3, self.help4, self.help5,
                   self.help6, self.help7, self.help8, self.help9, self.help10, self.help11]
        for index, button in enumerate(buttons):
            def thing(title, message): return lambda: func(title, message)
            button.config(command=thing(titles[index], messages[index]))

    def update_r_entry(self):
        obj = self.category.get()
        self.radius_entry.delete(0, "end")
        if obj == "Planet":
            self.radius_entry.insert(0, 10)
        elif obj == "Moon":
            self.radius_entry.insert(0, 3)
        elif obj == "Sun":
            self.radius_entry.insert(0, 30)
        elif obj == "Other":
            self.radius_entry.insert(0, 1)

#
# class Last_page(tk.Frame):
#     def __init__(self, window, label="Last", *args, **kwargs):
#         tk.Frame.__init__(self, window, *args, **kwargs)
#         self.config(height=window.winfo_height(),
#                     width=window.winfo_width())
#         self.name = label
#         self.parent = window
#         self.name_label = tk.Label(self, text=label, font="sans-serif")
#         self.name_label.grid(padx=4, pady=4, row=0, sticky="W")
#         self.control_pannel = Controls_container(self)
#         self.control_pannel.grid(row=1, column=0, padx=10, sticky='NSEW')
#         self.control_pannel.grid_propagate(False)
#
#         def backward(): return window.show_frame("Objects")
#         self.back_button = tk.Button(self, text="<-", command=backward)
#         self.back_button.grid(row=2, column=0, sticky="E", pady=4)
#
#         def play():
#             if self.parent.universe:
#                 self.parent.universe.fig.canvas.draw()
#                 self.parent.universe.fig.canvas.flush_events()
#                 try:
#                     oo = self.parent.frames['Objects page']
#                     oo.delete_object.place_forget()
#                     oo.delete_object_info.place_forget()
#                     delattr(oo, "delete_object")
#                 except:
#                     None
#             try:
#                 show()
#             except:
#                 None
#             try:
#                 plt.close("all")
#             except:
#                 None
#         self.play_button = tk.Button(self.control_pannel, text="Play!", command=play, bg="green")
#         self.play_button.grid(column=0, row=0, padx=10, pady=1)
#         self.play_button.config(height=10, width=10)


if __name__ == "__main__":
    window = Window()
    page1 = Universe_page(window)
    page2 = Objects_page(window)
    page3 = Last_page(window)
    window.update_pages(page1, page2, page3)
    page2.make_object
    window.mainloop()
