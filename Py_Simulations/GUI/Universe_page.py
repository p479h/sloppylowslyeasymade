import tkinter as tk
from PIL import Image, ImageTk
import tkinter.ttk as ttk
from os import getcwd, path
from Frontpage import Controls_container
from matplotlib.pyplot import close
import sys
sys.path.insert(1, r"C:\Users\phfer\Desktop\Python\Physics")  # To allow to use Physics
if True:
    from Physics import Physics
if __name__ == "__main__":
    from Frontpage import Window
    from Physics import Physics
    from Objects_page import Objects_page
    from Last_page import Last_page


class Universe_page(tk.Frame):
    """The actual page that will contain the universe setters"""
    instances = []

    def __init__(self, window, label="Universe", *args, **kwargs):
        tk.Frame.__init__(self, window, *args, **kwargs)
        self.config(height=window.winfo_height(),
                    width=window.winfo_width())
        self.name = label
        self.parent = window
        self.name_label = tk.Label(self, text=label, font="sans-serif")
        self.name_label.grid(padx=4, pady=4, row=0, sticky="W")
        window.frames['Universe page'] = self

        self.control_pannel = Controls_container(self)
        self.control_pannel.grid(row=1, column=0, padx=10, sticky='NSEW')
        self.control_pannel.grid_propagate(False)
        self.control_pannel.columnconfigure([3], minsize=100)
        self.control_pannel.rowconfigure([x for x in range(8)], minsize=2)

        self.beg_mess = """First time using the app"""
        self.ft_button = tk.Button(self.control_pannel,
                                   text =self.beg_mess)

        self.control_pannel.rowconfigure([8,9], minsize = 60)
        self.ft_button.grid(column = 0, row = 9)
        self.ft_button.config(command = lambda: Physics.threed())

        def forward():
            self.update_v_p_entries()
            if self.parent.universe:
                if self.parent.universe.num_dims != self.num_dims.get():
                    message = "Please input the correct number of dimensions and update the universe"
                    tk.messagebox.showwarning("YOU SCREWED UP THE DIMENSIONS", message)
            window.show_frame("Objects")
        self.forward_button = tk.Button(self, text="->", command=forward)
        self.forward_button.grid(row=2, column=1, sticky="E", pady=4)

        self.label_names = ("Display time, Show stars, Number of dimensions, " +
                            "Initial t, dt, Universe side length, Title").split(", ")
        for index, label in enumerate(self.label_names):
            _label = tk.Label(self.control_pannel, text=label, font="Verdana 10")
            _label.grid(column=0, columnspan=2, row=index, padx=3, pady=3, sticky="W")
            setattr(self, f"label{index}", _label)

        self.num_dims = tk.IntVar()  # Radiobuttons controlling the num_dims
        self.num_dims.set(2)
        self.R2d = ttk.Radiobutton(self.control_pannel,
                                  variable=self.num_dims,
                                  value=2, text='2',
                                  takefocus = 0)  # Show time

        self.R3d = ttk.Radiobutton(self.control_pannel,
                                  variable=self.num_dims,
                                  value=3, text='3',
                                  takefocus = 0)  # Show stars
        self.R2d.grid(column=2, row=2, sticky='W')
        self.R3d.grid(column=2, row=2, sticky="E")

        self.R2d.configure(command=lambda: [self.num_dims.set(2),
                                            self.update_u_size(),
                                            ])
        self.R3d.configure(command=lambda: [self.num_dims.set(3),
                                            self.update_u_size(),
                                            ])

        self.stars = tk.BooleanVar()
        s2 = ttk.Style()
        s2.configure('Kim.TCheckbutton', highlightthickness = 0)
        self.check_stars = ttk.Checkbutton(self.control_pannel, text="yes",
                                          variable=self.stars, onvalue=True,
                                          offvalue=False, style = 'Kim.TCheckbutton',
                                          takefocus = 0)
        self.check_stars.grid(column=2, row=1)

        self.show_time = tk.BooleanVar()
        self.check_time = ttk.Checkbutton(self.control_pannel, text="yes",
                                         variable=self.show_time,
                                         onvalue=True, offvalue=False,
                                         takefocus = 0)
        self.check_time.grid(column=2, row=0)

        self.t = tk.Entry(self.control_pannel, text="Hello",
                          width=10, relief = "flat")
        self.t.grid(column=2, row=3)
        self.t.insert(0, 0)

        self.dt = tk.Entry(self.control_pannel, width=10, relief = "flat")
        self.dt.grid(column=2, row=4)
        self.dt.insert(0, 0.1)

        self.u_size = tk.Entry(self.control_pannel, width=10, relief = "flat")
        self.u_size.insert(0, 6000)
        self.u_size.grid(column=2, row=5)

        self.title = tk.Entry(self.control_pannel, width=10, relief = "flat")
        self.title.grid(column=2, row=6)
        Mess = "Predru\'s world"
        self.title.insert(0, Mess)

        img = Image.open(path.join(window.image_path, "question.png")).resize((25, 25))
        self.question_mark = ImageTk.PhotoImage(img)
        for x in range(7):
            help = tk.Button(self.control_pannel, compound="left", relief = "flat",
                            border = 0)#, bg='blue')
            help.config(image=self.question_mark)
            help.grid(column=3, row=x)
            setattr(self, f"help{x}", help)
        window.update_pages(self)
        self.assign_functions_to_questions()
        img = Image.open(path.join(self.parent.image_path, "box.PNG")).resize((150, 150))
        self.side_length_img = ImageTk.PhotoImage(img)

        self.side_label = tk.Label(self.control_pannel, image=self.side_length_img)
        self.side_label.place(x=290, y=160)

        def test_button_universe(): return self.make_universe()
        self.test_button = tk.Button(self.control_pannel,
                                     text="Make universe!",
                                     command=test_button_universe,
                                     bg="green")
        self.test_button.grid(row=0, column=4, rowspan=3)
        self.test_button.config(height=5, width=12)

    def assign_functions_to_questions(self):
        message0 = """
        If ticked, the current time passed
        since the beginning of the simulation
        will be displayed."""
        message1 = """
        If ticked, there will be stars
        in the background. This slows down
        the 3d simulation a little."""
        message2 = """
        Number of dimensions of graph
        if you choose to have 2 dimensions, leave
        the z components of other inputs empty
        else, write ALL the inputs, even if they are 0."""
        message3 = """
        Initial time of the simulation.
        It doesn't really affect anything but
        people might want to not start at t=0."""
        message4 = """
        Time step between calculations
        smaller dt lead to more accurate calculations.
        The drawback is loss of quality."""
        message5 = """
        The size of the side of the universe.
        This is NOT just for scalling of the graph.
        Make sure this input is larger than the largest
        distance from an object to the center of the universe."""
        message6 = """
        Name that will be displayed in the graph"""

        def func(title, message):
            return tk.messagebox.showinfo(title, message)
        messages = [message0, message1, message2, message3, message4, message5, message6]
        titles = 'Time, Stars, Number of dimensions, Time, dt, Universe side length, Title'.split(", ")
        buttons = [self.help0, self.help1, self.help2, self.help3, self.help4, self.help5, self.help6]
        for index, button in enumerate(buttons):
            def thing(title, message): return lambda: func(title, message)
            button.config(command=thing(titles[index], messages[index]))

    def make_universe(self):
        try:
            close()
        except:
            None
        window = self.parent
        universe_page = self
        num_dims = universe_page.num_dims.get()
        stars = universe_page.stars.get()
        show_time = universe_page.show_time.get()
        try:
            t = float(universe_page.t.get()) if eval(universe_page.t.get()) else 0
        except:
            t = 0
        try:
            dt = float(universe_page.dt.get()) if eval(universe_page.dt.get()) else 0.01
        except:
            dt = 0.01
        try:
            u_size = float(universe_page.u_size.get()) if eval(universe_page.u_size.get()) else 2000
        except:
            u_size = 2000
        try:
            title = universe_page.title.get()
        except:
            title = "Predru's world"

        window.universe = Physics(num_dims=num_dims, u_size=u_size,
                                  stars=stars, show_time=show_time, name=title, dt=dt, t=t)
        print("UNiverse was created!")
        self.test_button.config(text="Reset universe")
        self.delete_universe = tk.Button(universe_page.control_pannel,
                                         text="Delete universe", bg="red",
                                         height=5, width=12)
        self.delete_universe.grid(row=3, column=4, rowspan=3)
        setters = dict(visible=False)

        def deleter():
            self.delete_universe.grid_forget(),
            setattr(window, "universe", False),
            self.test_button.config(text="Make Universe!"),
            try:
                plt.close(self.parent.universe.fig)
            except:
                None
            try:
                plt.close(self.parent.universe.widgets_fig)
            except:
                None
        self.delete_universe.config(command=deleter)

    def update_v_p_entries(self):
        Objects_page = self.parent.frames["Objects page"]
        v, p = Objects_page.vector_p, Objects_page.vector_v
        dims = "x y z".split() if self.num_dims.get() == 3 else "x y".split()
        for dim in dims:
            v[dim].delete(0, "end")
            p[dim].delete(0, "end")
            v[dim].insert(0, "0")
            p[dim].insert(0, "0")

    def update_u_size(self):
        self.u_size.delete(0, "end")
        if self.num_dims.get() == 2:
            self.u_size.insert(0, 6000)

        elif self.num_dims.get() == 3:
            self.u_size.insert(0, 2000)


if __name__ == "__main__":
    window = Window()
    page1 = Universe_page(window)
    page2 = Objects_page(window)
    page3 = Last_page(window)
    window.update_pages(page1, page2, page3)
    window.mainloop()
